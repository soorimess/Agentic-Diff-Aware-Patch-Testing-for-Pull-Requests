"""Per-instance SWE-bench containers: the environment, and the isolation.

Why containers at all
---------------------
Cloning a repository and building a virtualenv on the host works for
`psf/requests` and stops working immediately after. django needs its own test runner
and a settings module, sympy ships `bin/test` instead of pytest, scikit-learn and
matplotlib need compiling against pinned numpy/scipy, and half the older instances do
not build on a modern interpreter at all. SWE-bench publishes a prepared image per
instance for exactly this reason -- 4503 of them -- and using them removes the entire
build problem in one step. It also makes our numbers comparable with published ones,
since it is the same environment the leaderboard runs in.

Why containers are also the answer to leakage
---------------------------------------------
Measured on this machine, a plain shell reaches `pypi.org` and `github.com` and can run
`git ls-remote https://github.com/psf/requests` successfully. Stripping proxy variables
changes nothing, because the host has direct egress. So an agent whose terminal runs on
the host has a network no matter what we set, and could simply `pip download` a later
release of the library it is being tested on -- which contains both the fix and the
developer's test.

`--network none` is the only thing measured to actually stop it: inside the container,
`pip download django==5.0` fails with a DNS error. That is the difference between an
isolation claim and an isolation fact.

What the images do and do not contain
-------------------------------------
Checked on django__django-17029: `/testbed` is the repo at base_commit with 31825
commits of history, but `git rev-list --all --not HEAD` is 0 and there are no dangling
commits -- the history is truncated at base and no ref reaches the fix. The remotes are
also stripped, so nothing can be fetched. That is already better than our own worktrees,
whose mirror held the entire future. We still delete `.git` for the agent, because
history at base is reconnaissance we did not intend to hand over, and the developer's
own test is not in it either way.
"""
from __future__ import annotations

import contextlib
import difflib
import fcntl
import json
import os
import re
import shlex
import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from openhands_f2p import flow

PLATFORM = "linux/amd64"          # SWE-bench publishes amd64 only; emulated on arm64
IMAGE = "swebench/sweb.eval.x86_64.{tag}:latest"
REPO_DIR = "/testbed"


def image_for(instance_id: str) -> str:
    """swebench uses `_1776_` where the instance id has `__`."""
    return IMAGE.format(tag=instance_id.replace("__", "_1776_"))


def _run(cmd: list[str], stdin: str | None = None, timeout: int = 1800):
    """Run a command, turning a timeout into a failed result rather than an exception.

    `subprocess.run` raises TimeoutExpired, which walks straight past any caller that
    only inspects `returncode`. That is exactly what defeated the pull retry: it checked
    the return code, the timeout raised instead, and two instances died with a traceback
    after ninety minutes without a single retry. A stalled command is a failure like any
    other and belongs in the same channel as one.
    """
    try:
        return subprocess.run(cmd, input=stdin, capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        def text(v):
            return v.decode(errors="replace") if isinstance(v, bytes) else (v or "")
        return subprocess.CompletedProcess(
            cmd, 124, text(exc.stdout),
            text(exc.stderr) + f"\ntimed out after {timeout}s")


def have_image(image: str) -> bool:
    return _run(["docker", "image", "inspect", image], timeout=60).returncode == 0


_OWNER = re.compile(r"-p(\d+)-[0-9a-f]{6}$")


def _owner_alive(name: str) -> bool:
    """True if the process that created this container is still running.

    Signal 0 asks the kernel whether we could signal the process without sending
    anything. A pid can in principle be recycled by an unrelated process, in which case
    we decline to reap a container that really was orphaned -- the safe direction to be
    wrong in. Containers from before this naming scheme carry no pid and are reaped.
    """
    m = _OWNER.search(name.strip())
    if not m:
        return False
    try:
        os.kill(int(m.group(1)), 0)
    except (ProcessLookupError, ValueError):
        return False
    except PermissionError:
        return True     # exists, owned by someone else
    return True


def reap_orphans(quiet: bool = True) -> int:
    """Remove containers left behind by a killed run.

    `Sandbox` cleans up in `__exit__`, which never runs if the process is killed --
    Ctrl-C, a stopped background job, an OOM. Three containers were found still running twenty-four minutes after their runs were
    stopped, holding memory and, more to the point, disk: the Docker VM has its own
    58 GB volume and a full one presents as `no space left on device` in the middle of
    an unrelated pull.

    Only containers whose owning process is gone are removed. This used to reap by name
    alone, which was correct for one run at a time and catastrophic under `--parallel`:
    every worker calls this before pulling, so the fifth worker's pull deleted the four
    live containers its siblings were writing tests in. Those runs did not crash -- the
    agent kept issuing tool calls into a container that no longer existed, collected
    forty `No such container` errors, and finished having written nothing.
    """
    listed = _run(["docker", "ps", "-a", "--filter", "name=f2p-",
                   "--format", "{{.ID}}\t{{.Names}}"], timeout=120)
    ids = []
    for line in listed.stdout.splitlines():
        cid, _, name = line.partition("\t")
        if not cid.strip():
            continue
        if _owner_alive(name):
            continue
        ids.append(cid.strip())
    if ids:
        _run(["docker", "rm", "-f", *ids], timeout=300)
        if not quiet:
            print(f"  removed {len(ids)} orphaned container(s) from an earlier run")
    return len(ids)


def vm_free_gb() -> float | None:
    """Free space inside the Docker VM, which is not the host's free space.

    Worth its own function because the two are unrelated and the failure is misleading.
    The host had 53 GB free while the VM's own 58 GB volume was 100% full, and the pull
    that hit it reported `no space left on device` -- which reads like a host problem and
    is not one. Three images failed to download for this reason before anyone looked.
    """
    r = _run(["docker", "run", "--rm", "--platform", PLATFORM, "alpine",
              "df", "-Pk", "/"], timeout=180)
    for line in r.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 4:
            try:
                return int(parts[3]) / (1024 * 1024)
            except ValueError:
                return None
    return None


# Workers under `--parallel` are separate processes, so an image one of them is about
# to use is invisible to the others between the moment its pull finishes and the moment
# its container starts. A claim file bridges that window; it is named after the owning
# process so a claim left by a killed run expires on its own.
CLAIMS = Path("/tmp/f2p-image-claims")


def claim_image(image: str) -> None:
    try:
        CLAIMS.mkdir(exist_ok=True)
        (CLAIMS / f"p{os.getpid()}").write_text(image)
    except OSError:
        pass            # a claim is an optimisation, never a precondition


def release_image() -> None:
    with contextlib.suppress(OSError):
        (CLAIMS / f"p{os.getpid()}").unlink(missing_ok=True)


def claimed_images() -> set[str]:
    """Images live sibling processes have claimed. Dead owners' claims are cleaned up."""
    out: set[str] = set()
    for f in CLAIMS.glob("p*") if CLAIMS.is_dir() else ():
        if _owner_alive(f"-{f.name}-000000"):
            out.add(f.read_text().strip())
        else:
            f.unlink(missing_ok=True)
    return out


def evict_one_image(keep: str) -> bool:
    """Delete the largest prepared image not currently in use, to make room for another.

    Twenty-six instances is roughly eighty gigabytes of images and the Docker VM holds
    fifty-eight, so a run over the whole set cannot keep them all. Evicting the biggest
    idle one costs a re-download later and lets the run finish; keeping them all does
    not. Images with a live container are skipped, which is what makes this safe to call
    while other instances are running in parallel.
    """
    listed = _run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}\t{{.Size}}",
                   "swebench/*"], timeout=180)
    in_use = set()
    ps = _run(["docker", "ps", "-a", "--format", "{{.Image}}"], timeout=180)
    in_use.update(x for x in ps.stdout.split() if x)
    in_use.update(claimed_images())

    def gb(text: str) -> float:
        try:
            n = float(text[:-2])
        except ValueError:
            return 0.0
        return n if text.endswith("GB") else n / 1024 if text.endswith("MB") else 0.0

    best, best_size = None, 0.0
    for line in listed.stdout.splitlines():
        if "\t" not in line:
            continue
        name, size = line.split("\t", 1)
        if name == keep or name in in_use:
            continue
        if gb(size.strip()) > best_size:
            best, best_size = name, gb(size.strip())
    if not best:
        return False
    _run(["docker", "image", "rm", "-f", best], timeout=600)
    print(f"  evicted {best.split('.')[-1]} ({best_size:.1f} GB) to make room")
    return True


# Headroom for one image. Deliberately about double the largest compressed size: docker
# writes the download and then extracts it, so a 4.6 GB image transiently needs well
# over nine. At the old 6 GB threshold the guard let two pulls start with 6.2 GB free;
# they filled the disk, stalled, and burned three twenty-minute attempts each without
# ever reporting a disk problem.
DEFAULT_IMAGE_HEADROOM_GB = 14.0


PULL_LOCK = Path("/tmp/f2p-pull.lock")


def pull_image(image: str, quiet: bool = False,
               need_gb: float = DEFAULT_IMAGE_HEADROOM_GB) -> None:
    """Fetch one prepared image, one worker at a time.

    The lock is the point. These images are around 3 GB and the link they come down is
    not always fast; two workers pulling at once each get half of it and *both* miss the
    timeout, where run sequentially the first would have finished and the second started
    from a clean twenty minutes. Two concurrent pulls of matplotlib-26208 and
    scikit-learn-25747 shared 0.8 MB/s for forty-six minutes and neither landed a layer.

    Waiting here costs a worker nothing: it has no container yet and nothing to do until
    the image exists. `have_image` is re-checked after the wait because the worker ahead
    may have been fetching the very same image.
    """
    if have_image(image):
        return
    with PULL_LOCK.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            _pull_locked(image, quiet, need_gb)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def _pull_locked(image: str, quiet: bool, need_gb: float) -> None:
    if have_image(image):
        return                  # the worker ahead of us in the queue wanted it too
    free = vm_free_gb()
    if free is not None and free < need_gb:
        # Reclaim what is definitely safe before giving up: build cache is cache by
        # definition, and stopped containers of ours are finished work.
        reap_orphans()
        _run(["docker", "builder", "prune", "-af"], timeout=900)
        free = vm_free_gb()
    while free is not None and free < need_gb and evict_one_image(image):
        free = vm_free_gb()
    if free is not None and free < need_gb:
        raise SystemExit(
            f"the Docker VM has only {free:.1f} GB free and this image needs about "
            f"{need_gb:.0f}, with nothing left to evict. The host's free space is "
            f"irrelevant here -- the VM has its own volume. Raise the disk limit in "
            f"Docker Desktop > Settings > Resources. Note that `docker image prune -a` "
            f"would delete every prepared SWE-bench image, not just the spare ones.")
    if not quiet:
        print(f"  pulling {image} ({free:.0f} GB free in the VM)"
              if free else f"  pulling {image}")
    # Retried, because a multi-gigabyte pull is the longest-lived network operation in
    # the whole run and the cheapest thing to lose. Closing a laptop lid mid-pull kills
    # the connection, and without a retry that instance reports BROKEN for a reason that
    # has nothing to do with it. Docker resumes from the layers already on disk, so a
    # second attempt is not a second download.
    last = None
    for attempt in (1, 2, 3):
        # Forty minutes per attempt. That is far more than a healthy pull of a 3 GB
        # image needs, and deliberately so: the timeout exists to catch a *stalled*
        # pull, not a slow link, and cutting a slow-but-moving download off at twenty
        # minutes threw away everything it had fetched. Now that pulls are serialised,
        # one attempt has the whole link to itself.
        r = _run(["docker", "pull", "--platform", PLATFORM, image], timeout=2400)
        if r.returncode == 0:
            return
        last = r
        if "no space left" in (r.stderr or ""):
            break                          # retrying will not create disk
        if not quiet and attempt < 3:
            print(f"  pull attempt {attempt} failed, retrying "
                  f"({(r.stderr or '').strip().splitlines()[-1][:60] if r.stderr else ''})")
    hint = ("\n\nThe Docker VM is out of disk. Its volume is separate from the host's."
            if "no space left" in ((last.stderr if last else "") or "") else "")
    raise SystemExit(
        f"could not pull {image} after 3 attempts:\n"
        f"{(last.stderr if last else '')[-1200:]}{hint}")


# --------------------------------------------------------------- test invocation
#
# Three conventions live in this dataset, and a node id from one is meaningless to the
# others. Worse, only one of them can be passed on a command line at all:
#
#   pytest repos  'sklearn/utils/tests/test_set_output.py::test_set_output_pandas_keep_index'
#   django        'test_clear_cache (apps.tests.AppsTests.test_clear_cache)'
#                 'If the __path__ attr is empty, use __file__ if set.'      <-- a docstring
#   sympy         'test_issue_24543'                                        <-- no path
#
# Django's verbose runner prints a test's docstring in place of its name when it has
# one, and SWE-bench recorded whatever the runner printed. Those entries are not labels
# and never will be, so django cannot be driven by passing ids. sympy's ids carry no
# path, so they cannot locate a file.
#
# The way out is the one SWE-bench itself uses: run whole test *modules*, and decide
# per test by parsing the runner's output. So each repo needs two things -- what to run,
# and how to read what came back.
# No `--no-header`: pytest only grew that flag in 6.0, and these images span versions
# back to 4.5, where an unknown option is a usage error -- exit 4, nothing collected, and
# a verdict of BROKEN for a test that never got the chance to run. The header it would
# have suppressed is four lines of noise in a log nobody greps for.
# `-v` as well as `-rA`, because they are not the same guarantee. `-rA` prints a short
# summary section that pytest 3.3 -- astropy 1.3's pytest -- does not produce at all,
# leaving the log with a pass/fail count and not a single node id in it: "nothing
# collected on either side" for a run whose test really had failed and then passed.
# `-v` prints one `path::test STATUS` line per test on every version from 3 to 8.
PYTEST = ("python -m pytest -v -rA -p no:cacheprovider --tb=short "
          "--color=no")   # colour codes land inside the node id and defeat parsing

TEST_RUNNER: dict[str, dict[str, str]] = {
    "django/django": {"cmd": "./tests/runtests.py --verbosity 2", "kind": "django",
                      "gen_path": "tests/{name}.py"},
    "sympy/sympy": {"cmd": "bin/test -C --verbose", "kind": "sympy",
                    "gen_path": "sympy/core/tests/{name}.py"},
}
DEFAULT_RUNNER = {"cmd": PYTEST, "kind": "pytest", "gen_path": "tests/{name}.py"}


def runner_for(repo: str) -> dict[str, str]:
    return TEST_RUNNER.get(repo, DEFAULT_RUNNER)


def patched_test_files(test_patch: str) -> list[str]:
    """Test files the developer's patch touches -- the modules an instance lives in."""
    out = []
    for line in test_patch.splitlines():
        if line.startswith("diff --git "):
            path = line.split(" b/", 1)[-1].strip()
            if path.endswith(".py"):
                out.append(path)
    return out


def django_module(path: str) -> str:
    """'tests/apps/tests.py' -> 'apps.tests';  'tests/f2p_x.py' -> 'f2p_x'."""
    rel = path[len("tests/"):] if path.startswith("tests/") else path
    return rel[:-3].replace("/", ".") if rel.endswith(".py") else rel


def test_command(repo: str, targets: list[str]) -> str:
    """`targets` are node ids for pytest repos, and file paths everywhere else."""
    r = runner_for(repo)
    if r["kind"] == "django":
        args = " ".join(shlex.quote(django_module(t)) for t in targets)
    else:
        args = " ".join(shlex.quote(t) for t in targets)
    return f"{r['cmd']} {args}".strip()


PYTEST_LINE = re.compile(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+(\S+)")
# The verbose form, `astropy/tests/test_x.py::test_y PASSED   [ 50%]`. Non-greedy up to
# the status word so that a parametrised id containing spaces -- `test_x[1 2]` -- stays
# in one piece.
PYTEST_VERBOSE = re.compile(
    r"^(\S.*?::.+?)\s+(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)(?:\s|$)")
DJANGO_LINE = re.compile(r"^(.*?) \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure"
                         r"|unexpected success)\s*$")
SYMPY_LINE = re.compile(r"^(test_\w+)\s+(ok|F|E|fail|Fail|exception|skipped|w|s|X|f)\b")

_NORMAL = {"ok": "PASSED", "PASSED": "PASSED", "XPASS": "PASSED",
           "expected failure": "PASSED", "F": "FAILED", "FAIL": "FAILED",
           "FAILED": "FAILED", "fail": "FAILED", "Fail": "FAILED", "f": "FAILED",
           "E": "ERROR", "ERROR": "ERROR", "exception": "ERROR",
           "unexpected success": "FAILED"}


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def parse_output(repo: str, output: str) -> dict[str, str]:
    """Per-test outcome, keyed the way this repo's node ids are keyed.

    For django the key is whatever the runner printed, which is exactly what
    FAIL_TO_PASS/PASS_TO_PASS contain -- docstrings included.
    """
    kind = runner_for(repo)["kind"]
    out: dict[str, str] = {}
    for raw in output.splitlines():
        # Stripped even with --color=no: some runners colour regardless of the flag,
        # and the escape sequences sit *inside* the node id, not just around it.
        line = ANSI.sub("", raw).strip()
        if kind == "django":
            m = DJANGO_LINE.match(line)
            if m:
                name, status = m.group(1).strip(), m.group(2)
                out[name] = _NORMAL.get(status, "SKIPPED" if "skip" in status else status)
        elif kind == "sympy":
            m = SYMPY_LINE.match(line)
            if m:
                out[m.group(1)] = _NORMAL.get(m.group(2), "SKIPPED")
        else:
            m = PYTEST_LINE.match(line)
            if m:
                out[m.group(2)] = _NORMAL.get(m.group(1), m.group(1))
                continue
            m = PYTEST_VERBOSE.match(line)
            if m:
                out[m.group(1)] = _NORMAL.get(m.group(2), m.group(2))
    return out


def outcome_of(repo: str, outcomes: dict[str, str], node_id: str) -> str | None:
    """Look a node id up in parsed output, tolerating the formats' small differences."""
    if node_id in outcomes:
        return outcomes[node_id]
    if runner_for(repo)["kind"] == "django":
        # 'test_x (a.b.C.test_x)' may be printed as just 'test_x (a.b.C)' by some versions
        head = node_id.split(" (")[0]
        for k, v in outcomes.items():
            if k == head or k.startswith(head + " ("):
                return v
    return None


# ------------------------------------------------------------------- the sandbox
@dataclass
class ExecResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def output(self) -> str:
        return self.stdout + (("\n" + self.stderr) if self.stderr.strip() else "")


class Sandbox:
    """A running container for one instance, with no network.

    Use as a context manager. Everything the agent and the verifier do happens through
    `exec`, `write` and `read`, so there is one place where isolation is enforced and
    one place to audit.
    """

    def __init__(self, instance_id: str, network: bool = False, quiet: bool = False,
                 extra_packages: tuple[str, ...] = ()):
        self.instance_id = instance_id
        self.image = image_for(instance_id)
        self.network = network
        self.quiet = quiet
        self.extra_packages = tuple(extra_packages)
        # The owning process id is part of the name so that `reap_orphans` can tell a
        # container abandoned by a dead run from one a live sibling is working in. Under
        # `--parallel` the workers are separate processes sharing one Docker daemon, and
        # a reap that goes by name alone deletes their containers out from under them.
        self.name = (f"f2p-{instance_id.replace('__', '-')}"
                     f"-p{os.getpid()}-{uuid.uuid4().hex[:6]}")
        self.container: str | None = None

    # -- lifecycle -------------------------------------------------------------
    def start(self) -> "Sandbox":
        claim_image(self.image)
        pull_image(self.image, quiet=self.quiet)
        cmd = ["docker", "run", "-d", "--name", self.name, "--platform", PLATFORM]
        # `--network none` cannot be undone at runtime, and `extra_packages` needs a
        # network for exactly one pip install. So when something has to be installed the
        # container starts on the default bridge and is disconnected immediately after --
        # which ends in the same place, and `audit_isolation` is what proves it.
        needs_install = bool(self.extra_packages)
        if not self.network and not needs_install:
            cmd += ["--network", "none"]
        cmd += [self.image, "sleep", "infinity"]
        r = _run(cmd, timeout=600)
        if r.returncode:
            raise SystemExit(f"could not start container:\n{r.stderr[-1200:]}")
        self.container = r.stdout.strip()
        if needs_install:
            self._install_then_seal()
        net = "network=none" if not self.network else "NETWORK ENABLED"
        if not self.quiet:
            print(f"  sandbox {self.name[:28]} ({net})")
        flow.record(flow.SETUP, "container up", f"{self.name}  {net}",
                    image=self.image, container=self.container[:12])
        return self

    def _install_then_seal(self) -> None:
        """pip install the extras, then take the network away and check it is gone."""
        pkgs = " ".join(shlex.quote(p) for p in self.extra_packages)
        r = self.exec(f"pip install -q {pkgs}", workdir="/", timeout=900)
        installed = r.returncode == 0
        d = _run(["docker", "network", "disconnect", "bridge", self.container],
                 timeout=120)
        flow.record(flow.SETUP, "install then seal",
                    f"{pkgs}: {'ok' if installed else 'FAILED'}; "
                    f"network {'removed' if d.returncode == 0 else 'STILL ATTACHED'}")
        # Never take the seal on trust: if the disconnect silently failed we would run a
        # whole instance believing it was isolated when it was not.
        if self.audit_isolation()["dns_resolves"]:
            self.stop()
            raise SystemExit("could not remove the container network after installing "
                             f"{pkgs} -- refusing to run with an open network")

    def stop(self) -> None:
        if self.container:
            flow.record(flow.SETUP, "container down", self.name)
            _run(["docker", "rm", "-f", self.container], timeout=180)
            self.container = None
        release_image()

    def __enter__(self) -> "Sandbox":
        return self.start()

    def __exit__(self, *exc) -> None:
        self.stop()

    # -- operations ------------------------------------------------------------
    def exec(self, command: str, workdir: str = REPO_DIR,
             timeout: int = 1800) -> ExecResult:
        t0 = time.time()
        try:
            r = _run(["docker", "exec", "-w", workdir, self.container,
                      "bash", "-lc", command], timeout=timeout)
            out = ExecResult(r.returncode, r.stdout, r.stderr)
        except subprocess.TimeoutExpired:
            # Returned rather than raised. An agent that runs `grep -R x ..` recurses
            # out of /testbed into /proc and hangs; letting that propagate killed the
            # tool call with a stack trace instead of telling the agent what happened,
            # so it could not adjust. A timeout is a result, not a crash.
            out = ExecResult(124, "", f"timed out after {timeout}s and was killed")
        flow.record(flow.SETUP, "exec",
                    f"$ {command.splitlines()[0][:110]}"
                    + ("  ..." if "\n" in command else "")
                    + f"   -> exit {out.returncode}, {len(out.output)} bytes",
                    duration=time.time() - t0, returncode=out.returncode)
        return out

    def write(self, path: str, text: str) -> None:
        """Write a file inside the container without going through the shell's quoting."""
        target = path if path.startswith("/") else f"{REPO_DIR}/{path}"
        mkdir = f"mkdir -p {shlex.quote(str(Path(target).parent))}"
        _run(["docker", "exec", self.container, "bash", "-lc", mkdir], timeout=120)
        r = _run(["docker", "exec", "-i", self.container, "bash", "-lc",
                  f"cat > {shlex.quote(target)}"], stdin=text, timeout=300)
        if r.returncode:
            raise RuntimeError(f"write {target} failed: {r.stderr[-400:]}")

    def read(self, path: str) -> str | None:
        target = path if path.startswith("/") else f"{REPO_DIR}/{path}"
        r = _run(["docker", "exec", self.container, "cat", target], timeout=300)
        return r.stdout if r.returncode == 0 else None

    def exists(self, path: str) -> bool:
        target = path if path.startswith("/") else f"{REPO_DIR}/{path}"
        return self.exec(f"test -e {shlex.quote(target)}").returncode == 0

    # -- the two states of the code -------------------------------------------
    def apply_patch(self, diff: str, revert: bool = False) -> None:
        if not diff.endswith("\n"):
            diff += "\n"
        self.write("/tmp/f2p.patch", diff)
        flag = "-R " if revert else ""
        flow.record(flow.VERIFY, "revert patch" if revert else "apply patch",
                    f"{len(diff)} bytes")
        r = self.exec(f"git apply -p1 {flag}/tmp/f2p.patch")
        if r.returncode:
            r = self.exec(f"git apply -p1 -3 {flag}/tmp/f2p.patch")
        if r.returncode:
            raise RuntimeError(
                f"could not {'revert' if revert else 'apply'} patch: {r.output[-600:]}")

    # `.git` is deleted before the agent is let in, so `git checkout --` cannot restore
    # anything -- `git apply` works without a repository but `git checkout` does not.
    # That was harmless while nothing applied the patch except verify(). It stopped being
    # harmless once the agent could apply it too: a patch left applied would make the
    # harness's "before the fix" run actually be the after-the-fix run, and the whole
    # measurement would invert silently. So the tree's state is asked about, not assumed.
    def patch_state(self, patch: str) -> str:
        """'base' if the patch can still be applied, 'head' if it can be reversed."""
        self.write("/tmp/f2p_state.patch", patch if patch.endswith("\n") else patch + "\n")
        if self.exec("git apply --check -p1 /tmp/f2p_state.patch").returncode == 0:
            return "base"
        if self.exec("git apply -R --check -p1 /tmp/f2p_state.patch").returncode == 0:
            return "head"
        return "unknown"

    def ensure_base(self, patch: str) -> str:
        """Put the tree back at base if something left the patch applied."""
        state = self.patch_state(patch)
        if state == "head":
            flow.record(flow.SETUP, "tree was at head",
                        "patch left applied by the agent -- reverting before verification")
            self.apply_patch(patch, revert=True)
            state = self.patch_state(patch)
        return state

    # -- leakage ---------------------------------------------------------------
    def strip_git(self) -> None:
        """Remove version control before the agent is let in.

        The image's history is already truncated at base -- verified: no ref reaches
        past HEAD, no dangling commits, no remotes. This removes what is left, so
        `git log` is not a source of anything, and so that "the agent cannot inspect
        history" is a property of the box rather than a property of how SWE-bench
        happened to build it.
        """
        flow.record(flow.SETUP, "strip git", "rm -rf /testbed/.git")
        self.exec(f"rm -rf {REPO_DIR}/.git")

    def audit_isolation(self) -> dict:
        """Evidence, gathered from inside, that the box is what we say it is."""
        # No pipe here on purpose: piping to `tail` made the exit status tail's, so
        # this reported dns_resolves=True while printing a resolution failure.
        net = self.exec(
            "python -c \"import socket;socket.setdefaulttimeout(5);"
            "socket.gethostbyname('pypi.org')\"", timeout=120)
        return {
            "network_enabled": self.network,
            "dns_resolves": net.returncode == 0,
            "dns_probe_output": net.output.strip()[-160:],
            "git_present": self.exists(f"{REPO_DIR}/.git"),
            "image": self.image,
        }


SYMPY_COV_DRIVER = "/tmp/f2p_cov_driver.py"
# Import the test module and call its test functions, rather than asking sympy to find
# them. `sympy.test(path)` treats its argument as a filter and returns True when it
# matches nothing at all, so a path it does not recognise is indistinguishable from a
# suite that passed: sympy-12096 reported 0% coverage on a one-line patch its test
# demonstrably exercises, because under coverage the test had never run and the driver
# had exited 0 to say so. Importing the file by path cannot fail quietly -- if the
# module or a test is missing, this exits non-zero and says which.
SYMPY_DRIVER_SRC = '''import importlib.util, pathlib, sys, traceback

ran = failed = 0
for target in sys.argv[1:]:
    path = pathlib.Path(target.split("::")[0])
    if not path.exists():
        print("driver: no such file:", path)
        sys.exit(2)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    for name in sorted(vars(module)):
        fn = getattr(module, name)
        if name.startswith("test_") and callable(fn):
            ran += 1
            try:
                fn()
                print("PASSED", path, name)
            except Exception:
                failed += 1
                print("FAILED", path, name)
                traceback.print_exc()
print("driver: ran", ran, "test(s),", failed, "failed")
sys.exit(1 if failed or not ran else 0)
'''

# django's runner has to be able to import its own settings module, which lives in
# `tests/`. Running `./tests/runtests.py` directly puts that directory on the path;
# running it as `python -m coverage run ./tests/runtests.py` does not -- sys.path[0]
# becomes the working directory instead, and the run dies on
# `ModuleNotFoundError: No module named 'test_sqlite'` before a single test executes.
DJANGO_COV_PATH = "PYTHONPATH=$PWD/tests"


COV_RC = "/tmp/f2p_coverage.rc"
COV_DATA = "/tmp/f2p.coverage"

# Our own coverage configuration, imposed so the repository's cannot decide what we
# measure. Three settings in checked-in `.coveragerc` files quietly produce a wrong
# answer rather than an error:
#
#   parallel  -- pytest's sets `parallel = 1`, which writes `.coverage.<host>.<pid>.<n>`
#                instead of `.coverage`. `coverage json` then reports "No data to
#                report." and the instance is scored as having no coverage at all. This
#                is what silenced both sphinx runs and pytest-5262.
#   include   -- a whitelist. Any changed file outside it is invisible, so a test that
#                really does execute the patch reports 0%.
#   data_file -- moves the file out from under us for the same effect as `parallel`.
#
# `source` and `include` are deliberately left unset: we want everything the test
# imports, and the narrowing to the patch's own lines happens afterwards in
# `changed_line_coverage`.
COV_RC_SRC = f"""[run]
branch = True
parallel = False
data_file = {COV_DATA}
disable_warnings = no-data-collected, module-not-imported
"""


def coverage_command(box: "Sandbox", repo: str, targets: list[str]) -> str:
    """The repo's own runner, wrapped in `coverage run`.

    Wrapping rather than pytest-cov, because two of the three runners are not pytest.
    sympy needs more than a wrapper though: `coverage run bin/test ...` reports 12% of
    bin/test and 0% of everything else, because that launcher does not run the tests in
    a way coverage follows. Calling `sympy.test()` in-process from a small driver traces
    the library properly. pytest is not an option there -- it is not installed in that
    image at all.
    """
    box.write(COV_RC, COV_RC_SRC)
    kind = runner_for(repo)["kind"]
    if kind == "sympy":
        box.write(SYMPY_COV_DRIVER, SYMPY_DRIVER_SRC)
        args = " ".join(shlex.quote(t) for t in targets)
        inner = f"{SYMPY_COV_DRIVER} {args}"
    else:
        inner = test_command(repo, targets)
        if inner.startswith("python -m "):
            inner = inner[len("python "):]      # -> `-m pytest ...`
    prefix = f"{DJANGO_COV_PATH} " if kind == "django" else ""
    return f"{prefix}python -m coverage run --rcfile={COV_RC} {inner}"


def measure_coverage(box: "Sandbox", repo: str, targets: list[str],
                     limit_files: int = 12) -> dict:
    """Which lines the given tests executed, per file.

    Deliberately knows nothing about `patch`. It reports coverage of the files the test
    actually touched, and never which lines the pull request changed -- those come from
    the answer, and an agent told "you missed lines 977 and 980" has been handed the
    location of the bug. Change-specific coverage stays a measurement the harness makes
    afterwards, never an objective the agent optimises against.
    """
    box.exec(f"rm -f {COV_DATA} {COV_DATA}.* .coverage .coverage.* f2p_cov.json",
             timeout=120)
    run = box.exec(coverage_command(box, repo, targets), timeout=3600)
    # `combine` is a belt-and-braces step: our rcfile turns parallel mode off, but a
    # test suite that forks (pytest-xdist, django's --parallel) still leaves one data
    # file per process. With nothing to combine it is a no-op.
    box.exec(f"python -m coverage combine --rcfile={COV_RC} --append 2>/dev/null; true",
             timeout=300)
    rep = box.exec(f"python -m coverage json --rcfile={COV_RC} -o f2p_cov.json "
                   f"--pretty-print 2>&1 | tail -2", timeout=600)
    raw = box.read("f2p_cov.json")
    box.exec(f"rm -f {COV_DATA} {COV_DATA}.* f2p_cov.json", timeout=120)
    if not raw:
        # Both halves: `coverage json` says only "No data to report.", which is a
        # symptom. What the test run itself printed is the cause.
        return {"ok": False, "returncode": run.returncode, "files": {},
                "detail": f"coverage json: {rep.output.strip()[-200:]} | "
                          f"test run exit {run.returncode}: {run.output[-600:]}"}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"ok": False, "detail": "coverage produced unreadable json", "files": {}}

    files = {}
    raw: dict[str, dict[str, set[int]]] = {}
    for path, info in (data.get("files") or {}).items():
        rel = path[len(REPO_DIR) + 1:] if path.startswith(REPO_DIR) else path
        rel = rel.lstrip("./")
        summary = info.get("summary") or {}
        executed = set(info.get("executed_lines") or [])
        missing = set(info.get("missing_lines") or [])
        # `measurable` is what coverage can have an opinion about at all: comments,
        # blanks and docstrings appear in neither list.
        raw[rel] = {"executed": executed, "measurable": executed | missing}
        if not summary.get("num_statements"):
            continue
        # Test files themselves are noise here: of course the test ran.
        if is_test_file(rel) or rel.rsplit("/", 1)[-1] == "f2p_cov_driver.py":
            continue
        files[rel] = {
            "percent": round(summary.get("percent_covered", 0.0), 1),
            "executed": summary.get("covered_lines", 0),
            "statements": summary.get("num_statements", 0),
            "missing_lines": (info.get("missing_lines") or [])[:60],
        }
    ranked = sorted(files.items(), key=lambda kv: -kv[1]["executed"])
    top = dict(ranked if limit_files == 0 else ranked[:limit_files])
    return {"ok": True, "returncode": run.returncode, "files": top, "raw": raw,
            "test_output_tail": run.output[-600:]}


def changed_lines(diff: str) -> dict[str, set[int]]:
    """Post-image line numbers a unified diff adds or alters, per file.

    Post-image on purpose: these numbers only exist once the patch is applied, which is
    why the measurement has to happen at head.
    """
    result: dict[str, set[int]] = {}
    current: str | None = None
    new_ln = 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            path = path[2:] if path.startswith("b/") else path
            current = None if path == "/dev/null" else path
            if current:
                result.setdefault(current, set())
        elif line.startswith("@@") and current:
            try:
                new_ln = int(line.split("+", 1)[1].split("@@")[0].strip().split(",")[0])
            except (IndexError, ValueError):
                new_ln = 0
        elif current and new_ln:
            if line.startswith("+"):
                result[current].add(new_ln)
                new_ln += 1
            elif not line.startswith("-"):
                new_ln += 1
    return {k: v for k, v in result.items() if v}


def patched_source_files(patch: str) -> list[str]:
    """The non-test Python files a patch touches -- the subject of the measurement."""
    return [p for p in changed_lines(patch) if p.endswith(".py") and not is_test_file(p)]


def added_lines_between(base_text: str, head_text: str) -> set[int]:
    """Line numbers *in head* that the patch introduced or rewrote.

    Read off the two files rather than the diff header, because the header can be wrong
    about where the change lands. `git apply` matches on context and will relocate a
    hunk that no longer sits at its recorded offset -- for scikit-learn-10908 it
    reported `Hunk #1 succeeded at 993 (offset 22 lines)`, so the diff's 974-976 pointed
    22 lines above the real change, at an unrelated method. Coverage was then measured
    against three lines the pull request never touched and reported 0%, with nothing
    anywhere to say the number was meaningless.

    Pure deletions contribute nothing, which is correct: a line that no longer exists
    cannot be executed, and counting it would make full coverage unreachable.
    """
    base = base_text.splitlines()
    head = head_text.splitlines()
    added: set[int] = set()
    for tag, _, _, j1, j2 in difflib.SequenceMatcher(
            None, base, head, autojunk=False).get_opcodes():
        if tag in ("insert", "replace"):
            added.update(range(j1 + 1, j2 + 1))     # 1-based, as coverage reports them
    return added


def is_test_file(path: str) -> bool:
    """Whether a repository path is a test rather than the code under test.

    By convention, not by substring. `"test" in name` reads `src/_pytest/unittest.py` --
    the file pytest-10081 actually patches -- as a test file and drops it from the
    denominator, so the instance reports "the fix touches no source .py lines" for a fix
    that is entirely source. The conventions below are the ones pytest itself collects
    by, plus the two directory names these twelve repositories use.
    """
    name = path.rsplit("/", 1)[-1]
    parts = path.split("/")
    return (name.startswith("test_") or name.endswith("_test.py")
            or name == "conftest.py"
            or "tests" in parts[:-1] or "testing" in parts[:-1])


def changed_line_coverage(box: "Sandbox", repo: str, targets: list[str],
                          patch: str, base_files: dict[str, str] | None = None) -> dict:
    """Of the lines this pull request changed, how many does the test execute?

    The evaluation metric, and the harness computes it -- never the agent. The `coverage`
    tool the agent holds is deliberately blind to the diff; this is the half that reads
    it, and it runs only after the F2P verdict is settled.

    Three things make this harder than it sounds, and each one silently returns a wrong
    number rather than an error:

      * It must be measured at HEAD. A patch that adds lines has nothing at those line
        numbers until it is applied, so intersecting them with anything measured at base
        is empty by construction.
      * Comments and blank lines are invisible to coverage. Counting them in the
        denominator reports a fully covered four-line fix, two lines of which are
        comments, as 50%.
      * Test files in the patch are not the subject. A patch that also edits its own
        tests should be neither credited nor penalised for them.

    The caller is responsible for having applied `patch` before calling this.
    """
    # Preferred: diff the file against the copy taken before the patch went on, which
    # is what actually happened to the tree. The diff header is only a fallback for a
    # file the caller could not read at base -- a file the patch creates, say.
    wanted: dict[str, set[int]] = {}
    from_diff = changed_lines(patch)
    for path in patched_source_files(patch):
        base_text = (base_files or {}).get(path)
        head_text = box.read(path) if base_text is not None else None
        if base_text is not None and head_text is not None:
            lines = added_lines_between(base_text, head_text)
        else:
            lines = from_diff.get(path, set())
        if lines:
            wanted[path] = lines
    if not wanted:
        return {"measured": False, "reason": "the fix touches no source .py lines"}

    traced = measure_coverage(box, repo, targets, limit_files=0)
    if not traced.get("ok"):
        return {"measured": False, "reason": traced.get("detail", "coverage failed")}

    hit: list[str] = []
    missed: list[str] = []
    matched: dict[str, str] = {}
    for path, lines in wanted.items():
        info = traced["raw"].get(path)
        if info is not None:
            matched[path] = path
        else:
            # Suffix matching, but only at a path boundary. Plain `endswith` will happily
            # match an *installed* copy of the library in site-packages, which is not the
            # tree the patch was applied to -- its line numbers belong to the unpatched
            # code, so every number after that is measured against the wrong file.
            for k, v in traced["raw"].items():
                if k == path or k.endswith("/" + path) or path.endswith("/" + k):
                    info, matched[path] = v, k
                    break
        info = info or {"executed": set(), "measurable": set()}
        for ln in sorted(lines):
            if ln not in info["measurable"]:
                continue                       # comment, blank or docstring
            (hit if ln in info["executed"] else missed).append(f"{path}:{ln}")
    total = len(hit) + len(missed)
    if not total:
        # Say which of the two it was. django-16333 reported this with the fix's two
        # lines plainly executable, and the message gave no way to tell whether the file
        # had been missed or the lines had -- so the evidence needed to tell them apart
        # is carried out of the container here rather than guessed at afterwards.
        seen = sorted(traced["raw"])
        near = [k for k in seen if any(k.endswith(w) or w.endswith(k) for w in wanted)]
        return {"measured": False,
                "reason": ("the changed lines are all comments or blanks" if near else
                           "the changed file was never imported by this test"),
                "changed_files": sorted(wanted),
                "matched_traced_files": near,
                "traced_file_count": len(seen),
                "test_run_returncode": traced.get("returncode"),
                "test_output_tail": traced.get("test_output_tail", "")[-600:]}

    # A bare line number tells the agent nothing it can act on: to reach line 1631 it
    # has to know what is *on* that line and what guards it. So the source is read back
    # -- the line itself, plus the enclosing `if`/`def`, which is usually the condition
    # that has to be made true for the line to run at all.
    return {"measured": True, "percent": round(100 * len(hit) / total, 1),
            "covered": len(hit), "executable_changed_lines": total,
            "hit": hit, "missed": missed,
            # Which traced file each changed file was scored against. When these differ
            # from the key, coverage followed a copy of the library somewhere else and
            # the line numbers are not comparable -- worth being able to see.
            "matched_files": matched,
            # Carried even when the measurement succeeds, because a *low* number is as
            # likely to be a harness fault as a thin test and there is no way to tell
            # them apart afterwards without it. sympy-12096 reported 0% on a one-line
            # patch its test demonstrably exercises; the only thing that could settle
            # whether the test ran at all under `coverage` was this output.
            "test_run_returncode": traced.get("returncode"),
            "test_output_tail": traced.get("test_output_tail", "")[-600:],
            "missed_source": _annotate(box, missed)}


def _annotate(box: "Sandbox", refs: list[str], guards: int = 4) -> list[dict]:
    """For each `path:line`, the source of that line plus the conditions guarding it."""
    out: list[dict] = []
    by_file: dict[str, list[int]] = {}
    for ref in refs:
        path, _, ln = ref.rpartition(":")
        if ln.isdigit():
            by_file.setdefault(path, []).append(int(ln))
    for path, lines in by_file.items():
        text = box.read(path)
        if text is None:
            continue
        src = text.splitlines()
        for ln in sorted(lines)[:20]:
            if not 1 <= ln <= len(src):
                continue
            body = src[ln - 1]
            indent = len(body) - len(body.lstrip())
            context: list[str] = []
            for j in range(ln - 2, max(-1, ln - 80), -1):
                prev = src[j]
                if not prev.strip():
                    continue
                prev_indent = len(prev) - len(prev.lstrip())
                if prev_indent < indent and prev.lstrip().startswith(
                        ("if ", "elif ", "else", "for ", "while ", "with ", "try",
                         "except", "def ", "async def ", "class ")):
                    context.insert(0, f"{j + 1}: {prev.rstrip()}")
                    indent = prev_indent
                    if prev.lstrip().startswith(("def ", "async def ", "class ")):
                        break
                if len(context) >= guards:
                    break
            out.append({"ref": f"{path}:{ln}", "line": body.rstrip(),
                        "guards": context})
    return out


def repo_conventions(box: "Sandbox", repo: str, gen_path: str) -> dict:
    """How this project organises and runs its tests, read off the repository.

    Every project in this benchmark does it differently -- django has its own runner and
    dotted labels, sympy has bin/test and no pytest at all, scikit-learn keeps tests
    beside the code with no top-level tests/ directory. Putting that in the prompt means
    writing a paragraph per repository and rewriting it whenever a repository is added.
    Reading it off the checkout scales, and it is information the agent could gather
    itself with `run` -- this just saves it a dozen turns of `ls`.
    """
    r = runner_for(repo)
    info: dict = {"runner_command": r["cmd"], "write_your_test_at": gen_path}

    dirs = box.exec(
        "find . -type d -name tests -o -type d -name test 2>/dev/null "
        "| grep -v node_modules | head -12").output.split()
    info["test_directories"] = [d.lstrip("./") for d in dirs][:12]

    names = box.exec(
        "find . -name 'test_*.py' -o -name '*_test.py' 2>/dev/null | head -400"
    ).output.split()
    info["test_file_count"] = len(names)
    info["example_test_files"] = [n.lstrip("./") for n in names[:8]]

    info["conftest_files"] = [c.lstrip("./") for c in box.exec(
        "find . -name conftest.py 2>/dev/null | head -6").output.split()]

    # class-based or plain functions? counted rather than guessed, because it decides
    # what a generated test has to look like to be collected at all.
    cls = box.exec("grep -rl 'class Test\\|unittest.TestCase\\|SimpleTestCase' "
                   "--include='test_*.py' . 2>/dev/null | head -60").output.split()
    fn = box.exec("grep -rl '^def test_' --include='test_*.py' . 2>/dev/null "
                  "| head -60").output.split()
    info["style"] = {"class_based_files": len(cls), "function_based_files": len(fn)}

    sibling = box.exec(
        f"ls {shlex.quote(str(Path(gen_path).parent))} 2>/dev/null | head -10"
    ).output.split()
    info["files_next_to_your_test"] = sibling
    return info


def verify_environment(instance: dict, sample: int = 8, quiet: bool = False) -> dict:
    """Environment gate: do the PASS_TO_PASS tests pass at base?

    They are independent of any test we are judging, so if they fail here the box is
    wrong and no verdict computed in it means anything.
    """
    p2p = json.loads(instance.get("PASS_TO_PASS") or "[]")[:sample]
    if not p2p:
        return {"checked": 0, "ok": True, "detail": "no PASS_TO_PASS ids"}
    repo = instance["repo"]
    targets = (json.loads(instance["PASS_TO_PASS"])[:sample]
               if runner_for(repo)["kind"] == "pytest"
               else patched_test_files(instance["test_patch"]))
    with Sandbox(instance["instance_id"], quiet=quiet) as box:
        # The developer's test patch goes on first, because PASS_TO_PASS was recorded
        # after it was applied. psf__requests-5414 lists
        # test_invalid_url[InvalidURL-http://*example.com], a parametrize case that the
        # test patch *adds* -- so at base that id does not exist, and pytest treats one
        # unknown id as fatal for the whole run: "collected 7 items ... no tests ran".
        # A single missing id was zeroing the entire gate.
        box.apply_patch(instance["test_patch"])
        r = box.exec(test_command(repo, targets), timeout=3600)
    outcomes = parse_output(repo, r.output)
    failed = [n for n in p2p
              if (outcome_of(repo, outcomes, n) or "MISSING") != "PASSED"]
    return {"checked": len(p2p), "ok": not failed, "failed": failed[:5],
            "seen": len(outcomes), "detail": r.output[-800:]}

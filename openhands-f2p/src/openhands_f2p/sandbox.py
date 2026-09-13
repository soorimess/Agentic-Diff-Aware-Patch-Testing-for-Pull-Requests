"""One container per instance, and the only door into it.

`Sandbox` is our own class, not an SDK concept. Every `docker exec` in this project goes
through `exec()` here, which is what makes `--network none` enforceable: the agent runs on
the host and only its effects cross the boundary.

Two guarantees live in this file. The container is disposable -- no volumes are mounted,
so it cannot write to the host at all, and `__exit__` destroys it, discarding whatever the
agent left behind. And the tree\'s state is asked about rather than assumed: since the
agent can apply the patch itself, `ensure_base` checks before the harness trusts a "before
the fix" run.
"""
from __future__ import annotations

import os
import shlex
import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from openhands_f2p import flow
from openhands_f2p.images import (PLATFORM, _run, claim_image, image_for, pull_image,
                                  release_image)

REPO_DIR = "/testbed"

# A git repository for the *harness*, deliberately not inside the checkout.
#
# The tree needs to be diffable -- "the agent created one file and edited nothing else"
# should be a verified fact, not an assumption -- and git does that better than any
# hash manifest. But putting `.git` back under /testbed would change what we measure:
# `setuptools_scm` and friends compute a package version from git, and every verdict on
# record was measured with no repository there. A repo with one untagged commit could
# produce a different version string and break tests for reasons that have nothing to do
# with the agent.
#
# `--git-dir` outside the tree gives the diff without the tree ever knowing. The agent
# still finds no `.git` in the checkout, and the single commit holds nothing but the base
# state, so there is no history to leak either.
TREE_GIT = "/tmp/f2p_tree.git"


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
        # Three attempts. This is the one moment the container has a network, and it is
        # the only chance to get `coverage` in: a single transient PyPI failure cost
        # sympy-24562 its coverage figure, seventy seconds of retrying nothing, and a
        # measurement that could not be recovered without a fresh container.
        installed = False
        for attempt in (1, 2, 3):
            r = self.exec(f"pip install -q {pkgs}", workdir="/", timeout=900)
            installed = r.returncode == 0
            if installed:
                break
            flow.record(flow.SETUP, "install retry",
                        f"attempt {attempt} failed: {r.output.strip()[-160:]}")
            time.sleep(3)
        d = _run(["docker", "network", "disconnect", "bridge", self.container],
                 timeout=120)
        flow.record(flow.SETUP, "install then seal",
                    f"{pkgs}: {'ok' if installed else 'FAILED after 3 attempts'}; "
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

    # -- what the agent changed, verified rather than assumed ------------------
    def _tree_git(self) -> str:
        return f"git --git-dir={TREE_GIT} --work-tree={REPO_DIR}"

    def snapshot_tree(self) -> bool:
        """Commit the tree as it stands, before the agent is let in.

        Respects the project's own `.gitignore`, which is what makes this cheap: the
        build artefacts and `.pyc` files in these images are numerous, uninteresting,
        and already ignored by the repositories themselves.
        """
        g = self._tree_git()
        r = self.exec(
            f"{g} init -q && {g} add -A && "
            f"{g} -c user.email=f2p@local -c user.name=f2p "
            f"commit -q -m base --no-verify", timeout=900)
        ok = r.returncode == 0
        flow.record(flow.SETUP, "snapshot tree",
                    f"{TREE_GIT} holds the base state" if ok
                    else f"could not snapshot: {r.output.strip()[:160]}")
        return ok

    def tree_changes(self) -> list[str]:
        """Paths that differ from the snapshot. Empty when nothing was touched."""
        r = self.exec(f"{self._tree_git()} status --porcelain", timeout=300)
        if r.returncode != 0:
            return []
        return [line[3:].strip().strip('"') for line in r.output.splitlines()
                if len(line) > 3]

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

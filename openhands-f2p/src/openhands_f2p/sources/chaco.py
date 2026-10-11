"""ChaCo: the 145 pull requests of "Change And Cover" (Zhou et al., ICSE 2026).

The dataset is a list of pull request numbers and nothing else --
`config/benchmark/rq_full.json` in https://github.com/UCLA-SEAL/Change-Cover: 50 SciPy,
50 Qiskit and 45 pandas PRs, merged in 2024-2025, chosen because the developer's own
tests leave some of the changed lines uncovered. There is no instance file and no image
to pull; ChaCo's own Dockerfiles check out the PR head and run the whole suite for
coverage. Everything the harness needs is therefore derived here, in three steps:

    prepare   PR metadata from the GitHub API, the change itself from a git mirror:
              base = the merge commit's first parent, change = diff(base, merge commit),
              split into `patch` (source) and `test_patch` (the developer's tests).
              Writes the row and a Dockerfile per PR. No Docker.
    build     the image, from that Dockerfile (image_build.py). /testbed at base,
              dependencies resolved as of the base commit's date (`uv --exclude-newer`),
              the project installed editable so the source patch takes effect.
    validate  in the built image, the developer's test files at base+tests and at
              head+tests: FAIL_TO_PASS = failed before, passed after; PASS_TO_PASS =
              passed on both. SWE-bench computes these the same way.

Only a row whose developer tests actually flip is runnable (listed by `prs()`): our task
is a fail-to-pass test, and a PR whose own tests do not flip -- a refactor, a lint fix --
may have no fail-to-pass test at all. ChaCo's task is different (cover the uncovered
lines, at head, no flip required), so not every ChaCo PR is a valid instance here, and
`validate` records why for each one that is not.

GitHub API calls are cached under `.cache/github/`; `GITHUB_TOKEN` raises the
unauthenticated limit of 60 an hour, which 145 PRs (2-3 calls each) exceed.
"""
from __future__ import annotations

import contextlib
import fcntl
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from openhands_f2p.layout import CACHE, PROJECT_ROOT

NAME = "chaco"
HOME = PROJECT_ROOT / "datasets" / NAME
INSTANCES = HOME / "instances.json"
PRS_FILE = HOME / "prs.json"
DOCKERFILES = HOME / "dockerfiles"
REVIEW = HOME / "review"
BENCHMARK = HOME / "benchmark" / "rq_full.json"
# ChaCo's lists. `full` is the benchmark (RQ1, 145 PRs); `ablation` is the 30 (10 per
# project) its ablation study (RQ3) ran on, all of them inside `full`.
LISTS = {"full": "rq_full.json", "ablation": "rq_ablation.json", "f2p30": "f2p30.json"}
# `f2p30` is ours, not ChaCo's: 10 runnable PRs per project from `full`, chosen by `fill`
# (2026-10-10) -- every one with developer tests that flip and an oracle that agrees.

# The paper's artifact, pinned: the list must not move under a run that cites it.
CHACO_REPO = "UCLA-SEAL/Change-Cover"
CHACO_COMMIT = "d3be9a251d917a657a7675141728977c17aec117"
BENCHMARK_URL = (f"https://raw.githubusercontent.com/{CHACO_REPO}/{CHACO_COMMIT}"
                 f"/config/benchmark/{{name}}")

IMAGE_REPO = "f2p-chaco"
GH_CACHE = CACHE / "github"
MIRRORS = CACHE / "mirrors"


# ------------------------------------------------------------------ identities
def instance_id(repo: str, number: int) -> str:
    """SWE-bench's convention: `owner__repo-number`, case kept (`Qiskit__qiskit-12335`)."""
    owner, name = repo.split("/")
    return f"{owner}__{name}-{number}"


def parse_id(iid: str) -> tuple[str, int]:
    m = re.fullmatch(r"(.+?)__(.+)-(\d+)", iid)
    if not m:
        raise SystemExit(f"{iid!r} is not an owner__repo-number id")
    return f"{m.group(1)}/{m.group(2)}", int(m.group(3))


def image_for(iid: str) -> str:
    # Docker repository names are lower case; the id keeps GitHub's case.
    return f"{IMAGE_REPO}/{iid.lower()}:latest"


# ------------------------------------------------------------------ the benchmark list
def benchmark(which: str = "full") -> list[tuple[str, int]]:
    """(repo, PR number) of one of ChaCo's lists, in its order. Fetched once, then read
    from `benchmark/` (pinned at CHACO_COMMIT)."""
    if which not in LISTS:
        raise SystemExit(f"unknown ChaCo list {which!r}; known: {', '.join(LISTS)}")
    path = BENCHMARK.parent / LISTS[which]
    if not path.exists() and which == "f2p30":
        raise SystemExit("the f2p30 list does not exist yet; `sources fill chaco` makes it")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(BENCHMARK_URL.format(name=LISTS[which]),
                                    timeout=60) as r:
            path.write_bytes(r.read())
    projects = json.loads(path.read_text())["projects"]
    return [(repo, int(n)) for repo, v in projects.items() for n in v["pr_numbers"]]


def lists_of(iid: str) -> list[str]:
    """The ChaCo lists this PR is on."""
    repo, n = parse_id(iid)
    # Only lists that exist: `f2p30` is written by `fill`, after the rows it is made from.
    # Asking for it before then raised, which ended `prepare` before it rewrote a single
    # Dockerfile -- and the SciPy images were rebuilt without their import fix (2026-10-10).
    return [name for name in LISTS
            if (name != "f2p30" or (BENCHMARK.parent / LISTS[name]).exists())
            and (repo, n) in benchmark(name)]


# ------------------------------------------------------------------ GitHub, cached
def _gh(path: str):
    """One GitHub API GET, kept on disk so a re-prepare costs no quota."""
    cached = GH_CACHE / (path.strip("/").replace("/", "__") + ".json")
    if cached.exists():
        return json.loads(cached.read_text())
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "openhands-f2p"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com/{path.lstrip('/')}",
                                 headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 403 and e.headers.get("x-ratelimit-remaining") == "0":
            reset = int(e.headers.get("x-ratelimit-reset") or 0)
            raise SystemExit(
                f"GitHub API rate limit reached (resets in {max(0, reset - int(time.time()))}"
                f" s). Set GITHUB_TOKEN for 5000 calls an hour; what was fetched is cached.")
        raise
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_text(json.dumps(data))
    return data


# ------------------------------------------------------------------ git mirror
def _git(args: list[str], cwd: Path | None = None, timeout: int = 1800) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                       timeout=timeout)
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args[:3])}: {r.stderr.strip()[-600:]}")
    return r.stdout


def mirror(repo: str) -> Path:
    """A blobless bare clone: every commit and ref, file contents fetched on demand."""
    d = MIRRORS / (repo.replace("/", "__") + ".git")
    if not d.exists():
        d.parent.mkdir(parents=True, exist_ok=True)
        _git(["clone", "--bare", "--filter=blob:none", "-q",
              f"https://github.com/{repo}.git", str(d)], timeout=3600)
    return d


def _have_commit(git_dir: Path, sha: str) -> bool:
    return subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=git_dir,
                          capture_output=True).returncode == 0


# ------------------------------------------------------------------ the split
# Compiled sources. pandas and SciPy are installed editable with meson-python, which
# rebuilds changed extensions on the next import (offline, in the container), so a patch
# touching them still takes effect. Qiskit's Rust is built once by setuptools-rust and is
# not rebuilt on import: a Qiskit patch touching `crates/` would leave the head run on the
# base binary. Such rows are recorded and not run.
COMPILED = (".pyx", ".pxd", ".pxi", ".c", ".h", ".cpp", ".hpp", ".cc", ".f", ".f90",
            ".rs")


def is_test_path(path: str) -> bool:
    """`coverage_metric.is_test_file`, plus a top-level `test/` (Qiskit's tests live in
    `test/python/...`, and its helpers there are not named `test_*`)."""
    from openhands_f2p.coverage_metric import is_test_file
    return is_test_file(path) or path.split("/", 1)[0] in ("test", "tests", "testing")


def split_diff(diff: str) -> tuple[str, str, list[str]]:
    """(source patch, test patch, binary files left out)."""
    src, tests, binary = [], [], []
    for chunk in re.split(r"(?m)^(?=diff --git )", diff):
        if not chunk.startswith("diff --git "):
            continue
        path = chunk.split("\n", 1)[0].split(" b/", 1)[-1].strip()
        if re.search(r"(?m)^(Binary files |GIT binary patch)", chunk):
            binary.append(path)
            continue
        (tests if is_test_path(path) else src).append(chunk)
    return "".join(src), "".join(tests), binary


# ------------------------------------------------------------------ problem text
_CLOSES = re.compile(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+"
                     r"(?:https://github\.com/[\w.-]+/[\w.-]+/issues/|#)(\d+)")


def _clean(body: str | None) -> str:
    body = re.sub(r"(?s)<!--.*?-->", "", body or "")
    # The contribution checklist pandas and Qiskit put in every PR says nothing about
    # the change.
    body = "\n".join(ln for ln in body.splitlines()
                     if not re.match(r"\s*- \[[ xX]\]", ln))
    return body.strip()


def hints(repo: str, issues: list[int], before: str) -> str:
    """SWE-bench's `hints_text`: comments on the issue posted before the fix existed.

    SWE-bench cuts at the fix's first commit; this cuts at the PR's creation, which is
    the same moment for a PR opened with its first commit and a little later otherwise.
    """
    out = []
    for n in issues:
        try:
            comments = _gh(f"repos/{repo}/issues/{n}/comments?per_page=100")
        except urllib.error.HTTPError:
            continue
        out += [c.get("body") or "" for c in comments if c.get("created_at", "") < before]
    return "\n".join(c.strip() for c in out if c.strip())


def problem_statement(repo: str, pr: dict) -> tuple[str, list[int]]:
    """The issues the PR says it closes, then the PR's own title and description.

    SWE-bench's problem statement is the issue alone. Here the issue comes first, as the
    nearest equivalent, and the PR text after it, because many of these PRs close no
    issue and their description is then the only account of what changed and why.
    """
    issues = sorted({int(n) for n in _CLOSES.findall(pr.get("body") or "")})
    parts = []
    for n in issues:
        try:
            it = _gh(f"repos/{repo}/issues/{n}")
        except urllib.error.HTTPError:
            continue
        parts.append(f"Issue #{n}: {it.get('title', '').strip()}\n\n{_clean(it.get('body'))}")
    parts.append(f"Pull request #{pr['number']}: {pr['title'].strip()}\n\n"
                 f"{_clean(pr.get('body'))}")
    return "\n\n---\n\n".join(p.strip() for p in parts), issues


# ------------------------------------------------------------------ images
# Per repository: the base image, the system packages, how dependencies are installed
# and how the project is installed. Adapted from ChaCo's own Dockerfiles (docker/<proj>/),
# with three changes so the image meets the harness's contract: the checkout is at
# /testbed and at the *base* commit (ChaCo builds the PR head), everything runs as root,
# and nothing runs the test suite at build time. Dependencies are resolved as of the
# base commit's date, so a 2024 PR does not meet a 2026 numpy.
RECIPES = {
    "pandas-dev/pandas": {
        "python": "3.11",
        "dist": "pandas",
        # The X and GL libraries are for pytest-qt, which requirements-dev.txt installs
        # and pytest loads as a plugin: without libgthread every pandas test run is an
        # INTERNALERROR before collection (found by `validate`, 2026-10-08). ChaCo's own
        # pandas Dockerfile installs the same set.
        "apt": ("git build-essential pkg-config curl libhdf5-dev libglib2.0-0 "
                "libgles2-mesa-dev libsm6 libxrender1 libxext6"),
        "deps": "uv pip install --system --exclude-newer {date} -r requirements-dev.txt",
        "install": "python -m pip install --no-build-isolation -e . ",
        "check": "python -c 'import pandas; print(pandas.__version__)'",
    },
    "scipy/scipy": {
        "python": "3.12",
        "dist": "scipy",
        "apt": "git build-essential gfortran pkg-config curl libopenblas-dev liblapack-dev",
        "submodules": True,
        "deps": ("uv pip install --system --exclude-newer {date} "
                 "-r requirements/build.txt -r requirements/test.txt "
                 "-r requirements/default.txt"),
        "install": "python -m pip install --no-build-isolation -e . ",
        "check": "python -c 'import scipy; print(scipy.__version__)'",
        # meson-python's editable import hook knows only the files that existed at build
        # time, and SciPy's meson.build lists its test files one by one -- so a *new* test
        # file under scipy/ cannot be imported as `scipy.x.tests.test_new` at all
        # ("ModuleNotFoundError", every SciPy agent run of 2026-10-09). pytest's importlib
        # mode imports a test file by path instead. Existing SciPy test files give the same
        # results either way (25 of 28 relative-import files compared; the 3 that differ
        # are the vendored array_api_compat tests, which fail in both modes).
        "env": "PYTEST_ADDOPTS=--import-mode=importlib",
    },
    "Qiskit/qiskit": {
        "python": "3.11",
        "dist": "qiskit",
        "apt": "git build-essential pkg-config curl",
        "rust": True,
        "deps": ("uv pip install --system --exclude-newer {date} "
                 "$( [ -f constraints.txt ] && echo -c constraints.txt ) "
                 "-r requirements.txt -r requirements-dev.txt setuptools-rust 'pytest<8.2'"),
        # pytest: Qiskit runs its suite with stestr, and the harness runs tests with pytest
        # (it reads pytest's output), which collects Qiskit's unittest classes as they
        # are. Not in requirements-dev.txt; ChaCo's Qiskit Dockerfile adds it too.
        # Below 8.2: pytest 8.2 instantiates unittest classes while collecting, and
        # Qiskit's testtools-based QiskitTestCase then fails with "object has no
        # attribute 'runTest'" -- test_random_circuit.py collected two errors and no
        # test on either side (Qiskit-12483, 2026-10-09).
        "install": "python -m pip install --no-build-isolation -e . ",
        "check": "python -c 'import qiskit; print(qiskit.__version__)'",
    },
}


def dockerfile(row: dict) -> str:
    r = RECIPES[row["repo"]]
    date = row["base_date"]
    lines = [
        f"# {row['instance_id']}: {row['source_url']}",
        f"# Generated by openhands_f2p/sources/chaco.py. /testbed at base {row['base_commit']}",
        f"# (first parent of merge commit {row['merge_commit']}); dependencies as of {date}.",
        f"FROM python:{r['python']}-slim-bookworm",
        "ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1 PYTHONUNBUFFERED=1 "
        "LANG=C.UTF-8",
        f"RUN apt-get update && apt-get install -y --no-install-recommends {r['apt']} "
        "&& rm -rf /var/lib/apt/lists/*",
    ]
    if r.get("rust"):
        lines += ["ENV RUSTUP_HOME=/opt/rustup CARGO_HOME=/opt/cargo "
                  "PATH=/opt/cargo/bin:$PATH",
                  "RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs "
                  "| sh -s -- -y --profile minimal --default-toolchain stable "
                  "&& ln -s /opt/cargo/bin/* /usr/local/bin/"]
    lines += [
        "RUN pip install uv",
        f"RUN git clone --filter=blob:none -q https://github.com/{row['repo']}.git /testbed "
        f"&& cd /testbed && git checkout -q {row['base_commit']}",
        "WORKDIR /testbed",
    ]
    if r.get("submodules"):
        lines.append("RUN git submodule update --init --recursive --depth 1 -q")
    lines += [
        "RUN " + r["deps"].format(date=date),
        "RUN " + r["install"],
        # The harness's `coverage` wheel is installed offline per run (Sandbox); the
        # project's own test dependencies are all here, because the run has no network.
        "RUN " + r["check"],
        # OpenBLAS picks its kernels from cpuid, and on the server's QEMU virtual CPU it
        # picks one that executes an instruction the CPU lacks: SciPy's test_lapack.py
        # died with "Illegal instruction" after 8 of 1927 tests (2026-10-09). Haswell
        # (AVX2, FMA) is what that CPU and any recent x86 has; with it all 1926 pass.
        # Last, so changing it rebuilds one layer.
        "ENV OPENBLAS_CORETYPE=Haswell",
        *([f"ENV {r['env']}"] if r.get("env") else []),
    ]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ rows
def _read_rows() -> dict[str, dict]:
    if not INSTANCES.exists():
        return {}
    return {r["instance_id"]: r for r in json.loads(INSTANCES.read_text())}


@contextlib.contextmanager
def _locked():
    """One writer at a time: `build`/`validate --parallel` run a process per PR, and each
    saves its own row into the shared file."""
    INSTANCES.parent.mkdir(parents=True, exist_ok=True)
    with open(INSTANCES.with_suffix(".lock"), "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        yield


def save_row(row: dict) -> None:
    """Replace one row, re-reading the file under the lock so a sibling's row survives."""
    with _locked():
        rows = _read_rows()
        rows[row["instance_id"]] = row
        _write_rows(rows)


def _write_rows(rows: dict[str, dict]) -> None:
    INSTANCES.parent.mkdir(parents=True, exist_ok=True)
    order = {instance_id(r, n): i for i, (r, n) in enumerate(benchmark())}
    ordered = sorted(rows.values(), key=lambda r: order.get(r["instance_id"], 1 << 30))
    INSTANCES.write_text(json.dumps(ordered, indent=1) + "\n")
    runnable = [{"id": r["instance_id"], "tier": 0, "runner": "pytest",
                 "version": r.get("version", ""), "build": "built", "localise": "unknown",
                 "lists": r.get("chaco_lists", []),
                 "note": r["title"][:100], "why": r["source_url"]}
                for r in ordered if r.get("status") == "runnable"]
    PRS_FILE.write_text(json.dumps(runnable, indent=1) + "\n")


def prepare_one(repo: str, number: int) -> dict:
    iid = instance_id(repo, number)
    pr = _gh(f"repos/{repo}/pulls/{number}")
    row = {"instance_id": iid, "repo": repo, "pull_number": number,
           "dataset": NAME, "image": image_for(iid), "image_source": "build",
           "source_url": pr["html_url"], "title": pr["title"],
           "created_at": pr["created_at"], "merged_at": pr.get("merged_at"),
           "hints_text": "", "version": "", "FAIL_TO_PASS": "[]", "PASS_TO_PASS": "[]"}
    if not pr.get("merged") or not pr.get("merge_commit_sha"):
        return {**row, "base_commit": "", "patch": "", "test_patch": "",
                "problem_statement": "", "status": "unsupported",
                "why": "not merged: no merge commit to take the change from"}
    git_dir = mirror(repo)
    merge = pr["merge_commit_sha"]
    if not _have_commit(git_dir, merge):
        _git(["fetch", "-q", "origin", merge], cwd=git_dir)
    base = _git(["rev-parse", f"{merge}^1"], cwd=git_dir).strip()
    base_date = _git(["show", "-s", "--format=%cI", base], cwd=git_dir).strip()
    diff = _git(["diff", "--no-renames", "--full-index", base, merge], cwd=git_dir,
                timeout=3600)
    patch, test_patch, binary = split_diff(diff)
    problem, issues = problem_statement(repo, pr)
    row.update(base_commit=base, environment_setup_commit=base, merge_commit=merge,
               base_date=base_date, patch=patch, test_patch=test_patch,
               problem_statement=problem, closes_issues=issues,
               hints_text=hints(repo, issues, pr["created_at"]),
               chaco_lists=lists_of(iid), binary_files_left_out=binary)
    compiled = [p for p in _paths(patch) if p.endswith(COMPILED)]
    row["compiled_files"] = compiled
    if repo not in RECIPES:
        row.update(status="unsupported", why=f"no image recipe for {repo}")
    elif not patch.strip():
        row.update(status="unsupported", why="the change touches only test files")
    elif not any(p.endswith(".py") for p in _paths(patch)):
        row.update(status="unsupported", why="the change touches no Python source")
    elif not test_patch.strip():
        # Common in ChaCo, whose PRs were chosen for lines their own tests leave
        # uncovered: 9 of the 30 ablation PRs add no test at all. FAIL_TO_PASS cannot be
        # derived, and the developer column of mutation is "not measured"; the image is
        # still built and `validate` checks the patch applies and reverts in it, because
        # the user runs the whole ablation list (2026-10-11).
        row.update(status="no-developer-test",
                   why="the PR adds or changes no test: FAIL_TO_PASS cannot be derived")
    elif any(p.endswith(".rs") for p in compiled):
        # Qiskit's Rust is built once and not rebuilt when the patch is applied. Whether
        # the developer's tests still flip on the Python half alone is for `validate`
        # to find out, not to be assumed here.
        row.update(status="prepared",
                   why=f"awaiting build and validate; the change also touches Rust "
                       f"({compiled[:2]}), which is not rebuilt when the patch is applied")
    else:
        row.update(status="prepared", why="awaiting build and validate")
    if row["status"] != "unsupported":
        DOCKERFILES.mkdir(parents=True, exist_ok=True)
        (DOCKERFILES / f"{iid}.Dockerfile").write_text(dockerfile(row))
    return row


def _paths(diff: str) -> list[str]:
    return [ln.split(" b/", 1)[-1].strip() for ln in diff.splitlines()
            if ln.startswith("diff --git ")]


VALIDATION_FIELDS = ("FAIL_TO_PASS", "PASS_TO_PASS", "status", "why", "validated_at",
                     "validation", "version")


def prepare(ids: list[str] | None = None) -> list[dict]:
    """Rows for `ids`: instance ids, or a list name (`full`, `ablation`); all 145 when None.

    A row is always re-derived. When its base, change and tests come out identical, what
    `validate` found is kept; when any of them differ, the row goes back to `prepared`.
    """
    if not ids:
        todo = benchmark("full")
    else:
        todo = []
        for i in ids:
            todo += benchmark(i) if i in LISTS else [parse_id(i)]
    out = []
    for repo, number in todo:
        iid = instance_id(repo, number)
        row = prepare_one(repo, number)
        old = _read_rows().get(iid)
        if (old and old.get("validated_at") and row["status"] in ("prepared", "no-developer-test")
                and all(old.get(k) == row.get(k)
                        for k in ("base_commit", "patch", "test_patch"))):
            row.update({k: old[k] for k in VALIDATION_FIELDS if k in old})
        save_row(row)
        out.append(row)
        print(f"  {row['status']:<16} {iid:32s} {row.get('why', '')[:70]}")
    return out


# ------------------------------------------------------------------ validate
def validate(iid: str, quiet: bool = False) -> dict:
    """Derive FAIL_TO_PASS / PASS_TO_PASS by running the developer's tests, both sides.

    Then the oracle -- the same `verify()` an agent run is judged by, given the
    developer's test -- must reproduce the flip, or the row is not runnable.
    """
    from openhands_f2p import swebench_env as E
    from openhands_f2p import verify as V
    from openhands_f2p import sources

    rows = _read_rows()
    if iid not in rows:
        raise SystemExit(f"{iid} is not prepared; run prepare first")
    row = rows[iid]
    if row["status"] == "unsupported":
        print(f"  {iid}: {row['status']} -- {row.get('why')}")
        return row
    sources.select(NAME)
    files = E.patched_test_files(row["test_patch"])
    with E.Sandbox(iid, quiet=quiet) as box:
        # The image's checkout, read before `.git` goes: it has to be the base commit.
        head = box.exec("git rev-parse HEAD").stdout.strip()
        if head != row["base_commit"]:
            row.update(status="broken-env", validated_at=time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()), validation={"image_head": head},
                why=f"the image's /testbed is at {head[:12]}, not the base commit "
                    f"{row['base_commit'][:12]}")
            save_row(row)
            print(f"  {row['status']:<16} {iid:32s} {row['why'][:90]}")
            return row
        box.strip_git()
        if not row["test_patch"].strip():
            # No developer test: what can still be checked is that the change applies to
            # this tree and comes off it again, exactly as the harness will do it.
            box.apply_patch(row["patch"])
            at_head = box.patch_state(row["patch"])
            box.apply_patch(row["patch"], revert=True)
            at_base = box.patch_state(row["patch"])
            ok = at_head == "head" and at_base == "base"
            row.update(validated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       validation={"image_head": head, "patch_applies": ok},
                       status="no-developer-test" if ok else "broken-env",
                       why=("no developer test (FAIL_TO_PASS cannot be derived); image at "
                            "the base commit, patch applies and reverts" if ok else
                            f"patch did not apply and revert cleanly ({at_head}/{at_base})"))
            dist = RECIPES[row["repo"]]["dist"]
            v = box.exec("python -c \"import importlib.metadata as m; print(m.version('"
                         + dist + "'))\"", workdir="/").stdout.strip().splitlines()
            m = re.match(r"(\d+)\.(\d+)", v[-1] if v else "")
            row["version"] = f"{m.group(1)}.{m.group(2)}" if m else ""
            save_row(row)
            print(f"  {row['status']:<16} {iid:32s} {row['why'][:90]}")
            return row
        box.apply_patch(row["test_patch"])
        files = [f for f in files if box.exists(f)]
        cmd = E.test_command(box, files)
        before = box.exec(cmd, timeout=3600)
        box.apply_patch(row["patch"])
        after = box.exec(cmd, timeout=3600)
        b, a = E.parse_output(before.output), E.parse_output(after.output)
        # The verdict's rule: a test module that imports only once the change is applied
        # failed at base (`V.unimportable_at_base`).
        b = V.unimportable_at_base(b, a)
        f2p = sorted(n for n, s in b.items() if s in V.BEHAVIOURAL and a.get(n) == "PASSED")
        p2p = sorted(n for n, s in b.items() if s == "PASSED" and a.get(n) == "PASSED")
        box.apply_patch(row["patch"], revert=True)
        box.apply_patch(row["test_patch"], revert=True)
        # SWE-bench's `version`: the package's major.minor, read off the installed copy.
        dist = RECIPES[row["repo"]]["dist"]
        v = box.exec("python -c \"import importlib.metadata as m; print(m.version('"
                     + dist + "'))\"", workdir="/").stdout.strip().splitlines()
        m = re.match(r"(\d+)\.(\d+)", v[-1] if v else "")
        row["version"] = f"{m.group(1)}.{m.group(2)}" if m else ""

        def tally(o: dict) -> dict:
            out: dict[str, int] = {}
            for st in o.values():
                out[st] = out.get(st, 0) + 1
            return out
        row.update(FAIL_TO_PASS=json.dumps(f2p), PASS_TO_PASS=json.dumps(p2p),
                   validated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   validation={"image_head": head, "patch_applies": True,
                               "test_files": files, "collected_before": len(b),
                               "collected_after": len(a),
                               "outcomes_before": tally(b), "outcomes_after": tally(a),
                               "exit_before": before.returncode,
                               "exit_after": after.returncode,
                               "tail_before": before.output.strip()[-1500:],
                               "tail_after": after.output.strip()[-1500:],
                               "runner": E.runner_for(box)["cmd"]})
        # pytest ends every complete run with its summary line ("== 8 passed in 6.6s ==").
        # Without it the run died part-way -- a crash in a C extension, a timeout -- and
        # its outcomes are a prefix of the real ones (scipy, 2026-10-09: an illegal
        # instruction in OpenBLAS ended test_lapack.py after 8 of 1927 tests).
        done = re.compile(r"(?m)^=+ .*\bin [\d.]+s( \([^)]*\))? =+\s*$")
        unfinished = [side for side, r in (("before", before), ("after", after))
                      if not done.search(r.output)]
        if unfinished:
            row.update(status="broken-env",
                       why=f"pytest did not finish {' and '.join(unfinished)} the change "
                           f"(exit {before.returncode}/{after.returncode}): "
                           + (before if "before" in unfinished else after)
                           .output.strip()[-200:])
        elif (not b and not a) or (b and a and all(st == "ERROR" for st in b.values())
                                    and all(st == "ERROR" for st in a.values())):
            # Errors only, on both sides: the files never ran a test (a module that does not
            # import even with the change, a collection incompatibility).
            row.update(status="broken-env",
                       why="the developer's test files run no test on either side "
                           "(nothing collected, or only collection errors): "
                           + before.output.strip()[-300:])
        elif not f2p:
            row.update(status="not-fail-to-pass",
                       why=f"no developer test fails before the change and passes after "
                           f"({len(p2p)} pass on both sides)")
        else:
            oracle = V.verify(row, box, use_gold_test=True, coverage=False, quiet=True)
            if oracle.f2p == "YES":
                row.update(status="runnable",
                           why=f"{len(f2p)} developer test(s) flip; oracle reproduces it")
            else:
                row.update(status="oracle-mismatch",
                           why=f"derived {len(f2p)} flipping test(s) but verify() says "
                               f"{oracle.f2p}: {oracle.why[:200]}")
    save_row(row)
    print(f"  {row['status']:<16} {iid:32s} {row['why'][:90]}")
    return row


# ------------------------------------------------------------------ fill: a list of 30
PROJECTS = ("scipy/scipy", "Qiskit/qiskit", "pandas-dev/pandas")
CANDIDATE = ("prepared", "runnable", "broken-env", "oracle-mismatch")


def fill(per_project: int = 10, seed: int = 0, parallel: int = 4,
         redo: tuple[str, ...] = ()) -> dict[str, list[str]]:
    """Build and validate candidates until each project has `per_project` runnable PRs.

    Order per project: rows already runnable first (re-checked: `redo` lists those whose
    image changed since), then every other candidate with a developer test, shuffled by
    `seed` so the choice is reproducible and nobody picked it. Stops building a project
    once it has enough; the list is written to `benchmark/f2p30.json` in ChaCo's format.
    """
    import random
    rows = _read_rows()
    queue: dict[str, list[str]] = {}
    for repo in PROJECTS:
        mine = [r for r in rows.values() if r["repo"] == repo and r["status"] in CANDIDATE
                and "full" in r.get("chaco_lists", ["full"])]
        done = sorted(r["instance_id"] for r in mine if r["status"] == "runnable")
        rest = sorted(r["instance_id"] for r in mine if r["status"] != "runnable")
        random.Random(f"{seed}:{repo}").shuffle(rest)
        queue[repo] = done + rest
    chosen: dict[str, list[str]] = {repo: [] for repo in PROJECTS}
    checked: set[str] = set()

    def status(iid: str) -> str:
        return _read_rows()[iid]["status"]

    while True:
        batch = []
        for repo in PROJECTS:
            need = per_project - len(chosen[repo])
            pending = [i for i in queue[repo] if i not in checked]
            batch += pending[:max(0, need)]
        if not batch:
            break
        batch = batch[:max(parallel, 1) * 2]
        todo = [i for i in batch if i in redo or status(i) != "runnable"]
        if todo:
            ids = ",".join(todo)
            for action, extra in (("build", ["--rebuild"]), ("validate", [])):
                subprocess.run([sys.executable, "-m", "openhands_f2p.sources", action, NAME,
                                ids, "--parallel", str(parallel), *extra])
        for iid in batch:
            checked.add(iid)
            repo = rows[iid]["repo"]
            if status(iid) == "runnable" and len(chosen[repo]) < per_project:
                chosen[repo].append(iid)
        print("  fill: " + ", ".join(f"{r.split('/')[1]} {len(c)}/{per_project}"
                                     for r, c in chosen.items()), flush=True)
    out = {"note": f"ours, not ChaCo's: {per_project} runnable PRs per project from rq_full, "
                   f"seed {seed}, made by `sources fill chaco`",
           "projects": {repo: {"pr_numbers": [parse_id(i)[1] for i in ids]}
                        for repo, ids in chosen.items()}}
    path = BENCHMARK.parent / LISTS["f2p30"]
    path.write_text(json.dumps(out, indent=1) + "\n")
    for iid in (i for ids in chosen.values() for i in ids):
        row = _read_rows()[iid]
        row["chaco_lists"] = lists_of(iid)
        save_row(row)
    return chosen


# ------------------------------------------------------------------ check: against GitHub
def _counts(diff: str) -> dict[str, tuple[int, int]]:
    """Lines added and removed per file in a unified diff, counted inside hunks only."""
    out: dict[str, list[int]] = {}
    cur, in_hunk = None, False
    for ln in diff.splitlines():
        if ln.startswith("diff --git "):
            cur, in_hunk = ln.split(" b/", 1)[-1].strip(), False
            out.setdefault(cur, [0, 0])
        elif ln.startswith("@@"):
            in_hunk = True
        elif in_hunk and cur:
            if ln.startswith("+"):
                out[cur][0] += 1
            elif ln.startswith("-"):
                out[cur][1] += 1
    return {k: (a, d) for k, (a, d) in out.items()}


def check(which: str = "ablation") -> tuple[Path, int]:
    """Cross-check every row of `which` against GitHub's own record of the PR.

    Independent of how `prepare` derived the row: the PR, the merge commit's parents and
    the base...merge comparison all come from the GitHub API, not from our git mirror,
    and are compared with what the row says. Adds what `validate` saw inside the image
    (its checkout is the base commit, the patch applies and reverts). Writes
    `review/CHECK.md`; returns it and the number of PRs with a problem.
    """
    rows = _read_rows()
    ids = [instance_id(r, n) for r, n in benchmark(which)]
    lines = [f"# ChaCo `{which}`: cross-check against GitHub", "",
             f"Generated by `python -m openhands_f2p.sources check chaco {which}` "
             f"({time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}). Each row of "
             "[`instances.json`](../instances.json) compared with the GitHub API -- the PR, "
             "the merge commit's parents, and GitHub's own `base...merge` comparison -- "
             "plus what `validate` found inside the built image.", "",
             "| PR | merged, same merge commit | base = merge's 1st parent | files and +/- "
             "lines match GitHub | tests vs source split | problem statement | image at "
             "base, patch applies | status |", "|---|---|---|---|---|---|---|---|"]
    details, bad = [], 0
    for iid in ids:
        r = rows.get(iid)
        if r is None:
            lines.append(f"| {iid} | not prepared | | | | | | |")
            bad += 1
            continue
        repo, n = r["repo"], r["pull_number"]
        probs: list[str] = []
        pr = _gh(f"repos/{repo}/pulls/{n}")
        c1 = bool(pr.get("merged")) and pr.get("merge_commit_sha") == r.get("merge_commit")
        if not c1:
            probs.append(f"PR merged={pr.get('merged')}, GitHub merge commit "
                         f"{str(pr.get('merge_commit_sha'))[:12]} vs row {r.get('merge_commit', '')[:12]}")
        commit = _gh(f"repos/{repo}/commits/{r['merge_commit']}")
        parents = [p["sha"] for p in commit.get("parents", [])]
        c2 = bool(parents) and parents[0] == r["base_commit"]
        if not c2:
            probs.append(f"merge commit parents {[p[:12] for p in parents]}, row base "
                         f"{r['base_commit'][:12]}")
        cmp = _gh(f"repos/{repo}/compare/{r['base_commit']}...{r['merge_commit']}")
        gh = {}
        for f in cmp.get("files", []):
            if f.get("status") == "renamed" and f.get("previous_filename"):
                gh.setdefault(f["previous_filename"], ("renamed-from", 0))
            gh[f["filename"]] = (f.get("additions", 0), f.get("deletions", 0))
        ours = _counts(r.get("patch", "") + r.get("test_patch", ""))
        skipped = set(r.get("binary_files_left_out") or [])
        diff_issues = []
        for path in sorted(set(gh) | set(ours)):
            if path in skipped:
                continue
            g, o = gh.get(path), ours.get(path)
            if g is None or o is None:
                diff_issues.append(f"`{path}` only in {'ours' if g is None else 'GitHub'}")
            elif g[0] != "renamed-from" and g != o:
                diff_issues.append(f"`{path}` +{o[0]}/-{o[1]} ours vs +{g[0]}/-{g[1]} GitHub")
        c3 = not diff_issues and len(cmp.get("files", [])) < 300
        if not c3:
            probs += diff_issues[:5] or ["GitHub lists 300+ files (truncated)"]
        tests, srcs = _paths(r.get("test_patch", "")), _paths(r.get("patch", ""))
        mis = [f for f in tests if not is_test_path(f)] + [f for f in srcs if is_test_path(f)]
        c4 = not mis
        if not c4:
            probs.append(f"split: {mis[:3]}")
        ps = r.get("problem_statement", "")
        c5 = pr["title"].strip() in ps and all(f"Issue #{i}:" in ps
                                              for i in r.get("closes_issues", []))
        if not c5:
            probs.append("problem statement lacks the PR title or a closed issue")
        v = r.get("validation") or {}
        c6 = v.get("image_head") == r["base_commit"] and v.get("patch_applies") is True
        if not c6:
            probs.append(f"image check: head={str(v.get('image_head'))[:12]}, "
                         f"patch_applies={v.get('patch_applies')}")
        ok = all((c1, c2, c3, c4, c5, c6))
        bad += not ok
        mark = lambda b: "✓" if b else "**✗**"
        lines.append(f"| [{iid}]({iid}.md) | {mark(c1)} | {mark(c2)} | {mark(c3)} "
                     f"({len(ours)} files) | {mark(c4)} | {mark(c5)} | {mark(c6)} | "
                     f"{r.get('status')} |")
        if probs:
            details.append(f"- **{iid}**: " + "; ".join(probs))
    lines += ["", f"**{len(ids) - bad} of {len(ids)} PRs pass every check.**", ""]
    if details:
        lines += ["## Problems", "", *details, ""]
    REVIEW.mkdir(parents=True, exist_ok=True)
    out = REVIEW / "CHECK.md"
    out.write_text("\n".join(lines) + "\n")
    return out, bad


# ------------------------------------------------------------------ review pages


def _fence(text: str, lang: str = "") -> str:
    ticks = "````" if "```" in text else "```"
    return f"{ticks}{lang}\n{text.rstrip()}\n{ticks}"


def review(which: str = "ablation") -> Path:
    """One Markdown page per row of `which`, plus an index -- everything the harness
    will use for that PR, laid out for a person to check against GitHub.

    Generated from `instances.json`; never edited by hand.
    """
    rows = _read_rows()
    ids = [instance_id(r, n) for r, n in benchmark(which)] if which in LISTS \
        else [i.strip() for i in which.split(",")]
    REVIEW.mkdir(parents=True, exist_ok=True)
    index = [f"# ChaCo `{which}` list: per-PR review", "",
             "Generated by `python -m openhands_f2p.sources review chaco "
             f"{which}` from [`instances.json`](../instances.json). One page per PR with "
             "everything the harness uses: base and merge commits, the source patch, "
             "the developer's test patch, FAIL_TO_PASS, the problem statement and hints.",
             "", "| PR | project | status | F2P | P2P | version | src / test files | title |",
             "|---|---|---|---|---|---|---|---|"]
    for iid in ids:
        r = rows.get(iid)
        if r is None:
            index.append(f"| {iid} | | not prepared | | | | | |")
            continue
        f2p = json.loads(r.get("FAIL_TO_PASS") or "[]")
        p2p = json.loads(r.get("PASS_TO_PASS") or "[]")
        src, tst = _paths(r.get("patch", "")), _paths(r.get("test_patch", ""))
        repo = r["repo"]
        index.append(f"| [{iid}]({iid}.md) | {repo.split('/')[1]} | {r.get('status')} | "
                     f"{len(f2p)} | {len(p2p)} | {r.get('version', '')} | "
                     f"{len(src)} / {len(tst)} | {r.get('title', '')[:70].replace('|', '/')} |")
        gh = f"https://github.com/{repo}"
        issues = ", ".join(f"[#{n}]({gh}/issues/{n})" for n in r.get("closes_issues", [])) \
            or "none"
        lines = [
            f"# {iid}", "",
            f"[back to the list](README.md) -- **{r.get('title', '')}**", "",
            "| field | value |", "|---|---|",
            f"| pull request | [{repo}#{r['pull_number']}]({r['source_url']}) "
            f"(created {r.get('created_at', '')[:10]}, merged {str(r.get('merged_at'))[:10]}) |",
            f"| ChaCo lists | {', '.join(r.get('chaco_lists', []))} |",
            f"| status | **{r.get('status')}** -- {r.get('why', '')} |",
            f"| base commit | [`{r.get('base_commit', '')[:12]}`]({gh}/commit/{r.get('base_commit', '')}) "
            f"({r.get('base_date', '')[:10]}), first parent of the merge commit |",
            f"| merge commit | [`{r.get('merge_commit', '')[:12]}`]({gh}/commit/{r.get('merge_commit', '')}) |",
            f"| issues closed | {issues} |",
            f"| version | {r.get('version') or '(set by validate)'} |",
            f"| image | `{r.get('image')}` -- [Dockerfile](../dockerfiles/{iid}.Dockerfile) |",
            f"| source files (`patch`) | {', '.join(f'`{x}`' for x in src) or 'none'} |",
            f"| test files (`test_patch`) | {', '.join(f'`{x}`' for x in tst) or 'none'} |",
            f"| compiled files changed | {', '.join(r.get('compiled_files', [])) or 'none'} |",
            f"| binary files left out | {', '.join(r.get('binary_files_left_out', [])) or 'none'} |",
            "", f"## FAIL_TO_PASS ({len(f2p)})", "",
            *(f"- `{n}`" for n in f2p), *([] if f2p else ["(none)"]),
            "", f"## PASS_TO_PASS ({len(p2p)})", "",
            "<details><summary>show</summary>", "",
            *(f"- `{n}`" for n in p2p), *([] if p2p else ["(none)"]),
            "", "</details>",
            "", "## Problem statement (what the agent may be shown)", "",
            _fence(r.get("problem_statement", ""), "text"),
            "", "## Hints (issue comments before the PR; not shown to the agent)", "",
            _fence(r.get("hints_text") or "(none)", "text"),
            "", "## `patch` -- the change under test", "", _fence(r.get("patch", ""), "diff"),
            "", "## `test_patch` -- the developer's tests (held out)", "",
            _fence(r.get("test_patch", ""), "diff"), ""]
        if r.get("validation"):
            lines += ["## Validation", "", _fence(json.dumps(r["validation"], indent=1), "json")]
        (REVIEW / f"{iid}.md").write_text("\n".join(lines) + "\n")
    (REVIEW / "README.md").write_text("\n".join(index) + "\n")
    return REVIEW


# ------------------------------------------------------------------ the adapter
class ChaCo:
    name = NAME
    description = ("ChaCo benchmark (Zhou et al., ICSE 2026; UCLA-SEAL/Change-Cover "
                   "config/benchmark/rq_full.json): 145 merged PRs of SciPy, Qiskit and "
                   "pandas; images built here")

    def load(self, iid: str) -> dict:
        rows = _read_rows()
        if iid not in rows:
            raise SystemExit(f"{iid} is not prepared in {INSTANCES}; "
                             f"`python -m openhands_f2p.sources prepare chaco {iid}`")
        return rows[iid]

    def prs(self) -> list[dict] | None:
        return json.loads(PRS_FILE.read_text()) if PRS_FILE.exists() else []

    def image_for(self, iid: str) -> str:
        return image_for(iid)

    def owns_image(self, image: str) -> bool:
        return image.startswith(IMAGE_REPO + "/")

    def recipe(self, image: str) -> tuple[str, Path]:
        """(instance id, Dockerfile) for one of this dataset's images."""
        name = image.split("/", 1)[1].rsplit(":", 1)[0]
        for iid in _read_rows():
            if iid.lower() == name:
                df = DOCKERFILES / f"{iid}.Dockerfile"
                if not df.exists():
                    raise SystemExit(f"{iid}: no Dockerfile at {df}; prepare it first")
                return iid, df
        raise SystemExit(f"no prepared ChaCo instance has the image {image}")

    def summary(self) -> dict:
        rows = list(_read_rows().values())
        status: dict[str, int] = {}
        for r in rows:
            status[r.get("status", "?")] = status.get(r.get("status", "?"), 0) + 1
        try:
            total = len(benchmark())
        except Exception:                       # offline and never fetched
            total = 145
        return {"name": self.name, "description": self.description,
                "instances": total, "prepared": len(rows), "status": status,
                "file": str(INSTANCES.relative_to(PROJECT_ROOT)), "images": "built"}


SOURCE = ChaCo()

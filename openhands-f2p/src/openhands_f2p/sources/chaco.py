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

import json
import os
import re
import subprocess
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
BENCHMARK = HOME / "benchmark" / "rq_full.json"

# The paper's artifact, pinned: the list must not move under a run that cites it.
CHACO_REPO = "UCLA-SEAL/Change-Cover"
CHACO_COMMIT = "d3be9a251d917a657a7675141728977c17aec117"
BENCHMARK_URL = (f"https://raw.githubusercontent.com/{CHACO_REPO}/{CHACO_COMMIT}"
                 f"/config/benchmark/rq_full.json")

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
def benchmark() -> list[tuple[str, int]]:
    """(repo, PR number), in the paper's order. Fetched once, then read from disk."""
    if not BENCHMARK.exists():
        BENCHMARK.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(BENCHMARK_URL, timeout=60) as r:
            BENCHMARK.write_bytes(r.read())
    projects = json.loads(BENCHMARK.read_text())["projects"]
    return [(repo, int(n)) for repo, v in projects.items() for n in v["pr_numbers"]]


# ------------------------------------------------------------------ GitHub, cached
def _gh(path: str) -> dict | list:
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
        "apt": "git build-essential gfortran pkg-config curl libopenblas-dev liblapack-dev",
        "submodules": True,
        "deps": ("uv pip install --system --exclude-newer {date} "
                 "-r requirements/build.txt -r requirements/test.txt "
                 "-r requirements/default.txt"),
        "install": "python -m pip install --no-build-isolation -e . ",
        "check": "python -c 'import scipy; print(scipy.__version__)'",
    },
    "Qiskit/qiskit": {
        "python": "3.11",
        "apt": "git build-essential pkg-config curl",
        "rust": True,
        "deps": ("uv pip install --system --exclude-newer {date} "
                 "$( [ -f constraints.txt ] && echo -c constraints.txt ) "
                 "-r requirements.txt -r requirements-dev.txt setuptools-rust pytest"),
        # pytest: Qiskit runs its suite with stestr, and the harness runs tests with pytest
        # (it reads pytest's output), which collects Qiskit's unittest classes as they
        # are. Not in requirements-dev.txt; ChaCo's Qiskit Dockerfile adds it too.
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
    ]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ rows
def _read_rows() -> dict[str, dict]:
    if not INSTANCES.exists():
        return {}
    return {r["instance_id"]: r for r in json.loads(INSTANCES.read_text())}


def _write_rows(rows: dict[str, dict]) -> None:
    INSTANCES.parent.mkdir(parents=True, exist_ok=True)
    order = {instance_id(r, n): i for i, (r, n) in enumerate(benchmark())}
    ordered = sorted(rows.values(), key=lambda r: order.get(r["instance_id"], 1 << 30))
    INSTANCES.write_text(json.dumps(ordered, indent=1) + "\n")
    runnable = [{"id": r["instance_id"], "tier": 0, "runner": "pytest",
                 "version": r.get("version", ""), "build": "built", "localise": "unknown",
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
               binary_files_left_out=binary)
    compiled = [p for p in _paths(patch) if p.endswith(COMPILED)]
    row["compiled_files"] = compiled
    if repo not in RECIPES:
        row.update(status="unsupported", why=f"no image recipe for {repo}")
    elif not patch.strip():
        row.update(status="unsupported", why="the change touches only test files")
    elif not any(p.endswith(".py") for p in _paths(patch)):
        row.update(status="unsupported", why="the change touches no Python source")
    elif not test_patch.strip():
        row.update(status="prepared", why="no developer test: FAIL_TO_PASS cannot be "
                                          "derived, so there is nothing to judge against")
    elif any(p.endswith(".rs") for p in compiled):
        row.update(status="unsupported",
                   why=f"the change touches Rust ({compiled[:3]}), which the editable "
                       f"install does not rebuild on import")
    else:
        row.update(status="prepared", why="awaiting build and validate")
    if row["status"] != "unsupported":
        DOCKERFILES.mkdir(parents=True, exist_ok=True)
        (DOCKERFILES / f"{iid}.Dockerfile").write_text(dockerfile(row))
    return row


def _paths(diff: str) -> list[str]:
    return [ln.split(" b/", 1)[-1].strip() for ln in diff.splitlines()
            if ln.startswith("diff --git ")]


def prepare(ids: list[str] | None = None) -> list[dict]:
    """Rows for `ids` (all 145 when None). Rows already validated are kept as they are."""
    rows = _read_rows()
    todo = benchmark() if not ids else [parse_id(i) for i in ids]
    out = []
    for repo, number in todo:
        iid = instance_id(repo, number)
        if rows.get(iid, {}).get("status") in ("runnable", "not-fail-to-pass"):
            out.append(rows[iid])
            continue
        row = prepare_one(repo, number)
        rows[iid] = row
        _write_rows(rows)
        out.append(row)
        print(f"  {row['status']:<12} {iid:32s} {row.get('why', '')[:70]}")
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
    if row["status"] == "unsupported" or not row["test_patch"].strip():
        print(f"  {iid}: {row['status']} -- {row.get('why')}")
        return row
    sources.select(NAME)
    files = E.patched_test_files(row["test_patch"])
    with E.Sandbox(iid, quiet=quiet) as box:
        box.strip_git()
        box.apply_patch(row["test_patch"])
        files = [f for f in files if box.exists(f)]
        cmd = E.test_command(box, files)
        before = box.exec(cmd, timeout=3600)
        box.apply_patch(row["patch"])
        after = box.exec(cmd, timeout=3600)
        b, a = E.parse_output(before.output), E.parse_output(after.output)
        f2p = sorted(n for n, s in b.items() if s in V.BEHAVIOURAL and a.get(n) == "PASSED")
        p2p = sorted(n for n, s in b.items() if s == "PASSED" and a.get(n) == "PASSED")
        box.apply_patch(row["patch"], revert=True)
        box.apply_patch(row["test_patch"], revert=True)
        row.update(FAIL_TO_PASS=json.dumps(f2p), PASS_TO_PASS=json.dumps(p2p),
                   validated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   validation={"test_files": files, "collected_before": len(b),
                               "collected_after": len(a),
                               "runner": E.runner_for(box)["cmd"]})
        if not b and not a:
            row.update(status="broken-env",
                       why="the developer's test files collected nothing on either side: "
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
    rows[iid] = row
    _write_rows(rows)
    print(f"  {row['status']:<16} {iid:32s} {row['why'][:90]}")
    return row


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

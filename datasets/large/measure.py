"""Executable changed lines of a pull request, as the coverage measurement counts them.

    cd openhands-f2p
    uv run python ../datasets/large/measure.py <rows.json> <ids.txt|all> <out.json>

For each library Python file the patch touches (`coverage_metric.patched_source_files`):
the file at the base commit (from a blobless mirror of the repo), the same file with the
patch applied, the lines the patch added there (`added_lines_between`), and of those the
ones that start an executable statement (`statements.executable_lines`). Their sum is the
"executable changed lines" figure every run reports, worked out before any run.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from openhands_f2p.coverage_metric import added_lines_between, patched_source_files
from openhands_f2p.sources.chaco import mirror
from openhands_f2p.statements import executable_lines


def _show(git_dir: Path, sha: str, path: str) -> str | None:
    r = subprocess.run(["git", "--git-dir", str(git_dir), "show", f"{sha}:{path}"],
                       capture_output=True, timeout=600)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def measure(row: dict) -> dict:
    files = patched_source_files(row["patch"])
    if not files:
        return {"id": row["instance_id"], "executable": 0, "files": {}}
    git_dir = mirror(row["repo"])
    out: dict[str, int] = {}
    with tempfile.TemporaryDirectory() as tmp:
        base = {}
        for p in files:
            text = _show(git_dir, row["base_commit"], p)
            if text is not None:
                base[p] = text
                (Path(tmp) / p).parent.mkdir(parents=True, exist_ok=True)
                (Path(tmp) / p).write_text(text)
        r = subprocess.run(["git", "apply", *[f"--include={p}" for p in files], "-"],
                           input=row["patch"].encode(), cwd=tmp, capture_output=True,
                           timeout=120)
        if r.returncode:
            return {"id": row["instance_id"], "error": r.stderr.decode()[-300:]}
        for p in files:
            f = Path(tmp) / p
            if not f.exists():
                continue                      # the patch deletes it
            head = f.read_text()
            added = (added_lines_between(base[p], head) if p in base
                     else set(range(1, head.count("\n") + 2)))
            try:
                out[p] = len(added & executable_lines(head))
            except SyntaxError:
                out[p] = 0                    # Python 2 era source the parser refuses
    return {"id": row["instance_id"], "executable": sum(out.values()), "files": out}


if __name__ == "__main__":
    rows = {r["instance_id"]: r for r in json.loads(Path(sys.argv[1]).read_text())}
    want = (list(rows) if sys.argv[2] == "all"
            else Path(sys.argv[2]).read_text().split())
    # One mirror clone per repo first, so the threads below never race to clone it.
    for repo in sorted({rows[i]["repo"] for i in want}):
        mirror(repo)
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda i: measure(rows[i]), want))
    Path(sys.argv[3]).write_text(json.dumps(res, indent=0) + "\n")
    ok = [r for r in res if "error" not in r]
    print(f"{len(res)} measured, {len(res) - len(ok)} errors, "
          f"{sum(r['executable'] >= 50 for r in ok)} with 50+ executable changed lines")

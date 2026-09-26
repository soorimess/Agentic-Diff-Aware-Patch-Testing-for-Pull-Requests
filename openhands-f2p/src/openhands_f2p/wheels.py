"""Packages the harness puts into a container, fetched on the host.

The container never has a network. `coverage` used to be pip-installed over a bridge that
was disconnected right after. On 2026-09-26 Docker Desktop's proxy stopped answering: every
install timed out (3 x 109 s), and the run carried on with a `coverage` tool that could not
measure anything and no coverage figure -- a `full` arm silently missing a tool. Now the
host downloads the wheel, `docker cp` puts it in, and pip installs it with `--no-index`.
Anything that fails on the way is an error, never a run without the package.

The wheel chosen is the one pip would choose online: the newest non-yanked final release
whose `requires_python` admits the container's Python and that ships a wheel for it,
preferring the most specific tag (a `cp39` build over `py3-none-any`). The choice is kept
in the cache, so every run of a series installs the same file, and the file is checked
against PyPI's sha256 every time it is used.
"""
from __future__ import annotations

import hashlib
import json
import os
import urllib.request
from pathlib import Path

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.tags import compatible_tags, cpython_tags
from packaging.utils import InvalidWheelFilename, parse_wheel_filename
from packaging.version import InvalidVersion, Version

from openhands_f2p.layout import CACHE

WHEELS = CACHE / "wheels"
INDEX = "https://pypi.org/pypi/{}/json"
# Every SWE-bench image is x86_64 with a glibc far newer than 2.17, so these are all
# accepted there; they are also the only manylinux tags the packages we install publish.
PLATFORMS = ["manylinux_2_17_x86_64", "manylinux2014_x86_64", "manylinux_2_12_x86_64",
             "manylinux2010_x86_64", "manylinux_2_5_x86_64", "manylinux1_x86_64"]


def _tags(major: int, minor: int) -> list:
    """Tags a CPython major.minor on these platforms accepts, most preferred first."""
    py = (major, minor)
    tags = list(cpython_tags(py, platforms=PLATFORMS))
    tags += [t for t in compatible_tags(py, f"cp{major}{minor}", platforms=PLATFORMS)
             if t not in tags]
    return tags


def pick(package: str, python: str) -> dict:
    """The wheel pip would install for `package` on CPython `python` (e.g. "3.9.18")."""
    major, minor = (int(x) for x in python.split(".")[:2])
    rank = {t: i for i, t in enumerate(_tags(major, minor))}
    here = Version(python.split("+")[0])
    with urllib.request.urlopen(INDEX.format(package), timeout=60) as r:
        releases = json.load(r)["releases"]
    best = None
    for text, files in releases.items():
        try:
            version = Version(text)
        except InvalidVersion:
            continue
        if version.is_prerelease or version.is_devrelease:
            continue
        for f in files:
            if f.get("yanked") or f.get("packagetype") != "bdist_wheel":
                continue
            if f.get("requires_python"):
                try:
                    if here not in SpecifierSet(f["requires_python"]):
                        continue
                except InvalidSpecifier:
                    continue
            try:
                tags = parse_wheel_filename(f["filename"])[3]
            except InvalidWheelFilename:
                continue
            fit = min((rank[t] for t in tags if t in rank), default=None)
            if fit is None:
                continue
            key = (version, -fit)
            if best is None or key > best[0]:
                best = (key, f)
    if best is None:
        raise RuntimeError(f"PyPI has no {package} wheel for CPython {python} on x86_64")
    f = best[1]
    return {"package": package, "python": f"{major}.{minor}", "filename": f["filename"],
            "url": f["url"], "sha256": f["digests"]["sha256"]}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_atomic(path: Path, data: bytes) -> None:
    # Parallel workers share the cache; a half-written file must never be visible.
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def wheel_for(package: str, python: str) -> Path:
    """A verified local wheel of `package` for CPython `python`, downloading it once."""
    major, minor = python.split(".")[:2]
    WHEELS.mkdir(parents=True, exist_ok=True)
    choice_file = WHEELS / f"{package}-cp{major}{minor}.json"
    if choice_file.exists():
        choice = json.loads(choice_file.read_text())
    else:
        choice = pick(package, python)
        _write_atomic(choice_file, json.dumps(choice, indent=1).encode())
    path = WHEELS / choice["filename"]
    if path.exists() and _sha256(path.read_bytes()) == choice["sha256"]:
        return path
    with urllib.request.urlopen(choice["url"], timeout=300) as r:
        data = r.read()
    if _sha256(data) != choice["sha256"]:
        raise RuntimeError(f"{choice['filename']} does not match PyPI's sha256")
    _write_atomic(path, data)
    return path

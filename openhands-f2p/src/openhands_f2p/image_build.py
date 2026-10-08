"""Images no registry has: built here, from the Dockerfile a dataset's adapter wrote.

SWE-bench publishes an image per instance and `images.pull_image` fetches it. A dataset
like ChaCo publishes none, so its adapter writes a Dockerfile per instance at prepare time
(`sources/chaco.py`) and this module turns it into the image -- the same name every
other part of the harness already asks for, so `Sandbox` starts it like a pulled one.

`pull_image` comes here for any image whose dataset says `image_source: build`. The rules
are the pull path's: one build per slot (`F2P_BUILD_CONCURRENCY`, default 2 -- a build
uses every core, unlike a download), room made first, and the result archived at once
(`image_cache.save`), whatever `F2P_NO_ARCHIVE` says, because a rebuild costs tens of
minutes where a re-pull costs thirty seconds. The build log is kept beside the
Dockerfile's build context, under `.cache/builds/`.

    uv run python -m openhands_f2p.sources build chaco <instance id>
"""
from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path

from openhands_f2p.layout import CACHE

BUILD_SLOTS = max(1, int(os.getenv("F2P_BUILD_CONCURRENCY") or 2))
# A from-source build of SciPy or Qiskit is 15-30 minutes on the server; two hours is a
# stalled build, not a slow one.
BUILD_TIMEOUT = int(os.getenv("F2P_BUILD_TIMEOUT") or 7200)
# A build writes its layers and keeps the base image and the build cache besides.
BUILD_HEADROOM_GB = 25.0
BUILDS = CACHE / "builds"


def is_built(image: str) -> bool:
    """Whether `image` comes from a recipe here rather than from a registry."""
    from openhands_f2p import sources
    src = sources.source_of_image(image)
    return src is not None and hasattr(src, "recipe")


def log_for(image: str) -> Path:
    return BUILDS / re.sub(r"[^A-Za-z0-9._-]", "_", image) / "build.log"


def build(image: str, quiet: bool = False, need_gb: float = BUILD_HEADROOM_GB,
          force: bool = False) -> None:
    """Make `image` exist: from its archive if one was kept, else by building it."""
    from openhands_f2p import image_cache, sources
    from openhands_f2p.images import PLATFORM, _pull_slot, have_image, make_room

    if have_image(image) and not force:
        return
    if not force and image_cache.have_archive(image) and image_cache.load(image, quiet=quiet):
        return
    src = sources.source_of_image(image)
    iid, dockerfile = src.recipe(image)
    with _pull_slot("build", BUILD_SLOTS):
        if have_image(image) and not force:
            return                  # a sibling worker built it while we waited
        free = make_room(image, max(need_gb, BUILD_HEADROOM_GB))
        if free is not None and free < BUILD_HEADROOM_GB:
            raise SystemExit(f"only {free:.0f} GB free; building {image} needs about "
                             f"{BUILD_HEADROOM_GB:.0f}")
        log = log_for(image)
        log.parent.mkdir(parents=True, exist_ok=True)
        # The context is the empty directory holding the log: every Dockerfile here
        # fetches what it needs itself, so nothing on the host is sent to the daemon.
        cmd = ["docker", "build", "--platform", PLATFORM, "--progress=plain",
               "-t", image, "-f", str(dockerfile), str(log.parent)]
        if not quiet:
            print(f"  building {image} for {iid} (log: {log})", flush=True)
        t0 = time.time()
        with log.open("w") as fh:
            fh.write("$ " + " ".join(cmd) + "\n")
            fh.flush()
            try:
                rc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT,
                                    timeout=BUILD_TIMEOUT).returncode
            except subprocess.TimeoutExpired:
                rc = 124
                fh.write(f"\ntimed out after {BUILD_TIMEOUT}s\n")
        minutes = (time.time() - t0) / 60
        if rc or not have_image(image):
            tail = log.read_text(errors="replace").strip().splitlines()[-25:]
            raise SystemExit(f"could not build {image} (exit {rc}, {minutes:.0f} min). "
                             f"Log: {log}\n" + "\n".join(tail))
        if not quiet:
            print(f"  built {image} in {minutes:.0f} min", flush=True)
        image_cache.save(image, quiet=quiet)

"""Instance images kept on the host disk, so each one is pulled from the registry once.

These images are 3-4 GB each and the registry link here has been measured at 0.3 MB/s,
which is about three hours for one of them. Two runs died that way: one lost the Docker
socket 76 minutes into a pull when Docker Desktop restarted, the other was still
downloading when the run was stopped. Neither says anything about the instance, and both
would have been free if the image had ever been kept.

So it is kept. `docker save | gzip` to a file on the host, and next time `docker load`
from that file instead of pulling. The gain is not marginal -- a load off an SSD is
minutes where a pull is hours -- and it is the difference between adding an instance
being routine and being an afternoon.

The archive is the durable copy and Docker's image store is the working copy. Keeping
both forever would spend the space twice: sixteen images are ~36 GB in Docker and ~15 GB
compressed here. So after a run finishes with an image, the Docker copy is dropped and
the archive stays.

Two rules make that safe rather than merely tidy:

* **Nothing is deleted before its archive is verified.** Re-pulling costs hours, so a
  truncated archive is far worse than a wasted gigabyte. `verify` checks the gzip stream
  end to end and that the tar holds Docker's `manifest.json`.
* **An image in use is never touched.** `images.claimed_images()` reports what live runs
  have claimed, and eviction skips those -- the same guard that keeps one worker from
  deleting another's container.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from openhands_f2p.layout import PROJECT_ROOT

# In the project, git-ignored, because that is where the disk is. `F2P_IMAGE_CACHE`
# points it elsewhere -- an external drive is the obvious use.
#
# Several directories, separated like PATH (`image-cache:image-cache-evaluation`), are
# searched in order for an archive, and new archives go to the first. Since 2026-09-27
# every run is on the laptop over the 36 instances cached locally, 26 in `image-cache/`
# and 10 in `image-cache-evaluation/`, and one run has to see both. A relative entry is
# relative to the project root, wherever the command was started from.
CACHE_DIRS = [PROJECT_ROOT / p for p in (os.getenv("F2P_IMAGE_CACHE") or "").split(os.pathsep)
              if p] or [PROJECT_ROOT / "image-cache"]
CACHE_DIR = CACHE_DIRS[0]

# A stored archive smaller than this is a truncated save, not a small image: the
# smallest of these images compresses to about 300 MB.
MIN_PLAUSIBLE_BYTES = 50_000_000

# Whether to keep archives at all. The cache exists because a pull on the laptop link was
# measured at 0.3 MB/s -- three hours for one image -- so paying gzip once beat paying the
# download repeatedly. On the server that trade reverses: a pull there is 30 seconds and a
# load is 27, so the archives buy no time and spend 88 GB of a 146 GB disk, which is the
# only thing stopping a wide run from holding its images.
#
# `F2P_NO_ARCHIVE=1` turns them off. Nothing is written, nothing is read, and an image is
# dropped when its run is done on the strength of being cheap to fetch again rather than
# on the strength of a verified archive.
ARCHIVING = (os.getenv("F2P_NO_ARCHIVE") or "").strip().lower() not in ("1", "true", "yes", "on")


def archive_for(image: str) -> Path:
    """One file per image, named after it. `/` and `:` are not filename characters.

    The first cache directory holding a plausible archive of it; the first directory
    when none does, which is where a new one is written."""
    name = re.sub(r"[^A-Za-z0-9._-]", "_", image) + ".tar.gz"
    for d in CACHE_DIRS:
        p = d / name
        if p.exists() and p.stat().st_size >= MIN_PLAUSIBLE_BYTES:
            return p
    return CACHE_DIR / name


def have_archive(image: str) -> bool:
    if not ARCHIVING:
        return False
    p = archive_for(image)
    return p.exists() and p.stat().st_size >= MIN_PLAUSIBLE_BYTES


def _sh(cmd: str, timeout: int = 5400) -> subprocess.CompletedProcess:
    """A pipeline, so it has to go through a shell. No untrusted text reaches it: the
    only interpolated values are an image name from `prs.py` and a path we built."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          timeout=timeout)


def verify(path: Path) -> str | None:
    """None if the archive is sound, else why it is not.

    Checked before the image it came from is deleted, because that deletion is the one
    irreversible step here -- getting the image back means the three-hour pull again.
    """
    if not path.exists():
        return "no such file"
    size = path.stat().st_size
    if size < MIN_PLAUSIBLE_BYTES:
        return f"only {size / 1e6:.0f} MB -- a truncated save"
    r = _sh(f"gzip -t {path!s:s}".replace(str(path), f"'{path}'"), timeout=1800)
    if r.returncode != 0:
        return f"gzip reports a corrupt stream: {(r.stderr or '').strip()[:120]}"
    # A Docker save always contains a manifest. Listing the whole tar means decompressing
    # it again, but this runs once per image ever, against deleting something that costs
    # hours to replace.
    r = _sh(f"tar -tzf '{path}' | head -40", timeout=1800)
    if "manifest.json" not in (r.stdout or ""):
        return "no manifest.json inside -- not a docker save"
    return None


def save(image: str, quiet: bool = False) -> Path | None:
    """Write `image` to its archive. Returns the path, or None if it could not be made.

    Writes to a `.part` file and renames on success, so an interrupted save cannot leave
    something that `have_archive` would later accept and `docker load` would choke on.
    """
    if not ARCHIVING:
        return None
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    final = archive_for(image)
    if have_archive(image):
        return final
    part = final.with_suffix(".part")
    part.unlink(missing_ok=True)
    if not quiet:
        print(f"  archiving {image.split('.')[-1]} -> {final.name}", flush=True)
    r = _sh(f"docker save '{image}' | gzip -1 > '{part}'")
    if r.returncode != 0 or not part.exists():
        part.unlink(missing_ok=True)
        if not quiet:
            print(f"  could not archive {image}: {(r.stderr or '').strip()[:160]}")
        return None
    why = verify(part)
    if why:
        part.unlink(missing_ok=True)
        if not quiet:
            print(f"  archive of {image} rejected: {why}")
        return None
    part.replace(final)
    if not quiet:
        print(f"  archived {final.name} ({final.stat().st_size / 1e9:.1f} GB)",
              flush=True)
    return final


def load(image: str, quiet: bool = False) -> bool:
    """Restore `image` into Docker from its archive. True if it is now present."""
    path = archive_for(image)
    if not have_archive(image):
        return False
    if not quiet:
        print(f"  loading {image.split('.')[-1]} from {path.name} "
              f"({path.stat().st_size / 1e9:.1f} GB)", flush=True)
    # pigz when present: gunzip is one core, about a minute per image on the server.
    unzip = "pigz -dc" if shutil.which("pigz") else "gunzip -c"
    r = _sh(f"{unzip} '{path}' | docker load")
    if r.returncode != 0:
        if not quiet:
            print(f"  load failed, will pull instead: "
                  f"{(r.stderr or '').strip()[:160]}")
        return False
    from openhands_f2p import images as I
    return I.have_image(image)


def drop_image(image: str, quiet: bool = False) -> bool:
    """Remove Docker's copy, but only once the archive is known good.

    This is the step that saves the space, and the only one that can lose work, so the
    archive is verified here too rather than trusted from whenever it was written.
    """
    from openhands_f2p import images as I
    if not I.have_image(image):
        return True
    if image in I.claimed_images():
        return False                      # a live run is using it
    why = verify(archive_for(image))
    if why:
        if not quiet:
            print(f"  keeping {image}: its archive is not usable ({why})")
        return False
    r = _sh(f"docker rmi '{image}'", timeout=900)
    ok = r.returncode == 0 or not I.have_image(image)
    if not quiet:
        print(f"  dropped Docker's copy of {image.split('.')[-1]}" if ok else
              f"  could not drop {image}: {(r.stderr or '').strip()[:120]}")
    return ok


KEEP_IF_FREE_GB = float(os.getenv("F2P_KEEP_IMAGES_FREE_GB") or 100)


def release(image: str, quiet: bool = True) -> bool:
    """Give back the disk this image is holding, once its run is finished with it.

    Archiving on, this is the old pair: archive, verify, then drop Docker's copy -- the
    archive is the durable copy and nothing is deleted before it is known good.

    Archiving off, there is no archive to verify and none is wanted, so the image is
    simply removed. That is safe for exactly the reason the archives were dropped: the
    registry is thirty seconds away. It still refuses an image a live run has claimed,
    which is the guard that matters under `--parallel`.
    """
    from openhands_f2p import images as I
    # Kept while the disk has room: the next experiment needs the same 36 images, and
    # dropping each after its run made every job reload its archive (server, 2026-10-04).
    # `make_room` still evicts when a load or pull is short of space.
    free = I.vm_free_gb()
    if free is not None and free >= KEEP_IF_FREE_GB:
        return True
    if not ARCHIVING:
        if not I.have_image(image):
            return True
        if image in I.claimed_images():
            return False
        _sh(f"docker rmi '{image}'", timeout=900)
        ok = not I.have_image(image)
        if ok and not quiet:
            print(f"  dropped {image.split('.')[-1]} (not archiving)")
        return ok
    return bool(save(image, quiet=quiet)) and drop_image(image, quiet=quiet)


def stored() -> list[tuple[str, int]]:
    return sorted(((p.name, p.stat().st_size) for d in CACHE_DIRS if d.exists()
                   for p in d.glob("*.tar.gz")), key=lambda t: -t[1])


def _cli() -> int:
    import argparse

    from openhands_f2p import images as I
    from openhands_f2p.prs import PRS

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("list", "archive-all", "load", "archive"),
                   help="list: what is stored. archive-all: archive every image Docker "
                        "currently holds, then drop Docker's copy. archive/load: one "
                        "instance id")
    p.add_argument("which", nargs="?", default="",
                   help="an instance id, for archive/load")
    p.add_argument("--keep-images", action="store_true",
                   help="archive without dropping Docker's copy (uses the space twice)")
    a = p.parse_args()

    if a.action == "list":
        rows = stored()
        total = sum(n for _, n in rows)
        print(f"{', '.join(map(str, CACHE_DIRS))}  --  {len(rows)} archive(s), "
              f"{total / 1e9:.1f} GB\n")
        for name, n in rows:
            print(f"  {n / 1e9:5.1f} GB  {name}")
        if not rows:
            print("  (nothing stored yet)")
        return 0

    if a.action in ("archive", "load"):
        if not a.which:
            raise SystemExit(f"  {a.action} needs an instance id")
        image = I.image_for(a.which)
        if a.action == "load":
            return 0 if load(image) else 1
        if not I.have_image(image):
            raise SystemExit(f"  Docker does not have {image}")
        ok = save(image) is not None
        if ok and not a.keep_images:
            drop_image(image)
        return 0 if ok else 1

    # archive-all: every instance image Docker currently holds
    held = [I.image_for(pr["id"]) for pr in PRS]
    held = [im for im in held if I.have_image(im)]
    busy = I.claimed_images()
    todo = [im for im in held if im not in busy]
    skipped = [im for im in held if im in busy]
    print(f"  {len(held)} instance image(s) in Docker; "
          f"{len(todo)} to archive, {len(skipped)} in use by a live run")
    for im in skipped:
        print(f"    skipping {im.split('.')[-1]} -- claimed by a running instance")
    done = dropped = 0
    for im in todo:
        if save(im) is None:
            continue
        done += 1
        if not a.keep_images and drop_image(im):
            dropped += 1
    rows = stored()
    print(f"\n  archived {done}/{len(todo)}, dropped {dropped} Docker copies")
    print(f"  {CACHE_DIR}: {len(rows)} archive(s), "
          f"{sum(n for _, n in rows) / 1e9:.1f} GB")
    free = shutil.disk_usage(CACHE_DIR).free / 1e9 if CACHE_DIR.exists() else 0
    print(f"  host disk free: {free:.0f} GB")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())

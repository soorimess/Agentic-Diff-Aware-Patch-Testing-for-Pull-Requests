"""Instance images -- pulled from a registry or built (image_build.py) -- and the disk they compete for.

Twenty-six instances is roughly eighty gigabytes of images and the Docker VM holds
fifty-eight, so a run over the whole set cannot keep them all. Everything here exists to
make that survivable: pulls are serialised behind a lock, the biggest idle image is
evicted to make room, and containers left by a killed run are reaped -- carefully, since
under `--parallel` the workers are separate processes sharing one daemon.

Nothing in this module knows about `Sandbox`. It is the layer below it.
"""
from __future__ import annotations

import contextlib
import fcntl
import os
import time
import shutil
import re
import subprocess
from pathlib import Path


PLATFORM = "linux/amd64"          # SWE-bench publishes amd64 only; emulated on arm64
IMAGE = "swebench/sweb.eval.x86_64.{tag}:latest"

# Image repositories this harness may evict to make room: the ones it can get back --
# SWE-bench's by pulling, ours (`f2p-<dataset>/`, image_build.py) by building or from
# the archive written before eviction.
EVICTABLE = ("swebench/*", "f2p-*/*")


def image_for(instance_id: str) -> str:
    """The image of an instance in the active dataset (`openhands_f2p.sources`).

    For SWE-bench that is still `IMAGE` with `_1776_` where the id has `__`."""
    from openhands_f2p import sources
    return sources.image_for(instance_id)


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


def daemon_refusal() -> str | None:
    """Why Docker cannot be used, or None if it can.

    Checked once at startup for the same reason the gateway is. Without it the run gets
    all the way to fanning out children, and each one discovers separately that there is
    no daemon -- nine instances wrote nine BROKEN results and nine child.log files, at
    zero actions each, before anything said the words "docker daemon". A machine that has
    just rebooted is the ordinary way to arrive here.
    """
    r = _run(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=60)
    if r.returncode == 0:
        return None
    detail = (r.stderr or r.stdout or "").strip().splitlines()
    return ("docker is not answering, so no instance can run.\n"
            f"  {detail[0] if detail else 'no detail'}\n"
            "  Start Docker Desktop (`open -a Docker`) and run this again.")


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
    vm = None
    for line in r.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 4:
            try:
                vm = int(parts[3]) / (1024 * 1024)
            except ValueError:
                return None
            break
    if vm is None:
        return None
    # The other half: on Docker Desktop the VM's disk is a sparse file on the host, so
    # the VM can report room the host does not have. On the laptop (2026-09-28) the VM
    # said 79 GB free while the host had 52 -- twenty loaded images would have filled the
    # host first. The smaller of the two is what can actually be written.
    host = _host_free_gb()
    return vm if host is None else min(vm, host)


def _host_free_gb() -> float | None:
    """Free space on the host volume holding Docker Desktop's disk image; None when
    Docker is not Docker Desktop (a Linux host's daemon writes to its own disk, which the
    VM figure already is)."""
    data = Path.home() / "Library" / "Containers" / "com.docker.docker"
    if not data.exists():
        return None
    return shutil.disk_usage(data).free / 1e9


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
                   *(f"--filter=reference={r}" for r in EVICTABLE)], timeout=180)
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
    # Archived on the way out, if it is not already. Eviction used to mean a
    # three-hour re-download the next time this instance came up; with the archive it
    # means a load off the host disk. The archive is written before the delete, and
    # `image_cache.save` verifies it before this returns, so the expensive copy is never
    # thrown away on the strength of a file nobody read back.
    from openhands_f2p import image_cache
    try:
        image_cache.save(best, quiet=False)
    except Exception as exc:
        print(f"  could not archive {best} before evicting: "
              f"{type(exc).__name__}: {exc}")
    _run(["docker", "image", "rm", "-f", best], timeout=600)
    print(f"  evicted {best.split('.')[-1]} ({best_size:.1f} GB) to make room"
          f"{' (archived)' if image_cache.have_archive(best) else ''}")
    return True


# Headroom for one image. Deliberately about double the largest compressed size: docker
# writes the download and then extracts it, so a 4.6 GB image transiently needs well
# over nine. At the old 6 GB threshold the guard let two pulls start with 6.2 GB free;
# they filled the disk, stalled, and burned three twenty-minute attempts each without
# ever reporting a disk problem.
DEFAULT_IMAGE_HEADROOM_GB = 14.0

# Room each running container of ours is still going to write after its image is in:
# the coverage wheel, test runs, coverage data, mutated copies of the fixed files. The
# headroom above is checked once, when an image loads, so it only ever covered the load.
# The 36-instance base run on the laptop (2026-09-29) loaded its last images with the
# host above 14 GB free, then fourteen running containers wrote the rest of it away:
# the host reached 0, Docker Desktop stopped ("no space left on device"), and every job
# hung on its next `docker exec`.
CONTAINER_RESERVE_GB = 1.5


def running_containers() -> int:
    """How many of this harness's containers are running now (named `f2p-*`)."""
    r = _run(["docker", "ps", "--filter", "name=^f2p-", "--format", "{{.Names}}"],
             timeout=180)
    return sum(1 for x in r.stdout.split() if x)


PULL_LOCK = Path("/tmp/f2p-pull.lock")

# How many pulls may run at once. One by default, which is the behaviour every earlier
# measurement was taken with and the right one on a slow link: two workers sharing 0.8
# MB/s each miss their timeout where run in sequence the first would have finished.
#
# That reasoning is about the link, not about pulling, so it is a setting rather than a
# law. On the server the prefetch sustained 320 MB/s across eight concurrent streams --
# 40 MB/s each, no starvation -- and there a single lock turns thirty workers into a
# queue thirty deep for no reason. `F2P_PULL_CONCURRENCY=6` opens six slots.
PULL_SLOTS = max(1, int(os.getenv("F2P_PULL_CONCURRENCY") or 1))


# Loads at once. One until 2026-10-04: on the server, with every image dropped after its
# run, thirty jobs started one image-minute apart -- half an hour of ramp before the last
# container came up. `F2P_LOAD_CONCURRENCY=6` (run_exp) opens six.
LOAD_SLOTS = max(1, int(os.getenv("F2P_LOAD_CONCURRENCY") or 1))


@contextlib.contextmanager
def _pull_slot(kind: str = "pull", slots: int | None = None):
    """Hold one of `PULL_SLOTS` slots (or `slots` of `kind`), waiting if all are taken.

    A file per slot, tried without blocking in turn; if none is free we block on the
    first, which is as fair as this needs to be. Each is released when the process
    exits however it exits, so a killed worker cannot leave a slot held.
    """
    handles = []
    try:
        for i in range(slots or PULL_SLOTS):
            fh = Path(f"/tmp/f2p-{kind}-{i}.lock").open("w")
            handles.append(fh)
            try:
                fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                continue
            yield
            return
        fcntl.flock(handles[0], fcntl.LOCK_EX)      # all busy: wait for the first
        yield
    finally:
        for fh in handles:
            with contextlib.suppress(OSError):
                fcntl.flock(fh, fcntl.LOCK_UN)
                fh.close()


def make_room(keep: str, need_gb: float, quiet: bool = True) -> float | None:
    """Reclaim disk until `need_gb` is free, or return what is free if it cannot be.

    Split out of `_pull_locked` because loading an archive needs exactly the same
    headroom as pulling does and had none. `pull_image` tries the archive *before* the
    pull lock, deliberately -- a local load has no business queueing behind somebody
    else's download -- and that branch never asked whether the image would fit.

    It did not matter while runs were small. It matters at `--parallel 20` on a disk
    holding 93 GB of archives: twenty workers each loading a 5 GB image want 98 GB and
    have 53, and the failure is `no space left on device` somewhere in the middle of a
    four-hour run rather than a worker waiting its turn.

    Eviction is nearly free here, which is what makes this cheap to call: every image
    the run has finished with is already archived, so `evict_one_image` finds `save`
    already done and only has to `docker rmi`.
    """
    free = vm_free_gb()
    if free is None or free >= need_gb:
        return free
    reap_orphans()
    _run(["docker", "builder", "prune", "-af"], timeout=900)
    free = vm_free_gb()
    while free is not None and free < need_gb and evict_one_image(keep):
        free = vm_free_gb()
    return free




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
    # An image we build is only current while its Dockerfile is unchanged
    # (image_build.built_from vs recipe_hash); a stale one, or a stale archive, goes to
    # image_build.build, which rebuilds it. A pulled image is current by definition.
    from openhands_f2p import image_build
    if image_build.is_built(image):
        if have_image(image) and image_build.current(image):
            return
        image_build.build(image, quiet=quiet, need_gb=need_gb)
        return
    if have_image(image):
        return
    # The archive is tried *before* the lock, because a load is a local operation and
    # has no business queueing behind somebody else's download. It used to sit inside
    # the lock, and one instance with no archive pulling at 0.3 MB/s held seven that had
    # archives -- twenty-five seconds of work each -- waiting on it for hours.
    from openhands_f2p import image_cache
    if image_cache.have_archive(image):
        # Under its own lock, not the pull lock: the check and the load have to be one
        # step or two workers both see room for the last image, and a load is seconds
        # where a pull is hours, so queueing behind another *load* costs nothing.
        with _pull_slot("load", LOAD_SLOTS):
            # Short of room while jobs are running: wait for one to finish, and its
            # image becomes evictable. Falling through instead went to the pull path,
            # which on the laptop has no registry to pull from and fails the job.
            # The lock is held while waiting, so the loads queued behind this one
            # wait too rather than each taking the room this one is waiting for.
            while True:
                running = running_containers()
                need = need_gb + CONTAINER_RESERVE_GB * running
                free = make_room(image, need, quiet)
                if free is None or free >= need or running == 0:
                    break
                if not quiet:
                    print(f"  {free:.0f} GB free, {need:.0f} needed with {running} "
                          f"job(s) running; waiting for one to finish")
                time.sleep(30)
            need_gb = need
            if free is None or free >= need_gb:
                if image_cache.load(image, quiet=quiet):
                    return
            elif not quiet:
                print(f"  {free:.0f} GB free and this image needs about "
                      f"{need_gb:.0f}; falling through to the pull path")
    # No registry has it: an image of ours is built from its dataset's recipe instead
    # (image_build.py), and archived like a pulled one so it is built once.
    from openhands_f2p import image_build
    if image_build.is_built(image):
        image_build.build(image, quiet=quiet, need_gb=need_gb)
        return
    with _pull_slot():
        _pull_locked(image, quiet, need_gb)


def _pull_locked(image: str, quiet: bool, need_gb: float) -> None:
    if have_image(image):
        return                  # the worker ahead of us in the queue wanted it too
    # Re-checked here as well: the worker ahead in the queue may have pulled this very
    # image and archived it while we waited, in which case there is nothing left to do.
    from openhands_f2p import image_cache
    if image_cache.have_archive(image) and image_cache.load(image, quiet=quiet):
        return
    free = make_room(image, need_gb)
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
            # Archived here, while the lock is still held and the image is certainly
            # present. This is the only moment the expensive thing has just been paid
            # for, so it is the only moment worth spending two minutes of gzip on.
            from openhands_f2p import image_cache
            try:
                image_cache.save(image, quiet=quiet)
            except Exception as exc:      # a failed archive must not fail the run
                if not quiet:
                    print(f"  could not archive {image}: {type(exc).__name__}: {exc}")
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

"""The SWE-bench environment, as one import.

This module was 1091 lines holding four subjects that barely touched each other. They now
live in `images`, `runners`, `sandbox` and `coverage_metric`; what stays here is the
facade that keeps every existing `from openhands_f2p import swebench_env as E` working,
plus the two checks that genuinely need all four at once.

Read the split modules to change behaviour. Read this one to see what the environment
offers.
"""
from __future__ import annotations

import json

from openhands_f2p.coverage_metric import (COV_DATA, COV_RC, COV_RC_SRC,
                                           DJANGO_COV_PATH, SYMPY_COV_DRIVER,
                                           SYMPY_DRIVER_SRC,
                                           added_lines_between, changed_line_coverage,
                                           changed_lines, coverage_command, is_test_file,
                                           measure_coverage, patched_source_files)
from openhands_f2p.images import (CLAIMS, DEFAULT_IMAGE_HEADROOM_GB, IMAGE, PLATFORM,
                                  PULL_LOCK, claim_image, claimed_images,
                                  daemon_refusal, evict_one_image,
                                  have_image, image_for, pull_image, reap_orphans,
                                  release_image, vm_free_gb)
from openhands_f2p.runners import (ANSI, DEFAULT_RUNNER, DJANGO_LINE, PYTEST,
                                   PYTEST_LINE, PYTEST_VERBOSE, SYMPY_LINE,
                                   detect_runner, repo_facts, test_directory,
                                   dotted_label, outcome_of, parse_output,
                                   patched_test_files, runner_for, test_command)
from openhands_f2p.sandbox import REPO_DIR, ExecResult, Sandbox

__all__ = [
    # images
    "CLAIMS", "DEFAULT_IMAGE_HEADROOM_GB", "IMAGE", "PLATFORM", "PULL_LOCK",
    "claim_image", "claimed_images", "daemon_refusal", "evict_one_image",
    "have_image", "image_for",
    "pull_image", "reap_orphans", "release_image", "vm_free_gb",
    # runners
    "ANSI", "DEFAULT_RUNNER", "DJANGO_LINE", "PYTEST", "PYTEST_LINE", "PYTEST_VERBOSE",
    "SYMPY_LINE", "detect_runner", "dotted_label", "outcome_of", "parse_output",
    "repo_facts",
    "test_directory",
    "patched_test_files", "runner_for", "test_command",
    # sandbox
    "REPO_DIR", "ExecResult", "Sandbox",
    # the coverage metric
    "COV_DATA", "COV_RC", "COV_RC_SRC", "DJANGO_COV_PATH", "SYMPY_COV_DRIVER",
    "SYMPY_DRIVER_SRC", "added_lines_between", "changed_line_coverage", "changed_lines",
    "coverage_command", "is_test_file", "measure_coverage", "patched_source_files",
    # here
    "verify_environment",
]



def verify_environment(instance: dict, sample: int = 8, quiet: bool = False) -> dict:
    """Environment gate: do the PASS_TO_PASS tests pass at base?

    They are independent of any test we are judging, so if they fail here the box is
    wrong and no verdict computed in it means anything.
    """
    # Some rows carry entries that are not test ids: pytest-5262's PASS_TO_PASS begins
    # with the literal "[100%]", swept up from a progress line when the dataset was
    # built. Nothing will ever be named that, so leaving it in fails the gate for a
    # container that is fine -- a dataset artefact reported as an environment problem.
    p2p = [n for n in json.loads(instance.get("PASS_TO_PASS") or "[]")
           if not n.startswith("[")][:sample]
    if not p2p:
        return {"checked": 0, "ok": True, "detail": "no PASS_TO_PASS ids"}
    with Sandbox(instance["instance_id"], quiet=quiet) as box:
        # Inside the box: which form the ids take is a property of the checkout now,
        # so it cannot be decided before there is a checkout to look at.
        # `p2p`, not the raw list: it is the filtered one, and handing pytest the
        # "[100%]" that survives in the raw list is precisely the single-unknown-id
        # failure the comment below describes.
        targets = (p2p if runner_for(box)["args"] == "nodes"
                   else patched_test_files(instance["test_patch"]))
        # The developer's test patch goes on first, because PASS_TO_PASS was recorded
        # after it was applied. psf__requests-5414 lists
        # test_invalid_url[InvalidURL-http://*example.com], a parametrize case that the
        # test patch *adds* -- so at base that id does not exist, and pytest treats one
        # unknown id as fatal for the whole run: "collected 7 items ... no tests ran".
        # A single missing id was zeroing the entire gate.
        box.apply_patch(instance["test_patch"])
        r = box.exec(test_command(box, targets), timeout=3600)
    outcomes = parse_output(r.output)
    failed = [n for n in p2p
              if (outcome_of(outcomes, n) or "MISSING") != "PASSED"]
    return {"checked": len(p2p), "ok": not failed, "failed": failed[:5],
            "seen": len(outcomes), "detail": r.output[-800:]}

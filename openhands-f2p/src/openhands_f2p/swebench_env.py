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
import shlex
from pathlib import Path

from openhands_f2p.coverage_metric import (COV_DATA, COV_RC, COV_RC_SRC,
                                           DJANGO_COV_PATH, SYMPY_COV_DRIVER,
                                           SYMPY_DRIVER_SRC,
                                           added_lines_between, changed_line_coverage,
                                           changed_lines, coverage_command, is_test_file,
                                           measure_coverage, patched_source_files)
from openhands_f2p.images import (CLAIMS, DEFAULT_IMAGE_HEADROOM_GB, IMAGE, PLATFORM,
                                  PULL_LOCK, claim_image, claimed_images, evict_one_image,
                                  have_image, image_for, pull_image, reap_orphans,
                                  release_image, vm_free_gb)
from openhands_f2p.runners import (ANSI, DEFAULT_RUNNER, DJANGO_LINE, PYTEST,
                                   PYTEST_LINE, PYTEST_VERBOSE, SYMPY_LINE, TEST_RUNNER,
                                   django_module, outcome_of, parse_output,
                                   patched_test_files, runner_for, test_command)
from openhands_f2p.sandbox import REPO_DIR, ExecResult, Sandbox

__all__ = [
    # images
    "CLAIMS", "DEFAULT_IMAGE_HEADROOM_GB", "IMAGE", "PLATFORM", "PULL_LOCK",
    "claim_image", "claimed_images", "evict_one_image", "have_image", "image_for",
    "pull_image", "reap_orphans", "release_image", "vm_free_gb",
    # runners
    "ANSI", "DEFAULT_RUNNER", "DJANGO_LINE", "PYTEST", "PYTEST_LINE", "PYTEST_VERBOSE",
    "SYMPY_LINE", "TEST_RUNNER", "django_module", "outcome_of", "parse_output",
    "patched_test_files", "runner_for", "test_command",
    # sandbox
    "REPO_DIR", "ExecResult", "Sandbox",
    # the coverage metric
    "COV_DATA", "COV_RC", "COV_RC_SRC", "DJANGO_COV_PATH", "SYMPY_COV_DRIVER",
    "SYMPY_DRIVER_SRC", "added_lines_between", "changed_line_coverage", "changed_lines",
    "coverage_command", "is_test_file", "measure_coverage", "patched_source_files",
    # here
    "repo_conventions", "verify_environment",
]



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

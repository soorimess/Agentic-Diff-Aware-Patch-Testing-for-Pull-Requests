"""The instances we develop against: twenty-six, spanning every repository and a decade.

Two things this set is arranged to test, neither of which more instances from one place
would test.

**Every repository.** The differences that break a harness are per-repository: each
project has its own runner, its own idea of where tests live, its own node-id format.
All twelve in SWE-bench Verified are here.

**Every era.** Each repository appears twice, once old and once recent, because a
project's conventions move between releases. `psf/requests` 1.1 is from 2013 and its
vendored urllib3 does `from collections import MutableMapping`, removed in Python 3.10 --
it cannot run outside its prepared image at all. django gets five versions, 1.11 through
5.0, because it has by far the most instances and by far the most convention churn.

Two limits that cannot be worked around: `pallets/flask` has exactly ONE instance in the
split, and both `mwaskom/seaborn` instances are v0.12, so neither has an old/new pair.

The pairs do something singles cannot. Two instances from one repository share a build,
so any difference between them is localisation rather than plumbing -- and that is the
axis a run is supposed to differ on. `psf/requests` shows it plainly: both build in
seconds, but one was solved first try and the other failed five runs in a row.

Two axes of difficulty, recorded separately because they are not the same axis:

    build     can the environment be stood up and the tests run at all
    localise  can the bug be found from the issue text
"""
import os
from pathlib import Path

PRS = [
    {
        "id": "django__django-11119",
        "tier": 3, "build": "medium", "localise": "medium", "runner": "django",
        "version": "3.0",
        "note": "Engine.render_to_string() does not honour its own autoescape setting",
        "why": "The oldest django we can actually verify. The 1.11 instance was dropped: "
               "its FAIL_TO_PASS names a test its own test patch never adds, because "
               "django's verbose runner prints a docstring in place of the method name "
               "and SWE-bench recorded whatever was printed. No 1.11 instance in the "
               "split is free of that, so 3.0 is the floor.",
    },
    {
        "id": "django__django-13406",
        "tier": 3, "build": "medium", "localise": "medium", "runner": "django",
        "version": "3.2",
        "note": "a queryset pickled with values() comes back broken",
        "why": "Pickling a queryset and unpickling it, which means the test has to round-trip an object rather than call a function.",
    },
    {
        "id": "django__django-15098",
        "tier": 3, "build": "medium", "localise": "hard", "runner": "django",
        "version": "4.1",
        "note": "i18n_patterns does not work with a locale containing both script and region",
        "why": "URL routing plus locale parsing. The reproduction needs a request through the resolver, not a direct call.",
    },
    {
        "id": "django__django-16333",
        "tier": 3, "build": "medium", "localise": "medium", "runner": "django",
        "version": "4.2",
        "note": "UserCreationForm does not save its many-to-many fields",
        "why": "Replaced 16082, which had the same docstring-versus-name inconsistency "
               "as the 1.11 instance. A form saving related objects, so the test has to "
               "save and then read back.",
    },
    {
        "id": "django__django-17029",
        "tier": 3, "build": "medium", "localise": "medium", "runner": "django",
        "version": "5.0",
        "note": "Apps.clear_cache() does not clear the get_swappable_settings_name cache",
        "why": "The newest django. Five versions from 1.11 to 5.0 test whether the harness follows a project across a decade of its own convention changes.",
    },
    {
        "id": "psf__requests-1142",
        "tier": 2, "build": "trivial", "localise": "medium", "runner": "pytest",
        "version": "1.1",
        "note": "requests adds a Content-Length header to GET requests",
        "why": "requests 1.1, from 2013. Its vendored urllib3 does `from collections import MutableMapping`, removed in Python 3.10 -- unrunnable outside its prepared image.",
    },
    {
        "id": "psf__requests-6028",
        "tier": 2, "build": "trivial", "localise": "hard", "runner": "pytest",
        "version": "2.27",
        "note": "proxy credentials dropped from the proxy URL, surfacing as a 407",
        "why": "The hard-localisation case: a 407 three layers above the cause, and the issue never names prepend_scheme_if_needed. It failed five runs before the diff was an input.",
    },
    {
        "id": "pallets__flask-5014",
        "tier": 1, "build": "trivial", "localise": "easy", "runner": "pytest",
        "version": "2.3",
        "note": "a Blueprint with an empty name should be rejected",
        "why": "The only flask instance in the split, so it has no old/new pair.",
    },
    {
        "id": "pylint-dev__pylint-4970",
        "tier": 2, "build": "easy", "localise": "medium", "runner": "pytest",
        "version": "2.10",
        "note": "min-similarity-lines=0 makes the duplicate-code checker report everything",
        "why": "The older pylint. A configuration value of zero that should disable a check and instead inverts it.",
    },
    {
        "id": "pylint-dev__pylint-6903",
        "tier": 2, "build": "easy", "localise": "easy", "runner": "pytest",
        "version": "2.15",
        "note": "pylint crashes when run with --jobs=0 inside a container",
        "why": "The newer pylint, and an environmental bug: it depends on how many CPUs the machine reports.",
    },
    {
        "id": "pytest-dev__pytest-5262",
        "tier": 3, "build": "easy", "localise": "medium", "runner": "pytest",
        "version": "4.5",
        "note": "_pytest.capture.EncodedFile advertises a mode that includes 'b'",
        "why": "pytest 4.5, four majors behind its pair. Same project, very different internals.",
    },
    {
        "id": "pytest-dev__pytest-10081",
        "tier": 3, "build": "easy", "localise": "medium", "runner": "pytest",
        "version": "7.2",
        "note": "pdb teardown runs for a unittest class that was skipped",
        "why": "The newer pytest, and the one project that keeps tests in testing/ not tests/.",
    },
    {
        "id": "sphinx-doc__sphinx-7454",
        "tier": 3, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "3.0",
        "note": "autodoc renders None in a signature differently with autodoc_typehints",
        "why": "sphinx 3.0. Documentation output is the observable, so the test drives a build.",
    },
    {
        "id": "sphinx-doc__sphinx-10614",
        "tier": 3, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "7.2",
        "note": "inheritance diagram SVG links are wrong in nested directories",
        "why": "The newer sphinx, four majors on, same build-driven shape.",
    },
    {
        "id": "pydata__xarray-3677",
        "tier": 4, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "0.12",
        "note": "ds.merge() fails when passed a DataArray instead of a Dataset",
        "why": "xarray 0.12, from 2019, against numpy and pandas of that era.",
    },
    {
        "id": "pydata__xarray-7233",
        "tier": 4, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "2022.09",
        "note": "ds.Coarsen.construct demotes non-dimensional coordinates to variables",
        "why": "Modern xarray. Coordinate bookkeeping that needs a real dataset to observe.",
    },
    {
        "id": "astropy__astropy-7336",
        "tier": 4, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "1.3",
        "note": "units.quantity_input fails on a constructor annotated to return None",
        "why": "astropy 1.3, the oldest non-django instance here. A decorator interacting with type annotations, which behaved differently on old Pythons.",
    },
    {
        "id": "astropy__astropy-14995",
        "tier": 4, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "5.2",
        "note": "mask propagation fails when one operand has no mask",
        "why": "Modern astropy. The wrong answer is a mask rather than an exception.",
    },
    {
        "id": "sympy__sympy-12096",
        "tier": 4, "build": "medium", "localise": "hard", "runner": "sympy",
        "version": "1.0",
        "note": "evalf does not call _imp_ recursively",
        "why": "sympy 1.0. Bare function names as node ids and bin/test as the runner, on the oldest sympy in the split.",
    },
    {
        "id": "sympy__sympy-24562",
        "tier": 4, "build": "medium", "localise": "hard", "runner": "sympy",
        "version": "1.12",
        "note": "Rational('0.5', '100') returns 1/100100 instead of 1/200",
        "why": "Modern sympy. Coverage cannot follow bin/test, so this is the one instance needing a genuinely bespoke workaround.",
    },
    {
        "id": "mwaskom__seaborn-3069",
        "tier": 4, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "0.12",
        "note": "nominal scales should have Nominal-specific axis behaviour",
        "why": "One of only two seaborn instances, both v0.12 -- there is no older version to pair with. Its fix touches several files, which makes changed-line coverage a harder target than a one-line patch.",
    },
    {
        "id": "mwaskom__seaborn-3187",
        "tier": 4, "build": "medium", "localise": "medium", "runner": "pytest",
        "version": "0.12",
        "note": "legend entries lose their offset when the scale is large",
        "why": "The other seaborn. The observable is the content of a legend object.",
    },
    {
        "id": "matplotlib__matplotlib-13989",
        "tier": 5, "build": "hard", "localise": "medium", "runner": "pytest",
        "version": "3.0",
        "note": "hist() ignores range when density=True",
        "why": "matplotlib 3.0, from 2018, with its own compiled extensions of that era.",
    },
    {
        "id": "matplotlib__matplotlib-26208",
        "tier": 5, "build": "hard", "localise": "medium", "runner": "pytest",
        "version": "3.7",
        "note": "dataLims go to infinity when a twinned axis uses units",
        "why": "Modern matplotlib, and one of the few instances whose test is not an image comparison -- those need baseline PNGs and cannot be written from scratch.",
    },
    {
        "id": "scikit-learn__scikit-learn-10908",
        "tier": 5, "build": "hard", "localise": "medium", "runner": "pytest",
        "version": "0.20",
        "note": "CountVectorizer.get_feature_names raises when only a vocabulary was given",
        "why": "scikit-learn 0.20, from 2018. Cython against numpy and scipy of that era, which is the least likely thing in this set to build anywhere but its own image.",
    },
    {
        "id": "scikit-learn__scikit-learn-25747",
        "tier": 5, "build": "hard", "localise": "medium", "runner": "pytest",
        "version": "1.3",
        "note": "FeatureUnion fails with pandas output when a transformer changes rows",
        "why": "Modern scikit-learn. Reproducing it needs a custom transformer and a DatetimeIndex.",
    },
]

# An alternative instance list, for a set this system was not developed against.
#
# The twenty-six above were chosen by hand -- for coverage of repositories, runners and a
# decade of versions -- and every prompt and heuristic here has been tuned while looking
# at them. That makes them useless for the one question they cannot answer: whether the
# system works on instances nobody looked at. `F2P_PRS_FILE` points at a JSON list of the
# same shape, so an evaluation set runs through exactly the same code with nothing
# special-cased for it.
#
#     F2P_PRS_FILE=evaluation/prs.json F2P_IMAGE_CACHE=image-cache-evaluation \
#         uv run python -m openhands_f2p.agent all --model gpt-5-mini \
#         --out-root evaluation/out_gpt5mini --mutants 10 --parallel 10
_PRS_FILE = os.getenv("F2P_PRS_FILE")
if _PRS_FILE:
    import json as _json
    _loaded = _json.loads(Path(_PRS_FILE).read_text())
    missing = [k for k in ("id", "tier") for p in _loaded if k not in p]
    if missing:
        raise SystemExit(f"  {_PRS_FILE}: every entry needs at least 'id' and 'tier'")
    PRS = [{"build": "unknown", "localise": "unknown", "runner": "pytest",
            "version": "", "note": "", "why": "", **p} for p in _loaded]

BY_ID = {p["id"]: p for p in PRS}
BY_REPO: dict[str, list[str]] = {}
for _p in PRS:
    BY_REPO.setdefault(_p["id"].split("__")[0], []).append(_p["id"])


def f2p_is_consistent(instance: dict) -> list[str]:
    """FAIL_TO_PASS ids that the instance's own test patch never adds.

    A real dataset artefact, not a harness bug, and it silently inverts a verdict rather
    than raising: the named test is not the one the patch changed, so it passes at base,
    and the instance reads as "the test does not exercise the change".

    The cause is django-specific. Its verbose runner prints a test's *docstring* in place
    of the method name, and SWE-bench recorded whatever was printed -- so for a changed
    test that has a docstring, the recorded id belongs to some unrelated test that
    happened to move. Two of the twenty-six picks had it, both django, and the only
    django 1.11 instance in the whole split is one of them, which is why 3.0 is the
    oldest django here.

    Checked in a test rather than trusted, because the next instance added will not
    announce it.
    """
    import json
    f2p = json.loads(instance.get("FAIL_TO_PASS") or "[]")
    patch = instance.get("test_patch") or ""
    added = "\n".join(l[1:] for l in patch.splitlines()
                       if l.startswith("+") and not l.startswith("+++"))
    missing = []
    for nid in f2p:
        leaf = nid.split("::")[-1].split("[")[0].strip()
        if " (" in nid:                                  # django's display format
            leaf = nid.split(" (")[0].strip()
        if leaf and leaf not in added and leaf not in patch:
            missing.append(nid)
    return missing


def pick(which: str) -> list[dict]:
    """Select by number, id, repository prefix, tier, version, 'old', 'new', or 'all'."""
    if which == "all":
        return PRS
    # A comma-separated list, so an arbitrary subset -- the instances a fixed bug
    # actually touched, say -- can be one parallel run instead of a shell loop that
    # serialises them.
    if "," in which:
        out, seen = [], set()
        for part in (w.strip() for w in which.split(",") if w.strip()):
            for pr in pick(part):
                if pr["id"] not in seen:
                    seen.add(pr["id"])
                    out.append(pr)
        return out
    if which.isdigit() and 1 <= int(which) <= len(PRS):
        return [PRS[int(which) - 1]]
    if which in BY_ID:
        return [BY_ID[which]]
    if which.startswith("tier") and which[4:].strip().isdigit():
        hits = [p for p in PRS if p["tier"] == int(which[4:].strip())]
        if hits:
            return hits
    # 'old' and 'new' take the earliest and latest version of each repository, which is
    # the comparison the set was built for.
    if which in ("old", "new"):
        def key(p):
            return tuple(int("".join(c for c in part if c.isdigit()) or 0)
                         for part in p["version"].split("."))
        out = []
        for ids in BY_REPO.values():
            group = sorted((BY_ID[i] for i in ids), key=key)
            out.append(group[0] if which == "old" else group[-1])
        return sorted(out, key=lambda p: PRS.index(p))
    hits = [p for p in PRS if p["id"].startswith(which)]
    if hits:
        return hits
    raise SystemExit(
        f"unknown selector {which!r}. Use 1..{len(PRS)}, an instance id, a repository "
        f"prefix such as 'django', a tier such as 'tier5', 'old', 'new', or 'all'.")

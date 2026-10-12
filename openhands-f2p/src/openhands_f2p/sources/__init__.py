"""Where instances come from: one adapter per dataset, one standard row for the harness.

Everything downstream of this package -- the agent, the verifier, the coverage metric, the
oracle -- reads an instance as a SWE-bench Verified row and nothing else. That shape is
the standard here, not because SWE-bench is special but because the harness was built on
it and has been audited on it. A new dataset does not teach the harness a new shape; its
adapter produces the shape the harness already trusts:

    instance_id        owner__repo-number, the key everything is filed under
    repo               owner/repo
    base_commit        the tree the agent works in, before the change
    patch              the change under test, without its tests (unified diff)
    test_patch         the developer's tests for it (held out; read only to judge)
    problem_statement  the text the agent may be given about the change
    FAIL_TO_PASS       JSON list: developer tests that fail at base and pass with `patch`
    PASS_TO_PASS       JSON list: developer tests that pass on both sides
    version, created_at, hints_text, environment_setup_commit   carried, may be ""

plus three fields every adapter adds:

    dataset            which adapter made the row ("swebench", "chaco", ...)
    image              the Docker image the instance runs in
    image_source       "pull" (a registry has it) or "build" (we build it -- image_build.py)

The image contract is SWE-bench's as well: the checkout at `/testbed` at `base_commit`,
installed so its tests run with `python` under `bash -lc`, as root, with `git` and
coreutils `timeout` present, and with no network needed once the container starts.

Which dataset a run is over is never inferred from an instance id: `--dataset` (the env
var `F2P_DATASET_NAME`, default `swebench`) names it, and the run prints and records it.
`python -m openhands_f2p.sources` lists the datasets and what is prepared of each.
"""
from __future__ import annotations

import os
from typing import Protocol

DATASET_ENV = "F2P_DATASET_NAME"
DEFAULT_DATASET = "swebench"

# The fields the harness reads off a row. An adapter that leaves one out is refused at
# prepare time rather than discovered by a KeyError forty actions into a run.
REQUIRED_FIELDS = ("instance_id", "repo", "base_commit", "patch", "test_patch",
                   "problem_statement", "FAIL_TO_PASS", "PASS_TO_PASS",
                   "dataset", "image", "image_source")


class Source(Protocol):
    name: str
    description: str

    def load(self, instance_id: str) -> dict: ...
    def prs(self) -> list[dict] | None: ...
    def image_for(self, instance_id: str) -> str: ...
    def owns_image(self, image: str) -> bool: ...
    def summary(self) -> dict: ...
    def groups(self) -> dict: ...


def _registry() -> dict[str, Source]:
    # Imported here, not at module level: `images` asks this package for an image name,
    # and the adapters import the environment modules to build and validate theirs.
    from openhands_f2p.sources import chaco, swebench
    return {"swebench": swebench.SOURCE, "chaco": chaco.SOURCE}


def names() -> list[str]:
    return list(_registry())


def get(name: str) -> Source:
    reg = _registry()
    if name not in reg:
        raise SystemExit(f"unknown dataset {name!r}; known: {', '.join(reg)}")
    return reg[name]


def active_name() -> str:
    return (os.getenv(DATASET_ENV) or DEFAULT_DATASET).strip()


def active() -> Source:
    return get(active_name())


def select(name: str | None) -> Source:
    """Make `name` the dataset of this process and of every child it starts."""
    if name:
        get(name)                       # refuse an unknown name before setting it
        os.environ[DATASET_ENV] = name
    return active()


def load(instance_id: str) -> dict:
    return active().load(instance_id)


def groups() -> dict:
    """The active dataset's PR groups that reports mark: {key: {label, why, ids: {id: note}}}."""
    return active().groups()


def image_for(instance_id: str) -> str:
    return active().image_for(instance_id)


def source_of_image(image: str) -> Source | None:
    """The adapter that knows how to obtain `image`, whatever the active dataset is."""
    for src in _registry().values():
        if src.owns_image(image):
            return src
    return None


def check_row(row: dict) -> dict:
    missing = [k for k in REQUIRED_FIELDS if k not in row]
    if missing:
        raise ValueError(f"{row.get('instance_id', '?')}: row lacks {missing}")
    return row

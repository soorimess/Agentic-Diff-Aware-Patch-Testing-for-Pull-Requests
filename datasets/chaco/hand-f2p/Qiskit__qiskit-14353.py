import pytest

from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passmanager_config import PassManagerConfig
from qiskit.transpiler.preset_passmanagers import builtin_plugins as B

PLUGINS = ["DefaultLayoutPassManager", "TrivialLayoutPassManager",
           "DenseLayoutPassManager", "SabreLayoutPassManager"]
LAYOUT_PASSES = {"TrivialLayout", "DenseLayout", "SabreLayout", "VF2Layout"}


def _pass_names(pm):
    def walk(task):
        sub = getattr(task, "tasks", None)
        if sub is None:
            yield type(task).__name__
            return
        for t in sub:
            yield from walk(t)
    return list(walk(pm.to_flow_controller()))


@pytest.mark.parametrize("level", [0, 1, 2, 3])
@pytest.mark.parametrize("plugin", PLUGINS)
def test_no_layout_pass_without_coupling_map(plugin, level):
    # With nothing to lay out onto, the stage only embeds a given layout.
    pm = getattr(B, plugin)().pass_manager(PassManagerConfig(), optimization_level=level)
    names = _pass_names(pm)
    assert not LAYOUT_PASSES & set(names), names
    assert "SetLayout" in names


@pytest.mark.parametrize("plugin", PLUGINS)
def test_layout_pass_kept_with_coupling_map(plugin):
    config = PassManagerConfig(coupling_map=CouplingMap.from_line(3))
    names = _pass_names(getattr(B, plugin)().pass_manager(config, optimization_level=1))
    assert LAYOUT_PASSES & set(names), names

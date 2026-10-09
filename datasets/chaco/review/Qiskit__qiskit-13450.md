# Qiskit__qiskit-13450

[back to the list](README.md) -- **Fix post-oxidization change in `ConsolidateBlocks` behavior **

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#13450](https://github.com/Qiskit/qiskit/pull/13450) (created 2024-11-18, merged 2024-11-18) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 2 developer test(s) flip; oracle reproduces it |
| base commit | [`b9d5c9c6aeb4`](https://github.com/Qiskit/qiskit/commit/b9d5c9c6aeb4568b6e9fba8943517ebed300886d) (2024-11-14), first parent of the merge commit |
| merge commit | [`94cea419010b`](https://github.com/Qiskit/qiskit/commit/94cea419010b0c8210ef633bf39d4a89618ade01) |
| issues closed | none |
| version | 2.0 |
| image | `f2p-chaco/qiskit__qiskit-13450:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-13450.Dockerfile) |
| source files (`patch`) | `qiskit/transpiler/passes/optimization/consolidate_blocks.py` |
| test files (`test_patch`) | `test/python/transpiler/test_consolidate_blocks.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (2)

- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_no_kak_gates_in_preset_pm_1_2`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_no_kak_gates_in_preset_pm_2_3`

## PASS_TO_PASS (24)

<details><summary>show</summary>

- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_3q_blocks`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_block_spanning_two_regs`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_block_spanning_two_regs_different_index`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_classical_conditions_maintained`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_consolidate_blocks_big`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_consolidate_small_block`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_custom_no_target`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_descent_into_control_flow`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_identity_1q_unitary_is_removed`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_identity_unitary_is_removed`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_inverted_order`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_no_kak_in_basis`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_node_added_after_block`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_node_added_before_block`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_node_middle_of_blocks`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_not_crossing_between_control_flow_block_and_parent`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_not_crossing_between_control_flow_ops`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_overlapping_block_and_run`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_basis`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_basis_with_target`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_local_basis_with_target`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_target_with_matching_basis_gates`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_topological_order_preserved`
- `test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_wire_order`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #13450: Fix post-oxidization change in `ConsolidateBlocks` behavior

### Summary
Fixes the behavioral difference introduced by #13368 that caused #13438. 

The original implementation of the pass used to set the `ConsolidateBlocks` internal decomposer calling `unitary_synthesis._decomposer_2q_from_basis_gates`, which, when `kak_basis` wasn't found, would return `None`. During the oxidization efforts, `unitary_synthesis._decomposer_2q_from_basis_gates` was replaced with inline code that didn't contemplate this path (always set a default decomposer), which in the reproducing example led to a longer output circuit (the gates were collected into a unitary block and then decomposed differently).

### Details and comments
Technically not a bugfix because the change wasn't released yet.

Using the example shown in the issue ->

`ConsolidateBlocks` output dag with 1.2.4:
![image](https://github.com/user-attachments/assets/d3d297fd-fc76-41f6-9ece-68d252596ad6)

`ConsolidateBlocks` output dag with 1.3.0rc1:
![image](https://github.com/user-attachments/assets/b56ab05e-e9ae-4f16-a730-944ebd491938)

`ConsolidateBlocks` output dag after this fix:
![image](https://github.com/user-attachments/assets/d3d297fd-fc76-41f6-9ece-68d252596ad6)
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/transpiler/passes/optimization/consolidate_blocks.py b/qiskit/transpiler/passes/optimization/consolidate_blocks.py
index 63dca11f6d2dd013f2e74eddbf38250398709fdc..ce64233699b29d262f50e0ca3e2d3925097372b8 100644
--- a/qiskit/transpiler/passes/optimization/consolidate_blocks.py
+++ b/qiskit/transpiler/passes/optimization/consolidate_blocks.py
@@ -12,9 +12,11 @@
 
 """Replace each block of consecutive gates by a single Unitary node."""
 from __future__ import annotations
+from math import pi
 
 from qiskit.synthesis.two_qubit import TwoQubitBasisDecomposer
-from qiskit.circuit.library.standard_gates import CXGate, CZGate, iSwapGate, ECRGate
+from qiskit.circuit.library.standard_gates import CXGate, CZGate, iSwapGate, ECRGate, RXXGate
+
 from qiskit.transpiler.basepasses import TransformationPass
 from qiskit.transpiler.passmanager import PassManager
 from qiskit._accelerate.consolidate_blocks import consolidate_blocks
@@ -27,6 +29,7 @@ KAK_GATE_NAMES = {
     "cz": CZGate(),
     "iswap": iSwapGate(),
     "ecr": ECRGate(),
+    "rxx": RXXGate(pi / 2),
 }
 
 
@@ -70,7 +73,6 @@ class ConsolidateBlocks(TransformationPass):
         if basis_gates is not None:
             self.basis_gates = set(basis_gates)
         self.force_consolidate = force_consolidate
-
         if kak_basis_gate is not None:
             self.decomposer = TwoQubitBasisDecomposer(kak_basis_gate)
         elif basis_gates is not None:
@@ -79,8 +81,12 @@ class ConsolidateBlocks(TransformationPass):
                 self.decomposer = TwoQubitBasisDecomposer(
                     KAK_GATE_NAMES[kak_gates.pop()], basis_fidelity=approximation_degree or 1.0
                 )
+            elif "rzx" in basis_gates:
+                self.decomposer = TwoQubitBasisDecomposer(
+                    CXGate(), basis_fidelity=approximation_degree or 1.0
+                )
             else:
-                self.decomposer = TwoQubitBasisDecomposer(CXGate())
+                self.decomposer = None
         else:
             self.decomposer = TwoQubitBasisDecomposer(CXGate())
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/transpiler/test_consolidate_blocks.py b/test/python/transpiler/test_consolidate_blocks.py
index 3b3aff1db228a46696ec831bd5c107ad97136940..fbe11ff77db11712f64769262305a07a4ad2fe15 100644
--- a/test/python/transpiler/test_consolidate_blocks.py
+++ b/test/python/transpiler/test_consolidate_blocks.py
@@ -16,20 +16,19 @@ Tests for the ConsolidateBlocks transpiler pass.
 
 import unittest
 import numpy as np
+from ddt import ddt, data
 
 from qiskit.circuit import QuantumCircuit, QuantumRegister, IfElseOp, Gate
 from qiskit.circuit.library import U2Gate, SwapGate, CXGate, CZGate, UnitaryGate
 from qiskit.converters import circuit_to_dag
-from qiskit.transpiler.passes import ConsolidateBlocks
 from qiskit.quantum_info.operators import Operator
 from qiskit.quantum_info.operators.measures import process_fidelity
-from qiskit.transpiler import PassManager
-from qiskit.transpiler import Target
-from qiskit.transpiler.passes import Collect1qRuns
-from qiskit.transpiler.passes import Collect2qBlocks
+from qiskit.transpiler import PassManager, Target, generate_preset_pass_manager
+from qiskit.transpiler.passes import ConsolidateBlocks, Collect1qRuns, Collect2qBlocks
 from test import QiskitTestCase  # pylint: disable=wrong-import-order
 
 
+@ddt
 class TestConsolidateBlocks(QiskitTestCase):
     """
     Tests to verify that consolidating blocks of gates into unitaries
@@ -571,6 +570,26 @@ class TestConsolidateBlocks(QiskitTestCase):
 
         self.assertEqual(res, qc)
 
+    @data(2, 3)
+    def test_no_kak_gates_in_preset_pm(self, opt_level):
+        """Test correct initialization of ConsolidateBlocks pass when kak_gates aren't found.
+        Reproduces https://github.com/Qiskit/qiskit/issues/13438."""
+
+        qc = QuantumCircuit(2)
+        qc.cz(0, 1)
+        qc.sx([0, 1])
+        qc.cz(0, 1)
+
+        ref_pm = generate_preset_pass_manager(
+            optimization_level=1, basis_gates=["rz", "rzz", "sx", "x", "rx"]
+        )
+        ref_tqc = ref_pm.run(qc)
+        pm = generate_preset_pass_manager(
+            optimization_level=opt_level, basis_gates=["rz", "rzz", "sx", "x", "rx"]
+        )
+        tqc = pm.run(qc)
+        self.assertEqual(ref_tqc, tqc)
+
 
 if __name__ == "__main__":
     unittest.main()
```

## Validation

```json
{
 "test_files": [
  "test/python/transpiler/test_consolidate_blocks.py"
 ],
 "collected_before": 26,
 "collected_after": 26,
 "outcomes_before": {
  "PASSED": 24,
  "FAILED": 2
 },
 "outcomes_after": {
  "PASSED": 26
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "t_consolidate_blocks.py::TestConsolidateBlocks::test_node_middle_of_blocks\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_not_crossing_between_control_flow_block_and_parent\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_not_crossing_between_control_flow_ops\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_overlapping_block_and_run\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_basis\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_basis_with_target\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_local_basis_with_target\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_target_with_matching_basis_gates\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_topological_order_preserved\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_wire_order\nFAILED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_no_kak_gates_in_preset_pm_1_2\nFAILED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_no_kak_gates_in_preset_pm_2_3\n================== 2 failed, 24 passed, 148 warnings in 4.07s ==================",
 "tail_after": "ranspiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_node_added_after_block\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_node_added_before_block\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_node_middle_of_blocks\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_not_crossing_between_control_flow_block_and_parent\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_not_crossing_between_control_flow_ops\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_overlapping_block_and_run\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_basis\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_basis_with_target\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_local_basis_with_target\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_single_gate_block_outside_target_with_matching_basis_gates\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_topological_order_preserved\nPASSED test/python/transpiler/test_consolidate_blocks.py::TestConsolidateBlocks::test_wire_order\n======================= 26 passed, 68 warnings in 1.69s ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

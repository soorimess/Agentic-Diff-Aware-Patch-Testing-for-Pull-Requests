# Qiskit__qiskit-12814

[back to the list](README.md) -- **Light Cone Transpiler Pass**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#12814](https://github.com/Qiskit/qiskit/pull/12814) (created 2024-07-25, merged 2025-03-04) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 28 developer test(s) flip; oracle reproduces it |
| base commit | [`731e4744e949`](https://github.com/Qiskit/qiskit/commit/731e4744e9499e2f8063ddc793028aba70e625b0) (2025-03-03), first parent of the merge commit |
| merge commit | [`47e8c9851f7c`](https://github.com/Qiskit/qiskit/commit/47e8c9851f7c60715da57279c8d88cb9211f703e) |
| issues closed | none |
| version | 2.0 |
| image | `f2p-chaco/qiskit__qiskit-12814:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-12814.Dockerfile) |
| source files (`patch`) | `qiskit/transpiler/passes/optimization/light_cone.py`, `qiskit/transpiler/passes/utils/remove_final_measurements.py`, `releasenotes/notes/add-light-cone-pass-6c56085734512e98.yaml` |
| test files (`test_patch`) | `test/python/transpiler/test_light_cone.py`, `test/python/transpiler/test_remove_final_measurements.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (28)

- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_all_commuting`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_big_circuit_1`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_big_circuit_2`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_commuting_block`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_measurement_barriers`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_nonparameterized_commuting`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_nonparameterized_noncommuting_1_X`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_nonparameterized_noncommuting_2_Z`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_parameter_expression_1`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_parameter_expression_2`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_parameterized_asymmetric`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_parameterized_commuting`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_parameterized_noncommuting_1_Y`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_parameterized_noncommuting_2_Z`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_parameterized_symmetric`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_raise_error_for_invalid_bit_terms_characters`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_raise_error_when_circuit_measurements_and_observable_present`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_raise_error_when_indices_is_empty`
- `test/python/transpiler/test_light_cone.py::TestLightConePass::test_raise_error_when_indices_out_of_range`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_calc_final_ops`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_final_barriers_and_measures_complex`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_final_measures_share_dest`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_multi_bit_register_removed_if_all_bits_idle`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_multi_bit_register_removed_with_clbits`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_multi_reg_shared_bits_removed`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_overlapping_register_removal`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_remove_chained_final_measurements`
- `test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_remove_clbits_without_register`

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #12814: Light Cone Transpiler Pass

### Summary
When measuring or sampling a subset of the qubits of our circuit there will be some gates in our circuit that will not affect the outcome of the measurement. One can thus compute the causal light cone of the circuit and measurement, i.e. the set of gates that does affect the measurement. This transpiler pass provides an easy tool to reduce the number of gates in our circuit provided a Pauli observable to be measured or  a subset of measurements in the Z basis.
This PR adresses  #12792 

### Details and comments
This code takes inspiration from an implementation done by @aeddins-ibm.
Before finishing the unit-tests for this PR it would be interesting to solve #12790 .
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/transpiler/passes/optimization/light_cone.py b/qiskit/transpiler/passes/optimization/light_cone.py
new file mode 100644
index 0000000000000000000000000000000000000000..19273accbdc6253fcfe2274e01354ea05c15b648
--- /dev/null
+++ b/qiskit/transpiler/passes/optimization/light_cone.py
@@ -0,0 +1,135 @@
+# This code is part of Qiskit.
+#
+# (C) Copyright IBM 2017, 2019.
+#
+# This code is licensed under the Apache License, Version 2.0. You may
+# obtain a copy of this license in the LICENSE.txt file in the root directory
+# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
+#
+# Any modifications or derivative works of this code must retain this
+# copyright notice, and modified files need to carry a notice indicating
+# that they have been altered from the originals.
+
+"""Cancel the redundant (self-adjoint) gates through commutation relations."""
+from __future__ import annotations
+import warnings
+from qiskit.circuit import Gate, Qubit
+from qiskit.circuit.commutation_library import SessionCommutationChecker as scc
+from qiskit.circuit.library import PauliGate, ZGate
+from qiskit.dagcircuit import DAGCircuit
+from qiskit.transpiler.basepasses import TransformationPass
+from qiskit.transpiler.passes.utils.remove_final_measurements import calc_final_ops
+
+translation_table = str.maketrans({"+": "X", "-": "X", "l": "Y", "r": "Y", "0": "Z", "1": "Z"})
+
+
+class LightCone(TransformationPass):
+    """Remove the gates that do not affect the outcome of a measurement on a circuit.
+
+    Pass for computing the light-cone of an observable or measurement. The Pass can handle
+    either an observable one would like to measure or a measurement on a set of qubits.
+    """
+
+    def __init__(self, bit_terms: str | None = None, indices: list[int] | None = None) -> None:
+        """
+        Args:
+            bit_terms: If ``None`` the light-cone will be computed for the set of measurements
+                in the circuit. If a string is specified, the light-cone will correspond to the
+                reduced circuit with the same expectation value for the observable.
+            indices: list of non-trivial indices corresponding to the observable in ``bit_terms``.
+        """
+        super().__init__()
+        valid_characters = {"X", "Y", "Z", "+", "-", "l", "r", "0", "1"}
+        self.bit_terms = None
+        if bit_terms is not None:
+            if not indices:
+                raise ValueError("`indices` must be non-empty when providing `bit_terms`.")
+            if not set(bit_terms).issubset(valid_characters):
+                raise ValueError(
+                    f"`bit_terms` should contain only characters in {valid_characters}."
+                )
+            if len(bit_terms) != len(indices):
+                raise ValueError("`bit_terms` must be the same length as `indices`.")
+            self.bit_terms = bit_terms.translate(translation_table)
+        self.indices = indices
+
+    @staticmethod
+    def _find_measurement_qubits(dag: DAGCircuit) -> set[Qubit]:
+        final_nodes = calc_final_ops(dag, {"measure"})
+        qubits_measured = set()
+        for node in final_nodes:
+            qubits_measured |= set(node.qargs)
+        return qubits_measured
+
+    def _get_initial_lightcone(
+        self, dag: DAGCircuit
+    ) -> tuple[set[Qubit], list[tuple[Gate, list[Qubit]]]]:
+        """Returns the initial light-cone.
+        If observable is `None`, the light-cone is the set of measured qubits.
+        If a `bit_terms` is provided, the qubits corresponding to the
+        non-trivial Paulis define the light-cone.
+        """
+        lightcone_qubits = self._find_measurement_qubits(dag)
+        if self.bit_terms is None:
+            lightcone_operations = [(ZGate(), [qubit_index]) for qubit_index in lightcone_qubits]
+        else:
+            # Having both measurements and an observable is not allowed
+            if len(dag.qubits) < max(self.indices) + 1:
+                raise ValueError("`indices` contains values outside the qubit range.")
+            if lightcone_qubits:
+                raise ValueError(
+                    "The circuit contains measurements and an observable has been given: "
+                    "remove the observable or the measurements."
+                )
+            lightcone_qubits = [dag.qubits[i] for i in self.indices]
+            # `lightcone_operations` is a list of tuples, each containing (operation, list_of_qubits)
+            lightcone_operations = [(PauliGate(self.bit_terms), lightcone_qubits)]
+
+        return set(lightcone_qubits), lightcone_operations
+
+    def run(self, dag: DAGCircuit) -> DAGCircuit:
+        """Run the LightCone pass on `dag`.
+
+        Args:
+            dag: The DAG to reduce.
+
+        Returns:
+            The DAG reduced to the light-cone of the observable.
+        """
+
+        # Get the initial light-cone and operations
+        lightcone_qubits, lightcone_operations = self._get_initial_lightcone(dag)
+
+        #  Initialize a new, empty DAG
+        new_dag = dag.copy_empty_like()
+
+        # Iterate over the nodes in reverse topological order
+        for node in reversed(list(dag.topological_op_nodes())):
+            # Check if the node belongs to the light-cone
+            if lightcone_qubits.intersection(node.qargs):
+                # Check commutation with all previous operations
+                commutes_bool = True
+                for op in lightcone_operations:
+                    max_num_qubits = max(len(op[1]), len(node.qargs))
+                    if max_num_qubits > 10:
+                        warnings.warn(
+                            "LightCone pass is checking commutation of"
+                            f"operators of size {max_num_qubits}."
+                            "This operation can be slow.",
+                            category=RuntimeWarning,
+                        )
+                    commute_bool = scc.commute(
+                        op[0], op[1], [], node.op, node.qargs, [], max_num_qubits=max_num_qubits
+                    )
+                    if not commute_bool:
+                        # If the current node does not commute, update the light-cone
+                        lightcone_qubits.update(node.qargs)
+                        lightcone_operations.append((node.op, node.qargs))
+                        commutes_bool = False
+                        break
+
+                # If the node is in the light-cone and commutes with previous `ops`,
+                # add it to the new DAG at the front
+                if not commutes_bool:
+                    new_dag.apply_operation_front(node.op, node.qargs, node.cargs)
+        return new_dag
diff --git a/qiskit/transpiler/passes/utils/remove_final_measurements.py b/qiskit/transpiler/passes/utils/remove_final_measurements.py
index c3179e204cd4f0804fc619eb6bfb3f1c678dee99..a2c412f734eca1b5066130db34e11112913bc026 100644
--- a/qiskit/transpiler/passes/utils/remove_final_measurements.py
+++ b/qiskit/transpiler/passes/utils/remove_final_measurements.py
@@ -13,7 +13,45 @@
 """Remove final measurements and barriers at the end of a circuit."""
 
 from qiskit.transpiler.basepasses import TransformationPass
-from qiskit.dagcircuit import DAGOpNode
+from qiskit.dagcircuit import DAGCircuit, DAGOpNode
+
+
+def calc_final_ops(dag: DAGCircuit, final_op_names: set[str]) -> list[DAGOpNode]:
+    """Find the final operations of a circuit of a given type.
+    Args:
+        dag: the DAG circuit
+        final_op_names: names of the operations to find at the end of the circuit.
+
+    Returns:
+    List of nodes corresponding the the relevant operations at the end of the circuit.
+    """
+    final_ops = []
+
+    to_visit = [next(dag.predecessors(dag.output_map[qubit])) for qubit in dag.qubits]
+    barrier_encounters_remaining = {}
+
+    while to_visit:
+        node = to_visit.pop()
+        if not isinstance(node, DAGOpNode):
+            continue
+
+        if node.op.name == "barrier":
+            # Barrier is final if all children are final, so we track
+            # how many times we still need to encounter each barrier
+            # via a child node.
+            if node not in barrier_encounters_remaining:
+                barrier_encounters_remaining[node] = sum(1 for _ in dag.quantum_successors(node))
+            if barrier_encounters_remaining[node] - 1 > 0:
+                # We've encountered the barrier, but not (yet) via all children.
+                # Record the encounter, and bail!
+                barrier_encounters_remaining[node] -= 1
+                continue
+        if node.name in final_op_names:
+            # Current node is either a measure, or a barrier with all final op children.
+            final_ops.append(node)
+            to_visit.extend(dag.quantum_predecessors(node))
+
+    return final_ops
 
 
 class RemoveFinalMeasurements(TransformationPass):
@@ -32,37 +70,6 @@ class RemoveFinalMeasurements(TransformationPass):
     in a classical register that will remain.
     """
 
-    def _calc_final_ops(self, dag):
-        final_op_types = {"measure", "barrier"}
-        final_ops = []
-
-        to_visit = [next(dag.predecessors(dag.output_map[qubit])) for qubit in dag.qubits]
-        barrier_encounters_remaining = {}
-
-        while to_visit:
-            node = to_visit.pop()
-            if not isinstance(node, DAGOpNode):
-                continue
-            if node.op.name == "barrier":
-                # Barrier is final if all children are final, so we track
-                # how many times we still need to encounter each barrier
-                # via a child node.
-                if node not in barrier_encounters_remaining:
-                    barrier_encounters_remaining[node] = sum(
-                        1 for _ in dag.quantum_successors(node)
-                    )
-                if barrier_encounters_remaining[node] - 1 > 0:
-                    # We've encountered the barrier, but not (yet) via all children.
-                    # Record the encounter, and bail!
-                    barrier_encounters_remaining[node] -= 1
-                    continue
-            if node.name in final_op_types:
-                # Current node is either a measure, or a barrier with all final op children.
-                final_ops.append(node)
-                to_visit.extend(dag.quantum_predecessors(node))
-
-        return final_ops
-
     def run(self, dag):
         """Run the RemoveFinalMeasurements pass on `dag`.
 
@@ -72,7 +79,7 @@ class RemoveFinalMeasurements(TransformationPass):
         Returns:
             DAGCircuit: the optimized DAG.
         """
-        final_ops = self._calc_final_ops(dag)
+        final_ops = calc_final_ops(dag, {"measure", "barrier"})
         if not final_ops:
             return dag
 
diff --git a/releasenotes/notes/add-light-cone-pass-6c56085734512e98.yaml b/releasenotes/notes/add-light-cone-pass-6c56085734512e98.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..0303a9553444fbe61c440a910216df34f59a537d
--- /dev/null
+++ b/releasenotes/notes/add-light-cone-pass-6c56085734512e98.yaml
@@ -0,0 +1,43 @@
+---
+features_transpiler:
+  - |
+    Added a new transpiler pass, :class:`.LightCone` that is used
+    to get the lightcone of a circuit when measuring a subset of
+    qubits or a specific Pauli string.
+    For example if you had a circuit like:
+
+        .. plot::
+
+          from qiskit.transpiler.passes.optimization.light_cone import LightCone
+          from qiskit.transpiler.passmanager import PassManager
+          from qiskit.circuit import QuantumCircuit
+
+          qc = QuantumCircuit(3,1)
+          qc.h(range(3))
+          qc.cx(0,1)
+          qc.cx(2,1)
+          qc.h(range(3))
+          qc.measure(0,0)
+
+          qc.draw("mpl")
+
+    running the pass would eliminate the gates that do not affect the
+    outcome.
+
+        .. plot::
+           :include-source:
+
+            from qiskit.transpiler.passes.optimization.light_cone import LightCone
+            from qiskit.transpiler.passmanager import PassManager
+            from qiskit.circuit import QuantumCircuit
+
+            qc = QuantumCircuit(3,1)
+            qc.h(range(3))
+            qc.cx(0,1)
+            qc.cx(2,1)
+            qc.h(range(3))
+            qc.measure(0,0)
+
+            pm = PassManager([LightCone()])
+            new_circuit = pm.run(qc)
+            new_circuit.draw("mpl")
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/transpiler/test_light_cone.py b/test/python/transpiler/test_light_cone.py
new file mode 100644
index 0000000000000000000000000000000000000000..293bf94a2082845bf69778b2326a030b9e7cd8e5
--- /dev/null
+++ b/test/python/transpiler/test_light_cone.py
@@ -0,0 +1,364 @@
+# This code is part of Qiskit.
+#
+# (C) Copyright IBM 2017, 2019.
+#
+# This code is licensed under the Apache License, Version 2.0. You may
+# obtain a copy of this license in the LICENSE.txt file in the root directory
+# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
+#
+# Any modifications or derivative works of this code must retain this
+# copyright notice, and modified files need to carry a notice indicating
+# that they have been altered from the originals.
+
+"""Test the LightCone pass"""
+
+import unittest
+from test import QiskitTestCase  # pylint: disable=wrong-import-order
+
+import ddt
+
+from qiskit.circuit import (
+    Parameter,
+    QuantumCircuit,
+)
+from qiskit.circuit.library import real_amplitudes
+from qiskit.circuit.library.n_local.efficient_su2 import efficient_su2
+from qiskit.converters import circuit_to_dag
+from qiskit.quantum_info import SparsePauliOp, SparseObservable
+from qiskit.transpiler.passes.optimization.light_cone import LightCone
+from qiskit.transpiler.passmanager import PassManager
+
+
+@ddt.ddt
+class TestLightConePass(QiskitTestCase):
+    """Test the LightCone pass."""
+
+    @ddt.data("X", "Z")
+    def test_nonparameterized_noncommuting(self, pauli_label):
+        """Test for a non-commuting, asymmetric, weight-one Pauli."""
+        bit_terms = pauli_label
+        light_cone = LightCone(bit_terms=bit_terms, indices=[1])
+        pm = PassManager([light_cone])
+
+        qc = QuantumCircuit(2)
+        qc.x(0)
+        qc.s(1)
+        qc.cy(0, 1)
+
+        new_circuit = pm.run(qc)
+
+        expected = qc
+
+        self.assertEqual(expected, new_circuit)
+
+    def test_nonparameterized_commuting(self):
+        """Test for a commuting, asymmetric, weight-one Pauli."""
+        light_cone = LightCone(bit_terms="Y", indices=[1])
+        pm = PassManager([light_cone])
+
+        qc = QuantumCircuit(2)
+        qc.x(0)
+        qc.s(1)
+        qc.cy(0, 1)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(2)
+        expected.s(1)
+
+        self.assertEqual(expected, new_circuit)
+
+    @ddt.data("Y", "Z")
+    def test_parameterized_noncommuting(self, pauli_label):
+        """Test for a non-commuting, asymmetric, weight-one Pauli on a parameterized circuit."""
+        bit_terms = pauli_label
+        light_cone = LightCone(bit_terms=bit_terms, indices=[1])
+        pm = PassManager([light_cone])
+        theta = Parameter("θ")
+
+        qc = QuantumCircuit(2)
+        qc.rx(theta, 0)
+        qc.ry(theta, 1)
+        qc.cx(0, 1)
+
+        new_circuit = pm.run(qc)
+
+        expected = qc
+
+        self.assertEqual(expected, new_circuit)
+
+    def test_parameterized_commuting(self):
+        """Test for a commuting, asymmetric, weight-one Pauli on a parameterized circuit."""
+        bit_terms, indices, _ = SparsePauliOp("XI").to_sparse_list()[0]
+        light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+        pm = PassManager([light_cone])
+        theta = Parameter("θ")
+
+        qc = QuantumCircuit(2)
+        qc.rx(theta, 0)
+        qc.ry(theta, 1)
+        qc.cx(0, 1)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(2)
+        expected.ry(theta, 1)
+
+        self.assertEqual(expected, new_circuit)
+
+    def test_parameterized_symmetric(self):
+        """Test for a double symmetric `Z` observable on a parameterized circuit."""
+        bit_terms, indices, _ = SparsePauliOp("ZIIZ").to_sparse_list()[0]
+        light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+        pm = PassManager([light_cone])
+
+        qc = real_amplitudes(4, entanglement="pairwise", reps=1)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(4)
+        theta = qc.parameters
+        expected.ry(theta[0], 0)
+        expected.ry(theta[1], 1)
+        expected.ry(theta[2], 2)
+        expected.ry(theta[3], 3)
+        expected.cx(0, 1)
+        expected.cx(2, 3)
+        expected.ry(theta[4], 0)
+        expected.ry(theta[7], 3)
+
+        self.assertEqual(expected, new_circuit)
+
+    def test_parameterized_asymmetric(self):
+        """Test for a double asymmetric observable on a parameterized circuit."""
+        bit_terms, indices, _ = SparsePauliOp("IZIX").to_sparse_list()[0]
+        light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+        pm = PassManager([light_cone])
+
+        qc = efficient_su2(4, entanglement="circular", reps=1)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(4)
+        theta = qc.parameters
+        expected.ry(theta[0], 0)
+        expected.ry(theta[1], 1)
+        expected.ry(theta[2], 2)
+        expected.ry(theta[3], 3)
+        expected.rz(theta[4], 0)
+        expected.rz(theta[5], 1)
+        expected.rz(theta[6], 2)
+        expected.rz(theta[7], 3)
+        expected.cx(3, 0)
+        expected.cx(0, 1)
+        expected.cx(1, 2)
+        expected.cx(2, 3)
+        expected.ry(theta[8], 0)
+        expected.ry(theta[10], 2)
+        expected.rz(theta[14], 2)
+
+        self.assertEqual(expected, new_circuit)
+
+    def test_all_commuting(self):
+        """Test for a circuit that fully commutes with an observable."""
+        bit_terms, indices, _ = SparsePauliOp("IIIZ").to_sparse_list()[0]
+        light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+        pm = PassManager([light_cone])
+
+        qc = QuantumCircuit(4)
+        qc.s(0)
+        qc.z(0)
+        qc.h(2)
+        qc.cx(0, 1)
+        qc.cx(2, 3)
+
+        new_circuit = pm.run(qc)
+
+        self.assertEqual(sum(new_circuit.count_ops().values()), 0)
+
+    def test_commuting_block(self):
+        """Test for a commuting block. Currently, gates are checked
+        one by one and commuting blocks are thus ignored."""
+        bit_terms, indices, _ = SparsePauliOp("IIXII").to_sparse_list()[0]
+        light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+        pm = PassManager([light_cone])
+
+        qc = QuantumCircuit(5)
+        qc.cx(2, 1)
+        qc.cx(3, 4)
+        qc.cx(1, 0)
+        qc.cx(2, 3)
+        qc.cx(2, 1)
+        qc.x(1)
+        qc.cx(2, 1)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(5)
+        expected.cx(2, 1)
+        expected.cx(3, 4)
+        expected.cx(1, 0)
+        expected.cx(2, 3)
+        expected.cx(2, 1)
+        expected.cx(2, 1)
+
+        self.assertEqual(expected, new_circuit)
+
+    def test_measurement_barriers(self):
+        """Test for measurement and barriers."""
+        light_cone = LightCone()
+        pm = PassManager([light_cone])
+        theta = Parameter("θ")
+
+        qc = QuantumCircuit(2, 1)
+        qc.rz(theta, 1)
+        qc.ry(theta, 0)
+        qc.barrier()
+        qc.cx(0, 1)
+        qc.barrier()
+        qc.rz(theta, 1)
+        qc.measure(0, 0)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(2, 1)
+        expected.rz(theta, 1)
+        expected.ry(theta, 0)
+        expected.barrier()
+        expected.cx(0, 1)
+        expected.barrier()
+        expected.measure(0, 0)
+
+        self.assertEqual(expected, new_circuit)
+
+    @ddt.data(SparsePauliOp("IX"), SparseObservable("I+"))
+    def test_parameter_expression(self, sparse_object):
+        """Test for Parameter expressions."""
+        bit_terms, indices, _ = sparse_object.to_sparse_list()[0]
+        light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+        pm = PassManager([light_cone])
+        theta = Parameter("θ")
+
+        qc = QuantumCircuit(2)
+        qc.rz(theta + 2, 1)
+        qc.ry(theta - 2, 0)
+        qc.h(1)
+        qc.cz(0, 1)
+        qc.h(1)
+        qc.rz(theta * 2, 1)
+        qc.rz(theta / 2, 1)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(2)
+        expected.rz(theta + 2, 1)
+        expected.ry(theta - 2, 0)
+        expected.h(1)
+        expected.cz(0, 1)
+
+        self.assertEqual(expected, new_circuit)
+
+    @ddt.data(
+        SparsePauliOp.from_sparse_list([("XY", [119, 2], 1)], 120),
+        SparseObservable.from_sparse_list([("-l", [119, 2], 1)], 120),
+    )
+    def test_big_circuit(self, sparse_object):
+        """Test for large circuit and observable."""
+        num_qubits = sparse_object.num_qubits
+        bit_terms, indices, _ = sparse_object.to_sparse_list()[0]
+        light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+        pm = PassManager([light_cone])
+        theta = Parameter("θ")
+
+        qc = QuantumCircuit(num_qubits)
+        for i in range(num_qubits):
+            qc.h(i)
+        for i in range(0, num_qubits, 2):
+            qc.cx(i, i + 1)
+        for i in range(1, num_qubits - 1, 2):
+            qc.cx(i, i + 1)
+        for i in range(num_qubits):
+            qc.rz(theta, i)
+
+        new_circuit = pm.run(qc)
+
+        expected = QuantumCircuit(num_qubits)
+        expected.h(0)
+        expected.h(1)
+        expected.h(2)
+        expected.h(3)
+        expected.h(num_qubits - 2)
+        expected.h(num_qubits - 1)
+        expected.cx(0, 1)
+        expected.cx(2, 3)
+        expected.cx(1, 2)
+        expected.rz(theta, 2)
+        expected.cx(num_qubits - 2, num_qubits - 1)
+        expected.rz(theta, num_qubits - 1)
+
+        self.assertEqual(expected, new_circuit)
+
+    # This test should be uncommented once issue #13828 has been solved.
+    #
+    # @ddt.data(
+    #     SparsePauliOp.from_sparse_list([("IIIIIXZIII", list(range(10)), 1)], 10),
+    #     SparsePauliOp.from_sparse_list([("YYYYXZYYYY", list(range(10)), 1)], 10),
+    # )
+    # def test_large_observable(self, sparse_object):
+    #     """Test for a large initial observable."""
+    #
+    #     bit_terms, indices, _ = sparse_object.to_sparse_list()[0]
+    #     light_cone = LightCone(bit_terms=bit_terms, indices=indices)
+    #     pm = PassManager([light_cone])
+    #
+    #     q0 = QuantumRegister(10, "q0")
+    #     qc = QuantumCircuit(q0)
+    #     qc.cx(5, 6)
+    #
+    #     new_circuit = pm.run(qc)
+    #
+    #     expected = QuantumCircuit(q0)
+    #
+    #     self.assertEqual(expected, new_circuit)
+
+    def test_raise_error_when_indices_is_empty(self):
+        """Test that `ValueError` is raised if bit_terms is given but indices is empty."""
+        with self.assertRaises(
+            ValueError, msg="`indices` must be non-empty when providing `bit_terms`."
+        ):
+            _ = LightCone(bit_terms="X", indices=[])
+
+    def test_raise_error_for_invalid_bit_terms_characters(self):
+        """Test that `ValueError` is raised if `bit_terms` has characters not in `valid_characters`."""
+        with self.assertRaises(
+            ValueError, msg="`bit_terms` should contain only characters in {...}."
+        ):
+            _ = LightCone(bit_terms="AX", indices=[0])  # 'A' is invalid
+
+    def test_raise_error_when_indices_out_of_range(self):
+        """Test that `ValueError` is raised if an index is outside the DAG qubit range."""
+        qc = QuantumCircuit(1)
+        dag = circuit_to_dag(qc)
+
+        light_cone = LightCone(bit_terms="X", indices=[1])  # index 1 doesn't exist
+        with self.assertRaises(
+            ValueError, msg="`indices` contains values outside the qubit range."
+        ):
+            light_cone.run(dag)
+
+    def test_raise_error_when_circuit_measurements_and_observable_present(self):
+        """Test that `ValueError` is raised if the circuit has measurements
+        and `bit_terms` is also given."""
+        qc = QuantumCircuit(1, 1)
+        qc.measure(0, 0)  # A measurement on qubit 0
+        dag = circuit_to_dag(qc)
+
+        light_cone = LightCone(bit_terms="X", indices=[0])
+        with self.assertRaises(
+            ValueError, msg="The circuit contains measurements and an observable has been given"
+        ):
+            light_cone.run(dag)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/test/python/transpiler/test_remove_final_measurements.py b/test/python/transpiler/test_remove_final_measurements.py
index 2cfae3530eb1db777062431f3f9f46cdbb2c1bad..b73853e66fdaab06d57b97dfc0b39a795053d4d0 100644
--- a/test/python/transpiler/test_remove_final_measurements.py
+++ b/test/python/transpiler/test_remove_final_measurements.py
@@ -18,6 +18,7 @@ from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
 from qiskit.circuit.classicalregister import Clbit
 from qiskit.transpiler.passes import RemoveFinalMeasurements
 from qiskit.converters import circuit_to_dag
+from qiskit.transpiler.passes.utils.remove_final_measurements import calc_final_ops
 from test import QiskitTestCase  # pylint: disable=wrong-import-order
 
 
@@ -264,6 +265,45 @@ class TestRemoveFinalMeasurements(QiskitTestCase):
 
         self.assertEqual(dag, expected_dag())
 
+    def test_calc_final_ops(self):
+        """Test method to find the final operations in a circuit."""
+        q0 = QuantumRegister(5, "q0")
+        c0 = ClassicalRegister(1, "c0")
+        c1 = ClassicalRegister(1, "c1")
+        qc = QuantumCircuit(q0, c0, c1)
+
+        #       ┌───┐┌─┐ ░
+        # q0_0: ┤ H ├┤M├─░────
+        #       └┬─┬┘└╥┘ ░
+        # q0_1: ─┤M├──╫──░────
+        #        └╥┘  ║  ░
+        # q0_2: ──╫───╫──░────
+        #         ║   ║  ░ ┌─┐
+        # q0_3: ──╫───╫──░─┤M├
+        #         ║   ║  ░ └╥┘
+        # q0_4: ──╫───╫──░──╫─
+        #         ║   ║  ░  ║
+        # c0: 1/══╩═══╩═════╬═
+        #         0   0     ║
+        # c1: 1/════════════╩═
+        #                   0
+
+        qc.measure(q0[1], c0)
+        qc.h(q0[0])
+        qc.measure(q0[0], c0)
+        qc.barrier()
+        qc.measure(q0[3], c1)
+        final_measurements = [
+            node.qargs for node in calc_final_ops(circuit_to_dag(qc), {"measure"})
+        ]
+        self.assertEqual([(q0[3],)], final_measurements)
+
+        final_measurements_barriers = calc_final_ops(circuit_to_dag(qc), {"measure", "barrier"})
+        self.assertEqual(len(final_measurements_barriers), 4)
+
+        final_barriers = calc_final_ops(circuit_to_dag(qc), {"barrier"})
+        self.assertEqual(final_barriers, [])
+
 
 if __name__ == "__main__":
     unittest.main()
```

## Validation

```json
{
 "test_files": [
  "test/python/transpiler/test_light_cone.py",
  "test/python/transpiler/test_remove_final_measurements.py"
 ],
 "collected_before": 30,
 "collected_after": 28,
 "outcomes_before": {
  "ERROR": 30
 },
 "outcomes_after": {
  "PASSED": 28
 },
 "exit_before": 2,
 "exit_after": 0,
 "tail_before": "have valid Python names.\nTraceback:\n/usr/local/lib/python3.11/importlib/__init__.py:126: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\ntest/python/transpiler/test_light_cone.py:28: in <module>\n    from qiskit.transpiler.passes.optimization.light_cone import LightCone\nE   ModuleNotFoundError: No module named 'qiskit.transpiler.passes.optimization.light_cone'\n__ ERROR collecting test/python/transpiler/test_remove_final_measurements.py ___\nImportError while importing test module '/testbed/test/python/transpiler/test_remove_final_measurements.py'.\nHint: make sure your test modules/packages have valid Python names.\nTraceback:\n/usr/local/lib/python3.11/importlib/__init__.py:126: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\ntest/python/transpiler/test_remove_final_measurements.py:21: in <module>\n    from qiskit.transpiler.passes.utils.remove_final_measurements import calc_final_ops\nE   ImportError: cannot import name 'calc_final_ops' from 'qiskit.transpiler.passes.utils.remove_final_measurements' (/testbed/qiskit/transpiler/passes/utils/remove_final_measurements.py)\n=========================== short test summary info ============================\nERROR test/python/transpiler/test_light_cone.py\nERROR test/python/transpiler/test_remove_final_measurements.py\n!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!\n============================== 2 errors in 2.59s ===============================",
 "tail_after": "s_and_observable_present\nPASSED test/python/transpiler/test_light_cone.py::TestLightConePass::test_raise_error_when_indices_is_empty\nPASSED test/python/transpiler/test_light_cone.py::TestLightConePass::test_raise_error_when_indices_out_of_range\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_calc_final_ops\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_final_barriers_and_measures_complex\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_final_measures_share_dest\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_multi_bit_register_removed_if_all_bits_idle\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_multi_bit_register_removed_with_clbits\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_multi_reg_shared_bits_removed\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_overlapping_register_removal\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_remove_chained_final_measurements\nPASSED test/python/transpiler/test_remove_final_measurements.py::TestRemoveFinalMeasurements::test_remove_clbits_without_register\n======================= 28 passed, 28 warnings in 4.64s ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

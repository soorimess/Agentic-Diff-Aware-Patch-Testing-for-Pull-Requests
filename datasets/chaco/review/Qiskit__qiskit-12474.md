# Qiskit__qiskit-12474

[back to the list](README.md) -- **Add random circuit with graph**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#12474](https://github.com/Qiskit/qiskit/pull/12474) (created 2024-05-29, merged 2025-04-08) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 54 developer test(s) flip; oracle reproduces it |
| base commit | [`b0bc6d8cbebc`](https://github.com/Qiskit/qiskit/commit/b0bc6d8cbebc4e350a472583123f338f3c34b934) (2025-04-07), first parent of the merge commit |
| merge commit | [`45ee089d2346`](https://github.com/Qiskit/qiskit/commit/45ee089d23460ae82fd9478cb76e277325b2954c) |
| issues closed | none |
| version | 2.1 |
| image | `f2p-chaco/qiskit__qiskit-12474:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-12474.Dockerfile) |
| source files (`patch`) | `docs/apidoc/circuit_random.rst`, `docs/apidoc/index.rst`, `qiskit/circuit/__init__.py`, `qiskit/circuit/random/__init__.py`, `qiskit/circuit/random/utils.py`, `releasenotes/notes/Added-random-circuit-from-graph-95c22eeabdea89d0.yaml` |
| test files (`test_patch`) | `test/python/circuit/test_random_circuit.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (54)

- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_large_conditional`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_2and3_qubit_gates_only`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_3and4_qubit_gates_only`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_conditional_reset`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_num_operand_distribution`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_with_zero_distribution`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_depth_0`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_measure`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_mid_circuit_measure_conditional`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_simple_random`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_applied_to_edges_from_interaction_graph_1`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_applied_to_edges_from_interaction_graph_2`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_applied_to_edges_from_interaction_graph_3`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_applied_to_edges_from_interaction_graph_4`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_applied_to_edges_from_interaction_graph_5`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_applied_to_edges_from_interaction_graph_6`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_applied_to_edges_from_interaction_graph_7____0__13__21____1__13__20____1__14__15____2__14__21____3__15__10____4__15__16____4__16__21____5__16__11____6__17__11____7__17__17____7__18__15____8__18__20____0__9__13____3__9__13____5__12__22____8__12__17____10__14__11____10__16__19____11__15__12____11__17__21____0_`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_2q_gates_excluded_edges_with_zero_weight`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_conditionals_on_1q_operation`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_edges_prob`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_edges_weight_with_some_None_raises`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_invalid_interaction_graph`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_max_operands_not_between_1_2_raises`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_min_times_qubit_pair_usage_1`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_min_times_qubit_pair_usage_2`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_min_times_qubit_pair_usage_3`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_min_times_qubit_pair_usage_4`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_min_times_qubit_pair_usage_5`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_min_times_qubit_pair_usage_6`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_min_times_qubit_pair_usage_7____0__13__21____1__13__20____1__14__15____2__14__21____3__15__10____4__15__16____4__16__21____5__16__11____6__17__11____7__17__17____7__18__15____8__18__20____0__9__13____3__9__13____5__12__22____8__12__17____10__14__11____10__16__19____11__15__12____11__17__21____0_`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_negative_edge_weight_raises`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_no_1q_when_insert_1q_oper_is_false`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_raise_no_edges_insert_1q_oper_to_false`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_circuit_conditional_reset_1`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_circuit_conditional_reset_2`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_circuit_conditional_reset_3`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_circuit_conditional_reset_4`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_circuit_conditional_reset_5`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_circuit_conditional_reset_6`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_circuit_conditional_reset_7____0__13__21____1__13__20____1__14__15____2__14__21____3__15__10____4__15__16____4__16__21____5__16__11____6__17__11____7__17__17____7__18__15____8__18__20____0__9__13____3__9__13____5__12__22____8__12__17____10__14__11____10__16__19____11__15__12____11__17__21____0_`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_1`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_2`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_3`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_4`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_5`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_6`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_7____0__13__21____1__13__20____1__14__15____2__14__21____3__15__10____4__15__16____4__16__21____5__16__11____6__17__11____7__17__17____7__18__15____8__18__20____0__9__13____3__9__13____5__12__22____8__12__17____10__14__11____10__16__19____11__15__12____11__17__21____0_`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_1`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_2`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_3`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_4`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_5`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_6`
- `test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_7____0__13__21____1__13__20____1__14__15____2__14__21____3__15__10____4__15__16____4__16__21____5__16__11____6__17__11____7__17__17____7__18__15____8__18__20____0__9__13____3__9__13____5__12__22____8__12__17____10__14__11____10__16__19____11__15__12____11__17__21____0_`

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #12474: Add random circuit with graph

### Summary
The function `qiskit.circuit.random.utils.random_circuit_from_graph` adds a new feature
of generating random circuits with interaction graph.

### Details and comments
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/docs/apidoc/circuit_random.rst b/docs/apidoc/circuit_random.rst
new file mode 100644
index 0000000000000000000000000000000000000000..e0788b72a1f4546195535b9bf47e8f2581da3a39
--- /dev/null
+++ b/docs/apidoc/circuit_random.rst
@@ -0,0 +1,4 @@
+.. automodule:: qiskit.circuit.random
+   :no-members:
+   :no-inherited-members:
+   :no-special-members:
diff --git a/docs/apidoc/index.rst b/docs/apidoc/index.rst
index e8a05c4037fcf37517ab94222c87773cc5577a74..1b89fe0ef270f2a91581997f35f26c04f7620a42 100644
--- a/docs/apidoc/index.rst
+++ b/docs/apidoc/index.rst
@@ -16,6 +16,7 @@ Circuit construction:
    qiskit.circuit.QuantumCircuit
    circuit_classical
    circuit_library
+   circuit_random
    circuit_singleton
 
 Quantum information:
diff --git a/qiskit/circuit/__init__.py b/qiskit/circuit/__init__.py
index f681e80b0d31eb65f748fd9af2fb2bc4b41ea69a..376ed04bfe1f17cf7e7b054efcc56a1e7f5526ec 100644
--- a/qiskit/circuit/__init__.py
+++ b/qiskit/circuit/__init__.py
@@ -306,6 +306,7 @@ assist compilation workflows.  These include:
 There are also utilities for generating random circuits:
 
 * :func:`random.random_circuit`
+* :func:`random.random_circuit_from_graph`
 * :func:`random.random_clifford_circuit`
 
 Finally, the circuit module has its own exception class, to indicate when things went wrong in
@@ -1049,19 +1050,6 @@ default instances of the :class:`.BasisTranslator`.
     :data:`StandardEquivalenceLibrary`.
 
 
-
-Generating random circuits
---------------------------
-
-..
-    If we expand these capabilities in the future, it's probably best to move it to its own
-    module-level documentation page than to expand this "inline" module documentation.
-
-.. currentmodule:: qiskit.circuit.random
-.. autofunction:: random_circuit
-.. autofunction:: random_clifford_circuit
-.. currentmodule:: qiskit.circuit
-
 Apply Pauli twirling to a circuit
 ---------------------------------
 
diff --git a/qiskit/circuit/random/__init__.py b/qiskit/circuit/random/__init__.py
index 06e817bb4de89518aa8422e020e23a97d459c642..19cf8e51ec4559c78e8e59f0ae75267fab357b12 100644
--- a/qiskit/circuit/random/__init__.py
+++ b/qiskit/circuit/random/__init__.py
@@ -10,6 +10,41 @@
 # copyright notice, and modified files need to carry a notice indicating
 # that they have been altered from the originals.
 
-"""Method for generating random circuits."""
+"""
+==============================================
+Random Circuits (:mod:`qiskit.circuit.random`)
+==============================================
 
-from .utils import random_circuit, random_clifford_circuit
+.. currentmodule:: qiskit.circuit.random
+
+Overview
+========
+
+The :mod:`qiskit.circuit.random` module offers functions that can be used for generating 
+arbitrary circuits with gates randomly selected from a given set of gates. 
+
+These circuits can be used for benchmarking existing quantum hardware and estimating 
+the performance of quantum circuit transpilers and software infrastructure.
+The functions below can generate bespoke quantum circuits respecting various properties
+such as number of qubits, depth of the circuit, coupling map, gate set, etc.
+
+Generating arbitrary circuits
+------------------------------------
+
+.. autofunction:: random_circuit
+
+
+Generating arbitrary circuits respecting qubit-coupling
+--------------------------------------------------------------
+
+.. autofunction:: random_circuit_from_graph
+
+
+Generating arbitrary circuits with clifford gates
+--------------------------------------------------------
+
+.. autofunction:: random_clifford_circuit
+
+"""
+
+from .utils import random_circuit, random_clifford_circuit, random_circuit_from_graph
diff --git a/qiskit/circuit/random/utils.py b/qiskit/circuit/random/utils.py
index 808fcab812f777f00be5ae31ac32fa14eb191b9b..02c282d177da6e775c816e861be18b9296850c67 100644
--- a/qiskit/circuit/random/utils.py
+++ b/qiskit/circuit/random/utils.py
@@ -11,15 +11,451 @@
 # that they have been altered from the originals.
 
 """Utility functions for generating random circuits."""
-
 import numpy as np
+from rustworkx import PyDiGraph
 
-from qiskit.circuit import ClassicalRegister, QuantumCircuit, CircuitInstruction
+from qiskit.circuit import (
+    ClassicalRegister,
+    QuantumCircuit,
+    CircuitInstruction,
+)
 from qiskit.circuit import Reset
 from qiskit.circuit.library import standard_gates
 from qiskit.circuit.exceptions import CircuitError
 from qiskit.quantum_info.operators.symplectic.clifford_circuits import _BASIS_1Q, _BASIS_2Q
 
+# (Gate class, number of qubits, number of parameters)
+gates_1q_data = [
+    (standard_gates.IGate, 1, 0),
+    (standard_gates.SXGate, 1, 0),
+    (standard_gates.XGate, 1, 0),
+    (standard_gates.RZGate, 1, 1),
+    (standard_gates.RGate, 1, 2),
+    (standard_gates.HGate, 1, 0),
+    (standard_gates.PhaseGate, 1, 1),
+    (standard_gates.RXGate, 1, 1),
+    (standard_gates.RYGate, 1, 1),
+    (standard_gates.SGate, 1, 0),
+    (standard_gates.SdgGate, 1, 0),
+    (standard_gates.SXdgGate, 1, 0),
+    (standard_gates.TGate, 1, 0),
+    (standard_gates.TdgGate, 1, 0),
+    (standard_gates.UGate, 1, 3),
+    (standard_gates.U1Gate, 1, 1),
+    (standard_gates.U2Gate, 1, 2),
+    (standard_gates.U3Gate, 1, 3),
+    (standard_gates.YGate, 1, 0),
+    (standard_gates.ZGate, 1, 0),
+]
+
+gates_2q_data = [
+    (standard_gates.CXGate, 2, 0),
+    (standard_gates.DCXGate, 2, 0),
+    (standard_gates.CHGate, 2, 0),
+    (standard_gates.CPhaseGate, 2, 1),
+    (standard_gates.CRXGate, 2, 1),
+    (standard_gates.CRYGate, 2, 1),
+    (standard_gates.CRZGate, 2, 1),
+    (standard_gates.CSXGate, 2, 0),
+    (standard_gates.CUGate, 2, 4),
+    (standard_gates.CU1Gate, 2, 1),
+    (standard_gates.CU3Gate, 2, 3),
+    (standard_gates.CYGate, 2, 0),
+    (standard_gates.CZGate, 2, 0),
+    (standard_gates.RXXGate, 2, 1),
+    (standard_gates.RYYGate, 2, 1),
+    (standard_gates.RZZGate, 2, 1),
+    (standard_gates.RZXGate, 2, 1),
+    (standard_gates.XXMinusYYGate, 2, 2),
+    (standard_gates.XXPlusYYGate, 2, 2),
+    (standard_gates.ECRGate, 2, 0),
+    (standard_gates.CSGate, 2, 0),
+    (standard_gates.CSdgGate, 2, 0),
+    (standard_gates.SwapGate, 2, 0),
+    (standard_gates.iSwapGate, 2, 0),
+]
+
+
+def random_circuit_from_graph(
+    interaction_graph,
+    min_2q_gate_per_edge=1,
+    max_operands=2,
+    measure=False,
+    conditional=False,
+    reset=False,
+    seed=None,
+    insert_1q_oper=True,
+    prob_conditional=0.1,
+    prob_reset=0.1,
+):
+    """Generate random circuit of arbitrary size and form which strictly respects the interaction
+    graph passed as argument. Interaction Graph is a graph G=(V, E) where V are the qubits in the
+    circuit, and, E is the set of two-qubit gate interactions between two particular qubits in the
+    circuit.
+
+    This function will generate a random circuit by randomly selecting 1Q and 2Q gates from the set
+    of standard gates in :mod:`qiskit.circuit.library.standard_gates`. The user can attach a numerical
+    value as a metadata to the edge of the graph indicating the edge weight for that particular edge,
+    These edge weights would be normalized to the probabilities of the edges getting selected.
+    If all the edge weights are passed as `None`, then the probability of each qubit-pair of getting
+    selected is set to 1/N, where `N` is the number of edges in the `interaction_graph` passed in,
+    i.e each edge is drawn uniformly. If any weight of an edge is set as zero, that particular
+    edge will not be included in the output circuit.
+
+    Passing a list of tuples of control qubit, target qubit and associated probability is also
+    acceptable as a way to specify an interaction graph.
+
+    If numerical values are present as probabilities but some/any are None, or negative, when
+    `max_operands=2` this will raise a ValueError.
+
+    If `max_operands` is set to 1, then there are no 2Q operations, so no need to take care
+    of the edges, in such case the function will return a circuit from the `random_circuit` function,
+    which would be passed with the `max_operands` as 1.
+
+    If `max_operands` is set to 2, then in every while-iteration 2Q gates are chosen randomly, and
+    qubit-pairs which exist in the input interaction graph are also chosen randomly based on the
+    probability attached to the qubit-pair. Then in a for-iteration 2Q gates are applied to the
+    randomly chosen qubit-pairs with the aim to reach the count of 2Q on any qubit-pair to
+    `min_2q_gate_per_edge` criteria as soon as possible within a particular iteration. Now, if
+    some qubits are still idle after applying 2Q gates for that particular iteration, then randomly
+    chosen 1Q gates are applied to those idle qubits if `insert_1q_oper` is set to True.
+
+    Example:
+
+    .. plot::
+       :alt: Pass in interaction graph and minimum 2Q gate per edge as a bare minimum.
+       :include-source:
+
+       from qiskit.circuit.random.utils import random_circuit_from_graph
+       import rustworkx as rx
+       pydi_graph = rx.PyDiGraph()
+       pydi_graph.add_nodes_from(range(7))
+       cp_map = [(0, 1, 0.18), (1, 2, 0.15), (2, 3, 0.15), (3, 4, 0.22), (4, 5, 0.13), (5, 6, 0.17)]
+       pydi_graph.add_edges_from(cp_map)
+       # cp_map can be passed in directly as interaction_graph
+       qc = random_circuit_from_graph(pydi_graph, min_2q_gate_per_edge=2, seed=12345)
+       qc.draw(output='mpl')
+
+    Args:
+        interaction_graph (PyGraph | PyDiGraph | List[Tuple[int, int, float]]): Interaction Graph
+        min_2q_gate_per_edge (int): Minimum number of times every qubit-pair must be used
+            in the random circuit. (optional, default:1)
+        max_operands (int): maximum qubit operands of each gate(should be 1 or 2)
+            (optional, default:2)
+        measure (bool): if True, measure all qubits at the end. (optional, default: False)
+        conditional (bool): if True, insert middle measurements and conditionals.
+            (optional, default: False)
+        reset (bool): if True, insert middle resets. (optional, default: False)
+        seed (int): sets random seed. (If `None`, a random seed is chosen) (optional)
+        insert_1q_oper (bool): Insert 1Q operations to the circuit. (optional, default: True)
+        prob_conditional (float): Probability less than 1.0, this is used to control the occurrence
+            of conditionals in the circuit. (optional, default: 0.1)
+        prob_reset (float): Probability less than 1.0, this is used to control the occurrence of
+            reset in the circuit. (optional, default: 0.1)
+
+    Returns:
+        QuantumCircuit: constructed circuit
+
+    Raises:
+        CircuitError: When `max_operands` is not 1 or 2.
+        CircuitError: When `max_operands` is set to 1, but no 1Q operations are allowed by setting
+            `insert_1q_oper` to false.
+        CircuitError: When the interaction graph has no edges, so only 1Q gates are possible in
+            the circuit, but `insert_1q_oper` is set to False.
+        CircuitError: When an invalid interaction graph object is passed.
+        ValueError: Given `max_operands=2`, when any edge have probability `None` but not all, or any
+            of the probabilities are negative.
+    """
+
+    # max_operands should be 1 or 2
+    if max_operands not in {1, 2}:
+        raise CircuitError("`max_operands` should be either 1 or 2")
+
+    if max_operands == 1 and not insert_1q_oper:
+        raise CircuitError(
+            "`max_operands` of 1 means only 1Q gates are allowed, but `insert_1q_oper` is False"
+        )
+
+    # Declaring variables so lint doesn't complaint.
+    num_qubits = 0
+    num_edges = None
+    edge_list = None
+    edges_probs = None
+
+    if isinstance(interaction_graph, list):
+        num_edges = len(interaction_graph)
+        edge_list = []
+        edges_probs = []
+        for ctrl, trgt, prob in interaction_graph:
+            edge_list.append((ctrl, trgt))
+            edges_probs.append(prob)
+
+            if ctrl > num_qubits:
+                num_qubits = ctrl
+
+            if trgt > num_qubits:
+                num_qubits = trgt
+
+        num_qubits += 1  # ctrl, trgt are qubit indices.
+        edge_list = np.array(edge_list)
+        edges_probs = np.array(edges_probs)
+    elif isinstance(interaction_graph, PyDiGraph):
+        num_qubits = interaction_graph.num_nodes()
+        num_edges = interaction_graph.num_edges()
+        edge_list = np.array(interaction_graph.edge_list())
+        edges_probs = np.array(interaction_graph.edges())
+    else:
+        raise CircuitError("Invalid interaction graph object has been passed")
+
+    if num_qubits == 0:
+        return QuantumCircuit()
+
+    max_operands = max_operands if num_qubits > max_operands else num_qubits
+
+    if num_edges == 0 and not insert_1q_oper:
+        raise CircuitError(
+            "There are no edges in the `interaction_graph` so, there could be only 1Q gates, "
+            "however `insert_1q_oper` is set to `False`"
+        )
+
+    if num_edges == 0 or max_operands == 1:
+        # If there is no edge then there could be no 2Q operation
+        # or, if only 1Q operations are allowed, then there is no
+        # point in considering edges.
+        return random_circuit(
+            num_qubits=num_qubits,
+            depth=min_2q_gate_per_edge,
+            max_operands=1,
+            measure=measure,
+            conditional=conditional,
+            reset=reset,
+            seed=seed,
+        )
+
+    # If any edge weight is zero, just remove that edge from the edge_list
+    if 0 in edges_probs:
+        _mask = edges_probs != 0
+        edges_probs = edges_probs[_mask]
+        edge_list = edge_list[_mask]
+
+        # Update 'num_edges'
+        num_edges = len(edge_list)
+
+    # Now, zeros are filtered out in above if-block.
+    # Now, If none of the edges_probs are `None`
+    if all(edges_probs):
+
+        # edge weights in interaction_graph must be positive
+        for prob in edges_probs:
+            if prob < 0:
+                raise ValueError("Probabilities cannot be negative")
+
+        # Normalize edge weights if not already normalized.
+        probs_sum = edges_probs.sum()
+        if not np.isclose(probs_sum, 1.000, rtol=0.001):
+            edges_probs = edges_probs / probs_sum
+    # If any of the values of the probability is None, then it would raise an error.
+    elif any(edges_probs):
+        raise ValueError(
+            "Some of the probabilities of a qubit-pair getting selected is `None`"
+            " It should either be all `None` or all positive numerical weights. "
+        )
+
+    # If all edge weights are none, assume the weight of each edge to be 1/N.
+    elif None in edges_probs:
+        edges_probs = np.ones(num_edges) / num_edges
+
+    gates_2q = np.array(
+        gates_2q_data,
+        dtype=[("class", object), ("num_qubits", np.int64), ("num_params", np.int64)],
+    )
+
+    if insert_1q_oper:
+        gates_1q = np.array(gates_1q_data, dtype=gates_2q.dtype)
+
+    qc = QuantumCircuit(num_qubits)
+
+    if measure or conditional:
+        cr = ClassicalRegister(num_qubits, "c")
+        qc.add_register(cr)
+
+    if seed is None:
+        seed = np.random.randint(0, np.iinfo(np.int32).max)
+    rng = np.random.default_rng(seed)
+
+    qubits = np.array(qc.qubits, dtype=object, copy=True)
+
+    edges_used = {tuple(edge): 0 for edge in edge_list}
+
+    # Declaring variables, so that lint doesn't complaint.
+    reset_2q = None
+    cond_val_2q = None
+    cond_val_1q = None
+
+    # If conditional is not required, there is no need to calculate random numbers.
+    # But, since the variables are required in the for-loop so let's get an array of false.
+    if not conditional:
+        cond_1q = np.zeros(num_qubits, dtype=bool)
+        cond_2q = np.zeros(num_edges, dtype=bool)
+
+    # Similarly, if resets are not required, then since, the variable is required
+    # in the for-loop, let's get an array of false.
+    if not reset:
+        reset_2q = np.zeros(num_edges, dtype=bool)
+
+    # This loop will keep on applying gates to qubits until every qubit-pair
+    # has 2Q operations applied at-least `min_2q_gate_per_edge` times.
+    while edges_used:
+
+        # For any given while-iteration, this is a set of qubits not having any 2Q gates.
+        # Qubits in this set will have 1Q gates, if `insert_1q_oper` is True.
+        qubit_idx_idle = set(range(num_qubits))
+
+        # normalized edge weights represent the probability with which each qubit-pair
+        # is inserted into the circuit.
+        edge_choices = rng.choice(
+            edge_list,
+            size=num_edges,
+            replace=True,
+            p=edges_probs,
+        )
+        gate_choices = rng.choice(gates_2q, size=num_edges, replace=True)
+
+        cumsum_params = np.cumsum(gate_choices["num_params"], dtype=np.int64)
+        parameters = rng.uniform(0, 2 * np.pi, size=cumsum_params[-1])
+
+        # If reset is required, then, generating a random boolean matrix of
+        # num_edges x 2, corresponding to probable reset on both control and
+        # target qubits of the edge from the edge_list.
+        if reset:
+            reset_2q = rng.random(size=(num_edges, 2)) < prob_reset
+
+        if conditional:
+            cond_2q = rng.random(size=len(gate_choices)) < prob_conditional
+            cond_val_2q = rng.integers(0, 1 << min(num_qubits, 63), size=np.count_nonzero(cond_2q))
+            clbit_2q_idx = 0
+
+        for gate, num_gate_params, edge, is_cond_2q, is_rst in zip(
+            gate_choices["class"],
+            gate_choices["num_params"],
+            edge_choices,
+            cond_2q,
+            reset_2q,
+        ):
+
+            control_qubit, target_qubit = tuple(edge)
+
+            # For every edge there are two probabilistically generated boolean values corresponding
+            # to control, target qubits of the edge
+            # an idle qubit for a particular iteration on which reset is applied is considered idle.
+
+            if reset:
+                is_rst_control, is_rst_target = is_rst
+                rst_oper = Reset()
+                if is_rst_control:
+                    qc._append(
+                        CircuitInstruction(
+                            operation=rst_oper,
+                            qubits=[qubits[control_qubit]],
+                        )
+                    )
+
+                if is_rst_target:
+                    qc._append(
+                        CircuitInstruction(
+                            operation=rst_oper,
+                            qubits=[qubits[target_qubit]],
+                        )
+                    )
+
+            params = parameters[:num_gate_params]
+            parameters = parameters[num_gate_params:]
+            current_instr = gate(*params)
+
+            if is_cond_2q:
+                qc.measure(qc.qubits, cr)
+                # The condition values are required to be bigints, not Numpy's fixed-width type.
+                with qc.if_test((cr, int(cond_val_2q[clbit_2q_idx]))):
+                    clbit_2q_idx += 1
+                    qc.append(
+                        CircuitInstruction(
+                            operation=current_instr,
+                            qubits=[qubits[control_qubit], qubits[target_qubit]],
+                        )
+                    )
+            else:
+                qc._append(
+                    CircuitInstruction(
+                        operation=current_instr,
+                        qubits=[qubits[control_qubit], qubits[target_qubit]],
+                    )
+                )
+
+            # Removing the qubits that have been applied with 2Q gates from the
+            # set of idle qubits for that while-iteration.
+            qubit_idx_idle = qubit_idx_idle - set(edge)
+
+            # Update the number of occurrences of the edge in the circuit.
+            _temp_edge = (control_qubit, target_qubit)
+            if _temp_edge in edges_used:
+                edges_used[_temp_edge] += 1
+                if edges_used[_temp_edge] >= min_2q_gate_per_edge:
+                    del edges_used[_temp_edge]
+
+        if insert_1q_oper:
+            num_unused_qubits = len(qubit_idx_idle)
+            if not num_unused_qubits == 0:
+
+                # Calculating for conditionals to make even the 1Q operations
+                # probabilistically conditional.
+                if conditional:
+                    cond_1q = rng.random(size=num_unused_qubits) < prob_conditional
+                    cond_val_1q = rng.integers(
+                        0, 1 << min(num_qubits, 63), size=np.count_nonzero(cond_1q)
+                    )
+                    clbit_1q_idx = 0
+
+                # Some extra 1Q Gate in to fill qubits which are still idle for this
+                # particular while iteration.
+                extra_1q_gates = rng.choice(gates_1q, size=num_unused_qubits, replace=True)
+
+                cumsum_params = np.cumsum(extra_1q_gates["num_params"], dtype=np.int64)
+                parameters_1q = rng.uniform(0, 2 * np.pi, size=cumsum_params[-1])
+
+                for gate_1q, num_gate_params, qubit_idx, is_cond_1q in zip(
+                    extra_1q_gates["class"],
+                    extra_1q_gates["num_params"],
+                    qubit_idx_idle,
+                    cond_1q,
+                ):
+                    params_1q = parameters_1q[:num_gate_params]
+                    parameters_1q = parameters_1q[num_gate_params:]
+                    current_instr = gate_1q(*params_1q)
+
+                    if is_cond_1q:
+                        qc.measure(qc.qubits, cr)
+                        # The condition values are required to be bigints, not Numpy's fixed-width type.
+                        with qc.if_test((cr, int(cond_val_1q[clbit_1q_idx]))):
+                            clbit_1q_idx += 1
+                            qc.append(
+                                CircuitInstruction(
+                                    operation=current_instr,
+                                    qubits=[qubits[qubit_idx]],
+                                )
+                            )
+                    else:
+                        qc._append(
+                            CircuitInstruction(
+                                operation=current_instr,
+                                qubits=[qubits[qubit_idx]],
+                            )
+                        )
+
+    if measure:
+        qc.measure(qc.qubits, cr)
+
+    return qc
+
 
 def random_circuit(
     num_qubits,
@@ -97,72 +533,24 @@ def random_circuit(
     if num_qubits == 0:
         return QuantumCircuit()
 
-    gates_1q = [
-        # (Gate class, number of qubits, number of parameters)
-        (standard_gates.IGate, 1, 0),
-        (standard_gates.SXGate, 1, 0),
-        (standard_gates.XGate, 1, 0),
-        (standard_gates.RZGate, 1, 1),
-        (standard_gates.RGate, 1, 2),
-        (standard_gates.HGate, 1, 0),
-        (standard_gates.PhaseGate, 1, 1),
-        (standard_gates.RXGate, 1, 1),
-        (standard_gates.RYGate, 1, 1),
-        (standard_gates.SGate, 1, 0),
-        (standard_gates.SdgGate, 1, 0),
-        (standard_gates.SXdgGate, 1, 0),
-        (standard_gates.TGate, 1, 0),
-        (standard_gates.TdgGate, 1, 0),
-        (standard_gates.UGate, 1, 3),
-        (standard_gates.U1Gate, 1, 1),
-        (standard_gates.U2Gate, 1, 2),
-        (standard_gates.U3Gate, 1, 3),
-        (standard_gates.YGate, 1, 0),
-        (standard_gates.ZGate, 1, 0),
-    ]
-    if reset:
-        gates_1q.append((Reset, 1, 0))
-    gates_2q = [
-        (standard_gates.CXGate, 2, 0),
-        (standard_gates.DCXGate, 2, 0),
-        (standard_gates.CHGate, 2, 0),
-        (standard_gates.CPhaseGate, 2, 1),
-        (standard_gates.CRXGate, 2, 1),
-        (standard_gates.CRYGate, 2, 1),
-        (standard_gates.CRZGate, 2, 1),
-        (standard_gates.CSXGate, 2, 0),
-        (standard_gates.CUGate, 2, 4),
-        (standard_gates.CU1Gate, 2, 1),
-        (standard_gates.CU3Gate, 2, 3),
-        (standard_gates.CYGate, 2, 0),
-        (standard_gates.CZGate, 2, 0),
-        (standard_gates.RXXGate, 2, 1),
-        (standard_gates.RYYGate, 2, 1),
-        (standard_gates.RZZGate, 2, 1),
-        (standard_gates.RZXGate, 2, 1),
-        (standard_gates.XXMinusYYGate, 2, 2),
-        (standard_gates.XXPlusYYGate, 2, 2),
-        (standard_gates.ECRGate, 2, 0),
-        (standard_gates.CSGate, 2, 0),
-        (standard_gates.CSdgGate, 2, 0),
-        (standard_gates.SwapGate, 2, 0),
-        (standard_gates.iSwapGate, 2, 0),
-    ]
     gates_3q = [
         (standard_gates.CCXGate, 3, 0),
         (standard_gates.CSwapGate, 3, 0),
         (standard_gates.CCZGate, 3, 0),
         (standard_gates.RCCXGate, 3, 0),
     ]
+
     gates_4q = [
         (standard_gates.C3SXGate, 4, 0),
         (standard_gates.RC3XGate, 4, 0),
     ]
 
     gates_1q = np.array(
-        gates_1q, dtype=[("class", object), ("num_qubits", np.int64), ("num_params", np.int64)]
+        gates_1q_data + [(Reset, 1, 0)] if reset else gates_1q_data,
+        dtype=[("class", object), ("num_qubits", np.int64), ("num_params", np.int64)],
     )
-    gates_2q = np.array(gates_2q, dtype=gates_1q.dtype)
+
+    gates_2q = np.array(gates_2q_data, dtype=gates_1q.dtype)
     gates_3q = np.array(gates_3q, dtype=gates_1q.dtype)
     gates_4q = np.array(gates_4q, dtype=gates_1q.dtype)
 
@@ -271,12 +659,13 @@ def random_circuit(
                 is_conditional,
             ):
                 operation = gate(*parameters[p_start:p_end])
+
                 if is_cond:
                     qc.measure(qc.qubits, cr)
                     # The condition values are required to be bigints, not Numpy's fixed-width type.
                     with qc.if_test((cr, int(condition_values[c_ptr]))):
                         c_ptr += 1
-                        qc._append(
+                        qc.append(
                             CircuitInstruction(operation=operation, qubits=qubits[q_start:q_end])
                         )
                 else:
diff --git a/releasenotes/notes/Added-random-circuit-from-graph-95c22eeabdea89d0.yaml b/releasenotes/notes/Added-random-circuit-from-graph-95c22eeabdea89d0.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..7703c7430622c26a48654f89ebad8b0b2be2910a
--- /dev/null
+++ b/releasenotes/notes/Added-random-circuit-from-graph-95c22eeabdea89d0.yaml
@@ -0,0 +1,37 @@
+---
+features_circuits:
+  - |
+    Added a function :func:`~qiskit.circuit.random.utils.random_circuit_from_graph` that generates a random circuit that 
+    induces the same interaction graph as the interaction graph specified by `interaction_graph`.
+
+    The probability of randomly drawing an edge from the interaction graph as a two-qubit gate can be set by the 
+    user in the weight attribute of an edge in the input interaction graph. If the user does not set the probability, 
+    each edge is drawn uniformly, i.e. each two-qubit gate represented by an edge in the interaction graph has the 
+    same probability of getting added to the random circuit. If only a subset of edge probabilities are set, 
+    `ValueError` will be raised.
+
+    This is an example where 'cp_map' is a list of edges with some arbitrary weights.
+
+    .. plot::
+      :include-source:
+        
+        from qiskit.circuit.random.utils import random_circuit_from_graph
+        import rustworkx as rx
+        pydi_graph = rx.PyDiGraph()
+        n_q = 5
+        cp_map = [(0, 1, 0.18), (1, 2, 0.15), (2, 3, 0.15), (3, 4, 0.22)]
+        pydi_graph.add_nodes_from(range(n_q))
+        pydi_graph.add_edges_from(cp_map)
+        # cp_map can be passed in directly as interaction_graph
+        qc = random_circuit_from_graph(interaction_graph = pydi_graph,
+          min_2q_gate_per_edge = 1, 
+          max_operands = 2, 
+          measure = True, 
+          conditional = True, 
+          reset = True, 
+          seed = 0, 
+          insert_1q_oper = True, 
+          prob_conditional = 0.21,
+          prob_reset = 0.1)
+        qc.draw(output='mpl')
+
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/circuit/test_random_circuit.py b/test/python/circuit/test_random_circuit.py
index 9e448a3860399da884c0cb24d549e3cd4be8f3b5..ba151913644507e9f205561fe14501db253a3412 100644
--- a/test/python/circuit/test_random_circuit.py
+++ b/test/python/circuit/test_random_circuit.py
@@ -12,10 +12,15 @@
 
 
 """Test random circuit generation utility."""
+from collections import defaultdict
+import rustworkx as rx
 import numpy as np
+import ddt
 from qiskit.circuit import QuantumCircuit, ClassicalRegister, Clbit
 from qiskit.circuit import Measure
+from qiskit.circuit.exceptions import CircuitError
 from qiskit.circuit.random import random_circuit
+from qiskit.circuit.random.utils import random_circuit_from_graph
 from qiskit.converters import circuit_to_dag
 from test import QiskitTestCase  # pylint: disable=wrong-import-order
 
@@ -75,13 +80,14 @@ class TestCircuitRandom(QiskitTestCase):
         circ = random_circuit(num_qubits, depth, conditional=True, seed=16)
         self.assertEqual(circ.width(), 2 * num_qubits)
         op_names = [instruction.operation.name for instruction in circ]
+        self.assertEqual(4, len(op_names))
+
         # Before a condition, there needs to be measurement in all the qubits.
-        self.assertEqual(5, len(op_names))
         self.assertEqual(["measure"] * num_qubits, op_names[1 : 1 + num_qubits])
         conditions = [
             bool(getattr(instruction.operation, "condition", None)) for instruction in circ
         ]
-        self.assertEqual([False, False, False, False, True], conditions)
+        self.assertEqual([False, False, False, True], conditions)
 
     def test_random_circuit_num_operand_distribution(self):
         """Test that num_operand_distribution argument generates gates in correct proportion"""
@@ -160,3 +166,403 @@ class TestCircuitRandom(QiskitTestCase):
         # Testing that there are no 1-qubit gate and 2-qubit in the generated random circuit
         self.assertEqual(gate_type_counter[1], 0.0)
         self.assertEqual(gate_type_counter[2], 0.0)
+
+
+def incomplete_graph(n_nodes):
+    # pylint: disable=missing-function-docstring
+    pydi_graph = rx.generators.directed_complete_graph(n_nodes)
+    pydi_graph.remove_edge(1, 3)
+    return pydi_graph
+
+
+def digraph_with_no_edges(n_nodes):
+    # pylint: disable=missing-function-docstring
+    graph = rx.PyDiGraph()
+    graph.add_nodes_from(range(n_nodes))
+    return graph
+
+
+test_cases = (
+    (rx.generators.directed_cycle_graph(5), 1550),
+    (rx.generators.directed_mesh_graph(4), 87978),
+    # The (almost) fully connected graph.
+    (incomplete_graph(4), 154),
+    (rx.generators.directed_heavy_hex_graph(3), 458),
+    # Sparse connected graph
+    (rx.generators.directed_path_graph(10), 458),
+    # A graph with no edges, should yeild a circuit with no edges,
+    # this means there would be no 2Q gates on that circuit.
+    (digraph_with_no_edges(10), 0),
+    # A list of tuples of control qubit, target qubit, and edge probability
+    # is also acceptable.
+    (
+        [
+            (0, 13, 21),
+            (1, 13, 20),
+            (1, 14, 15),
+            (2, 14, 21),
+            (3, 15, 10),
+            (4, 15, 16),
+            (4, 16, 21),
+            (5, 16, 11),
+            (6, 17, 11),
+            (7, 17, 17),
+            (7, 18, 15),
+            (8, 18, 20),
+            (0, 9, 13),
+            (3, 9, 13),
+            (5, 12, 22),
+            (8, 12, 17),
+            (10, 14, 11),
+            (10, 16, 19),
+            (11, 15, 12),
+            (11, 17, 21),
+        ],
+        0,
+    ),
+)
+
+
+@ddt.ddt
+class TestRandomCircuitFromGraph(QiskitTestCase):
+    """Testing random_circuit_from_graph from
+    qiskit.circuit.random.utils.py"""
+
+    @ddt.data(*test_cases)
+    @ddt.unpack
+    def test_simple_random(self, inter_graph, seed):
+        """Test creating a simple random circuit."""
+        n_nodes = 0
+        if isinstance(inter_graph, list):
+            for ctrl, trgt, _ in inter_graph:
+                if ctrl > n_nodes:
+                    n_nodes = ctrl
+                if trgt > n_nodes:
+                    n_nodes = trgt
+            n_nodes += 1  # ctrl, trgt are qubit indices.
+        else:
+            n_nodes = inter_graph.num_nodes()
+
+        circ = random_circuit_from_graph(interaction_graph=inter_graph, seed=seed)
+
+        self.assertIsInstance(circ, QuantumCircuit)
+        self.assertEqual(circ.width(), n_nodes)
+
+    @ddt.data(*test_cases)
+    @ddt.unpack
+    def test_min_times_qubit_pair_usage(self, inter_graph, seed):
+        """the `min_2q_gate_per_edge` parameter specifies how often each qubit-pair must at
+        least be used in a two-qubit gate before the circuit is returned"""
+
+        freq = 8  # Some arbitrary repetations, don't put 1.
+        qc = random_circuit_from_graph(
+            interaction_graph=inter_graph, min_2q_gate_per_edge=freq, seed=seed
+        )
+        count_register = defaultdict(int)
+
+        for c_instr in qc._data:
+            qubits = c_instr.qubits
+            if len(qubits) == 2:
+                count_register[(qubits[0]._index, qubits[1]._index)] += 1
+
+        for occurrence in count_register.values():
+            self.assertLessEqual(freq, occurrence)
+
+    @ddt.data(*test_cases)
+    @ddt.unpack
+    def test_random_measure(self, inter_graph, seed):
+        """Test random circuit with final measurement."""
+
+        qc = random_circuit_from_graph(interaction_graph=inter_graph, measure=True, seed=seed)
+        self.assertIn("measure", qc.count_ops())
+
+    @ddt.data(*test_cases)
+    @ddt.unpack
+    def test_random_circuit_conditional_reset(self, inter_graph, seed):
+        """Test generating random circuits with conditional and reset."""
+        qc = random_circuit_from_graph(
+            interaction_graph=inter_graph,
+            min_2q_gate_per_edge=2,
+            conditional=True,
+            reset=True,
+            seed=seed,  # Do not change the seed or the args.
+            prob_conditional=0.95,
+            prob_reset=0.50,
+        )
+
+        # Check if reset is applied.
+        self.assertIn("reset", qc.count_ops())
+
+        # Now, checking for conditionals
+        cond_counter = 0
+        for instr in qc:
+            cond = getattr(instr.operation, "_condition", None)
+            if not cond is None:
+                cond_counter += 1
+                break  # even one conditional is enough for the check.
+
+        # See if conditionals are present.
+        self.assertNotEqual(cond_counter, 0)
+
+    @ddt.data(*test_cases)
+    @ddt.unpack
+    def test_2q_gates_applied_to_edges_from_interaction_graph(self, inter_graph, seed):
+        """Test 2Q gates are applied to the qubit-pairs given by the interaction graph supplied"""
+        qc = random_circuit_from_graph(
+            interaction_graph=inter_graph,
+            min_2q_gate_per_edge=2,
+            measure=True,
+            conditional=True,
+            reset=True,
+            seed=seed,  # Do not change the seed or args
+            prob_conditional=0.41,
+            prob_reset=0.50,
+        )
+
+        cp_map = set()
+        edge_list = None
+        if isinstance(inter_graph, list):
+            edge_list = []
+            for ctrl, trgt, _ in inter_graph:
+                edge_list.append((ctrl, trgt))
+        else:
+            edge_list = inter_graph.edge_list()
+
+        for c_instr in qc._data:
+            qubits = c_instr.qubits
+            if len(qubits) == 2:
+                cp_map.update({(qubits[0]._index, qubits[1]._index)})
+
+        # make sure every qubit-pair from the circuit actually present in the edge_list
+        for cp in cp_map:
+            self.assertIn(cp, edge_list)
+
+    def test_2q_gates_excluded_edges_with_zero_weight(self):
+        """Test 2Q gates are not applied to the qubit-pairs given by the interaction graph
+        whose weight is zero"""
+
+        num_qubits = 7
+        pydi_graph = rx.PyDiGraph()
+        pydi_graph.add_nodes_from(range(num_qubits))
+        cp_map = [(0, 1, 10), (1, 2, 11), (2, 3, 0), (3, 4, 9), (4, 5, 12), (5, 6, 13)]
+        pydi_graph.add_edges_from(cp_map)
+
+        qc = random_circuit_from_graph(
+            interaction_graph=pydi_graph,
+        )
+        ckt_cp_mp = set()
+        for c_instr in qc._data:
+            qubits = c_instr.qubits
+            if len(qubits) == 2:
+                ckt_cp_mp.update({(qubits[0]._index, qubits[1]._index)})
+
+        # make sure qubit-pair with zero weight is not present in the edge_list from
+        # the circuit.
+        self.assertFalse((2, 3) in ckt_cp_mp)
+
+    def test_edges_weight_with_some_None_raises(self):
+        """Test if the function raises ValueError, if some of the edge
+        weights are None, but not all."""
+
+        pydi_graph = rx.PyDiGraph()
+        pydi_graph.add_nodes_from(range(5))
+        cp_mp = [(0, 1, None), (1, 2, 54), (2, 3, 23), (3, 4, 32)]
+
+        pydi_graph.add_edges_from(cp_mp)
+        with self.assertRaisesRegex(ValueError, ".getting selected is."):
+            _ = random_circuit_from_graph(
+                interaction_graph=pydi_graph,
+            )
+
+    def test_max_operands_not_between_1_2_raises(self):
+        """Test if the function raises CircuitError when max_operands is not 1 or 2"""
+
+        pydi_graph = rx.PyDiGraph()
+        pydi_graph.add_nodes_from(range(10))
+        with self.assertRaisesRegex(CircuitError, ".should be either."):
+            _ = random_circuit_from_graph(
+                interaction_graph=pydi_graph,
+                min_2q_gate_per_edge=2,
+                max_operands=3,  # This would fail
+            )
+
+    def test_negative_edge_weight_raises(self):
+        """Test if negative edge weights raises ValueError"""
+
+        pydi_graph = rx.PyDiGraph()
+        pydi_graph.add_nodes_from(range(5))
+        cp_mp = [(0, 1, -10), (1, 2, 54), (2, 3, 23), (3, 4, 32)]
+
+        pydi_graph.add_edges_from(cp_mp)
+        with self.assertRaisesRegex(ValueError, "Probabilities cannot be negative"):
+            _ = random_circuit_from_graph(interaction_graph=pydi_graph)
+
+    def test_raise_no_edges_insert_1q_oper_to_false(self):
+        """Test if the function raises CircuitError when no edges are present in the
+        interaction graph, which means there cannot be any 2Q gates, and only
+        1Q gates present in the circuit, but `insert_1q_oper` is set to False"""
+        inter_graph = rx.PyDiGraph()
+        inter_graph.add_nodes_from(range(10))
+        with self.assertRaisesRegex(CircuitError, ".there could be only 1Q gates."):
+            _ = random_circuit_from_graph(
+                interaction_graph=inter_graph,
+                min_2q_gate_per_edge=2,
+                conditional=True,
+                reset=True,
+                seed=0,
+                insert_1q_oper=False,  # This will error out!
+                prob_conditional=0.9,
+                prob_reset=0.9,
+            )
+
+    def test_no_1q_when_insert_1q_oper_is_false(self):
+        """Test no 1Q gates in the circuit, if `insert_1q_oper` is set to False."""
+        num_qubits = 7
+        pydi_graph = rx.PyDiGraph()
+        pydi_graph.add_nodes_from(range(num_qubits))
+        cp_map = [(0, 1, 10), (1, 2, 11), (2, 3, 0), (3, 4, 9), (4, 5, 12), (5, 6, 13)]
+        pydi_graph.add_edges_from(cp_map)
+
+        qc = random_circuit_from_graph(
+            interaction_graph=pydi_graph,
+            min_2q_gate_per_edge=2,
+            measure=True,
+            conditional=True,
+            reset=True,
+            seed=0,
+            insert_1q_oper=False,
+            prob_conditional=0.8,
+            prob_reset=0.6,
+        )
+
+        count_1q = 0
+        count_2q = 0
+
+        for instr in qc:
+            if instr.operation.name in {"measure", "delay", "reset"}:
+                continue
+
+            if instr.operation.num_qubits == 1:
+                count_1q += 1
+            if instr.operation.num_qubits == 2:
+                count_2q += 1
+
+        # 1Q gates should not be there in the circuits.
+        self.assertEqual(count_1q, 0)
+
+        # 2Q gates should be in the circuits.
+        self.assertNotEqual(count_2q, 0)
+
+    def test_conditionals_on_1q_operation(self):
+        """Test if conditionals are present on 1Q operations"""
+
+        num_qubits = 7
+        pydi_graph = rx.PyDiGraph()
+        pydi_graph.add_nodes_from(range(num_qubits))
+        cp_map = [(0, 1, 10), (1, 2, 11), (2, 3, 0), (3, 4, 9), (4, 5, 12), (5, 6, 13)]
+        pydi_graph.add_edges_from(cp_map)
+
+        qc = random_circuit_from_graph(
+            interaction_graph=pydi_graph,
+            min_2q_gate_per_edge=4,
+            measure=True,
+            conditional=True,
+            reset=True,
+            seed=0,
+            prob_conditional=0.91,
+            prob_reset=0.6,
+        )
+
+        cond_counter_1q = 0
+        cond_counter_2q = 0
+
+        for instr in qc:
+            if instr.operation.name in {"measure", "delay", "reset"}:
+                continue
+
+            cond = getattr(instr.operation, "_condition", None)
+            if not cond is None:
+                if instr.operation.num_qubits == 1:
+                    cond_counter_1q += 1
+
+                if instr.operation.num_qubits == 2:
+                    cond_counter_2q += 1
+
+        # Check if conditionals are present on 1Q and 2Q gates.
+        self.assertNotEqual(cond_counter_1q, 0)
+        self.assertNotEqual(cond_counter_2q, 0)
+
+    def test_edges_prob(self):
+        """Test if the probabilities of edges selected from the coupling
+        map is indeed equal to the probabilities supplied with the coupling
+        map, also test if for a sufficiently large circuit all edges in the
+        coupling map is present in the circuit.
+        """
+
+        num_qubits = 3
+        seed = 121
+        h_h_g = rx.generators.directed_heavy_hex_graph(d=num_qubits, bidirectional=False)
+        rng = np.random.default_rng(seed=seed)
+        cp_map_list = []
+        edge_list = h_h_g.edge_list()
+
+        # generating a non-normalized list.
+        list_choices = range(1, 100)  # keep the variance moderately high.
+        random_probs = rng.choice(list_choices, size=len(edge_list)).tolist()
+        sum_probs = sum(random_probs)
+
+        for idx, qubits in enumerate(edge_list):
+            ctrl, trgt = qubits
+            cp_map_list.append((ctrl, trgt, random_probs[idx]))
+
+        h_h_g.clear_edges()
+        h_h_g.add_edges_from(cp_map_list)
+
+        # The choices of probabilities are such that an edge might have a very low
+        # probability of getting selected, so we have to generate a fairly big
+        # circuit to include that edge in the circuit, and achieve the required
+        # probability.
+        qc = random_circuit_from_graph(
+            h_h_g,
+            min_2q_gate_per_edge=10,
+            conditional=True,  # Just making it a bit more challenging.
+            reset=True,
+            seed=seed,
+            insert_1q_oper=False,
+            prob_conditional=0.91,
+            prob_reset=0.50,
+        )
+        edge_count = defaultdict(int)
+
+        for c_instr in qc._data:
+            qubits = c_instr.qubits
+            if len(qubits) == 2:
+                edge_count[(qubits[0]._index, qubits[1]._index)] += 1
+
+        # make sure every qubit-pair from the edge_list is present in the circuit.
+        for ctrl, trgt, _ in cp_map_list:
+            self.assertIn((ctrl, trgt), edge_count)
+
+        edges_norm_qc = {}
+        for edge, prob in edge_count.items():
+            edges_norm_qc[edge] = prob / sum(edge_count.values())
+
+        edges_norm_orig = {}
+        for ctrl, trgt, prob in cp_map_list:
+            edges_norm_orig[(ctrl, trgt)] = prob / sum_probs
+
+        # Check if the probabilities of occurrences of edges in the circuit,
+        # is indeed equal to the probabilities supplied as the edge data in
+        # the interaction graph, upto a given tolerance.
+        prob_deviations = []
+        for edge_orig, prob_orig in edges_norm_orig.items():
+            prob_deviations.append(np.absolute(prob_orig - edges_norm_qc[edge_orig]))
+
+        # Setting 1% tolerance in probabilities.
+        self.assertLess(max(prob_deviations), 0.01)
+
+    def test_invalid_interaction_graph(self):
+        """Test if CircuitError is raised when passed with an invalid interaction graph"""
+        cp_map = [(0, 1, 10), (1, 2, 11), (2, 3, 0), (3, 4, 9), (4, 5, 12), (5, 6, 13)]
+        with self.assertRaisesRegex(CircuitError, ".interaction graph object."):
+            _ = random_circuit_from_graph(tuple(cp_map))  # Tuples are invalid interaction graph
```

## Validation

```json
{
 "test_files": [
  "test/python/circuit/test_random_circuit.py"
 ],
 "collected_before": 55,
 "collected_after": 54,
 "outcomes_before": {
  "ERROR": 55
 },
 "outcomes_after": {
  "PASSED": 54
 },
 "exit_before": 2,
 "exit_after": 0,
 "tail_before": "============================= test session starts ==============================\nplatform linux -- Python 3.11.17, pytest-8.1.2, pluggy-1.5.0 -- /usr/local/bin/python\nhypothesis profile 'default' -> database=DirectoryBasedExampleDatabase(PosixPath('/testbed/.hypothesis/examples'))\nrootdir: /testbed\nconfigfile: pyproject.toml\nplugins: hypothesis-6.130.10\ncollecting ... collected 0 items / 1 error\n\n==================================== ERRORS ====================================\n_________ ERROR collecting test/python/circuit/test_random_circuit.py __________\nImportError while importing test module '/testbed/test/python/circuit/test_random_circuit.py'.\nHint: make sure your test modules/packages have valid Python names.\nTraceback:\n/usr/local/lib/python3.11/importlib/__init__.py:126: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\ntest/python/circuit/test_random_circuit.py:23: in <module>\n    from qiskit.circuit.random.utils import random_circuit_from_graph\nE   ImportError: cannot import name 'random_circuit_from_graph' from 'qiskit.circuit.random.utils' (/testbed/qiskit/circuit/random/utils.py)\n=========================== short test summary info ============================\nERROR test/python/circuit/test_random_circuit.py\n!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!\n=============================== 1 error in 1.60s ===============================",
 "tail_after": "/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_6\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_random_measure_7____0__13__21____1__13__20____1__14__15____2__14__21____3__15__10____4__15__16____4__16__21____5__16__11____6__17__11____7__17__17____7__18__15____8__18__20____0__9__13____3__9__13____5__12__22____8__12__17____10__14__11____10__16__19____11__15__12____11__17__21____0_\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_1\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_2\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_3\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_4\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_5\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_6\nPASSED test/python/circuit/test_random_circuit.py::TestRandomCircuitFromGraph::test_simple_random_7____0__13__21____1__13__20____1__14__15____2__14__21____3__15__10____4__15__16____4__16__21____5__16__11____6__17__11____7__17__17____7__18__15____8__18__20____0__9__13____3__9__13____5__12__22____8__12__17____10__14__11____10__16__19____11__15__12____11__17__21____0_\n============================= 54 passed in 11.38s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

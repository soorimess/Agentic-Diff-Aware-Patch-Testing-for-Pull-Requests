# Qiskit__qiskit-12483

[back to the list](README.md) -- **[unitaryHACK] Controlling the Insertion of Multi-Qubit Gates in the Generation of Random Circuits #12059**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#12483](https://github.com/Qiskit/qiskit/pull/12483) (created 2024-05-31, merged 2024-06-07) |
| ChaCo lists | full, ablation |
| status | **runnable** -- 5 developer test(s) flip; oracle reproduces it |
| base commit | [`d18a74cd4592`](https://github.com/Qiskit/qiskit/commit/d18a74cd45922f4960a9eb90ceef89f9c6c184e5) (2024-06-07), first parent of the merge commit |
| merge commit | [`0b1c8bfd18d4`](https://github.com/Qiskit/qiskit/commit/0b1c8bfd18d422a3bdb5ef3c2c4fff977cdbe390) |
| issues closed | none |
| version | 1.2 |
| image | `f2p-chaco/qiskit__qiskit-12483:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-12483.Dockerfile) |
| source files (`patch`) | `qiskit/circuit/random/utils.py`, `releasenotes/notes/extended-random-circuits-049b67cce39003f4.yaml` |
| test files (`test_patch`) | `test/python/circuit/test_random_circuit.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (5)

- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_2and3_qubit_gates_only`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_3and4_qubit_gates_only`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_num_operand_distribution`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_with_zero_distribution`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_mid_circuit_measure_conditional`

## PASS_TO_PASS (5)

<details><summary>show</summary>

- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_large_conditional`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_conditional_reset`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_depth_0`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_measure`
- `test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_simple_random`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #12483: [unitaryHACK] Controlling the Insertion of Multi-Qubit Gates in the Generation of Random Circuits #12059

This pull request is submitted as a solution for issue #12059.

I have added a feature to the random_circuit() function that will allow users to specify a 'num_operand_distribution' by which thay can control the distribution of 1-qubit, 2-qubit, 3-qubit, and 4-qubit gates in the circuit. Alongwith the code I have also updated the release notes and have included some tests.

Thank you in advance for reviewing.



### Summary



### Details and comments
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/circuit/random/utils.py b/qiskit/circuit/random/utils.py
index fc497a300cba3afc86fe626d596fd960e01da37f..f27cbfbfca88398320c80e475123954e12961601 100644
--- a/qiskit/circuit/random/utils.py
+++ b/qiskit/circuit/random/utils.py
@@ -21,7 +21,14 @@ from qiskit.circuit.exceptions import CircuitError
 
 
 def random_circuit(
-    num_qubits, depth, max_operands=4, measure=False, conditional=False, reset=False, seed=None
+    num_qubits,
+    depth,
+    max_operands=4,
+    measure=False,
+    conditional=False,
+    reset=False,
+    seed=None,
+    num_operand_distribution: dict = None,
 ):
     """Generate random circuit of arbitrary size and form.
 
@@ -44,6 +51,10 @@ def random_circuit(
         conditional (bool): if True, insert middle measurements and conditionals
         reset (bool): if True, insert middle resets
         seed (int): sets random seed (optional)
+        num_operand_distribution (dict): a distribution of gates that specifies the ratio
+        of 1-qubit, 2-qubit, 3-qubit, ..., n-qubit gates in the random circuit. Expect a
+        deviation from the specified ratios that depends on the size of the requested
+        random circuit. (optional)
 
     Returns:
         QuantumCircuit: constructed circuit
@@ -51,11 +62,38 @@ def random_circuit(
     Raises:
         CircuitError: when invalid options given
     """
+    if seed is None:
+        seed = np.random.randint(0, np.iinfo(np.int32).max)
+    rng = np.random.default_rng(seed)
+
+    if num_operand_distribution:
+        if min(num_operand_distribution.keys()) < 1 or max(num_operand_distribution.keys()) > 4:
+            raise CircuitError("'num_operand_distribution' must have keys between 1 and 4")
+        for key, prob in num_operand_distribution.items():
+            if key > num_qubits and prob != 0.0:
+                raise CircuitError(
+                    f"'num_operand_distribution' cannot have {key}-qubit gates"
+                    f" for circuit with {num_qubits} qubits"
+                )
+        num_operand_distribution = dict(sorted(num_operand_distribution.items()))
+
+    if not num_operand_distribution and max_operands:
+        if max_operands < 1 or max_operands > 4:
+            raise CircuitError("max_operands must be between 1 and 4")
+        max_operands = max_operands if num_qubits > max_operands else num_qubits
+        rand_dist = rng.dirichlet(
+            np.ones(max_operands)
+        )  # This will create a random distribution that sums to 1
+        num_operand_distribution = {i + 1: rand_dist[i] for i in range(max_operands)}
+        num_operand_distribution = dict(sorted(num_operand_distribution.items()))
+
+    # Here we will use np.isclose() because very rarely there might be floating
+    # point precision errors
+    if not np.isclose(sum(num_operand_distribution.values()), 1):
+        raise CircuitError("The sum of all the values in 'num_operand_distribution' is not 1.")
+
     if num_qubits == 0:
         return QuantumCircuit()
-    if max_operands < 1 or max_operands > 4:
-        raise CircuitError("max_operands must be between 1 and 4")
-    max_operands = max_operands if num_qubits > max_operands else num_qubits
 
     gates_1q = [
         # (Gate class, number of qubits, number of parameters)
@@ -119,17 +157,26 @@ def random_circuit(
         (standard_gates.RC3XGate, 4, 0),
     ]
 
-    gates = gates_1q.copy()
-    if max_operands >= 2:
-        gates.extend(gates_2q)
-    if max_operands >= 3:
-        gates.extend(gates_3q)
-    if max_operands >= 4:
-        gates.extend(gates_4q)
-    gates = np.array(
-        gates, dtype=[("class", object), ("num_qubits", np.int64), ("num_params", np.int64)]
+    gates_1q = np.array(
+        gates_1q, dtype=[("class", object), ("num_qubits", np.int64), ("num_params", np.int64)]
     )
-    gates_1q = np.array(gates_1q, dtype=gates.dtype)
+    gates_2q = np.array(gates_2q, dtype=gates_1q.dtype)
+    gates_3q = np.array(gates_3q, dtype=gates_1q.dtype)
+    gates_4q = np.array(gates_4q, dtype=gates_1q.dtype)
+
+    all_gate_lists = [gates_1q, gates_2q, gates_3q, gates_4q]
+
+    # Here we will create a list 'gates_to_consider' that will have a
+    # subset of different n-qubit gates and will also create a list for
+    # ratio (or probability) for each gates
+    gates_to_consider = []
+    distribution = []
+    for n_qubits, ratio in num_operand_distribution.items():
+        gate_list = all_gate_lists[n_qubits - 1]
+        gates_to_consider.extend(gate_list)
+        distribution.extend([ratio / len(gate_list)] * len(gate_list))
+
+    gates = np.array(gates_to_consider, dtype=gates_1q.dtype)
 
     qc = QuantumCircuit(num_qubits)
 
@@ -137,29 +184,60 @@ def random_circuit(
         cr = ClassicalRegister(num_qubits, "c")
         qc.add_register(cr)
 
-    if seed is None:
-        seed = np.random.randint(0, np.iinfo(np.int32).max)
-    rng = np.random.default_rng(seed)
-
     qubits = np.array(qc.qubits, dtype=object, copy=True)
 
+    # Counter to keep track of number of different gate types
+    counter = np.zeros(len(all_gate_lists) + 1, dtype=np.int64)
+    total_gates = 0
+
     # Apply arbitrary random operations in layers across all qubits.
     for layer_number in range(depth):
         # We generate all the randomness for the layer in one go, to avoid many separate calls to
         # the randomisation routines, which can be fairly slow.
-
         # This reliably draws too much randomness, but it's less expensive than looping over more
         # calls to the rng. After, trim it down by finding the point when we've used all the qubits.
-        gate_specs = rng.choice(gates, size=len(qubits))
+
+        # Due to the stochastic nature of generating a random circuit, the resulting ratios
+        # may not precisely match the specified values from `num_operand_distribution`. Expect
+        # greater deviations from the target ratios in quantum circuits with fewer qubits and
+        # shallower depths, and smaller deviations in larger and deeper quantum circuits.
+        # For more information on how the distribution changes with number of qubits and depth
+        # refer to the pull request #12483 on Qiskit GitHub.
+
+        gate_specs = rng.choice(gates, size=len(qubits), p=distribution)
         cumulative_qubits = np.cumsum(gate_specs["num_qubits"], dtype=np.int64)
+
         # Efficiently find the point in the list where the total gates would use as many as
         # possible of, but not more than, the number of qubits in the layer.  If there's slack, fill
         # it with 1q gates.
         max_index = np.searchsorted(cumulative_qubits, num_qubits, side="right")
         gate_specs = gate_specs[:max_index]
+
         slack = num_qubits - cumulative_qubits[max_index - 1]
-        if slack:
-            gate_specs = np.hstack((gate_specs, rng.choice(gates_1q, size=slack)))
+
+        # Updating the counter for 1-qubit, 2-qubit, 3-qubit and 4-qubit gates
+        gate_qubits = gate_specs["num_qubits"]
+        counter += np.bincount(gate_qubits, minlength=len(all_gate_lists) + 1)
+
+        total_gates += len(gate_specs)
+
+        # Slack handling loop, this loop will add gates to fill
+        # the slack while respecting the 'num_operand_distribution'
+        while slack > 0:
+            gate_added_flag = False
+
+            for key, dist in sorted(num_operand_distribution.items(), reverse=True):
+                if slack >= key and counter[key] / total_gates < dist:
+                    gate_to_add = np.array(
+                        all_gate_lists[key - 1][rng.integers(0, len(all_gate_lists[key - 1]))]
+                    )
+                    gate_specs = np.hstack((gate_specs, gate_to_add))
+                    counter[key] += 1
+                    total_gates += 1
+                    slack -= key
+                    gate_added_flag = True
+            if not gate_added_flag:
+                break
 
         # For efficiency in the Python loop, this uses Numpy vectorisation to pre-calculate the
         # indices into the lists of qubits and parameters for every gate, and then suitably
@@ -202,7 +280,6 @@ def random_circuit(
             ):
                 operation = gate(*parameters[p_start:p_end])
                 qc._append(CircuitInstruction(operation=operation, qubits=qubits[q_start:q_end]))
-
     if measure:
         qc.measure(qc.qubits, cr)
 
diff --git a/releasenotes/notes/extended-random-circuits-049b67cce39003f4.yaml b/releasenotes/notes/extended-random-circuits-049b67cce39003f4.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..f4bb585053bc441a9fb8375637ec4deb0cc4fa92
--- /dev/null
+++ b/releasenotes/notes/extended-random-circuits-049b67cce39003f4.yaml
@@ -0,0 +1,21 @@
+---
+features_circuits:
+  - |
+    The `random_circuit` function from `qiskit.circuit.random.utils` has a new feature where
+    users can specify a distribution `num_operand_distribution` (a dict) that specifies the
+    ratio of 1-qubit, 2-qubit, 3-qubit, and 4-qubit gates in the random circuit. For example,
+    if `num_operand_distribution = {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}` is passed to the function
+    then the generated circuit will have approximately 25% of 1-qubit, 2-qubit, 3-qubit, and
+    4-qubit gates (The order in which the dictionary is passed does not matter i.e. you can specify
+    `num_operand_distribution = {3: 0.5, 1: 0.0, 4: 0.3, 2: 0.2}` and the function will still work
+    as expected). Also it should be noted that the if `num_operand_distribution` is not specified
+    then `max_operands` will default to 4 and a random circuit with a random gate distribution will 
+    be generated. If both `num_operand_distribution` and `max_operands` are specified at the same 
+    time then `num_operand_distribution` will be used to generate the random circuit.
+    Example usage::
+
+           from qiskit.circuit.random import random_circuit
+
+           circ = random_circuit(num_qubits=6, depth=5, num_operand_distribution = {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25})
+           circ.draw(output='mpl')
+
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/circuit/test_random_circuit.py b/test/python/circuit/test_random_circuit.py
index deadcd09d692c0ac111e83d3d4d5373e7cb708a4..ebbdfd28d6482132d63719a801ab6a3901fa9319 100644
--- a/test/python/circuit/test_random_circuit.py
+++ b/test/python/circuit/test_random_circuit.py
@@ -12,6 +12,7 @@
 
 
 """Test random circuit generation utility."""
+import numpy as np
 from qiskit.circuit import QuantumCircuit, ClassicalRegister, Clbit
 from qiskit.circuit import Measure
 from qiskit.circuit.random import random_circuit
@@ -71,7 +72,7 @@ class TestCircuitRandom(QiskitTestCase):
     def test_random_mid_circuit_measure_conditional(self):
         """Test random circuit with mid-circuit measurements for conditionals."""
         num_qubits = depth = 2
-        circ = random_circuit(num_qubits, depth, conditional=True, seed=4)
+        circ = random_circuit(num_qubits, depth, conditional=True, seed=16)
         self.assertEqual(circ.width(), 2 * num_qubits)
         op_names = [instruction.operation.name for instruction in circ]
         # Before a condition, there needs to be measurement in all the qubits.
@@ -81,3 +82,81 @@ class TestCircuitRandom(QiskitTestCase):
             bool(getattr(instruction.operation, "condition", None)) for instruction in circ
         ]
         self.assertEqual([False, False, False, True], conditions)
+
+    def test_random_circuit_num_operand_distribution(self):
+        """Test that num_operand_distribution argument generates gates in correct proportion"""
+        num_qubits = 50
+        depth = 300
+        num_op_dist = {2: 0.25, 3: 0.25, 1: 0.25, 4: 0.25}
+        circ = random_circuit(
+            num_qubits, depth, num_operand_distribution=num_op_dist, seed=123456789
+        )
+        total_gates = circ.size()
+        self.assertEqual(circ.width(), num_qubits)
+        self.assertEqual(circ.depth(), depth)
+        gate_qubits = [instruction.operation.num_qubits for instruction in circ]
+        gate_type_counter = np.bincount(gate_qubits, minlength=5)
+        for gate_type, prob in sorted(num_op_dist.items()):
+            self.assertAlmostEqual(prob, gate_type_counter[gate_type] / total_gates, delta=0.1)
+
+    def test_random_circuit_2and3_qubit_gates_only(self):
+        """
+        Test that the generated random circuit only has 2 and 3 qubit gates,
+        while disallowing 1-qubit and 4-qubit gates if
+        num_operand_distribution = {2: some_prob, 3: some_prob}
+        """
+        num_qubits = 10
+        depth = 200
+        num_op_dist = {2: 0.5, 3: 0.5}
+        circ = random_circuit(num_qubits, depth, num_operand_distribution=num_op_dist, seed=200)
+        total_gates = circ.size()
+        gate_qubits = [instruction.operation.num_qubits for instruction in circ]
+        gate_type_counter = np.bincount(gate_qubits, minlength=5)
+        # Testing that the distribution of 2 and 3 qubit gate matches with given distribution
+        for gate_type, prob in sorted(num_op_dist.items()):
+            self.assertAlmostEqual(prob, gate_type_counter[gate_type] / total_gates, delta=0.1)
+        # Testing that there are no 1-qubit gate and 4-qubit in the generated random circuit
+        self.assertEqual(gate_type_counter[1], 0.0)
+        self.assertEqual(gate_type_counter[4], 0.0)
+
+    def test_random_circuit_3and4_qubit_gates_only(self):
+        """
+        Test that the generated random circuit only has 3 and 4 qubit gates,
+        while disallowing 1-qubit and 2-qubit gates if
+        num_operand_distribution = {3: some_prob, 4: some_prob}
+        """
+        num_qubits = 10
+        depth = 200
+        num_op_dist = {3: 0.5, 4: 0.5}
+        circ = random_circuit(
+            num_qubits, depth, num_operand_distribution=num_op_dist, seed=11111111
+        )
+        total_gates = circ.size()
+        gate_qubits = [instruction.operation.num_qubits for instruction in circ]
+        gate_type_counter = np.bincount(gate_qubits, minlength=5)
+        # Testing that the distribution of 3 and 4 qubit gate matches with given distribution
+        for gate_type, prob in sorted(num_op_dist.items()):
+            self.assertAlmostEqual(prob, gate_type_counter[gate_type] / total_gates, delta=0.1)
+        # Testing that there are no 1-qubit gate and 2-qubit in the generated random circuit
+        self.assertEqual(gate_type_counter[1], 0.0)
+        self.assertEqual(gate_type_counter[2], 0.0)
+
+    def test_random_circuit_with_zero_distribution(self):
+        """
+        Test that the generated random circuit only has 3 and 4 qubit gates,
+        while disallowing 1-qubit and 2-qubit gates if
+        num_operand_distribution = {1: 0.0, 2: 0.0, 3: some_prob, 4: some_prob}
+        """
+        num_qubits = 10
+        depth = 200
+        num_op_dist = {1: 0.0, 2: 0.0, 3: 0.5, 4: 0.5}
+        circ = random_circuit(num_qubits, depth, num_operand_distribution=num_op_dist, seed=12)
+        total_gates = circ.size()
+        gate_qubits = [instruction.operation.num_qubits for instruction in circ]
+        gate_type_counter = np.bincount(gate_qubits, minlength=5)
+        # Testing that the distribution of 3 and 4 qubit gate matches with given distribution
+        for gate_type, prob in sorted(num_op_dist.items()):
+            self.assertAlmostEqual(prob, gate_type_counter[gate_type] / total_gates, delta=0.1)
+        # Testing that there are no 1-qubit gate and 2-qubit in the generated random circuit
+        self.assertEqual(gate_type_counter[1], 0.0)
+        self.assertEqual(gate_type_counter[2], 0.0)
```

## Validation

```json
{
 "test_files": [
  "test/python/circuit/test_random_circuit.py"
 ],
 "collected_before": 10,
 "collected_after": 10,
 "outcomes_before": {
  "PASSED": 5,
  "FAILED": 5
 },
 "outcomes_after": {
  "PASSED": 10
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "se.py\", line 873, in assertEqual\n    assertion_func(first, second, msg=msg)\n  File \"/usr/local/lib/python3.11/unittest/case.py\", line 866, in _baseAssertEqual\n    raise self.failureException(msg)\nAssertionError: 4 != 5\n\n==================================== PASSES ====================================\n=========================== short test summary info ============================\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_large_conditional\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_conditional_reset\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_depth_0\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_measure\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_simple_random\nFAILED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_2and3_qubit_gates_only\nFAILED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_3and4_qubit_gates_only\nFAILED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_num_operand_distribution\nFAILED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_with_zero_distribution\nFAILED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_mid_circuit_measure_conditional\n========================= 5 failed, 5 passed in 2.30s ==========================",
 "tail_after": "]\ntest/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_mid_circuit_measure_conditional PASSED [ 90%]\ntest/python/circuit/test_random_circuit.py::TestCircuitRandom::test_simple_random PASSED [100%]\n\n==================================== PASSES ====================================\n=========================== short test summary info ============================\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_large_conditional\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_2and3_qubit_gates_only\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_3and4_qubit_gates_only\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_conditional_reset\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_num_operand_distribution\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_circuit_with_zero_distribution\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_depth_0\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_measure\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_random_mid_circuit_measure_conditional\nPASSED test/python/circuit/test_random_circuit.py::TestCircuitRandom::test_simple_random\n============================== 10 passed in 1.63s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

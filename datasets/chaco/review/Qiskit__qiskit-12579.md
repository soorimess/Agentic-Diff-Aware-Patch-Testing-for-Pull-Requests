# Qiskit__qiskit-12579

[back to the list](README.md) -- **Fix some bugs in loading Solovay Kitaev decompositions**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#12579](https://github.com/Qiskit/qiskit/pull/12579) (created 2024-06-14, merged 2024-06-26) |
| ChaCo lists | full, ablation, f2p30 |
| status | **runnable** -- 1 developer test(s) flip; oracle reproduces it |
| base commit | [`1ed5951a98b5`](https://github.com/Qiskit/qiskit/commit/1ed5951a98b594808525c8428e06178c160cfcbb) (2024-06-25), first parent of the merge commit |
| merge commit | [`6974b4500f6c`](https://github.com/Qiskit/qiskit/commit/6974b4500f6c716b407b599e5cec80afbb757516) |
| issues closed | [#12576](https://github.com/Qiskit/qiskit/issues/12576) |
| version | 1.2 |
| image | `f2p-chaco/qiskit__qiskit-12579:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-12579.Dockerfile) |
| source files (`patch`) | `qiskit/synthesis/discrete_basis/generate_basis_approximations.py`, `qiskit/synthesis/discrete_basis/solovay_kitaev.py`, `releasenotes/notes/fix-sk-load-from-file-02c6eabbbd7fcda3.yaml` |
| test files (`test_patch`) | `test/python/transpiler/test_solovay_kitaev.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (1)

- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_load_from_file`

## PASS_TO_PASS (33)

<details><summary>show</summary>

- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_adjoint`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_append`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_copy`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_dot`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_eq`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_from_invalid_matrix`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_from_so3_matrix`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_from_su2_matrix`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_getitem`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_len_1_0`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_len_2_1`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_len_3_10`
- `test/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_to_circuit`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_approximation_on_qft`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_exact_decomposition_acts_trivially`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_fails_with_no_to_matrix`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_generating_default_approximation`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_i_returns_empty_circuit`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_plugin`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_str_basis_gates`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_u_gates_work`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_unitary_synthesis`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_1`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_2`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_3`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_4`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_5`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_1`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_2`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_3`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_4`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_5`
- `test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_generate_basis_approximation_gates`

</details>

## Problem statement (what the agent may be shown)

````text
Issue #12576: Solovay Kitaev Decomposition doesn't correctly load saved approximations from file

### Environment

- **Qiskit version**: 1.1.0
- **Python version**: 3.10.11
- **Operating system**: Windows 11 23H2
- **Numpy version**: 1.26.4

### What is happening?

After specifying a file to save the approximations of `generate_basic_approximations` into, attempting to load this into a new `SolovayKitaevDecomposition` gives a runtime error.

This is somewhat easily fixable by replacing [this line](https://github.com/Qiskit/qiskit/blob/03aeee81fefb2f915a82ceee37d64971eadbf6f0/qiskit/synthesis/discrete_basis/solovay_kitaev.py#L80) with the following temporary fix:
```py
        for gatestring, matrix in data.flat[0].items():
```
After this, the `SolovayKitaevDecomposition` object can be instantiated, but still contains a separate logic error. Some inputs can cause the circuits generated by this object to have different global phases than the ones generated by a `SolovayKitaevDecomposition` which did not load these approximations from a file (see example).

### How can we reproduce the issue?

## Minimal Example
```py
from qiskit.synthesis.discrete_basis.solovay_kitaev import (
    SolovayKitaevDecomposition,
)
from qiskit.synthesis.discrete_basis import generate_basic_approximations

import numpy as np
from qiskit.synthesis.discrete_basis.gate_sequence import (
    _convert_so3_to_su2,
)

generate_basic_approximations(["t", "tdg", "h"], 10, "test.npy")
sk = SolovayKitaevDecomposition()
sk_file = SolovayKitaevDecomposition("test.npy")
# first issue occurs on line above

rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])

qc = sk.run(_convert_so3_to_su2(rotation), 2)
qc_file = sk_file.run(_convert_so3_to_su2(rotation), 2)

print(f"{qc.global_phase = }")
print(f"{qc_file.global_phase = }")

print(f"qc =\n{qc.draw()}")
print(f"qc_file =\n{qc_file.draw()}")
```
## Output
### Runtime Error on loading file
```
Traceback (most recent call last):
  File "[omitted]\saved_approximations.py", line 13, in <module>
    sk_file = SolovayKitaevDecomposition("test.npy")    
  File "[omitted]\env\lib\site-packages\qiskit\synthesis\discrete_basis\solovay_kitaev.py", line 54, in __init__
    self.basic_approximations = self.load_basic_approximations(basic_approximations)
  File "[omitted]\env\lib\site-packages\qiskit\synthesis\discrete_basis\solovay_kitaev.py", line 80, in load_basic_approximations
    for gatestring, matrix in data.items():
AttributeError: 'numpy.ndarray' object has no attribute 'items'. Did you mean: 'item'?
```
### After Runtime Error Fix
```
qc.global_phase = 3.141592653589793
qc_file.global_phase = 0.0
qc =
global phase: π
   ┌───┐┌───┐┌───┐┌───┐┌───┐
q: ┤ H ├┤ T ├┤ T ├┤ T ├┤ T ├
   └───┘└───┘└───┘└───┘└───┘
qc_file =
   ┌───┐┌───┐┌───┐┌───┐┌───┐
q: ┤ H ├┤ T ├┤ T ├┤ T ├┤ T ├
   └───┘└───┘└───┘└───┘└───┘ 
```

### What should happen?

The circuit created using the `SolovayKitaevDecomposition` created with saved approximations (`qc_file`) should behave the same as the one without (`qc`) - they should both give the same result gates and global phase, as well as run without runtime errors.

### Any suggestions?

- The temporary fix for the `AttributeError` issue should probably not be used (or at least checked before used). On my system, at least, the value of `data` at line 79 in `solovay_kitaev.py` is a 0 dimensional `np.ndarray` containing the object loaded from the file. I am not sure whether this is consistent on other systems or numpy versions.
  - Also, `data.size` is not checked in this one-line solution, so there could be some sort of security vulnerability if this is used.
- It seems that only the gates and product are saved into the file ([source code here](https://github.com/Qiskit/qiskit/blob/03aeee81fefb2f915a82ceee37d64971eadbf6f0/qiskit/synthesis/discrete_basis/generate_basis_approximations.py#L157)). It is also mentioned explicitly in the [constructor docstring of `SolovayKitaevDecomposition`](https://github.com/Qiskit/qiskit/blob/03aeee81fefb2f915a82ceee37d64971eadbf6f0/qiskit/synthesis/discrete_basis/solovay_kitaev.py#L46), so I'm unsure if this is intentional. If not and this needs to be changed, this documentation should also be updated.

---

Pull request #12579: Fix some bugs in loading Solovay Kitaev decompositions

### Summary

Fixes #12576 and some other small bugs in storing & loading basic approximations for the Solovay Kitaev algorithm.

### Details and comments

* as #12576 mentioned, there is a missing `.item()` unwrapping when loading the dictionary from the `npy` file
* reloading the gate sequence also missed the correct `labels` and `global_phase`
* a test is now checking all of the above works correctly
````

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/synthesis/discrete_basis/generate_basis_approximations.py b/qiskit/synthesis/discrete_basis/generate_basis_approximations.py
index 672d0eb9e8efbfb06d231ceabff7542170b92161..da9708c245594fe9ecdd55725217468e25364d50 100644
--- a/qiskit/synthesis/discrete_basis/generate_basis_approximations.py
+++ b/qiskit/synthesis/discrete_basis/generate_basis_approximations.py
@@ -156,7 +156,7 @@ def generate_basic_approximations(
         data = {}
         for sequence in sequences:
             gatestring = sequence.name
-            data[gatestring] = sequence.product
+            data[gatestring] = (sequence.product, sequence.global_phase)
 
         np.save(filename, data)
 
diff --git a/qiskit/synthesis/discrete_basis/solovay_kitaev.py b/qiskit/synthesis/discrete_basis/solovay_kitaev.py
index 2c8df5bd1b6d73985fe54ce7d34425963ca3e2b4..f367f6c0f0b5ba7a55c4d0376cc9cbe898433d44 100644
--- a/qiskit/synthesis/discrete_basis/solovay_kitaev.py
+++ b/qiskit/synthesis/discrete_basis/solovay_kitaev.py
@@ -51,14 +51,19 @@ class SolovayKitaevDecomposition:
 
         self.basic_approximations = self.load_basic_approximations(basic_approximations)
 
-    def load_basic_approximations(self, data: list | str | dict) -> list[GateSequence]:
+    @staticmethod
+    def load_basic_approximations(data: list | str | dict) -> list[GateSequence]:
         """Load basic approximations.
 
         Args:
             data: If a string, specifies the path to the file from where to load the data.
-                If a dictionary, directly specifies the decompositions as ``{gates: matrix}``.
-                There ``gates`` are the names of the gates producing the SO(3) matrix ``matrix``,
-                e.g. ``{"h t": np.array([[0, 0.7071, -0.7071], [0, -0.7071, -0.7071], [-1, 0, 0]]}``.
+                If a dictionary, directly specifies the decompositions as ``{gates: matrix}``
+                or ``{gates: (matrix, global_phase)}``. There, ``gates`` are the names of the gates
+                producing the SO(3) matrix ``matrix``, e.g.
+                ``{"h t": np.array([[0, 0.7071, -0.7071], [0, -0.7071, -0.7071], [-1, 0, 0]]}``
+                and the ``global_phase`` can be given to account for a global phase difference
+                between the U(2) matrix of the quantum gates and the stored SO(3) matrix.
+                If not given, the ``global_phase`` will be assumed to be 0.
 
         Returns:
             A list of basic approximations as type ``GateSequence``.
@@ -72,13 +77,20 @@ class SolovayKitaevDecomposition:
 
         # if a file, load the dictionary
         if isinstance(data, str):
-            data = np.load(data, allow_pickle=True)
+            data = np.load(data, allow_pickle=True).item()
 
         sequences = []
-        for gatestring, matrix in data.items():
+        for gatestring, matrix_and_phase in data.items():
+            if isinstance(matrix_and_phase, tuple):
+                matrix, global_phase = matrix_and_phase
+            else:
+                matrix, global_phase = matrix_and_phase, 0
+
             sequence = GateSequence()
             sequence.gates = [_1q_gates[element] for element in gatestring.split()]
+            sequence.labels = [gate.name for gate in sequence.gates]
             sequence.product = np.asarray(matrix)
+            sequence.global_phase = global_phase
             sequences.append(sequence)
 
         return sequences
diff --git a/releasenotes/notes/fix-sk-load-from-file-02c6eabbbd7fcda3.yaml b/releasenotes/notes/fix-sk-load-from-file-02c6eabbbd7fcda3.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..d995af06bccbf29872d0db319207945ec89644a4
--- /dev/null
+++ b/releasenotes/notes/fix-sk-load-from-file-02c6eabbbd7fcda3.yaml
@@ -0,0 +1,10 @@
+---
+fixes:
+  - |
+    Fix the :class:`.SolovayKitaev` transpiler pass when loading basic
+    approximations from an exising ``.npy`` file. Previously, loading
+    a stored approximation which allowed for further reductions (e.g. due
+    to gate cancellations) could cause a runtime failure.
+    Additionally, the global phase difference of the U(2) gate product
+    and SO(3) representation was lost during a save-reload procedure.
+    Fixes `Qiskit/qiskit#12576 <https://github.com/Qiskit/qiskit/issues/12576>`_.
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/transpiler/test_solovay_kitaev.py b/test/python/transpiler/test_solovay_kitaev.py
index e15a080f6f0324f9d9ebc22195c141c9fc8e9a26..62b811c8e3bd8c8febd3c867d728c57837d3d7d8 100644
--- a/test/python/transpiler/test_solovay_kitaev.py
+++ b/test/python/transpiler/test_solovay_kitaev.py
@@ -12,8 +12,10 @@
 
 """Test the Solovay Kitaev transpilation pass."""
 
+import os
 import unittest
 import math
+import tempfile
 import numpy as np
 import scipy
 
@@ -230,6 +232,35 @@ class TestSolovayKitaev(QiskitTestCase):
         included_gates = set(discretized.count_ops().keys())
         self.assertEqual(set(basis_gates), included_gates)
 
+    def test_load_from_file(self):
+        """Test loading basic approximations from a file works.
+
+        Regression test of Qiskit/qiskit#12576.
+        """
+        filename = "approximations.npy"
+
+        with tempfile.TemporaryDirectory() as tmp_dir:
+            fullpath = os.path.join(tmp_dir, filename)
+
+            # dump approximations to file
+            generate_basic_approximations(basis_gates=["h", "s", "sdg"], depth=3, filename=fullpath)
+
+            # circuit to decompose and reference decomp
+            circuit = QuantumCircuit(1)
+            circuit.rx(0.8, 0)
+
+            reference = QuantumCircuit(1, global_phase=3 * np.pi / 4)
+            reference.h(0)
+            reference.s(0)
+            reference.h(0)
+
+            # load the decomp and compare to reference
+            skd = SolovayKitaev(basic_approximations=fullpath)
+            # skd = SolovayKitaev(basic_approximations=filename)
+            discretized = skd(circuit)
+
+        self.assertEqual(discretized, reference)
+
 
 @ddt
 class TestGateSequence(QiskitTestCase):
```

## Validation

```json
{
 "image_head": "1ed5951a98b594808525c8428e06178c160cfcbb",
 "patch_applies": true,
 "test_files": [
  "test/python/transpiler/test_solovay_kitaev.py"
 ],
 "collected_before": 34,
 "collected_after": 34,
 "outcomes_before": {
  "PASSED": 33,
  "FAILED": 1
 },
 "outcomes_after": {
  "PASSED": 34
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "on/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_1\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_2\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_3\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_4\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_5\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_1\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_2\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_3\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_4\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_5\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_generate_basis_approximation_gates\nFAILED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaev::test_load_from_file\n================== 1 failed, 33 passed, 11 warnings in 55.01s ==================",
 "tail_after": "/python/transpiler/test_solovay_kitaev.py::TestGateSequence::test_to_circuit\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_1\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_2\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_3\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_4\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_decomposes_correctly_5\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_1\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_2\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_3\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_4\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_commutator_decompose_return_type_5\nPASSED test/python/transpiler/test_solovay_kitaev.py::TestSolovayKitaevUtils::test_generate_basis_approximation_gates\n================== 34 passed, 11 warnings in 63.13s (0:01:03) ==================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

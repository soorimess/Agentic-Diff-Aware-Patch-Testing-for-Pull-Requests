# Qiskit__qiskit-13624

[back to the list](README.md) -- **Fix phase of `pauli_list.insert(..., qubit=True)` for length-1 `pauli_list`**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#13624](https://github.com/Qiskit/qiskit/pull/13624) (created 2025-01-08, merged 2025-01-08) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 1 developer test(s) flip; oracle reproduces it |
| base commit | [`682cf3b7887d`](https://github.com/Qiskit/qiskit/commit/682cf3b7887d88d187164ec5dc723874c4e1c294) (2025-01-08), first parent of the merge commit |
| merge commit | [`408741ca1ae4`](https://github.com/Qiskit/qiskit/commit/408741ca1ae4d291f6ae12d3f419ecd841ad8b39) |
| issues closed | [#13623](https://github.com/Qiskit/qiskit/issues/13623) |
| version | 2.0 |
| image | `f2p-chaco/qiskit__qiskit-13624:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-13624.Dockerfile) |
| source files (`patch`) | `qiskit/quantum_info/operators/symplectic/pauli_list.py`, `releasenotes/notes/fix-paulilist-length1-phase-688d0e3a64ec9a9f.yaml` |
| test files (`test_patch`) | `test/python/quantum_info/operators/symplectic/test_pauli_list.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (1)

- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_insert`

## PASS_TO_PASS (141)

<details><summary>show</summary>

- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListInit::test_array_init`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListInit::test_init_from_settings`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListInit::test_list_init`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListInit::test_string_init`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListIteration::test_enumerate`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListIteration::test_iter`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListIteration::test_label_iter`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListIteration::test_matrix_iter`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListIteration::test_matrix_iter_sparse`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListIteration::test_zip`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_from_labels_1q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_from_labels_1q_with_phase`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_from_labels_2q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_from_labels_2q_with_phase`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_from_labels_5q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_labels_round_trip`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_labels_round_trip_array`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_to_labels_1q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_to_labels_1q_array`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_to_labels_1q_array_with_phase`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListLabels::test_to_labels_1q_with_phase`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_1q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_1q_array`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_1q_sparse`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_2q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_2q_array`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_2q_sparse`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_5q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_5q_sparse`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_5q_sparse_with_phase`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMatrix::test_to_matrix_5q_with_phase`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_anticommutes`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_anticommutes_with_all`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_commutes`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_commutes_with_all`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_delete`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_01`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_02`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_03`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_04`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_05`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_06`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_07`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_08`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_09`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_10`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_11`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_12`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_13`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford1_14`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_01`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_02`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_03`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_04`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_05`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_06`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_07`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_08`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_09`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_10`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford_qargs_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford_qargs_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_group_commuting`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_group_qubit_wise_commuting`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_noncommutation_graph_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_noncommutation_graph_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_phase_dtype_evolve_clifford`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_sort`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_unique`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_compose_1q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_dot_1q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_3`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_4`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_5`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_6`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_7`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_8`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_9`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_3`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_4`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_5`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_6`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_7`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_8`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_expand_with_phase_9`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_qargs_compose_1q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_qargs_compose_2q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_qargs_compose_3q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_qargs_dot_1q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_qargs_dot_2q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_qargs_dot_3q`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_3`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_4`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_5`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_6`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_7`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_8`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_9`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_3`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_4`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_5`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_6`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_7`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_8`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListOperator::test_tensor_with_phase_9`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_add_methods`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_add_qargs`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_eq`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_getitem_methods`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_len_methods`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_3`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_4`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_5`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_6`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_7`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_8`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_n_qubit_property_9`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_phase_property`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_setitem_methods`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_shape_property`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_1`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_2`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_3`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_4`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_5`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_6`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_7`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_8`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_size_property_9`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_x_property`
- `test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListProperties::test_z_property`

</details>

## Problem statement (what the agent may be shown)

````text
Issue #13623: `pauli_list.insert(..., qubit=True)` with length-1 `pauli_list` sets `phase` to wrong shape

### Environment

- **Qiskit version**: 1.3.1
- **Python version**: 3.11
- **Operating system**: macos


### What is happening?

I believe the `phase` attribute of any `PauliList` should always be a 1D numpy array.

For instance, this creates a `PauliList` where the `phase` attribute is a 1D array of length 1:
```
plist = PauliList(['XYZ'])
```

However, this code:
```
plist = plist.insert(1, PauliList(['X']), qubit=True)
```
makes `plist.phase` a 2D numpy array (shape = 1 x 1).

This causes problems when further manipulating the object. For example, trying to pass it to `SparsePauliOp()` fails.

### How can we reproduce the issue?

```
import qiskit.quantum_info as qi

plist1 = qi.PauliList(['XX'])

plist2 = qi.PauliList(['X'])
plist2 = plist2.insert(1, qi.PauliList(['X']), qubit=True)

# qiskit thinks the two PauliLists are equivalent:
print(f'{(plist1 == plist2) = }') # np.True_

# but their phase attributes are different shapes:
print(f'{plist1.phase.shape = }') # (1,)
print(f'{plist2.phase.shape = }') # (1, 1)

# and plist1 can be used to construct a SparsePauliOp:
qi.SparsePauliOp(plist1)

# whereas plist2 cannot:
qi.SparsePauliOp(plist2) # raises an error
```

### What should happen?

The `phase` attribute of the output of `insert` should be a 1D array, not a 2D array.
Perhaps the `PauliList.from_symplectic()` constructor (called at the end of `insert`) should also verify/coerce that the `phase` argument is 1D.

(If that's somehow actually the correct behavior, then maybe we'd instead need to fix the SparsePauliOp constructor to handle that input.)

### Any suggestions?

The issue may be how these lines in `PauliList.insert()` treat `phase` on the same footing as `x` and `z`, which are 2D arrays:
https://github.com/Qiskit/qiskit/blob/e33da2ad22b1202fb8c96736416ae585d7b2c593/qiskit/quantum_info/operators/symplectic/pauli_list.py#L448-L452

---

Pull request #13624: Fix phase of `pauli_list.insert(..., qubit=True)` for length-1 `pauli_list`

### Summary
Fix #13623.


### Details and comments
Fixes bug in `PauliList.insert(..., qubit=True)` method, where the output `PauliList` would have a 2D `phase` attribute (should be 1D).

The bug was in a line of code manually broadcasting the `phase` of the `PauliList` being inserted to match the shape of the `phase` of the original `PauliList`. This PR removes this line of code, and lets numpy handle the broadcasting of `phase`.

This PR also adds a check in `PauliList.from_symplectic(..., phase)` to reject `phase` if it is a multi-dimensional array, and a test for issue #13623.

(For the record, I messed up the commit message in 92161ec. The simpler `if/elif` case is indeed moved to be first, but in the commit message I mixed up the two cases).
````

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/quantum_info/operators/symplectic/pauli_list.py b/qiskit/quantum_info/operators/symplectic/pauli_list.py
index af2a0ed9407f02c18362d9e558da7e533a333d57..8e23b6f31a872a18b452a45414045b5a875fb684 100644
--- a/qiskit/quantum_info/operators/symplectic/pauli_list.py
+++ b/qiskit/quantum_info/operators/symplectic/pauli_list.py
@@ -451,16 +451,14 @@ class PauliList(BasePauli, LinearMixin, GroupMixin):
                 f"Index {ind} is greater than number of qubits"
                 f" in the PauliList ({self.num_qubits})"
             )
-        if len(value) == 1:
-            # Pad blocks to correct size
-            value_x = np.vstack(size * [value.x])
-            value_z = np.vstack(size * [value.z])
-            value_phase = np.vstack(size * [value.phase])
-        elif len(value) == size:
+        if len(value) == size:
             #  Blocks are already correct size
             value_x = value.x
             value_z = value.z
-            value_phase = value.phase
+        elif len(value) == 1:
+            # Pad blocks to correct size
+            value_x = np.vstack(size * [value.x])
+            value_z = np.vstack(size * [value.z])
         else:
             # Blocks are incorrect size
             raise QiskitError(
@@ -471,7 +469,7 @@ class PauliList(BasePauli, LinearMixin, GroupMixin):
         # Build new array by blocks
         z = np.hstack([self.z[:, :ind], value_z, self.z[:, ind:]])
         x = np.hstack([self.x[:, :ind], value_x, self.x[:, ind:]])
-        phase = self.phase + value_phase
+        phase = self.phase + value.phase
 
         return PauliList.from_symplectic(z, x, phase)
 
@@ -1131,6 +1129,8 @@ class PauliList(BasePauli, LinearMixin, GroupMixin):
         Returns:
             PauliList: the constructed PauliList.
         """
+        if isinstance(phase, np.ndarray) and np.ndim(phase) > 1:
+            raise ValueError(f"phase should be at most 1D but has {np.ndim(phase)} dimensions.")
         base_z, base_x, base_phase = cls._from_array(z, x, phase)
         return cls(BasePauli(base_z, base_x, base_phase))
 
diff --git a/releasenotes/notes/fix-paulilist-length1-phase-688d0e3a64ec9a9f.yaml b/releasenotes/notes/fix-paulilist-length1-phase-688d0e3a64ec9a9f.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..a1a59708003c37dea38f23767913101ac6346dea
--- /dev/null
+++ b/releasenotes/notes/fix-paulilist-length1-phase-688d0e3a64ec9a9f.yaml
@@ -0,0 +1,6 @@
+---
+fixes:
+  - |
+    Fixed a bug that caused :meth:`.PauliList.insert` with ``qubit=True`` to produce a `phase`
+    attribute with the wrong shape when the original object was length 1.
+    Fixed `#13623 <https://github.com/Qiskit/qiskit/issues/13623>`__.
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/quantum_info/operators/symplectic/test_pauli_list.py b/test/python/quantum_info/operators/symplectic/test_pauli_list.py
index 8c96f63c4ddf534fda5f4447d8fed14f222e5436..9abc473dc333f59a431974ae4bd04c08c911f065 100644
--- a/test/python/quantum_info/operators/symplectic/test_pauli_list.py
+++ b/test/python/quantum_info/operators/symplectic/test_pauli_list.py
@@ -1560,6 +1560,15 @@ class TestPauliListMethods(QiskitTestCase):
                 value1 = pauli.insert(1, insert)
                 self.assertEqual(value1, target1)
 
+        # Insert single column to length-1 PauliList:
+        with self.subTest(msg="length-1, single-column, single-val"):
+            pauli = PauliList(["X"])
+            insert = PauliList(["Y"])
+            target0 = PauliList(["YX"])
+            value0 = pauli.insert(1, insert, qubit=True)
+            self.assertEqual(value0, target0)
+            self.assertEqual(value0.phase.shape, (1,))
+
         # Insert single column
         pauli = PauliList(["X", "Y", "Z", "-iI"])
         for i in ["I", "X", "Y", "Z", "iY"]:
```

## Validation

```json
{
 "test_files": [
  "test/python/quantum_info/operators/symplectic/test_pauli_list.py"
 ],
 "collected_before": 142,
 "collected_after": 142,
 "outcomes_before": {
  "PASSED": 141,
  "FAILED": 1
 },
 "outcomes_after": {
  "PASSED": 142
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "ED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_09\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_10\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford_qargs_1\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford_qargs_2\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_group_commuting\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_group_qubit_wise_commuting\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_noncommutation_graph_1\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_noncommutation_graph_2\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_phase_dtype_evolve_clifford\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_sort\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_unique\nFAILED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_insert\n================== 1 failed, 141 passed, 2 warnings in 5.60s ===================",
 "tail_after": "ED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_09\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford2_10\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford_qargs_1\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_evolve_clifford_qargs_2\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_group_commuting\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_group_qubit_wise_commuting\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_insert\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_noncommutation_graph_1\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_noncommutation_graph_2\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_phase_dtype_evolve_clifford\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_sort\nPASSED test/python/quantum_info/operators/symplectic/test_pauli_list.py::TestPauliListMethods::test_unique\n======================= 142 passed, 2 warnings in 3.41s ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

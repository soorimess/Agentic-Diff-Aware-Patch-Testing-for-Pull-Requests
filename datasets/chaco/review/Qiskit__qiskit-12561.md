# Qiskit__qiskit-12561

[back to the list](README.md) -- **Do not retain and expose old elements of `ParameterVector`**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#12561](https://github.com/Qiskit/qiskit/pull/12561) (created 2024-06-13, merged 2024-06-13) |
| ChaCo lists | full, ablation |
| status | **not-fail-to-pass** -- no developer test fails before the change and passes after (176 pass on both sides) |
| base commit | [`8d2144cec32d`](https://github.com/Qiskit/qiskit/commit/8d2144cec32d5f20e03a8c9af1999a0b7b7a1645) (2024-06-12), first parent of the merge commit |
| merge commit | [`8a1bcc2d5236`](https://github.com/Qiskit/qiskit/commit/8a1bcc2d5236ac090cd9bcbd7cdf5ce8efbcb18c) |
| issues closed | [#12541](https://github.com/Qiskit/qiskit/issues/12541) |
| version | 1.2 |
| image | `f2p-chaco/qiskit__qiskit-12561:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-12561.Dockerfile) |
| source files (`patch`) | `qiskit/circuit/parametervector.py`, `qiskit/qpy/binary_io/value.py` |
| test files (`test_patch`) | `test/python/circuit/test_parameters.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (176)

<details><summary>show</summary>

- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_equal_self`
- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_equal_to_identical_expression`
- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_expression_equal_floats_to_ints`
- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_expression_equal_to_identical`
- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_expression_equal_to_self`
- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_expression_not_equal_if_params_differ`
- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_not_equal_param_of_same_name`
- `test/python/circuit/test_parameters.py::TestParameterEquality::test_parameter_symbol_equal_after_ufunc`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_abs_function_when_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_abs_function_when_not_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_binding_across_broadcast_instruction`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_expression_is_real`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_01_RGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_02_RXGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_03_RYGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_04_RZGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_05_RXXGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_06_RYYGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_07_RZXGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_08_RZZGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_09_CRXGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_10_CRYGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_11_CRZGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_bound_gate_to_matrix_12_XXPlusYYGate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_complex_when_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_float_intermediate_complex_value`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_float_of_complex_fails`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_float_when_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_float_when_underlying_expression_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_int_when_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_int_when_bound_truncates_after_evaluation`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_cast_to_int_when_underlying_expression_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_compare_to_value_when_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_complex_angle_raises_when_not_supported`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_complex_parameter_bound_to_real`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_conjugate`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_division_by_zero`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_constant_1_2`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_constant_2_1_3`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_constant_3_0`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_constant_4__1`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_constant_5__1_0`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_constant_6_3_141592653589793`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_constant_7`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_of_parameter_with_parameter`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_expressions_operation_order`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_name_collision`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_negated_expression`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_nested_expressions`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_numeric`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_operating_on_a_parameter_with_a_non_float_will_raise`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_parameter_expression_exp_log_vs_pow`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_parameter_expression_grad`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_positive_expression`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_raise_if_cast_to_complex_when_not_fully_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_raise_if_cast_to_float_when_not_fully_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_raise_if_cast_to_int_when_not_fully_bound`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_raise_if_sub_unknown_parameters`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_raise_if_subbing_in_parameter_name_conflict`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_standard_cu3`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_sub_allow_unknown_parameters`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_substituting_compound_expression`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_substituting_parameter_with_compound_expression`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_substituting_parameter_with_simple_expression`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_substituting_simple_with_simple_expression`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_expression_parameter_map_1`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_expression_parameter_map_2`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_expression_parameter_map_3`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_expression_parameter_map_4`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_with_expression_1`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_with_expression_2`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_with_expression_3`
- `test/python/circuit/test_parameters.py::TestParameterExpressions::test_to_instruction_with_expression_4`
- `test/python/circuit/test_parameters.py::TestParameterReferences::test_copy_param_refs`
- `test/python/circuit/test_parameters.py::TestParameterReferences::test_equal_inst_diff_instance`
- `test/python/circuit/test_parameters.py::TestParameterReferences::test_equal_inst_same_instance`
- `test/python/circuit/test_parameters.py::TestParameterReferences::test_extend_refs`
- `test/python/circuit/test_parameters.py::TestParameterReferences::test_pickle_unpickle`
- `test/python/circuit/test_parameters.py::TestParameterTable::test_init_param_table`
- `test/python/circuit/test_parameters.py::TestParameterTable::test_set_references`
- `test/python/circuit/test_parameters.py::TestParameterTable::test_set_references_from_iterable`
- `test/python/circuit/test_parameters.py::TestParameterView::test_and`
- `test/python/circuit/test_parameters.py::TestParameterView::test_eq`
- `test/python/circuit/test_parameters.py::TestParameterView::test_ge`
- `test/python/circuit/test_parameters.py::TestParameterView::test_gt`
- `test/python/circuit/test_parameters.py::TestParameterView::test_le`
- `test/python/circuit/test_parameters.py::TestParameterView::test_len`
- `test/python/circuit/test_parameters.py::TestParameterView::test_lt`
- `test/python/circuit/test_parameters.py::TestParameterView::test_ne`
- `test/python/circuit/test_parameters.py::TestParameterView::test_or`
- `test/python/circuit/test_parameters.py::TestParameterView::test_xor`
- `test/python/circuit/test_parameters.py::TestParameters::test_append_copies_parametric`
- `test/python/circuit/test_parameters.py::TestParameters::test_assign_parameters_by_name`
- `test/python/circuit/test_parameters.py::TestParameters::test_bind_half_single_precision`
- `test/python/circuit/test_parameters.py::TestParameters::test_bind_parameters_allow_unknown`
- `test/python/circuit/test_parameters.py::TestParameters::test_bind_parameters_anonymously`
- `test/python/circuit/test_parameters.py::TestParameters::test_bind_parameters_custom_definition_global_phase`
- `test/python/circuit/test_parameters.py::TestParameters::test_bind_ryrz_vector`
- `test/python/circuit/test_parameters.py::TestParameters::test_binding_parameterized_circuits_built_in_multiproc`
- `test/python/circuit/test_parameters.py::TestParameters::test_calibration_assignment`
- `test/python/circuit/test_parameters.py::TestParameters::test_calibration_assignment_doesnt_mutate`
- `test/python/circuit/test_parameters.py::TestParameters::test_calibration_assignment_w_expressions`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_assignment_to_numeric_1_int`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_assignment_to_numeric_2_float`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_assignment_to_numeric_3_float16`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_assignment_to_numeric_4_float32`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_assignment_to_numeric_5_float64`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_composition`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_generation`
- `test/python/circuit/test_parameters.py::TestParameters::test_circuit_with_ufunc`
- `test/python/circuit/test_parameters.py::TestParameters::test_compile_quantum_circuit`
- `test/python/circuit/test_parameters.py::TestParameters::test_compile_vector`
- `test/python/circuit/test_parameters.py::TestParameters::test_compile_with_ufunc`
- `test/python/circuit/test_parameters.py::TestParameters::test_composite_instruction`
- `test/python/circuit/test_parameters.py::TestParameters::test_copy_after_dot_data_setter`
- `test/python/circuit/test_parameters.py::TestParameters::test_copy_after_inverse`
- `test/python/circuit/test_parameters.py::TestParameters::test_copy_after_reverse`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_bound_parameters_1`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_bound_parameters_2`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_bound_parameters_3`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_bound_parameters_4`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_deeply_bound_parameters_1`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_deeply_bound_parameters_2`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_deeply_bound_parameters_3`
- `test/python/circuit/test_parameters.py::TestParameters::test_decompose_propagates_deeply_bound_parameters_4`
- `test/python/circuit/test_parameters.py::TestParameters::test_duplicate_name_on_append`
- `test/python/circuit/test_parameters.py::TestParameters::test_equality`
- `test/python/circuit/test_parameters.py::TestParameters::test_execute_result_names`
- `test/python/circuit/test_parameters.py::TestParameters::test_executing_parameterized_instruction_bound_early_1_gate`
- `test/python/circuit/test_parameters.py::TestParameters::test_executing_parameterized_instruction_bound_early_2_instruction`
- `test/python/circuit/test_parameters.py::TestParameters::test_expression_partial_binding`
- `test/python/circuit/test_parameters.py::TestParameters::test_expression_partial_binding_zero`
- `test/python/circuit/test_parameters.py::TestParameters::test_fix_variable`
- `test/python/circuit/test_parameters.py::TestParameters::test_gate`
- `test/python/circuit/test_parameters.py::TestParameters::test_gate_multiplicity_binding`
- `test/python/circuit/test_parameters.py::TestParameters::test_get_parameter`
- `test/python/circuit/test_parameters.py::TestParameters::test_get_parameter_global_phase`
- `test/python/circuit/test_parameters.py::TestParameters::test_has_parameter`
- `test/python/circuit/test_parameters.py::TestParameters::test_instruction_ryrz_vector`
- `test/python/circuit/test_parameters.py::TestParameters::test_is_parameterized`
- `test/python/circuit/test_parameters.py::TestParameters::test_mixed_binding_1_True`
- `test/python/circuit/test_parameters.py::TestParameters::test_mixed_binding_2_False`
- `test/python/circuit/test_parameters.py::TestParameters::test_multiple_named_parameters`
- `test/python/circuit/test_parameters.py::TestParameters::test_multiple_parameters`
- `test/python/circuit/test_parameters.py::TestParameters::test_num_parameters`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_equality_through_serialization`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_equality_to_expression_1_single`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_equality_to_expression_2_vector`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_name_conflicts_raises`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_order`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_order_append`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_order_compose_1_True`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_order_compose_2_False`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_order_composing_nested_circuit`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameter_vector_equality_through_serialization`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameters_property`
- `test/python/circuit/test_parameters.py::TestParameters::test_parameters_property_by_index`
- `test/python/circuit/test_parameters.py::TestParameters::test_parametervector_resize`
- `test/python/circuit/test_parameters.py::TestParameters::test_partial_assignment`
- `test/python/circuit/test_parameters.py::TestParameters::test_partial_binding`
- `test/python/circuit/test_parameters.py::TestParameters::test_raise_if_assigning_params_not_in_circuit`
- `test/python/circuit/test_parameters.py::TestParameters::test_raise_if_sub_unknown_parameters`
- `test/python/circuit/test_parameters.py::TestParameters::test_rebinding_instruction_copy`
- `test/python/circuit/test_parameters.py::TestParameters::test_repeated_circuit`
- `test/python/circuit/test_parameters.py::TestParameters::test_repeated_gates_to_dag_and_back`
- `test/python/circuit/test_parameters.py::TestParameters::test_setting_global_phase_invalidates_cache`
- `test/python/circuit/test_parameters.py::TestParameters::test_sign_of_parameter`
- `test/python/circuit/test_parameters.py::TestParameters::test_sub_allow_unknown_parameters`
- `test/python/circuit/test_parameters.py::TestParameters::test_substitution`
- `test/python/circuit/test_parameters.py::TestParameters::test_to_instruction_after_inverse`
- `test/python/circuit/test_parameters.py::TestParameters::test_transpile_across_optimization_levels_1_0`
- `test/python/circuit/test_parameters.py::TestParameters::test_transpile_across_optimization_levels_2_1`
- `test/python/circuit/test_parameters.py::TestParameters::test_transpile_across_optimization_levels_3_2`
- `test/python/circuit/test_parameters.py::TestParameters::test_transpile_across_optimization_levels_4_3`
- `test/python/circuit/test_parameters.py::TestParameters::test_transpiling_multiple_parameterized_circuits`
- `test/python/circuit/test_parameters.py::TestParameters::test_two_parameter_expression_binding`

</details>

## Problem statement (what the agent may be shown)

````text
Issue #12541: Strange things about `ParameterVector`

### Environment

- **Qiskit version**: main
- **Python version**: 
- **Operating system**: 


### What is happening?

There are some weird things I have noticed while staring at the `ParameterVector` code.  One design choice is that it stores previous elements even if an array has been down-sized:

https://github.com/Qiskit/qiskit/blob/03d107e1f68f2a47ffdcf5599f906120e4efba63/qiskit/circuit/parametervector.py#L99-L104

Some methods, such as `__iter__` and `__str__` and a few others, correctly account for this:

https://github.com/Qiskit/qiskit/blob/03d107e1f68f2a47ffdcf5599f906120e4efba63/qiskit/circuit/parametervector.py#L87-L88
https://github.com/Qiskit/qiskit/blob/03d107e1f68f2a47ffdcf5599f906120e4efba63/qiskit/circuit/parametervector.py#L93-L94

However, other methods do not account for this, such as `index` and the `params` property:

https://github.com/Qiskit/qiskit/blob/03d107e1f68f2a47ffdcf5599f906120e4efba63/qiskit/circuit/parametervector.py#L69-L76

It appears that it may be intentional for `params` to return everything.  If so, this should be documented.  Also, it might be worth changing `index` to return only elements that currently exist.

### How can we reproduce the issue?

```python
pv = ParameterVector("theta", 20)
last = pv[-1]
pv.resize(3)
pv.index(last)  # returns 19, which is greater than len(pv) - 1
pv.params  # is a list of 20 elements, which is greater than len(pv)
```

### What should happen?

Up for discussion

### Any suggestions?

_No response_

---

Pull request #12561: Do not retain and expose old elements of `ParameterVector`

### Summary

This fixes #12541 according to https://github.com/Qiskit/qiskit/pull/12545#pullrequestreview-2114202382.


### Details and comments

Note that qpy does _not_ appear to store the `_root_uuid`, so if one deserializes a `ParameterVector` and then removes elements and later adds new ones, the uuids of the regenerated elements will change.
````

## Hints (issue comments before the PR; not shown to the agent)

```text
The resizing feature is something used in blueprint circuits, e.g. the `RawFeatureVector` which is essentially a parameterized `Initialize` instruction. Until these objects exists we should keep this feature. The `params` and `index` methods seem to not handle this correctly, after resizing the available parameters should correspond to the new size.
> The resizing feature is something used in blueprint circuits, e.g. the `RawFeatureVector` which is essentially a parameterized `Initialize` instruction. Until these objects exists we should keep this feature. The `params` and `index` methods seem to not handle this correctly, after resizing the available parameters should correspond to the new size.

OK great, this is a very reasonable outcome.  I will open a PR that does this.
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/circuit/parametervector.py b/qiskit/circuit/parametervector.py
index abc8a6f60ef713215f05ec6ca7625abfe3d0e0e2..151e3e7fea73c8d01d1a37af3ca039e1c87ecf3f 100644
--- a/qiskit/circuit/parametervector.py
+++ b/qiskit/circuit/parametervector.py
@@ -50,11 +50,10 @@ class ParameterVectorElement(Parameter):
 class ParameterVector:
     """ParameterVector class to quickly generate lists of parameters."""
 
-    __slots__ = ("_name", "_params", "_size", "_root_uuid")
+    __slots__ = ("_name", "_params", "_root_uuid")
 
     def __init__(self, name, length=0):
         self._name = name
-        self._size = length
         self._root_uuid = uuid4()
         root_uuid_int = self._root_uuid.int
         self._params = [
@@ -76,32 +75,38 @@ class ParameterVector:
         return self._params.index(value)
 
     def __getitem__(self, key):
-        if isinstance(key, slice):
-            start, stop, step = key.indices(self._size)
-            return self.params[start:stop:step]
-
-        if key > self._size:
-            raise IndexError(f"Index out of range: {key} > {self._size}")
         return self.params[key]
 
     def __iter__(self):
-        return iter(self.params[: self._size])
+        return iter(self.params)
 
     def __len__(self):
-        return self._size
+        return len(self._params)
 
     def __str__(self):
-        return f"{self.name}, {[str(item) for item in self.params[: self._size]]}"
+        return f"{self.name}, {[str(item) for item in self.params]}"
 
     def __repr__(self):
         return f"{self.__class__.__name__}(name={self.name}, length={len(self)})"
 
     def resize(self, length):
-        """Resize the parameter vector.
-
-        If necessary, new elements are generated. If length is smaller than before, the
-        previous elements are cached and not re-generated if the vector is enlarged again.
+        """Resize the parameter vector.  If necessary, new elements are generated.
+
+        Note that the UUID of each :class:`.Parameter` element will be generated
+        deterministically given the root UUID of the ``ParameterVector`` and the index
+        of the element.  In particular, if a ``ParameterVector`` is resized to
+        be smaller and then later resized to be larger, the UUID of the later
+        generated element at a given index will be the same as the UUID of the
+        previous element at that index.
         This is to ensure that the parameter instances do not change.
+
+        >>> from qiskit.circuit import ParameterVector
+        >>> pv = ParameterVector("theta", 20)
+        >>> elt_19 = pv[19]
+        >>> rv.resize(10)
+        >>> rv.resize(20)
+        >>> pv[19] == elt_19
+        True
         """
         if length > len(self._params):
             root_uuid_int = self._root_uuid.int
@@ -111,4 +116,5 @@ class ParameterVector:
                     for i in range(len(self._params), length)
                 ]
             )
-        self._size = length
+        else:
+            del self._params[length:]
diff --git a/qiskit/qpy/binary_io/value.py b/qiskit/qpy/binary_io/value.py
index fdad363867a3b2d574f8e77a7828e764d97a7121..c9f0f9af4798c2360d21df306f19e7e674d3540a 100644
--- a/qiskit/qpy/binary_io/value.py
+++ b/qiskit/qpy/binary_io/value.py
@@ -45,7 +45,7 @@ def _write_parameter_vec(file_obj, obj):
         struct.pack(
             formats.PARAMETER_VECTOR_ELEMENT_PACK,
             len(name_bytes),
-            obj._vector._size,
+            len(obj._vector),
             obj.uuid.bytes,
             obj._index,
         )
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/circuit/test_parameters.py b/test/python/circuit/test_parameters.py
index c9380fd076892cea97953983b1071b7dd91ef4f1..7cdc4ed56ab64dc2226b8736f87cf405b3a86b96 100644
--- a/test/python/circuit/test_parameters.py
+++ b/test/python/circuit/test_parameters.py
@@ -1368,10 +1368,8 @@ class TestParameters(QiskitTestCase):
         with self.subTest("enlargen"):
             vec.resize(3)
             self.assertEqual(len(vec), 3)
-            # ensure we still have the same instance not a copy with the same name
-            # this is crucial for adding parameters to circuits since we cannot use the same
-            # name if the instance is not the same
-            self.assertIs(element, vec[1])
+            # ensure we still have an element with the same uuid
+            self.assertEqual(element, vec[1])
             self.assertListEqual([param.name for param in vec], _paramvec_names("x", 3))
 
     def test_raise_if_sub_unknown_parameters(self):
```

## Validation

```json
{
 "image_head": "8d2144cec32d5f20e03a8c9af1999a0b7b7a1645",
 "patch_applies": true,
 "test_files": [
  "test/python/circuit/test_parameters.py"
 ],
 "collected_before": 176,
 "collected_after": 176,
 "outcomes_before": {
  "PASSED": 176
 },
 "outcomes_after": {
  "PASSED": 176
 },
 "exit_before": 0,
 "exit_after": 0,
 "tail_before": "py_param_refs\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_equal_inst_diff_instance\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_equal_inst_same_instance\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_extend_refs\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_pickle_unpickle\nPASSED test/python/circuit/test_parameters.py::TestParameterTable::test_init_param_table\nPASSED test/python/circuit/test_parameters.py::TestParameterTable::test_set_references\nPASSED test/python/circuit/test_parameters.py::TestParameterTable::test_set_references_from_iterable\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_and\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_eq\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_ge\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_gt\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_le\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_len\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_lt\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_ne\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_or\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_xor\n============================= 176 passed in 8.69s ==============================",
 "tail_after": "py_param_refs\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_equal_inst_diff_instance\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_equal_inst_same_instance\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_extend_refs\nPASSED test/python/circuit/test_parameters.py::TestParameterReferences::test_pickle_unpickle\nPASSED test/python/circuit/test_parameters.py::TestParameterTable::test_init_param_table\nPASSED test/python/circuit/test_parameters.py::TestParameterTable::test_set_references\nPASSED test/python/circuit/test_parameters.py::TestParameterTable::test_set_references_from_iterable\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_and\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_eq\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_ge\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_gt\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_le\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_len\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_lt\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_ne\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_or\nPASSED test/python/circuit/test_parameters.py::TestParameterView::test_xor\n============================= 176 passed in 4.12s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

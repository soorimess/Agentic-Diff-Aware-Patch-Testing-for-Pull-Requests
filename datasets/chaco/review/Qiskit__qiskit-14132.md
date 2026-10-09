# Qiskit__qiskit-14132

[back to the list](README.md) -- **Replace internal representation in ObservablesArray with SparseObservable**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#14132](https://github.com/Qiskit/qiskit/pull/14132) (created 2025-03-31, merged 2025-04-27) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 15 developer test(s) flip; oracle reproduces it |
| base commit | [`551819fb057a`](https://github.com/Qiskit/qiskit/commit/551819fb057a8fb3a6f807418a0fda311006fa06) (2025-04-25), first parent of the merge commit |
| merge commit | [`6400d4c32e6d`](https://github.com/Qiskit/qiskit/commit/6400d4c32e6de1edbc78f6896aec3129aee32450) |
| issues closed | none |
| version | 2.1 |
| image | `f2p-chaco/qiskit__qiskit-14132:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-14132.Dockerfile) |
| source files (`patch`) | `qiskit/primitives/containers/observables_array.py` |
| test files (`test_patch`) | `test/python/primitives/containers/test_observables_array.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (15)

- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_duplicate_sparse_pauli_op`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_pauli_1_1`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_pauli_2_2`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_pauli_3_3`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_pauli_mapping`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_1_0`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_3_2`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_1__IXYZ`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_2__IXYZ`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_5__IXYZ`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_signed_sparse_pauli_op`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_str_1_0`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_str_2_1`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_str_3_2`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_zero_sparse_pauli_op`

## PASS_TO_PASS (42)

<details><summary>show</summary>

- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_array_1d`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_array_2d`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_array_single_1_0`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_array_single_2_1`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_array_single_3_2`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_array_single_4_3`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_0d`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_invalid_str_1_iXX`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_invalid_str_2_012`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_invalid_str_3____`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_2_1`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_4_3`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_3_iIXYZ`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_4__iIXYZ`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_format_invalid_mapping_basis`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_format_invalid_mapping_qubits`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_getitem_1d`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_getitem_2d`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_getitem_single_1_0`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_getitem_single_2_1`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_getitem_single_3_2`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_getitem_single_4_3`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_nested_list_sparse_pauli_op`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_nested_list_str`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_nested_pauli_list`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_pauli_list`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_ragged_array`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_single_sparse_pauli_op`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_validate_false`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_init_validate_true`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_ravel`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_reshape`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_1_0`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_2_1`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_3_2`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_4_3`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_1d`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_2d`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_1_0`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_2_1`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_3_2`
- `test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_4_3`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #14132: Replace internal representation in ObservablesArray with SparseObservable

### Summary

This PR will do some of the work items listed in #14129:


### Details and comments

- Other items of #14129 will be done in subsequent or parallel PRs, I'm trying to maximize the number of PRs.
- Currently WIP - the first commit only performs modifications to tests, without yet writing new tests and without implementation.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/primitives/containers/observables_array.py b/qiskit/primitives/containers/observables_array.py
index f339589ac79d3fe0dbaf7a0df004b09d69d0e048..fc0111e007f4d6211db6abc2798ab00d3f90018c 100644
--- a/qiskit/primitives/containers/observables_array.py
+++ b/qiskit/primitives/containers/observables_array.py
@@ -17,16 +17,14 @@ ND-Array container class for Estimator observables.
 from __future__ import annotations
 
 import re
-from collections import defaultdict
 from collections.abc import Iterable, Mapping as _Mapping
 from functools import lru_cache
 from typing import Union, Mapping, overload
-from numbers import Complex
 
 import numpy as np
 from numpy.typing import ArrayLike
 
-from qiskit.quantum_info import Pauli, PauliList, SparsePauliOp
+from qiskit.quantum_info import Pauli, PauliList, SparsePauliOp, SparseObservable
 
 from .object_array import object_array
 from .shape import ShapedMixin, shape_tuple
@@ -51,8 +49,6 @@ class ObservablesArray(ShapedMixin):
     """An ND-array of Hermitian observables for an :class:`.Estimator` primitive."""
 
     __slots__ = ("_array", "_shape")
-    ALLOWED_BASIS: str = "IXYZ01+-lr"
-    """The allowed characters in basis strings."""
 
     def __init__(
         self,
@@ -70,7 +66,7 @@ class ObservablesArray(ShapedMixin):
                 the input should already be an array-like.
 
         Raises:
-            ValueError: If ``validate=True`` and the input observables is not valid.
+            ValueError: If ``validate=True`` and the input observables array is not valid.
         """
         super().__init__()
         if isinstance(observables, ObservablesArray):
@@ -78,23 +74,38 @@ class ObservablesArray(ShapedMixin):
         self._array = object_array(observables, copy=copy, list_types=(PauliList,))
         self._shape = self._array.shape
         if validate:
-            num_qubits = None
             for ndi, obs in np.ndenumerate(self._array):
-                basis_obs = self.coerce_observable(obs)
-                basis_num_qubits = len(next(iter(basis_obs)))
-                if num_qubits is None:
-                    num_qubits = basis_num_qubits
-                elif basis_num_qubits != num_qubits:
-                    raise ValueError(
-                        "The number of qubits must be the same for all observables in the "
-                        "observables array."
-                    )
-                self._array[ndi] = basis_obs
+                self._array[ndi] = self.coerce_observable(obs)
+
+    @staticmethod
+    def _obs_to_dict(obs: SparseObservable) -> Mapping[str, float]:
+        """Convert a sparse observable to a mapping from Pauli strings to coefficients"""
+        result = {}
+        for sparse_pauli_str, pauli_qubits, coeff in obs.to_sparse_list():
+
+            if len(sparse_pauli_str) == 0:
+                full_pauli_str = "I" * obs.num_qubits
+            else:
+                sorted_lists = sorted(zip(pauli_qubits, sparse_pauli_str))
+                string_fragments = []
+                prev_qubit = -1
+                for qubit, pauli in sorted_lists:
+                    string_fragments.append("I" * (qubit - prev_qubit - 1) + pauli)
+                    prev_qubit = qubit
+
+                string_fragments.append("I" * (obs.num_qubits - max(pauli_qubits) - 1))
+                full_pauli_str = "".join(string_fragments)[::-1]
+
+            # We know that the dictionary doesn't contain yet full_pauli_str as a key
+            # because the observable is guaranteed to be simplified
+            result[full_pauli_str] = np.real(coeff)
+
+        return result
 
     def __repr__(self):
         prefix = f"{type(self).__name__}("
         suffix = f", shape={self.shape})"
-        array = np.array2string(self._array, prefix=prefix, suffix=suffix, threshold=50)
+        array = np.array2string(self.__array__(), prefix=prefix, suffix=suffix, threshold=50)
         return prefix + array + suffix
 
     def tolist(self) -> list | ObservableLike:
@@ -116,24 +127,33 @@ class ObservablesArray(ShapedMixin):
                 >>> print(type(oa.tolist()))
                 <class 'dict'>
         """
-        return self._array.tolist()
+        return self.__array__().tolist()
 
-    def __array__(self, dtype=None, copy=None):
-        """Convert to an Numpy.ndarray"""
+    def __array__(self, dtype=None, copy=None) -> np.ndarray:  # pylint: disable=unused-argument
+        """Convert to a Numpy.ndarray"""
         if dtype is None or dtype == object:
-            return self._array.copy() if copy else self._array
+            tmp_result = self.__getitem__(tuple(slice(None) for _ in self._array.shape))
+            if len(self._array.shape) == 0:
+                result = np.ndarray(shape=self._array.shape, dtype=dict)
+                result[()] = tmp_result
+            else:
+                result = np.ndarray(tmp_result.shape, dtype=dict)
+                for ndi, obs in np.ndenumerate(tmp_result._array):
+                    result[ndi] = self._obs_to_dict(obs)
+            return result
         raise ValueError("Type must be 'None' or 'object'")
 
     @overload
     def __getitem__(self, args: int | tuple[int, ...]) -> Mapping[str, float]: ...
 
     @overload
-    def __getitem__(self, args: slice) -> ObservablesArray: ...
+    def __getitem__(self, args: slice | tuple[slice, ...]) -> ObservablesArray: ...
 
     def __getitem__(self, args):
         item = self._array[args]
         if not isinstance(item, np.ndarray):
-            return item
+            return self._obs_to_dict(item)
+
         return ObservablesArray(item, copy=False, validate=False)
 
     def reshape(self, *shape: int | Iterable[int]) -> ObservablesArray:
@@ -162,7 +182,7 @@ class ObservablesArray(ShapedMixin):
         return self.reshape(self.size)
 
     @classmethod
-    def coerce_observable(cls, observable: ObservableLike) -> Mapping[str, float]:
+    def coerce_observable(cls, observable: ObservableLike) -> SparseObservable:
         """Format an observable-like object into the internal format.
 
         Args:
@@ -177,61 +197,39 @@ class ObservablesArray(ShapedMixin):
         """
         # Pauli-type conversions
         if isinstance(observable, SparsePauliOp):
-            observable = observable.simplify(atol=0)
-            # Check that the operator is Hermitian and has real coeffs
+            observable = SparseObservable.from_sparse_pauli_op(observable)
+        elif isinstance(observable, Pauli):
+            observable = SparseObservable.from_pauli(observable)
+        elif isinstance(observable, str):
+            observable = SparseObservable.from_label(observable)
+        elif isinstance(observable, _Mapping):
+            term_list = []
+            for basis, coeff in observable.items():
+                if isinstance(basis, str):
+                    term_list.append((basis, coeff))
+                elif isinstance(basis, Pauli):
+                    unphased_basis, phase = basis[:].to_label(), basis.phase
+                    term_list.append((unphased_basis, complex(0, 1) ** phase * coeff))
+                else:
+                    raise TypeError(f"Invalid observable basis type: {type(basis)}")
+            observable = SparseObservable.from_list(term_list)
+
+        if isinstance(observable, SparseObservable):
+            # Check that the operator has real coeffs
             coeffs = np.real_if_close(observable.coeffs)
             if np.iscomplexobj(coeffs):
                 raise ValueError(
                     "Non-Hermitian input observable: the input SparsePauliOp has non-zero"
                     " imaginary part in its coefficients."
                 )
-            paulis = observable.paulis.to_labels()
-            # Call simplify to combine duplicate keys before converting to a mapping
-            return dict(zip(paulis, coeffs))
-
-        if isinstance(observable, Pauli):
-            label, phase = observable[:].to_label(), observable.phase
-            if phase % 2:
-                raise ValueError(
-                    "Non-Hermitian input observable: the input Pauli has an imaginary phase."
-                )
-            return {label: 1} if phase == 0 else {label: -1}
 
-        # String conversion
-        if isinstance(observable, str):
-            cls._validate_basis(observable)
-            return {observable: 1}
-
-        # Mapping conversion (with possible Pauli keys)
-        if isinstance(observable, _Mapping):
-            num_qubits = len(next(iter(observable)))
-            unique = defaultdict(float)
-            for basis, coeff in observable.items():
-                if isinstance(basis, Pauli):
-                    basis, phase = basis[:].to_label(), basis.phase
-                    if phase % 2:
-                        raise ValueError(
-                            "Non-Hermitian input observable: the input Pauli has an imaginary phase."
-                        )
-                    if phase == 2:
-                        coeff = -coeff
-                # Truncate complex numbers to real
-                if isinstance(coeff, Complex):
-                    if abs(coeff.imag) > 1e-7:
-                        raise TypeError(
-                            f"Non-Hermitian input observable: {basis} term has a complex value"
-                            " coefficient."
-                        )
-                    coeff = coeff.real
-
-                # Validate basis
-                cls._validate_basis(basis)
-                if len(basis) != num_qubits:
-                    raise ValueError(
-                        "Number of qubits must be the same for all observable basis elements."
-                    )
-                unique[basis] += coeff
-            return dict(unique)
+            return SparseObservable.from_raw_parts(
+                observable.num_qubits,
+                coeffs,
+                observable.bit_terms,
+                observable.indices,
+                observable.boundaries,
+            ).simplify(tol=0)
 
         raise TypeError(f"Invalid observable type: {type(observable)}")
 
@@ -253,36 +251,14 @@ class ObservablesArray(ShapedMixin):
         """Validate the consistency in observables array."""
         num_qubits = None
         for obs in self._array.reshape(-1):
-            basis_num_qubits = len(next(iter(obs)))
             if num_qubits is None:
-                num_qubits = basis_num_qubits
-            elif basis_num_qubits != num_qubits:
+                num_qubits = obs.num_qubits
+            elif obs.num_qubits != num_qubits:
                 raise ValueError(
                     "The number of qubits must be the same for all observables in the "
                     "observables array."
                 )
 
-    @classmethod
-    def _validate_basis(cls, basis: str) -> None:
-        """Validate a basis string.
-
-        Args:
-            basis: a basis string to validate.
-
-        Raises:
-            ValueError: If basis string contains invalid characters
-        """
-        # NOTE: the allowed basis characters can be overridden by modifying the class
-        # attribute ALLOWED_BASIS
-        allowed_pattern = _regex_match(cls.ALLOWED_BASIS)
-        if not allowed_pattern.match(basis):
-            invalid_pattern = _regex_invalid(cls.ALLOWED_BASIS)
-            invalid_chars = list(set(invalid_pattern.findall(basis)))
-            raise ValueError(
-                f"Observable basis string '{basis}' contains invalid characters {invalid_chars},"
-                f" allowed characters are {list(cls.ALLOWED_BASIS)}.",
-            )
-
 
 @lru_cache(1)
 def _regex_match(allowed_chars: str) -> re.Pattern:
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/primitives/containers/test_observables_array.py b/test/python/primitives/containers/test_observables_array.py
index ea51718aebeaea24738c5f7f3f6b03da407aa8be..be215f28a4dbdbf47e5613128e6532ed33344a8a 100644
--- a/test/python/primitives/containers/test_observables_array.py
+++ b/test/python/primitives/containers/test_observables_array.py
@@ -28,24 +28,10 @@ class ObservablesArrayTestCase(QiskitTestCase):
     @ddt.data(0, 1, 2)
     def test_coerce_observable_str(self, num_qubits):
         """Test coerce_observable for allowed basis str input"""
-        for chars in it.permutations(ObservablesArray.ALLOWED_BASIS, num_qubits):
+        for chars in it.permutations("IXYZ01+-lr", num_qubits):
             label = "".join(chars)
             obs = ObservablesArray.coerce_observable(label)
-            self.assertEqual(obs, {label: 1})
-
-    def test_coerce_observable_custom_basis(self):
-        """Test coerce_observable for custom al flowed basis"""
-
-        class PauliArray(ObservablesArray):
-            """Custom array allowing only Paulis, not projectors"""
-
-            ALLOWED_BASIS = "IXYZ"
-
-        with self.assertRaises(ValueError):
-            PauliArray.coerce_observable("0101")
-        for p in qi.pauli_basis(1):
-            obs = PauliArray.coerce_observable(p)
-            self.assertEqual(obs, {p.to_label(): 1})
+            self.assertEqual(obs, qi.SparseObservable.from_label(label))
 
     @ddt.data("iXX", "012", "+/-")
     def test_coerce_observable_invalid_str(self, basis):
@@ -58,7 +44,7 @@ class ObservablesArrayTestCase(QiskitTestCase):
         """Test coerce_observable for Pauli input"""
         for p in qi.pauli_basis(num_qubits):
             obs = ObservablesArray.coerce_observable(p)
-            self.assertEqual(obs, {p.to_label(): 1})
+            self.assertEqual(obs, qi.SparseObservable.from_pauli(p))
 
     @ddt.data(0, 1, 2, 3)
     def test_coerce_observable_phased_pauli(self, phase):
@@ -71,10 +57,15 @@ class ObservablesArrayTestCase(QiskitTestCase):
                 ObservablesArray.coerce_observable(pauli)
         else:
             obs = ObservablesArray.coerce_observable(pauli)
-            self.assertIsInstance(obs, dict)
-            self.assertEqual(list(obs.keys()), ["IXYZ"])
-            np.testing.assert_allclose(
-                list(obs.values()), [coeff], err_msg=f"Wrong value for Pauli {pauli}"
+            self.assertIsInstance(obs, qi.SparseObservable)
+            obs_pauli, obs_qubits, obs_coeff = obs.to_sparse_list()[0]
+
+            # ZYX and not XYZ because the qubits in `obs_qubits` are ascending
+            self.assertEqual(obs_pauli, "ZYX")
+            self.assertEqual(obs_qubits, [0, 1, 2])
+
+            np.testing.assert_almost_equal(
+                obs_coeff, coeff, err_msg=f"Wrong value for Pauli {pauli}"
             )
 
     @ddt.data("+IXYZ", "-IXYZ", "iIXYZ", "+iIXYZ", "-IXYZ")
@@ -87,44 +78,58 @@ class ObservablesArrayTestCase(QiskitTestCase):
                 ObservablesArray.coerce_observable(pauli)
         else:
             obs = ObservablesArray.coerce_observable(pauli)
-            self.assertIsInstance(obs, dict)
-            self.assertEqual(list(obs.keys()), ["IXYZ"])
-            np.testing.assert_allclose(
-                list(obs.values()), [coeff], err_msg=f"Wrong value for Pauli {pauli}"
+            self.assertIsInstance(obs, qi.SparseObservable)
+            obs_pauli, obs_qubits, obs_coeff = obs.to_sparse_list()[0]
+
+            # ZYX and not XYZ because the qubits in `obs_qubits` are ascending
+            self.assertEqual(obs_pauli, "ZYX")
+            self.assertEqual(obs_qubits, [0, 1, 2])
+
+            np.testing.assert_almost_equal(
+                obs_coeff, coeff, err_msg=f"Wrong value for Pauli {pauli}"
             )
 
     def test_coerce_observable_signed_sparse_pauli_op(self):
         """Test coerce_observable for SparsePauliOp input with phase paulis"""
         op = qi.SparsePauliOp(["+I", "-X", "Y", "-Z"], [1, 2, 3, 4])
         obs = ObservablesArray.coerce_observable(op)
-        self.assertIsInstance(obs, dict)
-        self.assertEqual(len(obs), 4)
-        self.assertEqual(sorted(obs.keys()), sorted(["I", "X", "Y", "Z"]))
-        np.testing.assert_allclose([obs[i] for i in ["I", "X", "Y", "Z"]], [1, -2, 3, -4])
+        self.assertIsInstance(obs, qi.SparseObservable)
+        sparse_list = sorted(obs.to_sparse_list())
+        self.assertEqual(len(sparse_list), 4)
+        obs_paulis = [term[0] for term in sparse_list]
+        obs_coeffs = [term[2] for term in sparse_list]
+        self.assertEqual(obs_paulis, ["", "X", "Y", "Z"])
+        np.testing.assert_allclose(obs_coeffs, [1, -2, 3, -4])
 
     def test_coerce_observable_zero_sparse_pauli_op(self):
         """Test coerce_observable for SparsePauliOp input with zero val coeffs"""
         op = qi.SparsePauliOp(["I", "X", "Y", "Z"], [0, 0, 0, 1])
         obs = ObservablesArray.coerce_observable(op)
-        self.assertIsInstance(obs, dict)
-        self.assertEqual(len(obs), 1)
-        self.assertEqual(sorted(obs.keys()), ["Z"])
-        self.assertEqual(obs["Z"], 1)
+        self.assertIsInstance(obs, qi.SparseObservable)
+        sparse_list = obs.to_sparse_list()
+        self.assertEqual(len(sparse_list), 1)
+        obs_pauli, _, obs_coeff = sparse_list[0]
+        self.assertEqual(obs_pauli, "Z")
+        self.assertEqual(obs_coeff, 1)
 
     def test_coerce_observable_duplicate_sparse_pauli_op(self):
         """Test coerce_observable for SparsePauliOp with duplicate paulis"""
         op = qi.SparsePauliOp(["XX", "-XX", "XX", "-XX"], [2, 1, 3, 2])
         obs = ObservablesArray.coerce_observable(op)
-        self.assertIsInstance(obs, dict)
-        self.assertEqual(len(obs), 1)
-        self.assertEqual(list(obs.keys()), ["XX"])
-        self.assertEqual(obs["XX"], 2)
+        self.assertIsInstance(obs, qi.SparseObservable)
+        sparse_list = obs.to_sparse_list()
+        self.assertEqual(len(sparse_list), 1)
+        obs_pauli, _, obs_coeff = sparse_list[0]
+        self.assertEqual(obs_pauli, "XX")
+        self.assertEqual(obs_coeff, 2)
 
     def test_coerce_observable_pauli_mapping(self):
         """Test coerce_observable for pauli-keyed Mapping input"""
         mapping = dict(zip(qi.pauli_basis(1), range(1, 5)))
         obs = ObservablesArray.coerce_observable(mapping)
-        target = {key.to_label(): val for key, val in mapping.items()}
+        target = qi.SparseObservable.from_list(
+            [(key.to_label(), val) for key, val in mapping.items()]
+        ).simplify()
         self.assertEqual(obs, target)
 
     def test_coerce_0d(self):
@@ -198,13 +203,13 @@ class ObservablesArrayTestCase(QiskitTestCase):
 
     def test_init_validate_false(self):
         """Test init validate kwarg"""
-        obj = [["A", "B", "C"], ["D", "E", "F"]]
+        obj = [["X", "Y", "Z"], ["I", "0", "1"]]
         obs = ObservablesArray(obj, validate=False)
         self.assertEqual(obs.shape, (2, 3))
         self.assertEqual(obs.size, 6)
         for i in range(2):
             for j in range(3):
-                self.assertEqual(obs[i, j], obj[i][j])
+                self.assertEqual(obs._array[i, j], obj[i][j])
 
     def test_init_validate_true(self):
         """Test init validate kwarg"""
@@ -218,7 +223,7 @@ class ObservablesArrayTestCase(QiskitTestCase):
         obs = {"XX": 1}
         for _ in range(ndim):
             obs = [obs]
-        arr = ObservablesArray(obs, validate=False)
+        arr = ObservablesArray(obs)
         self.assertEqual(arr.size, 1, msg="Incorrect ObservablesArray.size")
         self.assertEqual(arr.shape, (1,) * ndim, msg="Incorrect ObservablesArray.shape")
 
@@ -228,7 +233,7 @@ class ObservablesArrayTestCase(QiskitTestCase):
         obs = {"XX": 1}
         for _ in range(ndim):
             obs = [obs]
-        arr = ObservablesArray(obs, validate=False)
+        arr = ObservablesArray(obs)
         ls = arr.tolist()
         self.assertEqual(ls, obs)
 
@@ -238,7 +243,7 @@ class ObservablesArrayTestCase(QiskitTestCase):
         obs = {"XX": 1}
         for _ in range(ndim):
             obs = [obs]
-        arr = ObservablesArray(obs, validate=False)
+        arr = ObservablesArray(obs)
         nparr = np.array(arr)
         self.assertEqual(nparr.dtype, object)
         self.assertEqual(nparr.shape, arr.shape)
@@ -252,49 +257,52 @@ class ObservablesArrayTestCase(QiskitTestCase):
         obs = base_obs
         for _ in range(ndim):
             obs = [obs]
-        arr = ObservablesArray(obs, validate=False)
+        arr = ObservablesArray(obs)
         idx = ndim * (0,)
         item = arr[idx]
         self.assertEqual(item, base_obs)
 
     def test_tolist_1d(self):
         """Test tolist method"""
-        obj = ["A", "B", "C", "D"]
-        obs = ObservablesArray(obj, validate=False)
+        obj = [{"I": 1}, {"X": 2}, {"Y": 3}, {"Z": 4}]
+        obs = ObservablesArray(obj)
         self.assertEqual(obs.tolist(), obj)
 
     def test_tolist_2d(self):
         """Test tolist method"""
-        obj = [["A", "B", "C"], ["D", "E", "F"]]
-        obs = ObservablesArray(obj, validate=False)
+        obj = [[{"II": 1.0}, {"XI": 2.0}, {"IY": 3.0}], [{"XX": 1.0}, {"XY": 2.0}, {"YY": 3.0}]]
+        obs = ObservablesArray(obj)
         self.assertEqual(obs.tolist(), obj)
 
     def test_array_1d(self):
         """Test __array__ dunder method"""
-        obj = np.array(["A", "B", "C", "D"], dtype=object)
-        obs = ObservablesArray(obj, validate=False)
+        obj = np.array([{"I": 1}, {"X": 2}, {"Y": 3}, {"Z": 4}], dtype=object)
+        obs = ObservablesArray(obj)
         self.assertTrue(np.all(np.array(obs) == obj))
 
     def test_array_2d(self):
         """Test __array__ dunder method"""
-        obj = np.array([["A", "B", "C"], ["D", "E", "F"]], dtype=object)
-        obs = ObservablesArray(obj, validate=False)
+        obj = np.array(
+            [[{"II": 1}, {"XI": 2}, {"IY": 3}], [{"XX": 1}, {"XY": 2}, {"YY": 3}]], dtype=object
+        )
+        obs = ObservablesArray(obj)
         self.assertTrue(np.all(np.array(obs) == obj))
 
     def test_getitem_1d(self):
         """Test __getitem__ for 1D array"""
-        obj = np.array(["A", "B", "C", "D"], dtype=object)
-        obs = ObservablesArray(obj, validate=False)
+        obj = np.array([{"I": 1}, {"X": 2}, {"Y": 3}, {"Z": 4}], dtype=object)
+        obs = ObservablesArray(obj)
         for i in range(obj.size):
             self.assertEqual(obs[i], obj[i])
 
     def test_getitem_2d(self):
         """Test __getitem__ for 2D array"""
-        obj = np.array([["A", "B", "C"], ["D", "E", "F"]], dtype=object)
-        obs = ObservablesArray(obj, validate=False)
+        obj = np.array(
+            [[{"II": 1}, {"XI": 2}, {"IY": 3}], [{"XX": 1}, {"XY": 2}, {"YY": 3}]], dtype=object
+        )
+        obs = ObservablesArray(obj)
         for i in range(obj.shape[0]):
             row = obs[i]
-            self.assertIsInstance(row, ObservablesArray)
             self.assertEqual(row.shape, (3,))
             self.assertTrue(np.all(np.array(row) == obj[i]))
 
@@ -347,13 +355,3 @@ class ObservablesArrayTestCase(QiskitTestCase):
                             {labels_rs[idx]: 1},
                             msg=f"failed for shape {shape} with input format {input_shape}",
                         )
-
-    def test_validate(self):
-        """Test the validate method"""
-        ObservablesArray({"XX": 1}).validate()
-        ObservablesArray([{"XX": 1}] * 5).validate()
-        ObservablesArray([{"XX": 1}] * 15).reshape((3, 5)).validate()
-
-        obs = ObservablesArray([{"XX": 1}, {"XYZ": 1}], validate=False)
-        with self.assertRaisesRegex(ValueError, "number of qubits must be the same"):
-            obs.validate()
```

## Validation

```json
{
 "test_files": [
  "test/python/primitives/containers/test_observables_array.py"
 ],
 "collected_before": 57,
 "collected_after": 57,
 "outcomes_before": {
  "PASSED": 42,
  "FAILED": 15
 },
 "outcomes_after": {
  "PASSED": 57
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "array.py::ObservablesArrayTestCase::test_coerce_observable_pauli_mapping\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_1_0\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_3_2\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_1__IXYZ\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_2__IXYZ\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_phased_pauli_str_5__IXYZ\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_signed_sparse_pauli_op\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_str_1_0\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_str_2_1\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_str_3_2\nFAILED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_coerce_observable_zero_sparse_pauli_op\n======================== 15 failed, 42 passed in 2.00s =========================",
 "tail_after": "st_init_validate_true\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_ravel\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_reshape\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_1_0\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_2_1\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_3_2\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_size_and_shape_single_4_3\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_1d\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_2d\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_1_0\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_2_1\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_3_2\nPASSED test/python/primitives/containers/test_observables_array.py::ObservablesArrayTestCase::test_tolist_single_4_3\n============================== 57 passed in 1.65s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

# scipy__scipy-21435

[back to the list](README.md) -- **ENH: sparse: Add nD COO support for matmul, dot and tensordot**

| field | value |
|---|---|
| pull request | [scipy/scipy#21435](https://github.com/scipy/scipy/pull/21435) (created 2024-08-22, merged 2024-12-05) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 184 developer test(s) flip; oracle reproduces it |
| base commit | [`33335695aef2`](https://github.com/scipy/scipy/commit/33335695aef244321260b149ec3c1286b7fde4d6) (2024-12-05), first parent of the merge commit |
| merge commit | [`3c7071929278`](https://github.com/scipy/scipy/commit/3c707192927890207f719b887543640d3f6f3fdc) |
| issues closed | none |
| version | 1.15 |
| image | `f2p-chaco/scipy__scipy-21435:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-21435.Dockerfile) |
| source files (`patch`) | `scipy/sparse/_base.py`, `scipy/sparse/_coo.py`, `scipy/sparse/_generate_sparsetools.py`, `scipy/sparse/sparsetools/coo.h` |
| test files (`test_patch`) | `scipy/sparse/tests/test_coo.py` |
| compiled files changed | scipy/sparse/sparsetools/coo.h |
| binary files left out | none |

## FAIL_TO_PASS (184)

- `scipy/sparse/tests/test_coo.py::test_1d_add_dense`
- `scipy/sparse/tests/test_coo.py::test_1d_add_sparse`
- `scipy/sparse/tests/test_coo.py::test_1d_diagonal`
- `scipy/sparse/tests/test_coo.py::test_1d_matmul_multivector`
- `scipy/sparse/tests/test_coo.py::test_1d_matmul_vector`
- `scipy/sparse/tests/test_coo.py::test_1d_resize[1]`
- `scipy/sparse/tests/test_coo.py::test_1d_resize[2]`
- `scipy/sparse/tests/test_coo.py::test_1d_resize[4]`
- `scipy/sparse/tests/test_coo.py::test_1d_resize[5]`
- `scipy/sparse/tests/test_coo.py::test_1d_resize[8]`
- `scipy/sparse/tests/test_coo.py::test_1d_row_and_col`
- `scipy/sparse/tests/test_coo.py::test_1d_sparse_constructor`
- `scipy/sparse/tests/test_coo.py::test_1d_to_2d_resize[arg0]`
- `scipy/sparse/tests/test_coo.py::test_1d_to_2d_resize[arg1]`
- `scipy/sparse/tests/test_coo.py::test_1d_to_2d_resize[arg2]`
- `scipy/sparse/tests/test_coo.py::test_1d_to_2d_resize[arg3]`
- `scipy/sparse/tests/test_coo.py::test_1d_toformats`
- `scipy/sparse/tests/test_coo.py::test_1d_tuple_constructor`
- `scipy/sparse/tests/test_coo.py::test_1d_tuple_constructor_with_shape`
- `scipy/sparse/tests/test_coo.py::test_2d_matmul_multivector`
- `scipy/sparse/tests/test_coo.py::test_2d_to_1d_resize[1]`
- `scipy/sparse/tests/test_coo.py::test_2d_to_1d_resize[4]`
- `scipy/sparse/tests/test_coo.py::test_2d_to_1d_resize[6]`
- `scipy/sparse/tests/test_coo.py::test_2d_to_1d_resize[8]`
- `scipy/sparse/tests/test_coo.py::test_add_sparse_with_inf`
- `scipy/sparse/tests/test_coo.py::test_block_diag[shape0]`
- `scipy/sparse/tests/test_coo.py::test_block_diag[shape1]`
- `scipy/sparse/tests/test_coo.py::test_block_diag[shape2]`
- `scipy/sparse/tests/test_coo.py::test_block_diag[shape3]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape0-broadcast_shape0]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape1-broadcast_shape1]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape2-broadcast_shape2]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape3-broadcast_shape3]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape4-broadcast_shape4]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape5-broadcast_shape5]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape6-broadcast_shape6]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape7-broadcast_shape7]`
- `scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape8-broadcast_shape8]`
- `scipy/sparse/tests/test_coo.py::test_dense_constructor`
- `scipy/sparse/tests/test_coo.py::test_dense_constructor_with_inconsistent_shape`
- `scipy/sparse/tests/test_coo.py::test_dense_constructor_with_shape`
- `scipy/sparse/tests/test_coo.py::test_dot_1d_1d`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape0-b_shape0]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape1-b_shape1]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape2-b_shape2]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape3-b_shape3]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape4-b_shape4]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape5-b_shape5]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape6-b_shape6]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape7-b_shape7]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape8-b_shape8]`
- `scipy/sparse/tests/test_coo.py::test_dot_nd[a_shape9-b_shape9]`
- `scipy/sparse/tests/test_coo.py::test_dot_sparse_scalar`
- `scipy/sparse/tests/test_coo.py::test_dot_with_inconsistent_shapes`
- `scipy/sparse/tests/test_coo.py::test_eliminate_zeros`
- `scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape0]`
- `scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape1]`
- `scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape2]`
- `scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_dense[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_dense[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_dense[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_dense[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_dense[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_dense[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_dense[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse_with_inconsistent_shapes[a_shape0-b_shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse_with_inconsistent_shapes[a_shape1-b_shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_add_sparse_with_inconsistent_shapes[a_shape2-b_shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_eliminate_zeros`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape10-mat_shape20]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape11-mat_shape21]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape110-mat_shape210]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape111-mat_shape211]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape12-mat_shape22]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape13-mat_shape23]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape14-mat_shape24]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape15-mat_shape25]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape16-mat_shape26]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape17-mat_shape27]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape18-mat_shape28]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul[mat_shape19-mat_shape29]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_sparse_with_inconsistent_arrays`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape0-vec_shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape1-vec_shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape2-vec_shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape3-vec_shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape4-vec_shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape5-vec_shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape6-vec_shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape7-vec_shape7]`
- `scipy/sparse/tests/test_coo.py::test_nd_matmul_vector[mat_shape8-vec_shape8]`
- `scipy/sparse/tests/test_coo.py::test_nd_nnz[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_nnz[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_nnz[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_nnz[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_nnz[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_nnz[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_nnz[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_reshape[shape0-new_shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_reshape[shape1-new_shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_reshape[shape2-new_shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_reshape[shape3-new_shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_sparse_constructor[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_sparse_constructor[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_sparse_constructor[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_sparse_constructor[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_sparse_constructor[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_sparse_constructor[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_sparse_constructor[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_dense[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_dense[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_dense[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_dense[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_dense[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_dense[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_dense[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse_with_inconsistent_shapes[a_shape0-b_shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse_with_inconsistent_shapes[a_shape1-b_shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse_with_inconsistent_shapes[a_shape2-b_shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_sub_sparse_with_nan`
- `scipy/sparse/tests/test_coo.py::test_nd_todense[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_todense[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_todense[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_todense[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_todense[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_todense[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_todense[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose_with_axis[shape0-axis_perm0]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose_with_axis[shape1-axis_perm1]`
- `scipy/sparse/tests/test_coo.py::test_nd_transpose_with_axis[shape2-axis_perm2]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor_with_shape[shape0]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor_with_shape[shape1]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor_with_shape[shape2]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor_with_shape[shape3]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor_with_shape[shape4]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor_with_shape[shape5]`
- `scipy/sparse/tests/test_coo.py::test_nd_tuple_constructor_with_shape[shape6]`
- `scipy/sparse/tests/test_coo.py::test_nnz`
- `scipy/sparse/tests/test_coo.py::test_non_subscriptability`
- `scipy/sparse/tests/test_coo.py::test_reshape`
- `scipy/sparse/tests/test_coo.py::test_shape_constructor`
- `scipy/sparse/tests/test_coo.py::test_sum_duplicates`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape0-b_shape0-axes0]`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape1-b_shape1-axes1]`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape2-b_shape2-axes2]`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape3-b_shape3-axes3]`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape4-b_shape4-axes4]`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape5-b_shape5-3]`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape6-b_shape6-1]`
- `scipy/sparse/tests/test_coo.py::test_tensordot[a_shape7-b_shape7-axes7]`
- `scipy/sparse/tests/test_coo.py::test_tensordot_with_invalid_args`
- `scipy/sparse/tests/test_coo.py::test_transpose`
- `scipy/sparse/tests/test_coo.py::test_transpose_with_axis`
- `scipy/sparse/tests/test_coo.py::test_transpose_with_inconsistent_axis`
- `scipy/sparse/tests/test_coo.py::test_tuple_constructor_for_dim_size_zero`

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #21435: ENH: sparse: Add nD COO support for matmul, dot and tensordot

_**Context:** This is the second PR (follow-up to #21197) aiming to extend support for n-D COO arrays in SciPy (refer to https://github.com/scipy/scipy/issues/21169). I am undertaking this work as part of my summer internship with Quansight Labs till the end of September, under the mentorship of @rgommers and @izaid._

This PR aims to add support for n-dimensional matrix multiplication, dot, and tensordot for COO arrays, along with `broadcast_to` which replicates the behaviour of `np.broadcast_to` but for COO arrays.

The approach taken for these methods is as follows -

### `matmul`

#### sparse `a` x sparse `b`
We broadcast `a` and `b`, convert both to block_diagonal form in COO format (using helper function `_block_diag`). We convert the 2-D block diagonal `a` and `b` to 2-D CSR, use `csr_matmat` for 2-D sparse-sparse `matmul`, convert the 2-D block diagonal product to an n-D COO array (using helper function `_extract_block_diag`) to obtain our product.


#### sparse `a` x dense `b`
C++ function `coo_matmat_dense_nd` added to perform sparse-dense `matmul` (this is the n-D extension of 2-D `coo_matmat_dense` which was added at #21240).

 
### `dot`/`tensordot`

#### sparse `a` and sparse `b`
We map n-D COO arrays `a` and `b` to 2-D COO arrays (using `np.ravel_multi_index`), convert to CSR, use `csr_matmat`, then map the 2-D result to an n-D COO array (using `np.unravel_index`), which is the final result.
(thanks to the [proof-of-concept](https://gist.github.com/dschult/6b65bd18cd425d07b1a659eb7f67bc58) given by @dschult, mentioned at https://github.com/scipy/scipy/issues/21169#issuecomment-2231275707)

The case of `tensordot` is similar, though it involved some additional transposing based on the `axes` input.


#### sparse `a` and dense `b`
The implementation for sparse-dense `dot` involved reshaping `a` and `b` and using `matmul`. The reshaping can be described as follows -

For `a` of shape `(2,3,4,5)` and `b` shape `(6,7,5,9)` (where `a.shape[-1] == b.shape[-2]` for `dot`), `a.dot(b)` will have shape `(2,3,4,6,7,9)`.
If we reshape `a` to `(2,3,4,1,1,1)` and `b` to `(1,1,1,6,7,9)` and multiply the reshaped arrays after broadcasting, we get a product of shape `(2,3,4,6,7,9)`, which is equal to the dot of the original `a` and `b`.

The case for `tensordot` is once again similar, but required some transposing first.



I have also added extensive testing for the added and modified methods.
(**Note** - diff may be easier to view once #21197 has been merged, as currently it includes all the changes introduced in the first PR too.)
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/sparse/_base.py b/scipy/sparse/_base.py
index 295848ac52de7ba30dc53be448ce096cb812cc43..6f2d804c2cb0dd2239836b071418969681a8670e 100644
--- a/scipy/sparse/_base.py
+++ b/scipy/sparse/_base.py
@@ -685,8 +685,7 @@ class _spbase:
 
             return result
 
-        else:
-            raise ValueError('could not interpret dimensions')
+        return NotImplemented
 
     def __mul__(self, other):
         return self.multiply(other)
diff --git a/scipy/sparse/_coo.py b/scipy/sparse/_coo.py
index 64c2a65711702fa475b6a5c4abc15f596cbaa7d8..08d737428b303c57ca533dc009bcd70c7812f762 100644
--- a/scipy/sparse/_coo.py
+++ b/scipy/sparse/_coo.py
@@ -12,12 +12,13 @@ import numpy as np
 from .._lib._util import copy_if_needed
 from ._matrix import spmatrix
 from ._sparsetools import (coo_tocsr, coo_todense, coo_todense_nd,
-                           coo_matvec, coo_matvec_nd, coo_matmat_dense)
+                           coo_matvec, coo_matvec_nd, coo_matmat_dense,
+                           coo_matmat_dense_nd)
 from ._base import issparse, SparseEfficiencyWarning, _spbase, sparray
 from ._data import _data_matrix, _minmax_mixin
 from ._sputils import (upcast_char, to_native, isshape, getdtype,
                        getdata, downcast_intp_index, get_index_dtype,
-                       check_shape, check_reshape_kwargs, isscalarlike)
+                       check_shape, check_reshape_kwargs, isscalarlike, isdense)
 
 import operator
 
@@ -654,8 +655,51 @@ class _coo_base(_data_matrix, _minmax_mixin):
         return result
 
 
+    def _rmatmul_dispatch(self, other):
+        if isscalarlike(other):
+            return self._mul_scalar(other)
+        else:
+            # Don't use asarray unless we have to
+            try:
+                o_ndim = other.ndim
+            except AttributeError:
+                other = np.asarray(other)
+                o_ndim = other.ndim
+            perm = tuple(range(o_ndim)[:-2]) + tuple(range(o_ndim)[-2:][::-1])
+            tr = other.transpose(perm)
+            
+            s_ndim = self.ndim
+            perm = tuple(range(s_ndim)[:-2]) + tuple(range(s_ndim)[-2:][::-1])
+            ret = self.transpose(perm)._matmul_dispatch(tr)
+            if ret is NotImplemented:
+                return NotImplemented
+            
+            if s_ndim == 1 or o_ndim == 1:
+                perm = range(ret.ndim)
+            else:
+                perm = tuple(range(ret.ndim)[:-2]) + tuple(range(ret.ndim)[-2:][::-1])
+            return ret.transpose(perm)
+        
+
     def _matmul_dispatch(self, other):
-        if self.ndim < 3:
+        if isscalarlike(other):
+            return self.multiply(other)
+        
+        if not (issparse(other) or isdense(other)):
+            # If it's a list or whatever, treat it like an array
+            other_a = np.asanyarray(other)
+
+            if other_a.ndim == 0 and other_a.dtype == np.object_:
+                # Not interpretable as an array; return NotImplemented so that
+                # other's __rmatmul__ can kick in if that's implemented.
+                return NotImplemented
+
+            try:
+                other.shape
+            except AttributeError:
+                other = other_a
+
+        if self.ndim < 3 and other.ndim < 3:
             return _spbase._matmul_dispatch(self, other)
 
         N = self.shape[-1]
@@ -669,54 +713,91 @@ class _coo_base(_data_matrix, _minmax_mixin):
             if other.ndim == 1:
                 msg = f"{err_prefix} (n,k={N}),(k={other.shape[0]},)->(n,)"
                 raise ValueError(msg)
-            msg = "n-D matrix-matrix multiplication not implemented for ndim>2"
-            raise NotImplementedError(msg)
-
+            if other.shape[-2] == N:
+                # check for batch dimensions compatibility
+                batch_shape_A = self.shape[:-2]
+                batch_shape_B = other.shape[:-2]
+                if batch_shape_A != batch_shape_B:
+                    try:
+                        # This will raise an error if the shapes are not broadcastable
+                        np.broadcast_shapes(batch_shape_A, batch_shape_B)
+                    except ValueError:
+                        raise ValueError("Batch dimensions are not broadcastable")
+            
+                return self._matmul_multivector(other)
+            else:
+                raise ValueError(
+                    f"{err_prefix} (n,..,k={N}),(k={other.shape[-2]},..,m)->(n,..,m)"
+                )
+        
+            
         if isscalarlike(other):
             # scalar value
             return self._mul_scalar(other)
 
         if issparse(other):
-            raise NotImplementedError("sparse-sparse matmul not implemented for ndim>2")
+            self_is_1d = self.ndim == 1
+            other_is_1d = other.ndim == 1
 
-        # If it's a list or whatever, treat it like an array
-        other_a = np.asanyarray(other)
+            # reshape to 2-D if self or other is 1-D
+            if self_is_1d:
+                self = self.reshape(self._shape_as_2d) # prepend 1 to shape
 
-        if other_a.ndim == 0 and other_a.dtype == np.object_:
-            # Not interpretable as an array; return NotImplemented so that
-            # other's __rmatmul__ can kick in if that's implemented.
-            return NotImplemented
+            if other_is_1d:
+                other = other.reshape((other.shape[0], 1)) # append 1 to shape
 
-        try:
-            other.shape
-        except AttributeError:
-            other = other_a
-
-        if other.ndim == 1 or other.ndim == 2 and other.shape[1] == 1:
-            # dense row or column vector
-            if other.shape[0] != N:
+            # Check if the inner dimensions match for matrix multiplication
+            if N != other.shape[-2]:
                 raise ValueError(
-                    f"{err_prefix} (n,k={N}),(k={other.shape[0]},1?)->(n,1?)"
+                    f"{err_prefix} (n,..,k={N}),(k={other.shape[-2]},..,m)->(n,..,m)"
                 )
-
-            result = self._matmul_vector(np.ravel(other))
-
-            if isinstance(other, np.matrix):
-                result = self._ascontainer(result)
-
-            if other.ndim == 2 and other.shape[1] == 1:
-                # If 'other' was an (nx1) column vector, reshape the result
-                result = result.reshape((*self.shape[:-1], 1))
-
+            
+            # If A or B has more than 2 dimensions, check for
+            # batch dimensions compatibility
+            if self.ndim > 2 or other.ndim > 2:
+                batch_shape_A = self.shape[:-2]
+                batch_shape_B = other.shape[:-2]
+                if batch_shape_A != batch_shape_B:
+                    try:
+                        # This will raise an error if the shapes are not broadcastable
+                        np.broadcast_shapes(batch_shape_A, batch_shape_B)
+                    except ValueError:
+                        raise ValueError("Batch dimensions are not broadcastable")
+            
+            result = self._matmul_sparse(other)
+
+            # reshape back if a or b were originally 1-D
+            if self_is_1d:
+                # if self was originally 1-D, reshape result accordingly
+                result = result.reshape(tuple(result.shape[:-2]) +
+                                        tuple(result.shape[-1:]))
+            if other_is_1d:
+                result = result.reshape(result.shape[:-1])
             return result
 
-        else:
-            # dense nD array or matrix ("multivector") not implemented
-            return NotImplemented
-
 
     def _matmul_multivector(self, other):
         result_dtype = upcast_char(self.dtype.char, other.dtype.char)
+        if self.ndim >= 3 or other.ndim >= 3:
+            # if self has shape (N,), reshape to (1,N)
+            if self.ndim == 1:
+                result = self.reshape(1, self.shape[0])._matmul_multivector(other)
+                return result.reshape(tuple(other.shape[:-2]) + tuple(other.shape[-1:]))
+            
+            broadcast_shape = np.broadcast_shapes(self.shape[:-2], other.shape[:-2])
+            self_shape = broadcast_shape + self.shape[-2:]
+            other_shape = broadcast_shape + other.shape[-2:]
+            
+            self = self._broadcast_to(self_shape)
+            other = np.broadcast_to(other, other_shape)
+            result_shape = broadcast_shape + self.shape[-2:-1] + other.shape[-1:]
+            result = np.zeros(result_shape, dtype=result_dtype)
+            coo_matmat_dense_nd(self.nnz, len(self.shape), other.shape[-1],
+                                np.array(other_shape), np.array(result_shape),
+                                np.concatenate(self.coords),
+                                self.data, other.ravel('C'), result)
+            return result
+        
         if self.ndim == 2:
             result_shape = (self.shape[0], other.shape[1])
             col = self.col
@@ -725,16 +806,436 @@ class _coo_base(_data_matrix, _minmax_mixin):
             result_shape = (other.shape[1],)
             col = self.coords[0]
             row = np.zeros_like(col)
-        else:
-            raise NotImplementedError(
-                f"coo_matmat_dense not implemented for ndim={self.ndim}")
-
         result = np.zeros(result_shape, dtype=result_dtype)
         coo_matmat_dense(self.nnz, other.shape[-1], row, col,
                          self.data, other.ravel('C'), result)
         return result.view(type=type(other))
 
 
+    def dot(self, other):
+        if not (issparse(other) or isdense(other) or isscalarlike(other)):
+            # If it's a list or whatever, treat it like an array
+            o_array = np.asanyarray(other)
+
+            if o_array.ndim == 0 and o_array.dtype == np.object_:
+                # Not interpretable as an array; return NotImplemented so that
+                # other's __rmatmul__ can kick in if that's implemented.
+                return NotImplemented
+
+            try:
+                other.shape
+            except AttributeError:
+                other = o_array
+
+        if self.ndim < 3 and (np.isscalar(other) or other.ndim<3):
+            return _spbase.dot(self, other)
+        # Handle scalar multiplication
+        if np.isscalar(other):
+            return self * other
+        if isdense(other):
+            return self._dense_dot(other)
+        elif other.format != "coo":
+            raise TypeError("input must be a COO matrix/array")
+        elif self.ndim == 1 and other.ndim == 1:
+            # Handle inner product of vectors (1-D arrays)
+            if self.shape[0] != other.shape[0]:
+                raise ValueError(f"shapes {self.shape} and {other.shape}"
+                                 " are not aligned for inner product")
+            return self @ other
+        elif self.ndim == 2 and other.ndim == 2:
+            # Handle matrix multiplication (2-D arrays)
+            if self.shape[1] != other.shape[0]:
+                raise ValueError(f"shapes {self.shape} and {other.shape}"
+                                 " are not aligned for matmul")
+            return self @ other
+        else:
+            return self._sparse_dot(other)
+
+    
+    def _sparse_dot(self, other):
+        self_is_1d = self.ndim == 1
+        other_is_1d = other.ndim == 1
+
+        # reshape to 2-D if self or other is 1-D
+        if self_is_1d:
+            self = self.reshape(self._shape_as_2d)  # prepend 1 to shape
+        if other_is_1d:
+            other = other.reshape((other.shape[0], 1))  # append 1 to shape
+
+        if self.shape[-1] != other.shape[-2]:
+                raise ValueError(f"shapes {self.shape} and {other.shape}"
+                                 " are not aligned for n-D dot")
+        
+        # Prepare the tensors for dot operation
+        # Ravel non-reduced axes coordinates
+        self_raveled_coords = _ravel_non_reduced_axes(self.coords,
+                                                      self.shape, [self.ndim-1])
+        other_raveled_coords = _ravel_non_reduced_axes(other.coords,
+                                                       other.shape, [other.ndim-2])
+
+        # Get the shape of the non-reduced axes
+        self_nonreduced_shape = self.shape[:-1]
+        other_nonreduced_shape = other.shape[:-2] + other.shape[-1:]
+        
+        # Create 2D coords arrays
+        ravel_coords_shape_self = (math.prod(self_nonreduced_shape), self.shape[-1])
+        ravel_coords_shape_other = (other.shape[-2], math.prod(other_nonreduced_shape))
+        
+        self_2d_coords = (self_raveled_coords, self.coords[-1])
+        other_2d_coords = (other.coords[-2], other_raveled_coords)
+
+        self_2d = coo_array((self.data, self_2d_coords), ravel_coords_shape_self)
+        other_2d = coo_array((other.data, other_2d_coords), ravel_coords_shape_other)
+        
+        prod = (self_2d @ other_2d).tocoo() # routes via 2-D CSR
+
+        # Combine the shapes of the non-reduced axes
+        combined_shape = self_nonreduced_shape + other_nonreduced_shape
+
+        # Unravel the 2D coordinates to get multi-dimensional coordinates
+        shapes = (self_nonreduced_shape, other_nonreduced_shape)
+        prod_coords = []
+        for c, s in zip(prod.coords, shapes):
+            prod_coords.extend(np.unravel_index(c, s))
+
+        prod_arr = coo_array((prod.data, prod_coords), combined_shape)
+        
+        # reshape back if a or b were originally 1-D
+        # TODO: Move this logic before computation of prod_coords for efficiency
+        if self_is_1d:
+            prod_arr = prod_arr.reshape(combined_shape[1:])
+        if other_is_1d:
+            prod_arr = prod_arr.reshape(combined_shape[:-1])
+
+        return prod_arr
+    
+    def _dense_dot(self, other):
+        self_is_1d = self.ndim == 1
+        other_is_1d = other.ndim == 1
+
+        # reshape to 2-D if self or other is 1-D
+        if self_is_1d:
+            self = self.reshape(self._shape_as_2d)  # prepend 1 to shape
+        if other_is_1d:
+            other = other.reshape((other.shape[0], 1))  # append 1 to shape
+
+        if self.shape[-1] != other.shape[-2]:
+                raise ValueError(f"shapes {self.shape} and {other.shape}"
+                                 " are not aligned for n-D dot")
+
+        new_shape_self = (
+            self.shape[:-1] + (1,) * (len(other.shape) - 1) + self.shape[-1:]
+        )
+        new_shape_other = (1,) * (len(self.shape) - 1) + other.shape
+
+        result_shape = self.shape[:-1] + other.shape[:-2] + other.shape[-1:]
+        result = self.reshape(new_shape_self) @ other.reshape(new_shape_other)
+        prod_arr = result.reshape(result_shape)
+
+        # reshape back if a or b were originally 1-D
+        if self_is_1d:
+            prod_arr = prod_arr.reshape(result_shape[1:])
+        if other_is_1d:
+            prod_arr = prod_arr.reshape(result_shape[:-1])
+
+        return prod_arr
+
+    def tensordot(self, other, axes=2):
+        if not isdense(other) and not issparse(other):
+            # If it's a list or whatever, treat it like an array
+            other_array = np.asanyarray(other)
+
+            if other_array.ndim == 0 and other_array.dtype == np.object_:
+                # Not interpretable as an array; return NotImplemented so that
+                # other's __rmatmul__ can kick in if that's implemented.
+                return NotImplemented
+
+            try:
+                other.shape
+            except AttributeError:
+                other = other_array
+
+        axes_self, axes_other = _process_axes(self.ndim, other.ndim, axes)
+
+        # Check for shape compatibility along specified axes
+        if any(self.shape[ax] != other.shape[bx]
+               for ax, bx in zip(axes_self, axes_other)):
+            raise ValueError("sizes of the corresponding axes must match")
+        
+        if isdense(other):
+            return self._dense_tensordot(other, axes_self, axes_other)
+        else:
+            return self._sparse_tensordot(other, axes_self, axes_other)
+
+
+    def _sparse_tensordot(self, other, axes_self, axes_other):
+        ndim_self = len(self.shape)
+        ndim_other = len(other.shape)
+
+        # Prepare the tensors for tensordot operation       
+        # Ravel non-reduced axes coordinates
+        self_non_red_coords = _ravel_non_reduced_axes(self.coords, self.shape,
+                                                      axes_self)
+        self_reduced_coords = np.ravel_multi_index(
+            [self.coords[ax] for ax in axes_self], [self.shape[ax] for ax in axes_self])
+        other_non_red_coords = _ravel_non_reduced_axes(other.coords, other.shape,
+                                                       axes_other)
+        other_reduced_coords = np.ravel_multi_index(
+            [other.coords[a] for a in axes_other], [other.shape[a] for a in axes_other]
+        )
+        # Get the shape of the non-reduced axes
+        self_nonreduced_shape = tuple(self.shape[ax] for ax in range(ndim_self)
+                              if ax not in axes_self)
+        other_nonreduced_shape = tuple(other.shape[ax] for ax in range(ndim_other)
+                               if ax not in axes_other)
+        
+        # Create 2D coords arrays
+        ravel_coords_shape_self = (math.prod(self_nonreduced_shape),
+                                math.prod([self.shape[ax] for ax in axes_self]))
+        ravel_coords_shape_other = (math.prod([other.shape[ax] for ax in axes_other]),
+                                    math.prod(other_nonreduced_shape))
+
+        self_2d_coords = (self_non_red_coords, self_reduced_coords)
+        other_2d_coords = (other_reduced_coords, other_non_red_coords)
+
+        self_2d = coo_array((self.data, self_2d_coords), ravel_coords_shape_self)
+        other_2d = coo_array((other.data, other_2d_coords), ravel_coords_shape_other)
+
+        # Perform matrix multiplication (routed via 2-D CSR)
+        prod = (self_2d @ other_2d).tocoo()
+
+        # Combine the shapes of the non-contracted axes
+        combined_shape = self_nonreduced_shape + other_nonreduced_shape
+
+        # Unravel the 2D coordinates to get multi-dimensional coordinates
+        coords = []
+        for c, s in zip(prod.coords, (self_nonreduced_shape, other_nonreduced_shape)):
+            if s:
+                coords.extend(np.unravel_index(c, s))
+
+        if coords == []:  # if result is scalar
+            return sum(prod.data)
+            
+        # Construct the resulting COO array with combined coordinates and shape
+        return coo_array((prod.data, coords), shape=combined_shape)
+
+
+    def _dense_tensordot(self, other, axes_self, axes_other):
+        ndim_self = len(self.shape)
+        ndim_other = len(other.shape)
+
+        non_reduced_axes_self = [ax for ax in range(ndim_self) if ax not in axes_self]
+        reduced_shape_self = [self.shape[s] for s in axes_self]
+        non_reduced_shape_self = [self.shape[s] for s in non_reduced_axes_self]
+
+        non_reduced_axes_other = [ax for ax in range(ndim_other)
+                                  if ax not in axes_other]
+        reduced_shape_other = [other.shape[s] for s in axes_other]
+        non_reduced_shape_other = [other.shape[s] for s in non_reduced_axes_other]
+
+        permute_self = non_reduced_axes_self + axes_self
+        permute_other = (
+            non_reduced_axes_other[:-1] + axes_other + non_reduced_axes_other[-1:]
+        )
+        self = self.transpose(permute_self)
+        other = np.transpose(other, permute_other)
+
+        reshape_self = (*non_reduced_shape_self, math.prod(reduced_shape_self))
+        reshape_other = (*non_reduced_shape_other[:-1], math.prod(reduced_shape_other),
+                        *non_reduced_shape_other[-1:])
+
+        return self.reshape(reshape_self).dot(other.reshape(reshape_other))
+
+
+    def _matmul_sparse(self, other):
+        """
+        Perform sparse-sparse matrix multiplication for two n-D COO arrays.
+        The method converts input n-D arrays to 2-D block array format,
+        uses csr_matmat to multiply them, and then converts the
+        result back to n-D COO array.
+        
+        Parameters:
+        self (COO): The first n-D sparse array in COO format.
+        other (COO): The second n-D sparse array in COO format.
+        
+        Returns:
+        prod (COO): The resulting n-D sparse array after multiplication.
+        """
+        if self.ndim < 3 and other.ndim < 3:
+            return _spbase._matmul_sparse(self, other)
+
+        # Get the shapes of self and other
+        self_shape = self.shape
+        other_shape = other.shape
+        
+        # Determine the new shape to broadcast self and other
+        broadcast_shape = np.broadcast_shapes(self_shape[:-2], other_shape[:-2])
+        self_new_shape = tuple(broadcast_shape) + self_shape[-2:]
+        other_new_shape = tuple(broadcast_shape) + other_shape[-2:]
+
+        self_broadcasted = self._broadcast_to(self_new_shape)
+        other_broadcasted = other._broadcast_to(other_new_shape)
+        
+        # Convert n-D COO arrays to 2-D block diagonal arrays
+        self_block_diag = _block_diag(self_broadcasted)
+        other_block_diag = _block_diag(other_broadcasted)
+        
+        # Use csr_matmat to perform sparse matrix multiplication
+        prod_block_diag = (self_block_diag @ other_block_diag).tocoo()
+        
+        # Convert the 2-D block diagonal array back to n-D
+        return _extract_block_diag(
+            prod_block_diag,
+            shape=(*broadcast_shape, self.shape[-2], other.shape[-1]),
+        )
+
+
+    def _broadcast_to(self, new_shape, copy=False):
+        if self.shape == new_shape:
+            return self.copy() if copy else self
+        
+        old_shape = self.shape
+
+        # Check if the new shape is compatible for broadcasting
+        if len(new_shape) < len(old_shape):
+            raise ValueError("New shape must have at least as many dimensions"
+                             " as the current shape")
+        
+        # Add leading ones to shape to ensure same length as `new_shape` 
+        shape = (1,) * (len(new_shape) - len(old_shape)) + tuple(old_shape)
+        
+        # Ensure the old shape can be broadcast to the new shape
+        if any((o != 1 and o != n) for o, n in zip(shape, new_shape)):
+            raise ValueError(f"current shape {old_shape} cannot be "
+                             "broadcast to new shape {new_shape}")
+
+        # Reshape the COO array to match the new dimensions
+        self = self.reshape(shape)
+
+        coords = self.coords
+        new_data = self.data
+        new_coords = coords[-1:]  # Copy last coordinate to start
+        cum_repeat = 1 # Cumulative repeat factor for broadcasting
+        
+        if shape[-1] != new_shape[-1]: # broadcasting the n-th (col) dimension
+            repeat_count = new_shape[-1]
+            cum_repeat *= repeat_count
+            new_data = np.tile(new_data, repeat_count)
+            new_dim = np.repeat(np.arange(0, repeat_count), self.nnz)
+            new_coords = (new_dim,)
+        
+        for i in range(-2, -(len(shape)+1), -1):
+            if shape[i] != new_shape[i]:
+                repeat_count = new_shape[i] # number of times to repeat data, coords
+                cum_repeat *= repeat_count # update cumulative repeat factor
+                nnz = len(new_data) # Number of non-zero elements so far
+
+                # Tile data and coordinates to match the new repeat count
+                new_data = np.tile(new_data, repeat_count)
+                new_coords = tuple(np.tile(new_coords[i+1:], repeat_count))
+
+                # Create new dimensions and stack them
+                new_dim = np.repeat(np.arange(0, repeat_count), nnz)
+                new_coords = (new_dim,) + new_coords
+            else:
+                # If no broadcasting needed, tile the coordinates
+                new_dim = np.tile(coords[i], cum_repeat)
+                new_coords = (new_dim,) + new_coords
+                
+        return coo_array((new_data, new_coords), new_shape)
+        
+
+def _block_diag(self):
+    """
+    Converts an N-D COO array into a 2-D COO array in block diagonal form.
+
+    Parameters:
+    self (coo_array): An N-Dimensional COO sparse array.
+
+    Returns:
+    coo_array: A 2-Dimensional COO sparse array in block diagonal form.
+    """
+    if self.ndim<2:
+        raise ValueError("array must have atleast dim=2")
+    num_blocks = math.prod(self.shape[:-2])
+    n_col = self.shape[-1]
+    n_row = self.shape[-2]
+    res_arr = self.reshape((num_blocks, n_row, n_col))
+    new_coords = (
+        res_arr.coords[1] + res_arr.coords[0] * res_arr.shape[1],
+        res_arr.coords[2] + res_arr.coords[0] * res_arr.shape[2],
+    )
+
+    new_shape = (num_blocks * n_row, num_blocks * n_col)
+    return coo_array((self.data, tuple(new_coords)), shape=new_shape)
+
+
+def _extract_block_diag(self, shape):
+    n_row, n_col = shape[-2], shape[-1]
+
+    # Extract data and coordinates from the block diagonal COO array
+    data = self.data
+    row, col = self.row, self.col
+
+    # Initialize new coordinates array
+    new_coords = np.empty((len(shape), self.nnz), dtype=int)
+    
+    # Calculate within-block indices
+    new_coords[-2] = row % n_row
+    new_coords[-1] = col % n_col
+
+    # Calculate coordinates for higher dimensions
+    temp_block_idx = row // n_row
+    for i in range(len(shape) - 3, -1, -1):
+        size = shape[i]
+        new_coords[i] = temp_block_idx % size
+        temp_block_idx = temp_block_idx // size
+
+    # Create the new COO array with the original n-D shape
+    return coo_array((data, tuple(new_coords)), shape=shape)
+
+
+def _process_axes(ndim_a, ndim_b, axes):
+    if isinstance(axes, int):
+        if axes < 1 or axes > min(ndim_a, ndim_b):
+            raise ValueError("axes integer is out of bounds for input arrays")
+        axes_a = list(range(ndim_a - axes, ndim_a))
+        axes_b = list(range(axes))
+    elif isinstance(axes, (tuple, list)):
+        if len(axes) != 2:
+            raise ValueError("axes must be a tuple/list of length 2")
+        axes_a, axes_b = axes
+        if len(axes_a) != len(axes_b):
+            raise ValueError("axes lists/tuples must be of the same length")
+        if any(ax >= ndim_a or ax < -ndim_a for ax in axes_a) or \
+           any(bx >= ndim_b or bx < -ndim_b for bx in axes_b):
+            raise ValueError("axes indices are out of bounds for input arrays")
+    else:
+        raise TypeError("axes must be an integer or a tuple/list of integers")
+    
+    axes_a = [axis + ndim_a if axis < 0 else axis for axis in axes_a]
+    axes_b = [axis + ndim_b if axis < 0 else axis for axis in axes_b]
+    return axes_a, axes_b
+
+
+def _ravel_non_reduced_axes(coords, shape, axes):
+    ndim = len(shape)
+    non_reduced_axes = [ax for ax in range(ndim) if ax not in axes]
+
+    if not non_reduced_axes:
+        # Return an array with one row
+        return np.zeros_like(coords[0])
+    
+    # Extract the shape of the non-reduced axes
+    non_reduced_shape = [shape[ax] for ax in non_reduced_axes]
+    
+    # Extract the coordinates of the non-reduced axes
+    non_reduced_coords = tuple(coords[idx] for idx in non_reduced_axes)
+    
+    # Ravel the coordinates into 1D
+    return np.ravel_multi_index(non_reduced_coords, non_reduced_shape)
+
+
 def _ravel_coords(coords, shape, order='C'):
     """Like np.ravel_multi_index, but avoids some overflow issues."""
     if len(coords) == 1:
diff --git a/scipy/sparse/_generate_sparsetools.py b/scipy/sparse/_generate_sparsetools.py
index c34195eab0fb7264c16c17095ebd9d193eac52cf..cc946db4cd45deaeb95a81449644e2553b0ea7c1 100644
--- a/scipy/sparse/_generate_sparsetools.py
+++ b/scipy/sparse/_generate_sparsetools.py
@@ -124,6 +124,7 @@ coo_todense_nd      v IllIT*Ti
 coo_matvec          v lIITT*T
 coo_matvec_nd       v llIITT*T
 coo_matmat_dense    v llIITT*T
+coo_matmat_dense_nd v lllIIITT*T
 dia_matvec          v iiiiITT*T
 cs_graph_components i iII*I
 """
diff --git a/scipy/sparse/sparsetools/coo.h b/scipy/sparse/sparsetools/coo.h
index e87dffce51b3ac3780728c8a5789a6d2e6cfe53d..9b6be5dbdada8176405fbd68fd1da8bc65b99b68 100644
--- a/scipy/sparse/sparsetools/coo.h
+++ b/scipy/sparse/sparsetools/coo.h
@@ -258,4 +258,71 @@ void coo_matmat_dense(const npy_int64 nnz,
     }
 }
 
+
+/*
+ *
+ * Input Arguments:
+ *   npy_int64  nnz           - number of nonzeros in A
+ *   npy_int64  n_dim         - number of dimensions of A
+ *   npy_int64  n_col_B       - number of columns in B
+ *   I  shape_B[]             - shape of B
+ *   I  shape_Y[]             - shape of result Y
+ *   I  A_coords[]            - flattened coordinates of A of shape (n_dim * nnz)
+ *   T  Ax[nnz]               - nonzero values of A
+ *   T  Bx[]                  - input tensor B flattened
+ *
+ * Output Arguments:
+ *   T  Yx[]                  - output tensor flattened
+ *
+ * Notes:
+ *   Output array Yx must be preallocated
+ * 
+ */
+template <class I, class T>
+void coo_matmat_dense_nd(const npy_int64 nnz,
+                         const npy_int64 n_dim,
+                         const npy_int64 n_col_B,
+                         const I shape_B[],
+                         const I shape_Y[],
+                         const I A_coords[],
+                         const T Ax[],
+                         const T Bx[],
+                         T Yx[])
+{
+    std::vector<npy_int64> strides_B(n_dim);
+    std::vector<npy_int64> strides_Y(n_dim);
+    std::vector<npy_int64> dim_nnz(n_dim);
+
+    strides_B[n_dim - 1] = 1;
+    strides_Y[n_dim - 1] = 1;
+    dim_nnz[n_dim - 1] = (n_dim - 1) * nnz;
+    for (npy_int64 i = n_dim - 2; i >= 0; --i) {
+        strides_B[i] = strides_B[i + 1] * shape_B[i + 1];
+        strides_Y[i] = strides_Y[i + 1] * shape_Y[i + 1];
+        dim_nnz[i] = i * nnz;
+    }
+    
+    // Iterate over all non-zero elements
+    for (npy_int64 n = 0; n < nnz; ++n) {
+        const T x = Ax[n];
+        if (x != 0) {
+            // Compute the offset in the output tensor Y
+            npy_int64 src_offset = 0;
+            npy_int64 dst_offset = 0;
+            for (npy_int64 dim = 0; dim < n_dim-2; ++dim) {
+                src_offset += A_coords[dim_nnz[dim] + n] * strides_B[dim];
+                dst_offset += A_coords[dim_nnz[dim] + n] * strides_Y[dim];
+            }
+           
+            dst_offset += n_col_B * A_coords[dim_nnz[n_dim - 2] + n];
+            src_offset += n_col_B * A_coords[dim_nnz[n_dim - 1] + n];
+            
+            // Multiply and accumulate in the output tensor Y
+            for (npy_int64 i = 0; i < n_col_B; ++i) {
+                Yx[dst_offset + i] += x * Bx[src_offset + i];
+            }
+        }
+    }
+}
+
 #endif
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/sparse/tests/test_coo.py b/scipy/sparse/tests/test_coo.py
index 628f4a851cdb18c15687f4b635c1b60137d593a9..6e7f97bcd6461a6cb718ba892a397b985e034555 100644
--- a/scipy/sparse/tests/test_coo.py
+++ b/scipy/sparse/tests/test_coo.py
@@ -1,7 +1,9 @@
 import numpy as np
 from numpy.testing import assert_equal
 import pytest
+from scipy.linalg import block_diag
 from scipy.sparse import coo_array, random_array
+from .._coo import _block_diag, _extract_block_diag
 
 
 def test_shape_constructor():
@@ -265,14 +267,6 @@ def test_sum_duplicates():
     assert arr1d.nnz == 2
     assert_equal(arr1d.toarray(), np.array([2, 4]))
 
-    # 2d case
-    arr2d = coo_array(([1, 2, 3, 4], ([0, 0, 1, 1], [1, 1, 0, 1])))
-    assert arr2d.nnz == 4
-    assert_equal(arr2d.toarray(), np.array([[0, 3], [3, 4]]))
-    arr2d.sum_duplicates()
-    assert arr2d.nnz == 3
-    assert_equal(arr2d.toarray(), np.array([[0, 3], [3, 4]]))
-
     # 4d case
     arr4d = coo_array(([2, 3, 7], ([1, 0, 1], [0, 2, 0], [1, 2, 1], [1, 0, 1])))
     assert arr4d.nnz == 3
@@ -286,7 +280,7 @@ def test_sum_duplicates():
     assert_equal(arr4d.toarray(), expected)
 
     # when there are no duplicates
-    arr_nodups = coo_array(([1, 2, 3, 4], ([0, 0, 1, 1], [0, 1, 0, 1])))
+    arr_nodups = coo_array(([1, 2, 3, 4], ([0, 1, 2, 3],)))
     assert arr_nodups.nnz == 4
     arr_nodups.sum_duplicates()
     assert arr_nodups.nnz == 4
@@ -304,31 +298,6 @@ def test_eliminate_zeros():
     assert_equal(arr1d.col, np.array([1]))
     assert_equal(arr1d.row, np.array([0]))
 
-    # for 2d sparse arrays
-    arr2d_a = coo_array(([1, 0, 3], ([0, 1, 1], [0, 1, 2])))
-    assert arr2d_a.nnz == 3
-    assert arr2d_a.count_nonzero() == 2
-    assert_equal(arr2d_a.toarray(), np.array([[1, 0, 0], [0, 0, 3]]))
-    arr2d_a.eliminate_zeros()
-    assert arr2d_a.nnz == 2
-    assert arr2d_a.count_nonzero() == 2
-    assert_equal(arr2d_a.toarray(), np.array([[1, 0, 0], [0, 0, 3]]))
-    assert_equal(arr2d_a.col, np.array([0, 2]))
-    assert_equal(arr2d_a.row, np.array([0, 1]))
-
-    # for 2d sparse arrays (when the 0 data element is the only
-    # element in the last row and last column)
-    arr2d_b = coo_array(([1, 3, 0], ([0, 1, 1], [0, 1, 2])))
-    assert arr2d_b.nnz == 3
-    assert arr2d_b.count_nonzero() == 2
-    assert_equal(arr2d_b.toarray(), np.array([[1, 0, 0], [0, 3, 0]]))
-    arr2d_b.eliminate_zeros()
-    assert arr2d_b.nnz == 2
-    assert arr2d_b.count_nonzero() == 2
-    assert_equal(arr2d_b.toarray(), np.array([[1, 0, 0], [0, 3, 0]]))
-    assert_equal(arr2d_b.col, np.array([0, 1]))
-    assert_equal(arr2d_b.row, np.array([0, 1]))
-
 
 def test_1d_add_dense():
     den_a = np.array([0, -2, -3, 0])
@@ -405,18 +374,16 @@ def test_1d_diagonal():
         coo_array(den).diagonal()
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (7,), (0,0), (2,0), (4,7),
-                                   (0,0,0), (3,6,2), (5,10,3,13), (1,0,3),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_todense(shape):
     np.random.seed(12)
     arr = np.random.randint(low=0, high=5, size=shape)
     assert_equal(coo_array(arr).todense(), arr)
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (2,), (4,), (7,), (12,),
-                                   (0,0), (2,0), (3,3), (4,7), (8,6),
-                                   (0,0,0), (3,6,2), (3,9,4,5,2,1,6),
-                                   (4,4,4,4,4), (5,10,3,13), (1,0,0,3),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_sparse_constructor(shape):
     empty_arr = coo_array(shape)
     res = coo_array(empty_arr)
@@ -424,10 +391,8 @@ def test_nd_sparse_constructor(shape):
     assert_equal(res.toarray(), np.zeros(shape))
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (2,), (4,), (7,), (12,),
-                                   (0,0), (2,0), (3,3), (4,7), (8,6),
-                                   (0,0,0), (3,6,2), (3,9,4,5,2,1,6),
-                                   (4,4,4,4,4), (5,10,3,13), (1,0,0,3),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_tuple_constructor(shape):
     np.random.seed(12)
     arr = np.random.randn(*shape)
@@ -436,10 +401,8 @@ def test_nd_tuple_constructor(shape):
     assert_equal(res.toarray(), arr)
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (2,), (4,), (7,), (12,),
-                                   (0,0), (2,0), (3,3), (4,7), (8,6),
-                                   (0,0,0), (3,6,2), (3,9,4,5,2,1,6),
-                                   (4,4,4,4,4), (5,10,3,13), (1,0,0,3),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_tuple_constructor_with_shape(shape):
     np.random.seed(12)
     arr = np.random.randn(*shape)
@@ -451,11 +414,11 @@ def test_nd_tuple_constructor_with_shape(shape):
 def test_tuple_constructor_for_dim_size_zero():
     # arrays with a dimension of size 0
     with pytest.raises(ValueError, match='exceeds matrix dimension'):
-        coo_array(([9,8], ([1,2],[1,0])), shape=(4,0))
-
-    empty_arr = coo_array(([], ([],[])), shape=(4,0))
-    assert_equal(empty_arr.toarray(), np.empty((4,0)))
+        coo_array(([9, 8], ([1, 2], [1, 0], [2, 1])), shape=(3,4,0))
 
+    empty_arr = coo_array(([], ([], [], [], [])), shape=(4,0,2,3))
+    assert_equal(empty_arr.toarray(), np.empty((4,0,2,3)))
+    
 
 @pytest.mark.parametrize(('shape', 'new_shape'), [((4,9,6,5), (3,6,15,4)),
                                                   ((4,9,6,5), (36,30)),
@@ -475,8 +438,8 @@ def test_nd_reshape(shape, new_shape):
     assert_equal(res_arr.toarray(), exp_arr)
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (3,), (7,), (0,0), (5,12),
-                                   (8,7,3), (7,9,3,2,4,5),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_nnz(shape):
     rng = np.random.default_rng(23409823)
 
@@ -484,8 +447,8 @@ def test_nd_nnz(shape):
     assert arr.nnz == np.count_nonzero(arr.toarray())
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (3,), (7,), (0,0), (5,12),
-                                   (8,7,3), (7,9,3,2,4,5),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_transpose(shape):
     rng = np.random.default_rng(23409823)
 
@@ -541,8 +504,8 @@ def test_nd_eliminate_zeros():
     assert_equal(arr5d.coords, ([], [], [], [], []))
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (3,), (7,), (0,0), (5,12),
-                                   (8,7,3), (7,9,3,2,4),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_add_dense(shape):
     rng = np.random.default_rng(23409823)
     sp_x = random_array(shape, density=0.6, rng=rng, dtype=int)
@@ -554,8 +517,8 @@ def test_nd_add_dense(shape):
     assert_equal(res, exp)
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (3,), (7,), (0,0), (5,12),
-                                   (8,7,3), (7,9,3,2,4),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_add_sparse(shape):
     rng = np.random.default_rng(23409823)
     sp_x = random_array((shape), density=0.6, rng=rng, dtype=int)
@@ -589,8 +552,8 @@ def test_nd_add_sparse_with_inconsistent_shapes(a_shape, b_shape):
         arr_a + arr_b
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (3,), (7,), (0,0), (5,12),
-                                   (8,7,3), (7,9,3,2,4),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_sub_dense(shape):
     rng = np.random.default_rng(23409823)
     sp_x = random_array(shape, density=0.6, rng=rng, dtype=int)
@@ -602,8 +565,8 @@ def test_nd_sub_dense(shape):
     assert_equal(res, exp)
 
 
-@pytest.mark.parametrize('shape', [(0,), (1,), (3,), (7,), (0,0), (5,12),
-                                   (8,7,3), (7,9,3,2,4),])
+@pytest.mark.parametrize('shape', [(0,), (7,), (4,7), (0,0,0), (3,6,2),
+                                   (1,0,3), (7,9,3,2,4,5)])
 def test_nd_sub_sparse(shape):
     rng = np.random.default_rng(23409823)
 
@@ -660,3 +623,201 @@ def test_nd_matmul_vector(mat_shape, vec_shape):
     assert_equal(res,exp)
     res = sp_x @ list(den_y)
     assert_equal(res,exp)
+
+
+mat_mat_shapes = [
+    ((2, 3, 4, 5), (2, 3, 5, 7)), 
+    ((0, 0), (0,)), 
+    ((4, 4, 2, 0), (0,)),
+    ((7, 8, 3), (3,)),
+    ((7, 8, 3), (3, 1)),
+    ((6, 5, 3, 2, 4), (4, 3)),
+    ((1, 3, 2, 4), (6, 5, 1, 4, 3)),
+    ((6, 1, 1, 2, 4), (1, 3, 4, 3)),
+    ((4,), (2, 4, 3)),
+    ((3,), (5, 6, 7, 3, 2)),
+    ((4,), (4, 3)),
+    ((2, 5), (5, 1)),
+]
+@pytest.mark.parametrize(('mat_shape1', 'mat_shape2'), mat_mat_shapes)
+def test_nd_matmul(mat_shape1, mat_shape2):
+    rng = np.random.default_rng(23409823)
+
+    sp_x = random_array(mat_shape1, density=0.6, random_state=rng, dtype=int)
+    sp_y = random_array(mat_shape2, density=0.6, random_state=rng, dtype=int)
+    den_x, den_y = sp_x.toarray(), sp_y.toarray()
+    exp = den_x @ den_y
+    # sparse-sparse
+    res = sp_x @ sp_y
+    assert_equal(res.toarray(), exp)
+    # sparse-dense
+    res = sp_x @ den_y
+    assert_equal(res, exp)
+    res = sp_x @ list(den_y)
+    assert_equal(res, exp)
+
+    # dense-sparse
+    res = den_x @ sp_y
+    assert_equal(res, exp)
+
+
+def test_nd_matmul_sparse_with_inconsistent_arrays():
+    rng = np.random.default_rng(23409823)
+
+    sp_x = random_array((4,5,7,6,3), density=0.6, random_state=rng, dtype=int)
+    sp_y = random_array((1,5,3,2,5), density=0.6, random_state=rng, dtype=int)
+    with pytest.raises(ValueError, match="matmul: dimension mismatch with signature"):
+        sp_x @ sp_y
+    with pytest.raises(ValueError, match="matmul: dimension mismatch with signature"):
+        sp_x @ (sp_y.toarray())
+    
+    sp_z = random_array((1,5,3,2), density=0.6, random_state=rng, dtype=int)
+    with pytest.raises(ValueError, match="Batch dimensions are not broadcastable"):
+        sp_x @ sp_z
+    with pytest.raises(ValueError, match="Batch dimensions are not broadcastable"):
+        sp_x @ (sp_z.toarray())
+
+
+def test_dot_1d_1d(): # 1-D inner product
+    a = coo_array([1,2,3])
+    b = coo_array([4,5,6])
+    exp = np.dot(a.toarray(), b.toarray())
+    res = a.dot(b)
+    assert_equal(res, exp)
+    res = a.dot(b.toarray())
+    assert_equal(res, exp)
+
+
+def test_dot_sparse_scalar():    
+    a = coo_array([[1, 2], [3, 4], [5, 6]])
+    b = 3
+    res = a.dot(b)
+    exp = np.dot(a.toarray(), b)
+    assert_equal(res.toarray(), exp)
+
+
+def test_dot_with_inconsistent_shapes(): 
+    arr_a = coo_array([[[1, 2]], [[3, 4]]])
+    arr_b = coo_array([4, 5, 6])
+    with pytest.raises(ValueError, match="not aligned for n-D dot"):
+        arr_a.dot(arr_b)
+
+
+dot_shapes = [
+    ((3,3), (3,3)), ((4,6), (6,7)), ((1,4), (4,1)), # matrix multiplication 2-D
+    ((3,2,4,7), (7,)), ((5,), (6,3,5,2)), # dot of n-D and 1-D arrays
+    ((3,2,4,7), (7,1)), ((1,5,), (6,3,5,2)),
+    ((4,6), (3,2,6,4)), ((2,8,7), (4,5,7,7,2)), # dot of n-D and m-D arrays
+    ((4,5,7,6), (3,2,6,4)), 
+]
+@pytest.mark.parametrize(('a_shape', 'b_shape'), dot_shapes)
+def test_dot_nd(a_shape, b_shape): 
+    rng = np.random.default_rng(23409823)
+    
+    arr_a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
+    arr_b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)
+
+    exp = np.dot(arr_a.toarray(), arr_b.toarray())
+    # sparse-dense
+    res = arr_a.dot(arr_b.toarray())
+    assert_equal(res, exp)
+    res = arr_a.dot(list(arr_b.toarray()))
+    assert_equal(res, exp)
+    # sparse-sparse
+    res = arr_a.dot(arr_b)
+    assert_equal(res.toarray(), exp)
+
+
+tensordot_shapes_and_axes = [
+    ((4,6), (6,7), ([1], [0])),
+    ((3,2,4,7), (7,), ([3], [0])),
+    ((5,), (6,3,5,2), ([0], [2])),
+    ((4,5,7,6), (3,2,6,4), ([0, 3], [3, 2])),
+    ((2,8,7), (4,5,7,8,2), ([0, 1, 2], [4, 3, 2])),
+    ((4,5,3,2,6), (3,2,6,7,8), 3),
+    ((4,5,7), (7,3,7), 1),
+    ((2,3,4), (2,3,4), ([0, 1, 2], [0, 1, 2])),
+]
+@pytest.mark.parametrize(('a_shape', 'b_shape', 'axes'), tensordot_shapes_and_axes)
+def test_tensordot(a_shape, b_shape, axes): 
+    rng = np.random.default_rng(23409823)
+    
+    arr_a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
+    arr_b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)
+
+    exp = np.tensordot(arr_a.toarray(), arr_b.toarray(), axes=axes)
+
+    # sparse-dense
+    res = arr_a.tensordot(arr_b.toarray(), axes=axes)
+    assert_equal(res, exp)
+    res = arr_a.tensordot(list(arr_b.toarray()), axes=axes)
+    assert_equal(res, exp)
+
+    # sparse-sparse
+    res = arr_a.tensordot(arr_b, axes=axes)
+    if type(res) is coo_array:
+        assert_equal(res.toarray(), exp)
+    else:
+        assert_equal(res, exp)
+        
+
+def test_tensordot_with_invalid_args(): 
+    rng = np.random.default_rng(23409823)
+    
+    arr_a = random_array((3,4,5), density=0.6, random_state=rng, dtype=int)
+    arr_b = random_array((3,4,6), density=0.6, random_state=rng, dtype=int)
+
+    axes = ([2], [2]) # sizes of 2nd axes of both shapes do not match
+    with pytest.raises(ValueError, match="sizes of the corresponding axes must match"):
+        arr_a.tensordot(arr_b, axes=axes)
+
+    arr_a = random_array((5,4,2,3,7), density=0.6, random_state=rng, dtype=int)
+    arr_b = random_array((4,6,3,2), density=0.6, random_state=rng, dtype=int)
+
+    axes = ([2,0,1], [1,3]) # lists have different lengths
+    with pytest.raises(ValueError, match="axes lists/tuples must be of the"
+                       " same length"):
+        arr_a.tensordot(arr_b, axes=axes)
+
+
+@pytest.mark.parametrize(('actual_shape', 'broadcast_shape'),
+                         [((1,3,5,4), (2,3,5,4)), ((2,1,5,4), (6,2,3,5,4)),
+                          ((1,1,7,8,9), (4,5,6,7,8,9)), ((1,3), (4,5,3)),
+                          ((7,8,1), (7,8,5)), ((3,1), (3,4)), ((1,), (5,)),
+                          ((1,1,1), (4,5,6)), ((1,3,1,5,4), (8,2,3,9,5,4)),])
+def test_broadcast_to(actual_shape, broadcast_shape):
+    rng = np.random.default_rng(23409823)
+    
+    arr = random_array(actual_shape, density=0.6, random_state=rng, dtype=int)
+    res = arr._broadcast_to(broadcast_shape)
+    exp = np.broadcast_to(arr.toarray(), broadcast_shape)
+    assert_equal(res.toarray(), exp)
+
+
+@pytest.mark.parametrize(('shape'), [(4,5,6,7,8), (6,4),
+                                     (5,9,3,2), (9,5,2,3,4),])
+def test_block_diag(shape):
+    rng = np.random.default_rng(23409823)
+    sp_x = random_array(shape, density=0.6, random_state=rng, dtype=int)
+    den_x = sp_x.toarray()
+
+    # converting n-d numpy array to an array of slices of 2-D matrices,
+    # to pass as argument into scipy.linalg.block_diag
+    num_slices = int(np.prod(den_x.shape[:-2]))
+    reshaped_array = den_x.reshape((num_slices,) + den_x.shape[-2:])
+    matrices = [reshaped_array[i, :, :] for i in range(num_slices)]
+    exp = block_diag(*matrices)
+
+    res = _block_diag(sp_x)
+
+    assert_equal(res.toarray(), exp)
+
+
+@pytest.mark.parametrize(('shape'), [(4,5,6,7,8), (6,4),
+                                     (5,9,3,2), (9,5,2,3,4),])
+def test_extract_block_diag(shape):
+    rng = np.random.default_rng(23409823)
+    sp_x = random_array(shape, density=0.6, random_state=rng, dtype=int)
+    res = _extract_block_diag(_block_diag(sp_x), shape)
+
+    assert_equal(res.toarray(), sp_x.toarray())
```

## Validation

```json
{
 "test_files": [
  "scipy/sparse/tests/test_coo.py"
 ],
 "collected_before": 185,
 "collected_after": 184,
 "outcomes_before": {
  "ERROR": 185
 },
 "outcomes_after": {
  "PASSED": 184
 },
 "exit_before": 2,
 "exit_after": 0,
 "tail_before": "=========\nplatform linux -- Python 3.12.15, pytest-8.3.4, pluggy-1.5.0 -- /usr/local/bin/python\nhypothesis profile 'deterministic' -> database=None, deadline=None, print_blob=True, derandomize=True, suppress_health_check=[HealthCheck.data_too_large, HealthCheck.filter_too_much, HealthCheck.too_slow, HealthCheck.large_base_example, HealthCheck.function_scoped_fixture, HealthCheck.differing_executors]\nrootdir: /testbed\nconfigfile: pytest.ini\nplugins: hypothesis-6.122.1, xdist-3.6.1, cov-6.0.0, timeout-2.3.1\ncollecting ... collected 0 items / 1 error\n\n==================================== ERRORS ====================================\n_______________ ERROR collecting scipy/sparse/tests/test_coo.py ________________\nImportError while importing test module '/testbed/scipy/sparse/tests/test_coo.py'.\nHint: make sure your test modules/packages have valid Python names.\nTraceback:\n/usr/local/lib/python3.12/importlib/__init__.py:90: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\nscipy/sparse/tests/test_coo.py:6: in <module>\n    from .._coo import _block_diag, _extract_block_diag\nE   ImportError: cannot import name '_block_diag' from 'scipy.sparse._coo' (/testbed/scipy/sparse/_coo.py)\n=========================== short test summary info ============================\nERROR scipy/sparse/tests/test_coo.py\n!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!\n=============================== 1 error in 0.70s ===============================",
 "tail_after": "pe7-axes7]\nPASSED scipy/sparse/tests/test_coo.py::test_tensordot_with_invalid_args\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape0-broadcast_shape0]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape1-broadcast_shape1]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape2-broadcast_shape2]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape3-broadcast_shape3]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape4-broadcast_shape4]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape5-broadcast_shape5]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape6-broadcast_shape6]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape7-broadcast_shape7]\nPASSED scipy/sparse/tests/test_coo.py::test_broadcast_to[actual_shape8-broadcast_shape8]\nPASSED scipy/sparse/tests/test_coo.py::test_block_diag[shape0]\nPASSED scipy/sparse/tests/test_coo.py::test_block_diag[shape1]\nPASSED scipy/sparse/tests/test_coo.py::test_block_diag[shape2]\nPASSED scipy/sparse/tests/test_coo.py::test_block_diag[shape3]\nPASSED scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape0]\nPASSED scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape1]\nPASSED scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape2]\nPASSED scipy/sparse/tests/test_coo.py::test_extract_block_diag[shape3]\n============================= 184 passed in 0.77s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

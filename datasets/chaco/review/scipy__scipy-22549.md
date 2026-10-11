# scipy__scipy-22549

[back to the list](README.md) -- **ENH: use `workers` keyword in `optimize._differentiable_functions.VectorFunction`**

| field | value |
|---|---|
| pull request | [scipy/scipy#22549](https://github.com/scipy/scipy/pull/22549) (created 2025-02-18, merged 2025-03-14) |
| ChaCo lists | full, ablation, f2p30 |
| status | **runnable** -- 1 developer test(s) flip; oracle reproduces it |
| base commit | [`8fabf09d50a8`](https://github.com/scipy/scipy/commit/8fabf09d50a8ee2a20a32673cabee786878f8252) (2025-03-14), first parent of the merge commit |
| merge commit | [`f2445c575828`](https://github.com/scipy/scipy/commit/f2445c5758284ea0739972f476622154ae117b12) |
| issues closed | none |
| version | 1.16 |
| image | `f2p-chaco/scipy__scipy-22549:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-22549.Dockerfile) |
| source files (`patch`) | `scipy/optimize/_differentiable_functions.py`, `scipy/optimize/_numdiff.py` |
| test files (`test_patch`) | `scipy/optimize/tests/test_differentiable_functions.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (1)

- `scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_workers`

## PASS_TO_PASS (16)

<details><summary>show</summary>

- `scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_finite_difference_grad`
- `scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_finite_difference_hess_linear_operator`
- `scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_float_size`
- `scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_fun_and_grad`
- `scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_lowest_x`
- `scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_workers`
- `scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_x_storage_overlap`
- `scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_finite_difference_hess_linear_operator`
- `scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_finite_difference_jac`
- `scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_float_size`
- `scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_x_storage_overlap`
- `scipy/optimize/tests/test_differentiable_functions.py::test_IdentityVectorFunction`
- `scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunction`
- `scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunctionNoReferenceCycle`
- `scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunction_memoization`
- `scipy/optimize/tests/test_differentiable_functions.py::test_ScalarFunctionNoReferenceCycle`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #22549: ENH: use `workers` keyword in `optimize._differentiable_functions.VectorFunction`

This PR adds the `workers` keyword to `VectorFunction`. The workers aid parallel evaluation of the jacobian when using finite differences. The keyword has no effect on the finite difference estimation of the hessian as this is carried out with a `LinearOperator` that only uses a small number of function evaluations.

Parallelising `VectorFunction` is a precursor step to using it in `optimize.least_squares` where its memoisation will reduce the number of function evaluations, as well as allowing the parallelisation of the `lm` method.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/optimize/_differentiable_functions.py b/scipy/optimize/_differentiable_functions.py
index 46d38254a0d16ea4346d64b6c400d4da97e49263..e990dae1ef15dde84ee06bf70d358dcd8331f97e 100644
--- a/scipy/optimize/_differentiable_functions.py
+++ b/scipy/optimize/_differentiable_functions.py
@@ -1,4 +1,6 @@
 from collections import namedtuple
+from functools import partial
+
 import numpy as np
 import scipy.sparse as sps
 from ._numdiff import approx_derivative, group_columns
@@ -12,7 +14,7 @@ from scipy._lib._util import _ScalarFunctionWrapper
 FD_METHODS = ('2-point', '3-point', 'cs')
 
 
-class _GradWrapper:
+class _ScalarGradWrapper:
     """
     Wrapper class for gradient calculation
     """
@@ -49,7 +51,7 @@ class _GradWrapper:
         return g
 
 
-class _HessWrapper:
+class _ScalarHessWrapper:
     """
     Wrapper class for hess calculation via finite differences
     """
@@ -205,8 +207,8 @@ class ScalarFunction:
            will be set. However, a subsequent call with a different argument
            of *any* of the methods may overwrite the attribute.
     """
-    def __init__(self, fun, x0, args, grad, hess, finite_diff_rel_step,
-                 finite_diff_bounds, epsilon=None, workers=None):
+    def __init__(self, fun, x0, args, grad, hess, finite_diff_rel_step=None,
+                 finite_diff_bounds=(-np.inf, np.inf), epsilon=None, workers=None):
 
         if not callable(grad) and grad not in FD_METHODS:
             raise ValueError(
@@ -273,7 +275,7 @@ class ScalarFunction:
         self._update_fun()
 
         # Initial gradient evaluation
-        self._wrapped_grad = _GradWrapper(
+        self._wrapped_grad = _ScalarGradWrapper(
             grad,
             fun=self._wrapped_fun,
             args=args,
@@ -292,7 +294,7 @@ class ScalarFunction:
             self._wrapped_hess = _FakeCounter(ngev=0, nhev=0)
         else:
             if callable(hess):
-                self._wrapped_hess = _HessWrapper(
+                self._wrapped_hess = _ScalarHessWrapper(
                     hess,
                     x0=x0,
                     args=args,
@@ -301,7 +303,7 @@ class ScalarFunction:
                 self.H = self._wrapped_hess.H
                 self.H_updated = True
             elif hess in FD_METHODS:
-                self._wrapped_hess = _HessWrapper(
+                self._wrapped_hess = _ScalarHessWrapper(
                     hess,
                     x0=x0,
                     args=args,
@@ -404,6 +406,10 @@ class ScalarFunction:
         return self.f, self.g
 
 
+def _VectorFunWrapper(fun, x):
+    return np.atleast_1d(fun(x))
+
+
 class VectorFunction:
     """Vector function and its derivatives.
 
@@ -422,8 +428,8 @@ class VectorFunction:
            of *any* of the methods may overwrite the attribute.
     """
     def __init__(self, fun, x0, jac, hess,
-                 finite_diff_rel_step, finite_diff_jac_sparsity,
-                 finite_diff_bounds, sparse_jacobian):
+                 finite_diff_rel_step=None, finite_diff_jac_sparsity=None,
+                 finite_diff_bounds=None, sparse_jacobian=None, workers=None):
         if not callable(jac) and jac not in FD_METHODS:
             raise ValueError(f"`jac` must be either callable or one of {FD_METHODS}.")
 
@@ -456,6 +462,9 @@ class VectorFunction:
         self.J_updated = False
         self.H_updated = False
 
+        # normalize workers
+        workers = workers or map
+
         finite_diff_options = {}
         if jac in FD_METHODS:
             finite_diff_options["method"] = jac
@@ -465,11 +474,17 @@ class VectorFunction:
                 finite_diff_options["sparsity"] = (finite_diff_jac_sparsity,
                                                    sparsity_groups)
             finite_diff_options["bounds"] = finite_diff_bounds
+            finite_diff_options["workers"] = workers
+            finite_diff_options["full_output"] = True
             self.x_diff = np.copy(self.x)
         if hess in FD_METHODS:
             finite_diff_options["method"] = hess
             finite_diff_options["rel_step"] = finite_diff_rel_step
             finite_diff_options["as_linear_operator"] = True
+            # workers is not useful for evaluation of the LinearOperator
+            # produced by approx_derivative. Only two/three function
+            # evaluations are used, and the LinearOperator may persist
+            # outside the scope that workers is valid in.
             self.x_diff = np.copy(self.x)
         if jac in FD_METHODS and hess in FD_METHODS:
             raise ValueError("Whenever the Jacobian is estimated via "
@@ -477,12 +492,10 @@ class VectorFunction:
                              "be estimated using one of the quasi-Newton "
                              "strategies.")
 
-        # Function evaluation
-        def fun_wrapped(x):
-            self.nfev += 1
-            return np.atleast_1d(fun(x))
+        fun_wrapped = partial(_VectorFunWrapper, fun)
 
         def update_fun():
+            self.nfev += 1
             self.f = fun_wrapped(self.x)
 
         self._update_fun_impl = update_fun
@@ -523,34 +536,38 @@ class VectorFunction:
                 self.J = jac_wrapped(self.x)
 
         elif jac in FD_METHODS:
-            self.J = approx_derivative(fun_wrapped, self.x, f0=self.f,
-                                       **finite_diff_options)
+            self.J, dct = approx_derivative(fun_wrapped, self.x, f0=self.f,
+                                            **finite_diff_options)
             self.J_updated = True
+            self.nfev += dct['nfev']
 
             if (sparse_jacobian or
                     sparse_jacobian is None and sps.issparse(self.J)):
                 def update_jac():
                     self._update_fun()
-                    self.J = sps.csr_array(
+                    self.J, dct = sps.csr_array(
                         approx_derivative(fun_wrapped, self.x, f0=self.f,
                                           **finite_diff_options))
+                    self.nfev += dct['nfev']
                 self.J = sps.csr_array(self.J)
                 self.sparse_jacobian = True
 
             elif sps.issparse(self.J):
                 def update_jac():
                     self._update_fun()
-                    self.J = approx_derivative(fun_wrapped, self.x, f0=self.f,
-                                               **finite_diff_options).toarray()
+                    self.J, dct = approx_derivative(fun_wrapped, self.x, f0=self.f,
+                                                    **finite_diff_options).toarray()
+                    self.nfev += dct['nfev']
                 self.J = self.J.toarray()
                 self.sparse_jacobian = False
 
             else:
                 def update_jac():
                     self._update_fun()
-                    self.J = np.atleast_2d(
-                        approx_derivative(fun_wrapped, self.x, f0=self.f,
-                                          **finite_diff_options))
+                    J, dct = approx_derivative(fun_wrapped, self.x, f0=self.f,
+                                               **finite_diff_options)
+                    self.J = np.atleast_2d(J)
+                    self.nfev += dct['nfev']
                 self.J = np.atleast_2d(self.J)
                 self.sparse_jacobian = False
 
@@ -591,6 +608,7 @@ class VectorFunction:
                                            f0=self.J.T.dot(self.v),
                                            args=(self.v,),
                                            **finite_diff_options)
+
             update_hess()
             self.H_updated = True
         elif isinstance(hess, HessianUpdateStrategy):
diff --git a/scipy/optimize/_numdiff.py b/scipy/optimize/_numdiff.py
index fe28b9a83800180aa4a69abdacfadc181e4162a7..98b137ed151a480128874bf662a6e4ec05c044f2 100644
--- a/scipy/optimize/_numdiff.py
+++ b/scipy/optimize/_numdiff.py
@@ -390,7 +390,10 @@ def approx_derivative(fun, x0, method='3-point', rel_step=None, abs_step=None,
         Dictionary containing extra information about the calculation. The
         keys include:
 
-        - `nfev`, number of function evaluations.
+        - `nfev`, number of function evaluations. If `as_linear_operator` is True
+           then `fun` is expected to track the number of evaluations itself.
+           This is because multiple calls may be made to the linear operator which
+           are not trackable here.
 
     See Also
     --------
@@ -555,8 +558,8 @@ def approx_derivative(fun, x0, method='3-point', rel_step=None, abs_step=None,
         if rel_step is None:
             rel_step = _eps_for_method(x0.dtype, f0.dtype, method)
 
-        J, _nfev = _linear_operator_difference(fun_wrapped, x0,
-                                               f0, rel_step, method)
+        J, _ = _linear_operator_difference(fun_wrapped, x0,
+                                           f0, rel_step, method)
     else:
         # by default we use rel_step
         if abs_step is None:
@@ -619,7 +622,7 @@ def _linear_operator_difference(fun, x0, f0, h, method):
     n = x0.size
 
     if method == '2-point':
-        nfev = 1
+        # nfev = 1
         def matvec(p):
             if np.array_equal(p, np.zeros_like(p)):
                 return np.zeros(m)
@@ -629,7 +632,7 @@ def _linear_operator_difference(fun, x0, f0, h, method):
             return df / dx
 
     elif method == '3-point':
-        nfev = 2
+        # nfev = 2
         def matvec(p):
             if np.array_equal(p, np.zeros_like(p)):
                 return np.zeros(m)
@@ -642,7 +645,7 @@ def _linear_operator_difference(fun, x0, f0, h, method):
             return df / dx
 
     elif method == 'cs':
-        nfev = 1
+        # nfev = 1
         def matvec(p):
             if np.array_equal(p, np.zeros_like(p)):
                 return np.zeros(m)
@@ -651,11 +654,10 @@ def _linear_operator_difference(fun, x0, f0, h, method):
             f1 = fun(x)
             df = f1.imag
             return df / dx
-
     else:
         raise RuntimeError("Never be here.")
 
-    return LinearOperator((m, n), matvec), nfev
+    return LinearOperator((m, n), matvec), 0
 
 
 def _dense_difference(fun, x0, f0, h, use_one_sided, method, workers):
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/optimize/tests/test_differentiable_functions.py b/scipy/optimize/tests/test_differentiable_functions.py
index 96bcd5f530f36b419b83fd5958c060c944bac3af..5c16672f73716fe20ea996b6c2bc0fb133eb73da 100644
--- a/scipy/optimize/tests/test_differentiable_functions.py
+++ b/scipy/optimize/tests/test_differentiable_functions.py
@@ -563,6 +563,76 @@ class TestVectorialFunction(TestCase):
         assert_array_almost_equal(f_analit, f_approx)
         assert_array_almost_equal(J_analit, J_approx)
 
+    @pytest.mark.fail_slow(5.0)
+    def test_workers(self):
+        x0 = np.array([2.5, 3.0])
+        ex = ExVectorialFunction()
+        ex2 = ExVectorialFunction()
+        v = np.array([1.0, 2.0])
+
+        with MapWrapper(2) as mapper:
+            approx = VectorFunction(ex.fun, x0, '2-point',
+                                    ex.hess, None, None, (-np.inf, np.inf),
+                                    False, workers=mapper)
+            approx_series = VectorFunction(ex2.fun, x0, '2-point',
+                                           ex2.hess, None, None, (-np.inf, np.inf),
+                                           False)
+
+            assert_allclose(approx.jac(x0), ex.jac(x0))
+            assert_allclose(approx_series.jac(x0), ex.jac(x0))
+            assert_allclose(approx_series.hess(x0, v), ex.hess(x0, v))
+            assert_allclose(approx.hess(x0, v), ex.hess(x0, v))
+            assert_equal(approx.nfev, approx_series.nfev)
+            assert_equal(approx_series.nfev, ex2.nfev)
+            assert_equal(approx.njev, approx_series.njev)
+            assert_equal(approx.nhev, approx_series.nhev)
+            assert_equal(approx_series.nhev, ex2.nhev)
+
+            ex.nfev = ex.njev = ex.nhev = 0
+            ex2.nfev = ex2.njev = ex2.nhev = 0
+            approx = VectorFunction(ex.fun, x0, '3-point',
+                                    ex.hess, None, None, (-np.inf, np.inf),
+                                    False, workers=mapper)
+            approx_series = VectorFunction(ex2.fun, x0, '3-point',
+                                           ex2.hess, None, None, (-np.inf, np.inf),
+                                           False)
+            assert_allclose(approx.jac(x0), ex.jac(x0))
+            assert_allclose(approx_series.jac(x0), ex.jac(x0))
+            assert_allclose(approx_series.hess(x0, v), ex.hess(x0, v))
+            assert_allclose(approx.hess(x0, v), ex.hess(x0, v))
+
+            assert_equal(approx.nfev, approx_series.nfev)
+            assert_equal(approx_series.nfev, ex2.nfev)
+            assert_equal(approx.njev, approx_series.njev)
+            assert_equal(approx.nhev, approx_series.nhev)
+            assert_equal(approx_series.nhev, ex2.nhev)
+
+            # The following tests are somewhat redundant because the LinearOperator
+            # produced by VectorFunction.hess does not use any parallelisation.
+            # The tests are left for completeness, in case that situation changes.
+            ex.nfev = ex.njev = ex.nhev = 0
+            ex2.nfev = ex2.njev = ex2.nhev = 0
+            approx = VectorFunction(ex.fun, x0, ex.jac,
+                                    '2-point', None, None, (-np.inf, np.inf),
+                                    False, workers=mapper)
+            approx_series = VectorFunction(ex2.fun, x0, ex2.jac,
+                                           '2-point', None, None, (-np.inf, np.inf),
+                                           False)
+            assert_allclose(approx.jac(x0), ex.jac(x0))
+            assert_allclose(approx_series.jac(x0), ex.jac(x0))
+
+            H_analit = ex2.hess(x0, v)
+            H_approx_series = approx_series.hess(x0, v)
+            H_approx = approx.hess(x0, v)
+            x = [5, 2.0]
+            assert_allclose(H_approx.dot(x), H_analit.dot(x))
+            assert_allclose(H_approx_series.dot(x), H_analit.dot(x))
+
+            assert_equal(approx.nfev, approx_series.nfev)
+            assert_equal(approx_series.nfev, ex2.nfev)
+            assert_equal(approx.njev, approx_series.njev)
+            assert_equal(approx.nhev, approx_series.nhev)
+
     def test_finite_difference_hess_linear_operator(self):
         ex = ExVectorialFunction()
         nfev = 0
```

## Validation

```json
{
 "image_head": "8fabf09d50a8ee2a20a32673cabee786878f8252",
 "patch_applies": true,
 "test_files": [
  "scipy/optimize/tests/test_differentiable_functions.py"
 ],
 "collected_before": 18,
 "collected_after": 18,
 "outcomes_before": {
  "PASSED": 16,
  "FAILED": 1,
  "XFAIL": 1
 },
 "outcomes_after": {
  "PASSED": 17,
  "XFAIL": 1
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "ctions.py::TestScalarFunction::test_lowest_x\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_workers\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_x_storage_overlap\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_finite_difference_hess_linear_operator\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_finite_difference_jac\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_float_size\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_x_storage_overlap\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunction\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunction_memoization\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_IdentityVectorFunction\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_ScalarFunctionNoReferenceCycle\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunctionNoReferenceCycle\nXFAIL scipy/optimize/tests/test_differentiable_functions.py::test_VectorFunctionNoReferenceCycle - TODO remove reference cycle from VectorFunction\nFAILED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_workers\n=================== 1 failed, 16 passed, 1 xfailed in 2.01s ====================",
 "tail_after": "ctions.py::TestScalarFunction::test_lowest_x\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_workers\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestScalarFunction::test_x_storage_overlap\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_finite_difference_hess_linear_operator\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_finite_difference_jac\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_float_size\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_workers\nPASSED scipy/optimize/tests/test_differentiable_functions.py::TestVectorialFunction::test_x_storage_overlap\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunction\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunction_memoization\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_IdentityVectorFunction\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_ScalarFunctionNoReferenceCycle\nPASSED scipy/optimize/tests/test_differentiable_functions.py::test_LinearVectorFunctionNoReferenceCycle\nXFAIL scipy/optimize/tests/test_differentiable_functions.py::test_VectorFunctionNoReferenceCycle - TODO remove reference cycle from VectorFunction\n======================== 17 passed, 1 xfailed in 1.47s =========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

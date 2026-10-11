# scipy__scipy-21485

[back to the list](README.md) -- **MAINT: interpolate: abstract out barycentric representation of a rational function**

| field | value |
|---|---|
| pull request | [scipy/scipy#21485](https://github.com/scipy/scipy/pull/21485) (created 2024-08-30, merged 2024-08-31) |
| ChaCo lists | full, ablation |
| status | **not-fail-to-pass** -- no developer test fails before the change and passes after (33 pass on both sides) |
| base commit | [`8cbd7b58432e`](https://github.com/scipy/scipy/commit/8cbd7b58432e25b2dec1e62ba8e5b800b16ed4e1) (2024-08-30), first parent of the merge commit |
| merge commit | [`a5b40f380223`](https://github.com/scipy/scipy/commit/a5b40f380223b47ed3ec26024f7cf7c4e808b36b) |
| issues closed | none |
| version | 1.15 |
| image | `f2p-chaco/scipy__scipy-21485:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-21485.Dockerfile) |
| source files (`patch`) | `scipy/interpolate/__init__.py`, `scipy/interpolate/_aaa.py`, `scipy/interpolate/_bary_rational.py`, `scipy/interpolate/meson.build` |
| test files (`test_patch`) | `scipy/interpolate/tests/meson.build`, `scipy/interpolate/tests/test_aaa.py`, `scipy/interpolate/tests/test_bary_rational.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (33)

<details><summary>show</summary>

- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-1e-06-1e-07]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-1e-14-0]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-2e-13-1e-07_0]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-2e-13-1e-07_1]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-3.5e-13-0]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-5e-13-1e-07]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-7e-13-0]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_convergence_error`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_dtype_preservation[complex128]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_dtype_preservation[complex64]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_dtype_preservation[float32]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_dtype_preservation[float64]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_exp`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_infinite_data`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_input_validation`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_log_func`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_nan`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_poles_zeros_residues`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>0]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>1]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>2]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>3]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>4]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>5]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>6]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>7]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>8]`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_residues`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_scale_invariance`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_short_cases`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_spiral`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_spiral_cleanup`
- `scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_tan`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #21485: MAINT: interpolate: abstract out barycentric representation of a rational function

The barycentric representation used in AAA is not unique to AAA. It is likely we want to add Floater Hormann weights too. This pr abstracts out the barycentric representation in preparation for this.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/interpolate/__init__.py b/scipy/interpolate/__init__.py
index faa8ed71486054c35daf8c8116485a662dc1fddd..c7a5777086de63a067a52314458d65d02b0e2778 100644
--- a/scipy/interpolate/__init__.py
+++ b/scipy/interpolate/__init__.py
@@ -196,7 +196,7 @@ from ._rgi import *
 
 from ._ndbspline import NdBSpline
 
-from ._aaa import *
+from ._bary_rational import *
 
 # Deprecated namespaces, to be removed in v2.0.0
 from . import fitpack, fitpack2, interpolate, ndgriddata, polyint, rbf
diff --git a/scipy/interpolate/_aaa.py b/scipy/interpolate/_aaa.py
deleted file mode 100644
index 0faa46bb3ea6905d9685e72f34a83287429df8b3..0000000000000000000000000000000000000000
--- a/scipy/interpolate/_aaa.py
+++ /dev/null
@@ -1,555 +0,0 @@
-# Copyright (c) 2017, The Chancellor, Masters and Scholars of the University
-# of Oxford, and the Chebfun Developers. All rights reserved.
-#
-# Redistribution and use in source and binary forms, with or without
-# modification, are permitted provided that the following conditions are met:
-#     * Redistributions of source code must retain the above copyright
-#       notice, this list of conditions and the following disclaimer.
-#     * Redistributions in binary form must reproduce the above copyright
-#       notice, this list of conditions and the following disclaimer in the
-#       documentation and/or other materials provided with the distribution.
-#     * Neither the name of the University of Oxford nor the names of its
-#       contributors may be used to endorse or promote products derived from
-#       this software without specific prior written permission.
-#
-# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
-# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
-# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
-# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
-# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
-# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
-# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
-# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
-# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
-# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-
-import warnings
-import operator
-
-import numpy as np
-import scipy
-
-
-__all__ = ["AAA"]
-
-
-class AAA:
-    r"""
-    AAA real or complex rational approximation.
-
-    As described in [1]_, the AAA algorithm is a greedy algorithm for approximation by
-    rational functions on a real or complex set of points. The rational approximation is
-    represented in a barycentric form from which the roots (zeros), poles, and residues
-    can be computed.
-
-    Parameters
-    ----------
-    points : 1D array_like, shape (n,)
-        1-D array containing values of the independent variable. Values may be real or
-        complex but must be finite.
-    values : 1D array_like, shape (n,)
-        Function values ``f(z)`` at `points`. Infinite and NaN values of `values` and
-        corresponding values of `points` will be discarded.
-    rtol : float, optional
-        Relative tolerance, defaults to ``eps**0.75``. If a small subset of the entries
-        in `values` are much larger than the rest the default tolerance may be too
-        loose. If the tolerance is too tight then the approximation may contain
-        Froissart doublets or the algorithm may fail to converge entirely.
-    max_terms : int, optional
-        Maximum number of terms in the barycentric representation, defaults to ``100``.
-        Must be greater than or equal to one.
-    clean_up : bool, optional
-        Automatic removal of Froissart doublets, defaults to ``True``. See notes for
-        more details.
-    clean_up_tol : float, optional
-        Poles with residues less than this number times the geometric mean
-        of `values` times the minimum distance to `points` are deemed spurious by the
-        cleanup procedure, defaults to 1e-13. See notes for more details.
-
-    Attributes
-    ----------
-    support_points : array
-        Support points of the approximation. These are a subset of the provided
-        `points` at which the approximation strictly interpolates the provided `values`.
-        See notes for more details.
-    support_values : array
-        Value of the approximation at the `support_points`.
-    weights : array
-        Weights of the barycentric approximation.
-    errors : array
-        Error :math:`|f(z) - r(z)|_\infty` over `points` in the successive iterations
-        of AAA.
-
-    Warns
-    -----
-    RuntimeWarning
-        If `rtol` is not achieved in `max_terms` iterations.
-
-    See Also
-    --------
-    pade : Padé approximation
-
-    Notes
-    -----
-    At iteration :math:`m` (at which point there are :math:`m` terms in the both the
-    numerator and denominator of the approximation), the
-    rational approximation in the AAA algorithm takes the barycentric form
-
-    .. math::
-
-        r(z) = n(z)/d(z) =
-        \frac{\sum_{j=1}^m\ w_j f_j / (z - z_j)}{\sum_{j=1}^m w_j / (z - z_j)},
-
-    where :math:`z_1,\dots,z_m` are real or complex support points selected from
-    `points`, :math:`f_1,\dots,f_m` are the corresponding real or complex data values
-    from `values`, and :math:`w_1,\dots,w_m` are real or complex weights.
-
-    Each iteration of the algorithm has two parts: the greedy selection the next support
-    point and the computation of the weights. The first part of each iteration is to
-    select the next support point to be added :math:`z_{m+1}` from the remaining
-    unselected `points`, such that the nonlinear residual
-    :math:`|f(z_{m+1}) - n(z_{m+1})/d(z_{m+1})|` is maximised. The algorithm terminates
-    when this maximum is less than ``rtol * np.linalg.norm(f, ord=np.inf)``. This means
-    the interpolation property is only satisfied up to a tolerance, except at the
-    support points where approximation exactly interpolates the supplied data.
-
-    In the second part of each iteration, the weights :math:`w_j` are selected to solve
-    the least-squares problem
-
-    .. math::
-
-        \text{minimise}_{w_j}|fd - n| \quad \text{subject to} \quad
-        \sum_{j=1}^{m+1} w_j = 1,
-
-    over the unselected elements of `points`.
-
-    One of the challenges with working with rational approximations is the presence of
-    Froissart doublets, which are either poles with vanishingly small residues or
-    pole-zero pairs that are close enough together to nearly cancel, see [2]_. The
-    greedy nature of the AAA algorithm means Froissart doublets are rare. However, if
-    `rtol` is set too tight then the approximation will stagnate and many Froissart
-    doublets will appear. Froissart doublets can usually be removed by removing support
-    points and then resolving the least squares problem. The support point :math:`z_j`,
-    which is the closest support point to the pole :math:`a` with residue
-    :math:`\alpha`, is removed if the following is satisfied
-    
-    .. math::
-
-        |\alpha| / |z_j - a| < \verb|clean_up_tol| \cdot \tilde{f},
-    
-    where :math:`\tilde{f}` is the geometric mean of `support_values`.
-
-
-    References
-    ----------
-    .. [1] Y. Nakatsukasa, O. Sete, and L. N. Trefethen, "The AAA algorithm for
-            rational approximation", SIAM J. Sci. Comp. 40 (2018), A1494-A1522.
-            :doi:`10.1137/16M1106122`
-    .. [2] J. Gilewicz and M. Pindor, Pade approximants and noise: rational functions,
-           J. Comp. Appl. Math. 105 (1999), pp. 285-297.
-           :doi:`10.1016/S0377-0427(02)00674-X`
-
-    Examples
-    --------
-
-    Here we reproduce a number of the numerical examples from [1]_ as a demonstration
-    of the functionality offered by this method.
-
-    >>> import numpy as np
-    >>> import matplotlib.pyplot as plt
-    >>> from scipy.interpolate import AAA
-    >>> import warnings
-
-    For the first example we approximate the gamma function on ``[-3.5, 4.5]`` by
-    extrapolating from 100 samples in ``[-1.5, 1.5]``.
-
-    >>> from scipy.special import gamma
-    >>> sample_points = np.linspace(-1.5, 1.5, num=100)
-    >>> r = AAA(sample_points, gamma(sample_points))
-    >>> z = np.linspace(-3.5, 4.5, num=1000)
-    >>> fig, ax = plt.subplots()
-    >>> ax.plot(z, gamma(z), label="Gamma")
-    >>> ax.plot(sample_points, gamma(sample_points), label="Sample points")
-    >>> ax.plot(z, r(z).real, '--', label="AAA approximation")
-    >>> ax.set(xlabel="z", ylabel="r(z)", ylim=[-8, 8], xlim=[-3.5, 4.5])
-    >>> ax.legend()
-    >>> plt.show()
-
-    We can also view the poles of the rational approximation and their residues:
-
-    >>> order = np.argsort(r.poles())
-    >>> r.poles()[order]
-    array([-3.81591039e+00+0.j        , -3.00269049e+00+0.j        ,
-           -1.99999988e+00+0.j        , -1.00000000e+00+0.j        ,
-            5.85842812e-17+0.j        ,  4.77485458e+00-3.06919376j,
-            4.77485458e+00+3.06919376j,  5.29095868e+00-0.97373072j,
-            5.29095868e+00+0.97373072j])
-    >>> r.residues()[order]
-    array([ 0.03658074 +0.j        , -0.16915426 -0.j        ,
-            0.49999915 +0.j        , -1.         +0.j        ,
-            1.         +0.j        , -0.81132013 -2.30193429j,
-           -0.81132013 +2.30193429j,  0.87326839+10.70148546j,
-            0.87326839-10.70148546j])
-
-    For the second example, we call `AAA` with a spiral of 1000 points that wind 7.5
-    times around the origin in the complex plane.
-
-    >>> z = np.exp(np.linspace(-0.5, 0.5 + 15j*np.pi, 1000))
-    >>> r = AAA(z, np.tan(np.pi*z/2), rtol=1e-13)
-
-    We see that AAA takes 12 steps to converge with the following errors:
-
-    >>> r.errors.size
-    12
-    >>> r.errors
-    array([2.49261500e+01, 4.28045609e+01, 1.71346935e+01, 8.65055336e-02,
-           1.27106444e-02, 9.90889874e-04, 5.86910543e-05, 1.28735561e-06,
-           3.57007424e-08, 6.37007837e-10, 1.67103357e-11, 1.17112299e-13])
-
-    We can also plot the computed poles:
-
-    >>> fig, ax = plt.subplots()
-    >>> ax.plot(z.real, z.imag, '.', markersize=2, label="Sample points")
-    >>> ax.plot(r.poles().real, r.poles().imag, '.', markersize=5,
-    ...         label="Computed poles")
-    >>> ax.set(xlim=[-3.5, 3.5], ylim=[-3.5, 3.5], aspect="equal")
-    >>> ax.legend()
-    >>> plt.show()
-
-    We now demonstrate the removal of Froissart doublets using the `clean_up` method
-    using an example from [1]_. Here we approximate the function
-    :math:`f(z)=\log(2 + z^4)/(1 + 16z^4)` by sampling it at 1000 roots of unity. The
-    algorithm is run with ``rtol=0`` and ``clean_up=False`` to deliberately cause
-    Froissart doublets to appear.
-
-    >>> z = np.exp(1j*2*np.pi*np.linspace(0,1, num=1000))
-    >>> def f(z):
-    ...     return np.log(2 + z**4)/(1 - 16*z**4)
-    >>> with warnings.catch_warnings():  # filter convergence warning due to rtol=0
-    ...     warnings.simplefilter('ignore', RuntimeWarning)
-    ...     r = AAA(z, f(z), rtol=0, max_terms=50, clean_up=False)
-    >>> mask = np.abs(r.residues()) < 1e-13
-    >>> fig, axs = plt.subplots(ncols=2)
-    >>> axs[0].plot(r.poles().real[~mask], r.poles().imag[~mask], '.')
-    >>> axs[0].plot(r.poles().real[mask], r.poles().imag[mask], 'r.')
-
-    Now we call the `clean_up` method to remove Froissart doublets.
-
-    >>> with warnings.catch_warnings():
-    ...     warnings.simplefilter('ignore', RuntimeWarning)
-    ...     r.clean_up()
-    4
-    >>> mask = np.abs(r.residues()) < 1e-13
-    >>> axs[1].plot(r.poles().real[~mask], r.poles().imag[~mask], '.')
-    >>> axs[1].plot(r.poles().real[mask], r.poles().imag[mask], 'r.')
-    >>> plt.show()
-
-    The left image shows the poles prior of the approximation ``clean_up=False`` with
-    poles with residue less than ``10^-13`` in absolute value shown in red. The right
-    image then shows the poles after the `clean_up` method has been called.
-    """
-    def __init__(self, points, values, *, rtol=None, max_terms=100, clean_up=True,
-                 clean_up_tol=1e-13):
-        # input validation
-        z = np.asarray(points)
-        f = np.asarray(values)
-
-        if z.ndim != 1 or f.ndim != 1:
-            raise ValueError("`points` and `values` must be 1-D.")
-
-        if f.size != z.size:
-            raise ValueError("`points` and `values` must be the same size.")
-
-        if not np.all(np.isfinite(z)):
-            raise ValueError("`points` must be finite.")
-
-        max_terms = operator.index(max_terms)
-        if max_terms < 1:
-            raise ValueError("`max_terms` must be an integer value greater than or "
-                             "equal to one.")
-
-        # Remove infinite or NaN function values and repeated entries
-        to_keep = (np.isfinite(f)) & (~np.isnan(f))
-        f = f[to_keep]
-        z = z[to_keep]
-        z, uni = np.unique(z, return_index=True)
-        f = f[uni]
-
-        self._compute_weights(z, f, rtol, max_terms)
-
-        # only compute once
-        self._poles = None
-        self._residues = None
-        self._roots = None
-
-        if clean_up:
-            self.clean_up(clean_up_tol)
-
-    def _compute_weights(self, z, f, rtol, max_terms):
-        # Initialization for AAA iteration
-        M = np.size(z)
-        mask = np.ones(M, dtype=np.bool_)
-        dtype = np.result_type(z, f, 1.0)
-        rtol = np.finfo(dtype).eps**0.75 if rtol is None else rtol
-        atol = rtol * np.linalg.norm(f, ord=np.inf)
-        zj = np.empty(max_terms, dtype=dtype)
-        fj = np.empty(max_terms, dtype=dtype)
-        # Cauchy matrix
-        C = np.empty((M, max_terms), dtype=dtype)
-        # Loewner matrix
-        A = np.empty((M, max_terms), dtype=dtype)
-        errors = np.empty(max_terms, dtype=A.real.dtype)
-        R = np.repeat(np.mean(f), M)
-
-        # AAA iteration
-        for m in range(max_terms):
-            # Introduce next support point
-            # Select next support point
-            jj = np.argmax(np.abs(f[mask] - R[mask]))
-            # Update support points
-            zj[m] = z[mask][jj]
-            # Update data values
-            fj[m] = f[mask][jj]
-            # Next column of Cauchy matrix
-            # Ignore errors as we manually interpolate at support points
-            with np.errstate(divide="ignore", invalid="ignore"):
-                C[:, m] = 1 / (z - z[mask][jj])
-            # Update mask
-            mask[np.nonzero(mask)[0][jj]] = False
-            # Update Loewner matrix
-            # Ignore errors as inf values will be masked out in SVD call
-            with np.errstate(invalid="ignore"):
-                A[:, m] = (f - fj[m]) * C[:, m]
-
-            # Compute weights
-            rows = mask.sum()
-            if rows >= m + 1:
-                # The usual tall-skinny case
-                _, s, V = scipy.linalg.svd(
-                    A[mask, : m + 1], full_matrices=False, check_finite=False,
-                )
-                # Treat case of multiple min singular values
-                mm = s == np.min(s)
-                # Aim for non-sparse weight vector
-                wj = (V.conj()[mm, :].sum(axis=0) / np.sqrt(mm.sum())).astype(dtype)
-            else:
-                # Fewer rows than columns
-                V = scipy.linalg.null_space(A[mask, : m + 1], check_finite=False)
-                nm = V.shape[-1]
-                # Aim for non-sparse wt vector
-                wj = V.sum(axis=-1) / np.sqrt(nm)
-
-            # Compute rational approximant
-            # Omit columns with `wj == 0`
-            i0 = wj != 0
-            # Ignore errors as we manually interpolate at support points
-            with np.errstate(invalid="ignore"):
-                # Numerator
-                N = C[:, : m + 1][:, i0] @ (wj[i0] * fj[: m + 1][i0])
-                # Denominator
-                D = C[:, : m + 1][:, i0] @ wj[i0]
-            # Interpolate at support points with `wj !=0`
-            D_inf = np.isinf(D) | np.isnan(D)
-            D[D_inf] = 1
-            N[D_inf] = f[D_inf]
-            R = N / D
-
-            # Check if converged
-            max_error = np.linalg.norm(f - R, ord=np.inf)
-            errors[m] = max_error
-            if max_error <= atol:
-                break
-
-        if m == max_terms - 1:
-            warnings.warn(f"AAA failed to converge within {max_terms} iterations.",
-                          RuntimeWarning, stacklevel=2)
-
-        # Trim off unused array allocation
-        zj = zj[: m + 1]
-        fj = fj[: m + 1]
-
-        # Remove support points with zero weight
-        i_non_zero = wj != 0
-        self.support_points = zj[i_non_zero]
-        self.support_values = fj[i_non_zero]
-        self.weights = wj[i_non_zero]
-        self.errors = errors[: m + 1]
-        self._points = z
-        self._values = f
-
-    def clean_up(self, cleanup_tol=1e-13):
-        """Automatic removal of Froissart doublets.
-
-        Parameters
-        ----------
-        cleanup_tol : float, optional
-            Poles with residues less than this number times the geometric mean
-            of `values` times the minimum distance to `points` are deemed spurious by
-            the cleanup procedure, defaults to 1e-13.
-
-        Returns
-        -------
-        int
-            Number of Froissart doublets detected
-        """
-        # Find negligible residues
-        geom_mean_abs_f = scipy.stats.gmean(np.abs(self._values))
-
-        Z_distances = np.min(
-            np.abs(np.subtract.outer(self.poles(), self._points)), axis=1
-        )
-
-        with np.errstate(divide="ignore", invalid="ignore"):
-            ii = np.nonzero(
-                np.abs(self.residues()) / Z_distances < cleanup_tol * geom_mean_abs_f
-            )
-
-        ni = ii[0].size
-        if ni == 0:
-            return ni
-
-        warnings.warn(f"{ni} Froissart doublets detected.", RuntimeWarning,
-                        stacklevel=2)
-
-        # For each spurious pole find and remove closest support point
-        closest_spt_point = np.argmin(
-            np.abs(np.subtract.outer(self.support_points, self.poles()[ii])), axis=0
-        )
-        self.support_points = np.delete(self.support_points, closest_spt_point)
-        self.support_values = np.delete(self.support_values, closest_spt_point)
-
-        # Remove support points z from sample set
-        mask = np.logical_and.reduce(
-            np.not_equal.outer(self._points, self.support_points), axis=1
-        )
-        f = self._values[mask]
-        z = self._points[mask]
-        
-        # recompute weights, we resolve the least squares problem for the remaining
-        # support points
-
-        m = self.support_points.size
-
-        # Cauchy matrix
-        C = 1 / np.subtract.outer(z, self.support_points)
-        # Loewner matrix
-        A = f[:, np.newaxis] * C - C * self.support_values
-
-        # Solve least-squares problem to obtain weights
-        _, _, V = scipy.linalg.svd(A, check_finite=False)
-        self.weights = np.conj(V[m - 1,:])
-
-        # reset roots, poles, residues as cached values will be wrong with new weights
-        self._poles = None
-        self._residues = None
-        self._roots = None
-        
-        return ni
-
-    def __call__(self, z):
-        """Evaluate the rational approximation at given values.
-
-        Parameters
-        ----------
-        z : array_like
-            Input values.
-        """
-        # evaluate rational function in barycentric form.
-        z = np.asarray(z)
-        zv = np.ravel(z)
-
-        # Cauchy matrix
-        # Ignore errors due to inf/inf at support points, these will be fixed later
-        with np.errstate(invalid="ignore", divide="ignore"):
-            CC = 1 / np.subtract.outer(zv, self.support_points)
-            # Vector of values
-            r = CC @ (self.weights * self.support_values) / (CC @ self.weights)
-
-        # Deal with input inf: `r(inf) = lim r(z) = sum(w*f) / sum(w)`
-        if np.any(np.isinf(zv)):
-            r[np.isinf(zv)] = (np.sum(self.weights * self.support_values)
-                               / np.sum(self.weights))
-
-        # Deal with NaN
-        ii = np.nonzero(np.isnan(r))[0]
-        for jj in ii:
-            if np.isnan(zv[jj]) or not np.any(zv[jj] == self.support_points):
-                # r(NaN) = NaN is fine.
-                # The second case may happen if `r(zv[ii]) = 0/0` at some point.
-                pass
-            else:
-                # Clean up values `NaN = inf/inf` at support points.
-                # Find the corresponding node and set entry to correct value:
-                r[jj] = self.support_values[zv[jj] == self.support_points].squeeze()
-
-        return np.reshape(r, z.shape)
-
-    def poles(self):
-        """Compute the poles of the rational approximation.
-
-        Returns
-        -------
-        poles : array
-            Poles of the AAA approximation, repeated according to their multiplicity
-            but not in any specific order.
-        """
-        if self._poles is None:
-            # Compute poles via generalized eigenvalue problem
-            m = self.weights.size
-            B = np.eye(m + 1, dtype=self.weights.dtype)
-            B[0, 0] = 0
-
-            E = np.zeros_like(B, dtype=np.result_type(self.weights,
-                                                      self.support_points))
-            E[0, 1:] = self.weights
-            E[1:, 0] = 1
-            np.fill_diagonal(E[1:, 1:], self.support_points)
-
-            pol = scipy.linalg.eigvals(E, B)
-            self._poles = pol[np.isfinite(pol)]
-        return self._poles
-
-    def residues(self):
-        """Compute the residues of the poles of the approximation.
-
-        Returns
-        -------
-        residues : array
-            Residues associated with the `poles` of the approximation
-        """
-        if self._residues is None:
-            # Compute residues via formula for res of quotient of analytic functions
-            with np.errstate(divide="ignore", invalid="ignore"):
-                N = (1/(np.subtract.outer(self.poles(), self.support_points))) @ (
-                    self.support_values * self.weights
-                )
-                Ddiff = (
-                    -((1/np.subtract.outer(self.poles(), self.support_points))**2)
-                    @ self.weights
-                )
-                self._residues = N / Ddiff
-        return self._residues
-
-    def roots(self):
-        """Compute the zeros of the rational approximation.
-
-        Returns
-        -------
-        zeros : array
-            Zeros of the AAA approximation, repeated according to their multiplicity
-            but not in any specific order.
-        """
-        if self._roots is None:
-            # Compute zeros via generalized eigenvalue problem
-            m = self.weights.size
-            B = np.eye(m + 1, dtype=self.weights.dtype)
-            B[0, 0] = 0
-            E = np.zeros_like(B, dtype=np.result_type(self.weights, self.support_values,
-                                                      self.support_points))
-            E[0, 1:] = self.weights * self.support_values
-            E[1:, 0] = 1
-            np.fill_diagonal(E[1:, 1:], self.support_points)
-
-            zer = scipy.linalg.eigvals(E, B)
-            self._roots = zer[np.isfinite(zer)]
-        return self._roots
diff --git a/scipy/interpolate/_bary_rational.py b/scipy/interpolate/_bary_rational.py
new file mode 100644
index 0000000000000000000000000000000000000000..0e258af576eeb1081645e3622ccfdb09b35844a5
--- /dev/null
+++ b/scipy/interpolate/_bary_rational.py
@@ -0,0 +1,564 @@
+# Copyright (c) 2017, The Chancellor, Masters and Scholars of the University
+# of Oxford, and the Chebfun Developers. All rights reserved.
+#
+# Redistribution and use in source and binary forms, with or without
+# modification, are permitted provided that the following conditions are met:
+#     * Redistributions of source code must retain the above copyright
+#       notice, this list of conditions and the following disclaimer.
+#     * Redistributions in binary form must reproduce the above copyright
+#       notice, this list of conditions and the following disclaimer in the
+#       documentation and/or other materials provided with the distribution.
+#     * Neither the name of the University of Oxford nor the names of its
+#       contributors may be used to endorse or promote products derived from
+#       this software without specific prior written permission.
+#
+# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
+# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
+# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
+# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
+# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
+# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
+# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
+# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
+# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
+# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
+
+import warnings
+import operator
+
+import numpy as np
+import scipy
+
+
+__all__ = ["AAA"]
+
+
+class _Barycentric_Rational:
+    """Base class for Barycentric representation of a rational function."""
+    def __init__(self, points, values, **kwargs):
+        # input validation
+        z = np.asarray(points)
+        f = np.asarray(values)
+
+        if z.ndim != 1 or f.ndim != 1:
+            raise ValueError("`points` and `values` must be 1-D.")
+
+        if f.size != z.size:
+            raise ValueError("`points` and `values` must be the same size.")
+
+        if not np.all(np.isfinite(z)):
+            raise ValueError("`points` must be finite.")
+        
+        # Remove infinite or NaN function values and repeated entries
+        to_keep = (np.isfinite(f)) & (~np.isnan(f))
+        f = f[to_keep]
+        z = z[to_keep]
+        z, uni = np.unique(z, return_index=True)
+        f = f[uni]
+
+        self.support_points, self.support_values, self.weights = self._compute_weights(
+            z, f, **kwargs
+        )
+        
+        # only compute once
+        self._poles = None
+        self._residues = None
+        self._roots = None
+    
+    def _compute_weights(z, f, **kwargs):
+        raise NotImplementedError
+    
+    def __call__(self, z):
+        """Evaluate the rational approximation at given values.
+
+        Parameters
+        ----------
+        z : array_like
+            Input values.
+        """
+        # evaluate rational function in barycentric form.
+        z = np.asarray(z)
+        zv = np.ravel(z)
+
+        # Cauchy matrix
+        # Ignore errors due to inf/inf at support points, these will be fixed later
+        with np.errstate(invalid="ignore", divide="ignore"):
+            CC = 1 / np.subtract.outer(zv, self.support_points)
+            # Vector of values
+            r = CC @ (self.weights * self.support_values) / (CC @ self.weights)
+
+        # Deal with input inf: `r(inf) = lim r(z) = sum(w*f) / sum(w)`
+        if np.any(np.isinf(zv)):
+            r[np.isinf(zv)] = (np.sum(self.weights * self.support_values)
+                               / np.sum(self.weights))
+
+        # Deal with NaN
+        ii = np.nonzero(np.isnan(r))[0]
+        for jj in ii:
+            if np.isnan(zv[jj]) or not np.any(zv[jj] == self.support_points):
+                # r(NaN) = NaN is fine.
+                # The second case may happen if `r(zv[ii]) = 0/0` at some point.
+                pass
+            else:
+                # Clean up values `NaN = inf/inf` at support points.
+                # Find the corresponding node and set entry to correct value:
+                r[jj] = self.support_values[zv[jj] == self.support_points].squeeze()
+
+        return np.reshape(r, z.shape)
+
+    def poles(self):
+        """Compute the poles of the rational approximation.
+
+        Returns
+        -------
+        poles : array
+            Poles of the AAA approximation, repeated according to their multiplicity
+            but not in any specific order.
+        """
+        if self._poles is None:
+            # Compute poles via generalized eigenvalue problem
+            m = self.weights.size
+            B = np.eye(m + 1, dtype=self.weights.dtype)
+            B[0, 0] = 0
+
+            E = np.zeros_like(B, dtype=np.result_type(self.weights,
+                                                      self.support_points))
+            E[0, 1:] = self.weights
+            E[1:, 0] = 1
+            np.fill_diagonal(E[1:, 1:], self.support_points)
+
+            pol = scipy.linalg.eigvals(E, B)
+            self._poles = pol[np.isfinite(pol)]
+        return self._poles
+
+    def residues(self):
+        """Compute the residues of the poles of the approximation.
+
+        Returns
+        -------
+        residues : array
+            Residues associated with the `poles` of the approximation
+        """
+        if self._residues is None:
+            # Compute residues via formula for res of quotient of analytic functions
+            with np.errstate(divide="ignore", invalid="ignore"):
+                N = (1/(np.subtract.outer(self.poles(), self.support_points))) @ (
+                    self.support_values * self.weights
+                )
+                Ddiff = (
+                    -((1/np.subtract.outer(self.poles(), self.support_points))**2)
+                    @ self.weights
+                )
+                self._residues = N / Ddiff
+        return self._residues
+
+    def roots(self):
+        """Compute the zeros of the rational approximation.
+
+        Returns
+        -------
+        zeros : array
+            Zeros of the AAA approximation, repeated according to their multiplicity
+            but not in any specific order.
+        """
+        if self._roots is None:
+            # Compute zeros via generalized eigenvalue problem
+            m = self.weights.size
+            B = np.eye(m + 1, dtype=self.weights.dtype)
+            B[0, 0] = 0
+            E = np.zeros_like(B, dtype=np.result_type(self.weights, self.support_values,
+                                                      self.support_points))
+            E[0, 1:] = self.weights * self.support_values
+            E[1:, 0] = 1
+            np.fill_diagonal(E[1:, 1:], self.support_points)
+
+            zer = scipy.linalg.eigvals(E, B)
+            self._roots = zer[np.isfinite(zer)]
+        return self._roots
+
+
+class AAA(_Barycentric_Rational):
+    r"""
+    AAA real or complex rational approximation.
+
+    As described in [1]_, the AAA algorithm is a greedy algorithm for approximation by
+    rational functions on a real or complex set of points. The rational approximation is
+    represented in a barycentric form from which the roots (zeros), poles, and residues
+    can be computed.
+
+    Parameters
+    ----------
+    points : 1D array_like, shape (n,)
+        1-D array containing values of the independent variable. Values may be real or
+        complex but must be finite.
+    values : 1D array_like, shape (n,)
+        Function values ``f(z)`` at `points`. Infinite and NaN values of `values` and
+        corresponding values of `points` will be discarded.
+    rtol : float, optional
+        Relative tolerance, defaults to ``eps**0.75``. If a small subset of the entries
+        in `values` are much larger than the rest the default tolerance may be too
+        loose. If the tolerance is too tight then the approximation may contain
+        Froissart doublets or the algorithm may fail to converge entirely.
+    max_terms : int, optional
+        Maximum number of terms in the barycentric representation, defaults to ``100``.
+        Must be greater than or equal to one.
+    clean_up : bool, optional
+        Automatic removal of Froissart doublets, defaults to ``True``. See notes for
+        more details.
+    clean_up_tol : float, optional
+        Poles with residues less than this number times the geometric mean
+        of `values` times the minimum distance to `points` are deemed spurious by the
+        cleanup procedure, defaults to 1e-13. See notes for more details.
+
+    Attributes
+    ----------
+    support_points : array
+        Support points of the approximation. These are a subset of the provided
+        `points` at which the approximation strictly interpolates the provided `values`.
+        See notes for more details.
+    support_values : array
+        Value of the approximation at the `support_points`.
+    weights : array
+        Weights of the barycentric approximation.
+    errors : array
+        Error :math:`|f(z) - r(z)|_\infty` over `points` in the successive iterations
+        of AAA.
+
+    Warns
+    -----
+    RuntimeWarning
+        If `rtol` is not achieved in `max_terms` iterations.
+
+    See Also
+    --------
+    pade : Padé approximation
+
+    Notes
+    -----
+    At iteration :math:`m` (at which point there are :math:`m` terms in the both the
+    numerator and denominator of the approximation), the
+    rational approximation in the AAA algorithm takes the barycentric form
+
+    .. math::
+
+        r(z) = n(z)/d(z) =
+        \frac{\sum_{j=1}^m\ w_j f_j / (z - z_j)}{\sum_{j=1}^m w_j / (z - z_j)},
+
+    where :math:`z_1,\dots,z_m` are real or complex support points selected from
+    `points`, :math:`f_1,\dots,f_m` are the corresponding real or complex data values
+    from `values`, and :math:`w_1,\dots,w_m` are real or complex weights.
+
+    Each iteration of the algorithm has two parts: the greedy selection the next support
+    point and the computation of the weights. The first part of each iteration is to
+    select the next support point to be added :math:`z_{m+1}` from the remaining
+    unselected `points`, such that the nonlinear residual
+    :math:`|f(z_{m+1}) - n(z_{m+1})/d(z_{m+1})|` is maximised. The algorithm terminates
+    when this maximum is less than ``rtol * np.linalg.norm(f, ord=np.inf)``. This means
+    the interpolation property is only satisfied up to a tolerance, except at the
+    support points where approximation exactly interpolates the supplied data.
+
+    In the second part of each iteration, the weights :math:`w_j` are selected to solve
+    the least-squares problem
+
+    .. math::
+
+        \text{minimise}_{w_j}|fd - n| \quad \text{subject to} \quad
+        \sum_{j=1}^{m+1} w_j = 1,
+
+    over the unselected elements of `points`.
+
+    One of the challenges with working with rational approximations is the presence of
+    Froissart doublets, which are either poles with vanishingly small residues or
+    pole-zero pairs that are close enough together to nearly cancel, see [2]_. The
+    greedy nature of the AAA algorithm means Froissart doublets are rare. However, if
+    `rtol` is set too tight then the approximation will stagnate and many Froissart
+    doublets will appear. Froissart doublets can usually be removed by removing support
+    points and then resolving the least squares problem. The support point :math:`z_j`,
+    which is the closest support point to the pole :math:`a` with residue
+    :math:`\alpha`, is removed if the following is satisfied
+    
+    .. math::
+
+        |\alpha| / |z_j - a| < \verb|clean_up_tol| \cdot \tilde{f},
+    
+    where :math:`\tilde{f}` is the geometric mean of `support_values`.
+
+
+    References
+    ----------
+    .. [1] Y. Nakatsukasa, O. Sete, and L. N. Trefethen, "The AAA algorithm for
+            rational approximation", SIAM J. Sci. Comp. 40 (2018), A1494-A1522.
+            :doi:`10.1137/16M1106122`
+    .. [2] J. Gilewicz and M. Pindor, Pade approximants and noise: rational functions,
+           J. Comp. Appl. Math. 105 (1999), pp. 285-297.
+           :doi:`10.1016/S0377-0427(02)00674-X`
+
+    Examples
+    --------
+
+    Here we reproduce a number of the numerical examples from [1]_ as a demonstration
+    of the functionality offered by this method.
+
+    >>> import numpy as np
+    >>> import matplotlib.pyplot as plt
+    >>> from scipy.interpolate import AAA
+    >>> import warnings
+
+    For the first example we approximate the gamma function on ``[-3.5, 4.5]`` by
+    extrapolating from 100 samples in ``[-1.5, 1.5]``.
+
+    >>> from scipy.special import gamma
+    >>> sample_points = np.linspace(-1.5, 1.5, num=100)
+    >>> r = AAA(sample_points, gamma(sample_points))
+    >>> z = np.linspace(-3.5, 4.5, num=1000)
+    >>> fig, ax = plt.subplots()
+    >>> ax.plot(z, gamma(z), label="Gamma")
+    >>> ax.plot(sample_points, gamma(sample_points), label="Sample points")
+    >>> ax.plot(z, r(z).real, '--', label="AAA approximation")
+    >>> ax.set(xlabel="z", ylabel="r(z)", ylim=[-8, 8], xlim=[-3.5, 4.5])
+    >>> ax.legend()
+    >>> plt.show()
+
+    We can also view the poles of the rational approximation and their residues:
+
+    >>> order = np.argsort(r.poles())
+    >>> r.poles()[order]
+    array([-3.81591039e+00+0.j        , -3.00269049e+00+0.j        ,
+           -1.99999988e+00+0.j        , -1.00000000e+00+0.j        ,
+            5.85842812e-17+0.j        ,  4.77485458e+00-3.06919376j,
+            4.77485458e+00+3.06919376j,  5.29095868e+00-0.97373072j,
+            5.29095868e+00+0.97373072j])
+    >>> r.residues()[order]
+    array([ 0.03658074 +0.j        , -0.16915426 -0.j        ,
+            0.49999915 +0.j        , -1.         +0.j        ,
+            1.         +0.j        , -0.81132013 -2.30193429j,
+           -0.81132013 +2.30193429j,  0.87326839+10.70148546j,
+            0.87326839-10.70148546j])
+
+    For the second example, we call `AAA` with a spiral of 1000 points that wind 7.5
+    times around the origin in the complex plane.
+
+    >>> z = np.exp(np.linspace(-0.5, 0.5 + 15j*np.pi, 1000))
+    >>> r = AAA(z, np.tan(np.pi*z/2), rtol=1e-13)
+
+    We see that AAA takes 12 steps to converge with the following errors:
+
+    >>> r.errors.size
+    12
+    >>> r.errors
+    array([2.49261500e+01, 4.28045609e+01, 1.71346935e+01, 8.65055336e-02,
+           1.27106444e-02, 9.90889874e-04, 5.86910543e-05, 1.28735561e-06,
+           3.57007424e-08, 6.37007837e-10, 1.67103357e-11, 1.17112299e-13])
+
+    We can also plot the computed poles:
+
+    >>> fig, ax = plt.subplots()
+    >>> ax.plot(z.real, z.imag, '.', markersize=2, label="Sample points")
+    >>> ax.plot(r.poles().real, r.poles().imag, '.', markersize=5,
+    ...         label="Computed poles")
+    >>> ax.set(xlim=[-3.5, 3.5], ylim=[-3.5, 3.5], aspect="equal")
+    >>> ax.legend()
+    >>> plt.show()
+
+    We now demonstrate the removal of Froissart doublets using the `clean_up` method
+    using an example from [1]_. Here we approximate the function
+    :math:`f(z)=\log(2 + z^4)/(1 + 16z^4)` by sampling it at 1000 roots of unity. The
+    algorithm is run with ``rtol=0`` and ``clean_up=False`` to deliberately cause
+    Froissart doublets to appear.
+
+    >>> z = np.exp(1j*2*np.pi*np.linspace(0,1, num=1000))
+    >>> def f(z):
+    ...     return np.log(2 + z**4)/(1 - 16*z**4)
+    >>> with warnings.catch_warnings():  # filter convergence warning due to rtol=0
+    ...     warnings.simplefilter('ignore', RuntimeWarning)
+    ...     r = AAA(z, f(z), rtol=0, max_terms=50, clean_up=False)
+    >>> mask = np.abs(r.residues()) < 1e-13
+    >>> fig, axs = plt.subplots(ncols=2)
+    >>> axs[0].plot(r.poles().real[~mask], r.poles().imag[~mask], '.')
+    >>> axs[0].plot(r.poles().real[mask], r.poles().imag[mask], 'r.')
+
+    Now we call the `clean_up` method to remove Froissart doublets.
+
+    >>> with warnings.catch_warnings():
+    ...     warnings.simplefilter('ignore', RuntimeWarning)
+    ...     r.clean_up()
+    4
+    >>> mask = np.abs(r.residues()) < 1e-13
+    >>> axs[1].plot(r.poles().real[~mask], r.poles().imag[~mask], '.')
+    >>> axs[1].plot(r.poles().real[mask], r.poles().imag[mask], 'r.')
+    >>> plt.show()
+
+    The left image shows the poles prior of the approximation ``clean_up=False`` with
+    poles with residue less than ``10^-13`` in absolute value shown in red. The right
+    image then shows the poles after the `clean_up` method has been called.
+    """
+    def __init__(self, points, values, *, rtol=None, max_terms=100, clean_up=True,
+                 clean_up_tol=1e-13):
+        max_terms = operator.index(max_terms)
+        if max_terms < 1:
+            raise ValueError("`max_terms` must be an integer value greater than or "
+                             "equal to one.")
+
+        super().__init__(points, values, rtol=rtol, max_terms=max_terms)
+        
+        if clean_up:
+            self.clean_up(clean_up_tol)
+
+    def _compute_weights(self, z, f, rtol, max_terms):
+        # Initialization for AAA iteration
+        M = np.size(z)
+        mask = np.ones(M, dtype=np.bool_)
+        dtype = np.result_type(z, f, 1.0)
+        rtol = np.finfo(dtype).eps**0.75 if rtol is None else rtol
+        atol = rtol * np.linalg.norm(f, ord=np.inf)
+        zj = np.empty(max_terms, dtype=dtype)
+        fj = np.empty(max_terms, dtype=dtype)
+        # Cauchy matrix
+        C = np.empty((M, max_terms), dtype=dtype)
+        # Loewner matrix
+        A = np.empty((M, max_terms), dtype=dtype)
+        errors = np.empty(max_terms, dtype=A.real.dtype)
+        R = np.repeat(np.mean(f), M)
+
+        # AAA iteration
+        for m in range(max_terms):
+            # Introduce next support point
+            # Select next support point
+            jj = np.argmax(np.abs(f[mask] - R[mask]))
+            # Update support points
+            zj[m] = z[mask][jj]
+            # Update data values
+            fj[m] = f[mask][jj]
+            # Next column of Cauchy matrix
+            # Ignore errors as we manually interpolate at support points
+            with np.errstate(divide="ignore", invalid="ignore"):
+                C[:, m] = 1 / (z - z[mask][jj])
+            # Update mask
+            mask[np.nonzero(mask)[0][jj]] = False
+            # Update Loewner matrix
+            # Ignore errors as inf values will be masked out in SVD call
+            with np.errstate(invalid="ignore"):
+                A[:, m] = (f - fj[m]) * C[:, m]
+
+            # Compute weights
+            rows = mask.sum()
+            if rows >= m + 1:
+                # The usual tall-skinny case
+                _, s, V = scipy.linalg.svd(
+                    A[mask, : m + 1], full_matrices=False, check_finite=False,
+                )
+                # Treat case of multiple min singular values
+                mm = s == np.min(s)
+                # Aim for non-sparse weight vector
+                wj = (V.conj()[mm, :].sum(axis=0) / np.sqrt(mm.sum())).astype(dtype)
+            else:
+                # Fewer rows than columns
+                V = scipy.linalg.null_space(A[mask, : m + 1], check_finite=False)
+                nm = V.shape[-1]
+                # Aim for non-sparse wt vector
+                wj = V.sum(axis=-1) / np.sqrt(nm)
+
+            # Compute rational approximant
+            # Omit columns with `wj == 0`
+            i0 = wj != 0
+            # Ignore errors as we manually interpolate at support points
+            with np.errstate(invalid="ignore"):
+                # Numerator
+                N = C[:, : m + 1][:, i0] @ (wj[i0] * fj[: m + 1][i0])
+                # Denominator
+                D = C[:, : m + 1][:, i0] @ wj[i0]
+            # Interpolate at support points with `wj !=0`
+            D_inf = np.isinf(D) | np.isnan(D)
+            D[D_inf] = 1
+            N[D_inf] = f[D_inf]
+            R = N / D
+
+            # Check if converged
+            max_error = np.linalg.norm(f - R, ord=np.inf)
+            errors[m] = max_error
+            if max_error <= atol:
+                break
+
+        if m == max_terms - 1:
+            warnings.warn(f"AAA failed to converge within {max_terms} iterations.",
+                          RuntimeWarning, stacklevel=2)
+
+        # Trim off unused array allocation
+        zj = zj[: m + 1]
+        fj = fj[: m + 1]
+
+        # Remove support points with zero weight
+        i_non_zero = wj != 0
+        self.errors = errors[: m + 1]
+        self._points = z
+        self._values = f
+        return zj[i_non_zero], fj[i_non_zero], wj[i_non_zero]
+
+    def clean_up(self, cleanup_tol=1e-13):
+        """Automatic removal of Froissart doublets.
+
+        Parameters
+        ----------
+        cleanup_tol : float, optional
+            Poles with residues less than this number times the geometric mean
+            of `values` times the minimum distance to `points` are deemed spurious by
+            the cleanup procedure, defaults to 1e-13.
+
+        Returns
+        -------
+        int
+            Number of Froissart doublets detected
+        """
+        # Find negligible residues
+        geom_mean_abs_f = scipy.stats.gmean(np.abs(self._values))
+
+        Z_distances = np.min(
+            np.abs(np.subtract.outer(self.poles(), self._points)), axis=1
+        )
+
+        with np.errstate(divide="ignore", invalid="ignore"):
+            ii = np.nonzero(
+                np.abs(self.residues()) / Z_distances < cleanup_tol * geom_mean_abs_f
+            )
+
+        ni = ii[0].size
+        if ni == 0:
+            return ni
+
+        warnings.warn(f"{ni} Froissart doublets detected.", RuntimeWarning,
+                        stacklevel=2)
+
+        # For each spurious pole find and remove closest support point
+        closest_spt_point = np.argmin(
+            np.abs(np.subtract.outer(self.support_points, self.poles()[ii])), axis=0
+        )
+        self.support_points = np.delete(self.support_points, closest_spt_point)
+        self.support_values = np.delete(self.support_values, closest_spt_point)
+
+        # Remove support points z from sample set
+        mask = np.logical_and.reduce(
+            np.not_equal.outer(self._points, self.support_points), axis=1
+        )
+        f = self._values[mask]
+        z = self._points[mask]
+        
+        # recompute weights, we resolve the least squares problem for the remaining
+        # support points
+
+        m = self.support_points.size
+
+        # Cauchy matrix
+        C = 1 / np.subtract.outer(z, self.support_points)
+        # Loewner matrix
+        A = f[:, np.newaxis] * C - C * self.support_values
+
+        # Solve least-squares problem to obtain weights
+        _, _, V = scipy.linalg.svd(A, check_finite=False)
+        self.weights = np.conj(V[m - 1,:])
+
+        # reset roots, poles, residues as cached values will be wrong with new weights
+        self._poles = None
+        self._residues = None
+        self._roots = None
+        
+        return ni
diff --git a/scipy/interpolate/meson.build b/scipy/interpolate/meson.build
index 4718fda4d692588ed1404d6751658f199c521b10..6f5d5f16a246c16ffe0bcbd545dad2e9b57fa3d0 100644
--- a/scipy/interpolate/meson.build
+++ b/scipy/interpolate/meson.build
@@ -174,8 +174,8 @@ endif
 
 py3.install_sources([
     '__init__.py',
-    '_aaa.py',
     '_bsplines.py',
+    '_bary_rational.py',
     '_cubic.py',
     '_fitpack_impl.py',
     '_fitpack_py.py',
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/interpolate/tests/meson.build b/scipy/interpolate/tests/meson.build
index 87750d520691701cfc580cc7c186e1769071f0d0..cc677bd2566eddd0451bf4679c2c99defd68b59e 100644
--- a/scipy/interpolate/tests/meson.build
+++ b/scipy/interpolate/tests/meson.build
@@ -1,6 +1,6 @@
 py3.install_sources([
     '__init__.py',
-    'test_aaa.py',
+    'test_bary_rational.py',
     'test_bsplines.py',
     'test_fitpack.py',
     'test_fitpack2.py',
diff --git a/scipy/interpolate/tests/test_aaa.py b/scipy/interpolate/tests/test_aaa.py
deleted file mode 100644
index 64832b2ce9fa33529b95c25d6a9b7948d75237d0..0000000000000000000000000000000000000000
--- a/scipy/interpolate/tests/test_aaa.py
+++ /dev/null
@@ -1,237 +0,0 @@
-# Copyright (c) 2017, The Chancellor, Masters and Scholars of the University
-# of Oxford, and the Chebfun Developers. All rights reserved.
-#
-# Redistribution and use in source and binary forms, with or without
-# modification, are permitted provided that the following conditions are met:
-#     * Redistributions of source code must retain the above copyright
-#       notice, this list of conditions and the following disclaimer.
-#     * Redistributions in binary form must reproduce the above copyright
-#       notice, this list of conditions and the following disclaimer in the
-#       documentation and/or other materials provided with the distribution.
-#     * Neither the name of the University of Oxford nor the names of its
-#       contributors may be used to endorse or promote products derived from
-#       this software without specific prior written permission.
-#
-# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
-# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
-# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
-# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
-# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
-# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
-# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
-# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
-# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
-# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-
-
-import numpy as np
-from numpy.testing import assert_allclose, assert_equal
-import pytest
-import scipy
-from scipy.interpolate import AAA
-
-TOL = 1e4 * np.finfo(np.float64).eps
-UNIT_INTERVAL = np.linspace(-1, 1, num=1000)
-PTS = np.logspace(-15, 0, base=10, num=500)
-PTS = np.concatenate([-PTS[::-1], [0], PTS])
-
-class TestAAA:
-    def test_input_validation(self):
-        with pytest.raises(ValueError, match="same size"):
-            AAA([0], [1, 1])
-        with pytest.raises(ValueError, match="1-D"):
-            AAA([[0], [0]], [[1], [1]])
-        with pytest.raises(ValueError, match="finite"):
-            AAA([np.inf], [1])
-        with pytest.raises(TypeError):
-            AAA([1], [1], max_terms=1.0)
-        with pytest.raises(ValueError, match="greater"):
-            AAA([1], [1], max_terms=-1)
-    
-    def test_convergence_error(self):
-        with pytest.warns(RuntimeWarning, match="AAA failed"):
-            AAA(UNIT_INTERVAL, np.exp(UNIT_INTERVAL),  max_terms=1)
-
-    @pytest.mark.parametrize("dtype", [np.float32, np.float64, np.complex64, 
-                                       np.complex128])
-    def test_dtype_preservation(self, dtype):
-        rtol = np.finfo(dtype).eps ** 0.75 * 100
-        rng = np.random.default_rng(59846294526092468)
-
-        z = np.linspace(-1, 1, dtype=dtype)
-        r = AAA(z, np.sin(z))
-        
-        z2 = rng.uniform(-1, 1, size=100).astype(dtype)
-        assert_allclose(r(z2), np.sin(z2), rtol=rtol)
-        assert r(z2).dtype == dtype
-        
-        assert r.support_points.dtype == dtype
-        assert r.support_values.dtype == dtype
-        assert r.weights.dtype == dtype
-        assert r.errors.dtype == z.real.dtype
-        assert r.poles().dtype == np.result_type(dtype, 1j)
-        assert r.residues().dtype == np.result_type(dtype, 1j)
-        assert r.roots().dtype == np.result_type(dtype, 1j)
-    
-    # The following tests are based on:
-    # https://github.com/chebfun/chebfun/blob/master/tests/chebfun/test_aaa.m
-    def test_exp(self):
-        f = np.exp(UNIT_INTERVAL)
-        r = AAA(UNIT_INTERVAL, f)
-
-        assert_allclose(r(UNIT_INTERVAL), f, atol=TOL)
-        assert_equal(r(np.nan), np.nan)
-        assert np.isfinite(r(np.inf))
-
-        m1 = r.support_points.size
-        r = AAA(UNIT_INTERVAL, f, rtol=1e-3)
-        assert r.support_points.size < m1
-
-    def test_tan(self):
-        f = np.tan(np.pi * UNIT_INTERVAL)
-        r = AAA(UNIT_INTERVAL, f)
-
-        assert_allclose(r(UNIT_INTERVAL), f, atol=10 * TOL, rtol=1.4e-7)
-        assert_allclose(np.min(np.abs(r.roots())), 0, atol=3e-10)
-        assert_allclose(np.min(np.abs(r.poles() - 0.5)), 0, atol=TOL)
-        # Test for spurious poles (poles with tiny residue are likely spurious)
-        assert np.min(np.abs(r.residues())) > 1e-13
-
-    def test_short_cases(self):
-        # Computed using Chebfun:
-        # >> format long
-        # >> [r, pol, res, zer, zj, fj, wj, errvec] = aaa([1 2], [0 1])
-        z = np.array([0, 1])
-        f = np.array([1, 2])
-        r = AAA(z, f, rtol=1e-13)
-        assert_allclose(r(z), f, atol=TOL)
-        assert_allclose(r.poles(), 0.5)
-        assert_allclose(r.residues(), 0.25)
-        assert_allclose(r.roots(), 1/3)
-        assert_equal(r.support_points, z)
-        assert_equal(r.support_values, f)
-        assert_allclose(r.weights, [0.707106781186547, 0.707106781186547])
-        assert_equal(r.errors, [1, 0])
-        
-        # >> format long
-        # >> [r, pol, res, zer, zj, fj, wj, errvec] = aaa([1 0 0], [0 1 2])
-        z = np.array([0, 1, 2])
-        f = np.array([1, 0, 0])
-        r = AAA(z, f, rtol=1e-13)
-        assert_allclose(r(z), f, atol=TOL)
-        assert_allclose(np.sort(r.poles()),
-                        np.sort([1.577350269189626, 0.422649730810374]))
-        assert_allclose(np.sort(r.residues()),
-                        np.sort([-0.070441621801729, -0.262891711531604]))
-        assert_allclose(np.sort(r.roots()), np.sort([2, 1]))
-        assert_equal(r.support_points, z)
-        assert_equal(r.support_values, f)
-        assert_allclose(r.weights, [0.577350269189626, 0.577350269189626,
-                                    0.577350269189626])
-        assert_equal(r.errors, [1, 1, 0])
-
-    def test_scale_invariance(self):
-        z = np.linspace(0.3, 1.5)
-        f = np.exp(z) / (1 + 1j)
-        r1 = AAA(z, f)
-        r2 = AAA(z, (2**311 * f).astype(np.complex128))
-        r3 = AAA(z, (2**-311 * f).astype(np.complex128))
-        assert_equal(r1(0.2j), 2**-311 * r2(0.2j))
-        assert_equal(r1(1.4), 2**311 * r3(1.4))
-
-    def test_log_func(self):
-        rng = np.random.default_rng(1749382759832758297)
-        z = rng.standard_normal(10000) + 3j * rng.standard_normal(10000)
-
-        def f(z):
-            return np.log(5 - z) / (1 + z**2)
-
-        r = AAA(z, f(z))
-        assert_allclose(r(0), f(0), atol=TOL)
-
-    def test_infinite_data(self):
-        z = np.linspace(-1, 1)
-        r = AAA(z, scipy.special.gamma(z))
-        assert_allclose(r(0.63), scipy.special.gamma(0.63), atol=1e-15)
-
-    def test_nan(self):
-        x = np.linspace(0, 20)
-        with np.errstate(invalid="ignore"):
-            f = np.sin(x) / x
-        r = AAA(x, f)
-        assert_allclose(r(2), np.sin(2) / 2, atol=1e-15)
-
-    def test_residues(self):
-        x = np.linspace(-1.337, 2, num=537)
-        r = AAA(x, np.exp(x) / x)
-        ii = np.flatnonzero(np.abs(r.poles()) < 1e-8)
-        assert_allclose(r.residues()[ii], 1, atol=1e-15)
-
-        r = AAA(x, (1 + 1j) * scipy.special.gamma(x))
-        ii = np.flatnonzero(abs(r.poles() - (-1)) < 1e-8)
-        assert_allclose(r.residues()[ii], -1 - 1j, atol=1e-15)
-    
-    # The following tests are based on:
-    # https://github.com/complexvariables/RationalFunctionApproximation.jl/blob/main/test/interval.jl
-    @pytest.mark.parametrize("func,atol,rtol",
-                             [(lambda x: np.abs(x + 0.5 + 0.01j), 5e-13, 1e-7),
-                              (lambda x: np.sin(1/(1.05 - x)), 2e-13, 1e-7),
-                              (lambda x: np.exp(-1/(x**2)), 3.5e-13, 0),
-                              (lambda x: np.exp(-100*x**2), 7e-13, 0),
-                              (lambda x: np.exp(-10/(1.2 - x)), 1e-14, 0),
-                              (lambda x: 1/(1+np.exp(100*(x + 0.5))), 2e-13, 1e-7),
-                              (lambda x: np.abs(x - 0.95), 1e-6, 1e-7)])
-    def test_basic_functions(self, func, atol, rtol):
-        with np.errstate(divide="ignore"):
-            f = func(PTS)
-        assert_allclose(AAA(UNIT_INTERVAL, func(UNIT_INTERVAL))(PTS),
-                        f, atol=atol, rtol=rtol)
-    
-    def test_poles_zeros_residues(self):
-        def f(z):
-            return (z+1) * (z+2) / ((z+3) * (z+4))
-        r = AAA(UNIT_INTERVAL, f(UNIT_INTERVAL))
-        assert_allclose(np.sum(r.poles() + r.roots()), -10, atol=1e-12)
-        
-        def f(z):
-            return 2/(3 + z) + 5/(z - 2j)
-        r = AAA(UNIT_INTERVAL, f(UNIT_INTERVAL))
-        assert_allclose(r.residues().prod(), 10, atol=1e-8)
-        
-        r = AAA(UNIT_INTERVAL, np.sin(10*np.pi*UNIT_INTERVAL))
-        assert_allclose(np.sort(np.abs(r.roots()))[18], 0.9, atol=1e-12)
-        
-        def f(z):
-            return (z - (3 + 3j))/(z + 2)
-        r = AAA(UNIT_INTERVAL, f(UNIT_INTERVAL))
-        assert_allclose(r.poles()[0]*r.roots()[0],  -6-6j, atol=1e-12)
-    
-    @pytest.mark.parametrize("func",
-                             [lambda z: np.zeros_like(z), lambda z: z, lambda z: 1j*z,
-                              lambda z: z**2 + z, lambda z: z**3 + z,
-                              lambda z: 1/(1.1 + z), lambda z: 1/(1 + 1j*z),
-                              lambda z: 1/(3 + z + z**2), lambda z: 1/(1.01 + z**3)])
-    def test_polynomials_and_reciprocals(self, func):
-        assert_allclose(AAA(UNIT_INTERVAL, func(UNIT_INTERVAL))(PTS),
-                        func(PTS), atol=2e-13)
-
-    # The following tests are taken from:
-    # https://github.com/macd/BaryRational.jl/blob/main/test/test_aaa.jl
-    def test_spiral(self):
-        z = np.exp(np.linspace(-0.5, 0.5 + 15j*np.pi, num=1000))
-        r = AAA(z, np.tan(np.pi*z/2))
-        assert_allclose(np.sort(np.abs(r.poles()))[:4], [1, 1, 3, 3], rtol=9e-7)
-    
-    def test_spiral_cleanup(self):
-        z = np.exp(np.linspace(-0.5, 0.5 + 15j*np.pi, num=1000))
-        # here we set `rtol=0` to force froissart doublets, without cleanup there
-        # are many spurious poles
-        with pytest.warns(RuntimeWarning):
-            r = AAA(z, np.tan(np.pi*z/2), rtol=0, max_terms=60, clean_up=False)
-        n_spurious = np.sum(np.abs(r.residues()) < 1e-14)
-        with pytest.warns(RuntimeWarning):
-            assert r.clean_up() >= 1
-        # check there are less potentially spurious poles than before
-        assert np.sum(np.abs(r.residues()) < 1e-14) < n_spurious
-        # check accuracy
-        assert_allclose(r(z), np.tan(np.pi*z/2), atol=6e-12, rtol=3e-12)
diff --git a/scipy/interpolate/tests/test_bary_rational.py b/scipy/interpolate/tests/test_bary_rational.py
new file mode 100644
index 0000000000000000000000000000000000000000..64832b2ce9fa33529b95c25d6a9b7948d75237d0
--- /dev/null
+++ b/scipy/interpolate/tests/test_bary_rational.py
@@ -0,0 +1,237 @@
+# Copyright (c) 2017, The Chancellor, Masters and Scholars of the University
+# of Oxford, and the Chebfun Developers. All rights reserved.
+#
+# Redistribution and use in source and binary forms, with or without
+# modification, are permitted provided that the following conditions are met:
+#     * Redistributions of source code must retain the above copyright
+#       notice, this list of conditions and the following disclaimer.
+#     * Redistributions in binary form must reproduce the above copyright
+#       notice, this list of conditions and the following disclaimer in the
+#       documentation and/or other materials provided with the distribution.
+#     * Neither the name of the University of Oxford nor the names of its
+#       contributors may be used to endorse or promote products derived from
+#       this software without specific prior written permission.
+#
+# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
+# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
+# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
+# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
+# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
+# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
+# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
+# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
+# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
+# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
+
+
+import numpy as np
+from numpy.testing import assert_allclose, assert_equal
+import pytest
+import scipy
+from scipy.interpolate import AAA
+
+TOL = 1e4 * np.finfo(np.float64).eps
+UNIT_INTERVAL = np.linspace(-1, 1, num=1000)
+PTS = np.logspace(-15, 0, base=10, num=500)
+PTS = np.concatenate([-PTS[::-1], [0], PTS])
+
+class TestAAA:
+    def test_input_validation(self):
+        with pytest.raises(ValueError, match="same size"):
+            AAA([0], [1, 1])
+        with pytest.raises(ValueError, match="1-D"):
+            AAA([[0], [0]], [[1], [1]])
+        with pytest.raises(ValueError, match="finite"):
+            AAA([np.inf], [1])
+        with pytest.raises(TypeError):
+            AAA([1], [1], max_terms=1.0)
+        with pytest.raises(ValueError, match="greater"):
+            AAA([1], [1], max_terms=-1)
+    
+    def test_convergence_error(self):
+        with pytest.warns(RuntimeWarning, match="AAA failed"):
+            AAA(UNIT_INTERVAL, np.exp(UNIT_INTERVAL),  max_terms=1)
+
+    @pytest.mark.parametrize("dtype", [np.float32, np.float64, np.complex64, 
+                                       np.complex128])
+    def test_dtype_preservation(self, dtype):
+        rtol = np.finfo(dtype).eps ** 0.75 * 100
+        rng = np.random.default_rng(59846294526092468)
+
+        z = np.linspace(-1, 1, dtype=dtype)
+        r = AAA(z, np.sin(z))
+        
+        z2 = rng.uniform(-1, 1, size=100).astype(dtype)
+        assert_allclose(r(z2), np.sin(z2), rtol=rtol)
+        assert r(z2).dtype == dtype
+        
+        assert r.support_points.dtype == dtype
+        assert r.support_values.dtype == dtype
+        assert r.weights.dtype == dtype
+        assert r.errors.dtype == z.real.dtype
+        assert r.poles().dtype == np.result_type(dtype, 1j)
+        assert r.residues().dtype == np.result_type(dtype, 1j)
+        assert r.roots().dtype == np.result_type(dtype, 1j)
+    
+    # The following tests are based on:
+    # https://github.com/chebfun/chebfun/blob/master/tests/chebfun/test_aaa.m
+    def test_exp(self):
+        f = np.exp(UNIT_INTERVAL)
+        r = AAA(UNIT_INTERVAL, f)
+
+        assert_allclose(r(UNIT_INTERVAL), f, atol=TOL)
+        assert_equal(r(np.nan), np.nan)
+        assert np.isfinite(r(np.inf))
+
+        m1 = r.support_points.size
+        r = AAA(UNIT_INTERVAL, f, rtol=1e-3)
+        assert r.support_points.size < m1
+
+    def test_tan(self):
+        f = np.tan(np.pi * UNIT_INTERVAL)
+        r = AAA(UNIT_INTERVAL, f)
+
+        assert_allclose(r(UNIT_INTERVAL), f, atol=10 * TOL, rtol=1.4e-7)
+        assert_allclose(np.min(np.abs(r.roots())), 0, atol=3e-10)
+        assert_allclose(np.min(np.abs(r.poles() - 0.5)), 0, atol=TOL)
+        # Test for spurious poles (poles with tiny residue are likely spurious)
+        assert np.min(np.abs(r.residues())) > 1e-13
+
+    def test_short_cases(self):
+        # Computed using Chebfun:
+        # >> format long
+        # >> [r, pol, res, zer, zj, fj, wj, errvec] = aaa([1 2], [0 1])
+        z = np.array([0, 1])
+        f = np.array([1, 2])
+        r = AAA(z, f, rtol=1e-13)
+        assert_allclose(r(z), f, atol=TOL)
+        assert_allclose(r.poles(), 0.5)
+        assert_allclose(r.residues(), 0.25)
+        assert_allclose(r.roots(), 1/3)
+        assert_equal(r.support_points, z)
+        assert_equal(r.support_values, f)
+        assert_allclose(r.weights, [0.707106781186547, 0.707106781186547])
+        assert_equal(r.errors, [1, 0])
+        
+        # >> format long
+        # >> [r, pol, res, zer, zj, fj, wj, errvec] = aaa([1 0 0], [0 1 2])
+        z = np.array([0, 1, 2])
+        f = np.array([1, 0, 0])
+        r = AAA(z, f, rtol=1e-13)
+        assert_allclose(r(z), f, atol=TOL)
+        assert_allclose(np.sort(r.poles()),
+                        np.sort([1.577350269189626, 0.422649730810374]))
+        assert_allclose(np.sort(r.residues()),
+                        np.sort([-0.070441621801729, -0.262891711531604]))
+        assert_allclose(np.sort(r.roots()), np.sort([2, 1]))
+        assert_equal(r.support_points, z)
+        assert_equal(r.support_values, f)
+        assert_allclose(r.weights, [0.577350269189626, 0.577350269189626,
+                                    0.577350269189626])
+        assert_equal(r.errors, [1, 1, 0])
+
+    def test_scale_invariance(self):
+        z = np.linspace(0.3, 1.5)
+        f = np.exp(z) / (1 + 1j)
+        r1 = AAA(z, f)
+        r2 = AAA(z, (2**311 * f).astype(np.complex128))
+        r3 = AAA(z, (2**-311 * f).astype(np.complex128))
+        assert_equal(r1(0.2j), 2**-311 * r2(0.2j))
+        assert_equal(r1(1.4), 2**311 * r3(1.4))
+
+    def test_log_func(self):
+        rng = np.random.default_rng(1749382759832758297)
+        z = rng.standard_normal(10000) + 3j * rng.standard_normal(10000)
+
+        def f(z):
+            return np.log(5 - z) / (1 + z**2)
+
+        r = AAA(z, f(z))
+        assert_allclose(r(0), f(0), atol=TOL)
+
+    def test_infinite_data(self):
+        z = np.linspace(-1, 1)
+        r = AAA(z, scipy.special.gamma(z))
+        assert_allclose(r(0.63), scipy.special.gamma(0.63), atol=1e-15)
+
+    def test_nan(self):
+        x = np.linspace(0, 20)
+        with np.errstate(invalid="ignore"):
+            f = np.sin(x) / x
+        r = AAA(x, f)
+        assert_allclose(r(2), np.sin(2) / 2, atol=1e-15)
+
+    def test_residues(self):
+        x = np.linspace(-1.337, 2, num=537)
+        r = AAA(x, np.exp(x) / x)
+        ii = np.flatnonzero(np.abs(r.poles()) < 1e-8)
+        assert_allclose(r.residues()[ii], 1, atol=1e-15)
+
+        r = AAA(x, (1 + 1j) * scipy.special.gamma(x))
+        ii = np.flatnonzero(abs(r.poles() - (-1)) < 1e-8)
+        assert_allclose(r.residues()[ii], -1 - 1j, atol=1e-15)
+    
+    # The following tests are based on:
+    # https://github.com/complexvariables/RationalFunctionApproximation.jl/blob/main/test/interval.jl
+    @pytest.mark.parametrize("func,atol,rtol",
+                             [(lambda x: np.abs(x + 0.5 + 0.01j), 5e-13, 1e-7),
+                              (lambda x: np.sin(1/(1.05 - x)), 2e-13, 1e-7),
+                              (lambda x: np.exp(-1/(x**2)), 3.5e-13, 0),
+                              (lambda x: np.exp(-100*x**2), 7e-13, 0),
+                              (lambda x: np.exp(-10/(1.2 - x)), 1e-14, 0),
+                              (lambda x: 1/(1+np.exp(100*(x + 0.5))), 2e-13, 1e-7),
+                              (lambda x: np.abs(x - 0.95), 1e-6, 1e-7)])
+    def test_basic_functions(self, func, atol, rtol):
+        with np.errstate(divide="ignore"):
+            f = func(PTS)
+        assert_allclose(AAA(UNIT_INTERVAL, func(UNIT_INTERVAL))(PTS),
+                        f, atol=atol, rtol=rtol)
+    
+    def test_poles_zeros_residues(self):
+        def f(z):
+            return (z+1) * (z+2) / ((z+3) * (z+4))
+        r = AAA(UNIT_INTERVAL, f(UNIT_INTERVAL))
+        assert_allclose(np.sum(r.poles() + r.roots()), -10, atol=1e-12)
+        
+        def f(z):
+            return 2/(3 + z) + 5/(z - 2j)
+        r = AAA(UNIT_INTERVAL, f(UNIT_INTERVAL))
+        assert_allclose(r.residues().prod(), 10, atol=1e-8)
+        
+        r = AAA(UNIT_INTERVAL, np.sin(10*np.pi*UNIT_INTERVAL))
+        assert_allclose(np.sort(np.abs(r.roots()))[18], 0.9, atol=1e-12)
+        
+        def f(z):
+            return (z - (3 + 3j))/(z + 2)
+        r = AAA(UNIT_INTERVAL, f(UNIT_INTERVAL))
+        assert_allclose(r.poles()[0]*r.roots()[0],  -6-6j, atol=1e-12)
+    
+    @pytest.mark.parametrize("func",
+                             [lambda z: np.zeros_like(z), lambda z: z, lambda z: 1j*z,
+                              lambda z: z**2 + z, lambda z: z**3 + z,
+                              lambda z: 1/(1.1 + z), lambda z: 1/(1 + 1j*z),
+                              lambda z: 1/(3 + z + z**2), lambda z: 1/(1.01 + z**3)])
+    def test_polynomials_and_reciprocals(self, func):
+        assert_allclose(AAA(UNIT_INTERVAL, func(UNIT_INTERVAL))(PTS),
+                        func(PTS), atol=2e-13)
+
+    # The following tests are taken from:
+    # https://github.com/macd/BaryRational.jl/blob/main/test/test_aaa.jl
+    def test_spiral(self):
+        z = np.exp(np.linspace(-0.5, 0.5 + 15j*np.pi, num=1000))
+        r = AAA(z, np.tan(np.pi*z/2))
+        assert_allclose(np.sort(np.abs(r.poles()))[:4], [1, 1, 3, 3], rtol=9e-7)
+    
+    def test_spiral_cleanup(self):
+        z = np.exp(np.linspace(-0.5, 0.5 + 15j*np.pi, num=1000))
+        # here we set `rtol=0` to force froissart doublets, without cleanup there
+        # are many spurious poles
+        with pytest.warns(RuntimeWarning):
+            r = AAA(z, np.tan(np.pi*z/2), rtol=0, max_terms=60, clean_up=False)
+        n_spurious = np.sum(np.abs(r.residues()) < 1e-14)
+        with pytest.warns(RuntimeWarning):
+            assert r.clean_up() >= 1
+        # check there are less potentially spurious poles than before
+        assert np.sum(np.abs(r.residues()) < 1e-14) < n_spurious
+        # check accuracy
+        assert_allclose(r(z), np.tan(np.pi*z/2), atol=6e-12, rtol=3e-12)
```

## Validation

```json
{
 "image_head": "8cbd7b58432e25b2dec1e62ba8e5b800b16ed4e1",
 "patch_applies": true,
 "test_files": [
  "scipy/interpolate/tests/test_bary_rational.py"
 ],
 "collected_before": 33,
 "collected_after": 33,
 "outcomes_before": {
  "PASSED": 33
 },
 "outcomes_after": {
  "PASSED": 33
 },
 "exit_before": 0,
 "exit_after": 0,
 "tail_before": "ED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-2e-13-1e-07_1]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-1e-06-1e-07]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_poles_zeros_residues\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>0]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>1]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>2]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>3]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>4]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>5]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>6]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>7]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>8]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_spiral\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_spiral_cleanup\n============================= 33 passed in 11.24s ==============================",
 "tail_after": "ED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-2e-13-1e-07_1]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_basic_functions[<lambda>-1e-06-1e-07]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_poles_zeros_residues\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>0]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>1]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>2]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>3]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>4]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>5]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>6]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>7]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_polynomials_and_reciprocals[<lambda>8]\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_spiral\nPASSED scipy/interpolate/tests/test_bary_rational.py::TestAAA::test_spiral_cleanup\n============================== 33 passed in 9.60s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

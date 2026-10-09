# scipy__scipy-21462

[back to the list](README.md) -- **ENH: linalg.eig: support batched input**

| field | value |
|---|---|
| pull request | [scipy/scipy#21462](https://github.com/scipy/scipy/pull/21462) (created 2024-08-27, merged 2024-12-18) |
| ChaCo lists | full, ablation |
| status | **runnable** -- 32 developer test(s) flip; oracle reproduces it |
| base commit | [`639bdb83ef66`](https://github.com/scipy/scipy/commit/639bdb83ef66dfa49158edecafffb3eb463c9151) (2024-12-17), first parent of the merge commit |
| merge commit | [`6fbd2885ba29`](https://github.com/scipy/scipy/commit/6fbd2885ba29ec828f36a1fa31e89ae292bf918f) |
| issues closed | none |
| version | 1.16 |
| image | `f2p-chaco/scipy__scipy-21462:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-21462.Dockerfile) |
| source files (`patch`) | `doc/Makefile`, `doc/convert_notebooks.py`, `doc/source/tutorial/linalg.rst`, `doc/source/tutorial/linalg_batch.md`, `scipy/_lib/_util.py`, `scipy/linalg/_decomp.py` |
| test files (`test_patch`) | `scipy/linalg/tests/test_decomp.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (32)

- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-False-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-False-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-False-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-False-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-False-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-False-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-False-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-False-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-True-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-True-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-True-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-False-True-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-False-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-False-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-False-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-False-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-True-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-True-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-True-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[float32-True-True-True-True]`

## PASS_TO_PASS (526)

<details><summary>show</summary>

- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_low_dimensionality_error`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_non_associated_error`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_not_conjugate_pairs`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_not_square_error`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_random_1d_stacked_arrays`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_random_2d_stacked_arrays`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array0x0real`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array2x2_complex`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array2x2_real`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array3x3_complex`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array3x3_real`
- `scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_swapped_v_w_error`
- `scipy/linalg/tests/test_decomp.py::TestDatacopied::test_datacopied`
- `scipy/linalg/tests/test_decomp.py::TestDiagSVD::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_bad_geneig`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_falker`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_gh_11577`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_gh_3054`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_make_eigvals`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_not_square_error`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_shape_mismatch`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_simple_complex_eig`
- `scipy/linalg/tests/test_decomp.py::TestEig::test_singular`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_dgbtrf`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_dgbtrs`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_dsbev`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_dsbevd`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_dsbevx`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_eig_banded`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_eigvals_banded`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_zgbtrf`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_zgbtrs`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_zhbevd`
- `scipy/linalg/tests/test_decomp.py::TestEigBanded::test_zhbevx`
- `scipy/linalg/tests/test_decomp.py::TestEigTridiagonal::test_degenerate`
- `scipy/linalg/tests/test_decomp.py::TestEigTridiagonal::test_eigh_tridiagonal`
- `scipy/linalg/tests/test_decomp.py::TestEigTridiagonal::test_eigh_tridiagonal_1x1`
- `scipy/linalg/tests/test_decomp.py::TestEigTridiagonal::test_eigvalsh_tridiagonal`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_finite`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestEigVals::test_simple_tr`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_1x1_lwork[ev]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_1x1_lwork[evd]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_1x1_lwork[evr]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_1x1_lwork[evx]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_eigh_integer`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_eigh_of_sparse`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_eigvalsh_new_args`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_nonpositive_b`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_value_subsets`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gv-1]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gv-2]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gv-3]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gvd-1]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gvd-2]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gvd-3]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gvx-1]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gvx-2]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_generalized[gvx-3]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[ev-complex128]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[ev-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[ev-float32]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[ev-float64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evd-complex128]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evd-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evd-float32]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evd-float64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evr-complex128]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evr-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evr-float32]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evr-float64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evx-complex128]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evx-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evx-float32]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_various_drivers_standard[evx-float64]`
- `scipy/linalg/tests/test_decomp.py::TestEigh::test_wrong_inputs`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_2x2`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_random`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_random_complex`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_simple2`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_simple3`
- `scipy/linalg/tests/test_decomp.py::TestHessenberg::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesdd-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesdd-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesdd-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesdd-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesvd-False-False]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesvd-False-True]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesvd-True-False]`
- `scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesvd-True-True]`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_cef`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_diff_input_types`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_iuc`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_lhp`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_ouc`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_ref`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_rhp`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZ::test_sort_explicit`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZWorkspaceSize::test_decompose`
- `scipy/linalg/tests/test_decomp.py::TestOrdQZWorkspaceSize::test_decompose_ouc`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_eig`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_eig_banded`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_eigh`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_eigvals`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_eigvals_banded`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_eigvalsh`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_hessenberg`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_lu`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_lu_factor`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_lu_solve`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_qr`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_rq`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_schur`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_schur_complex`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_svd`
- `scipy/linalg/tests/test_decomp.py::TestOverwrite::test_svdvals`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_empty[0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_empty[0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_empty[2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_lwork`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_multiply_empty`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_complex`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_complex_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_complex_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_complex_right`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_right`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_tall`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_tall_e`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_tall_e_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_tall_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_tall_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_tall_right`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_trap`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_random_trap_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-False-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex128-True-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-False-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[complex64-True-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-False-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float32-True-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-False-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_shape_dtype[float64-True-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_left_conjugate`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_left_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_right`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_right_conjugate`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_right_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_complex_tall_left_conjugate`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat_e`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat_e_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat_left_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat_right`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_fat_right_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_left_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_right`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_right_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_complex_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_e`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_e_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_left`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_left_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_right`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_tall_right_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_trap`
- `scipy/linalg/tests/test_decomp.py::TestQR::test_simple_trap_pivoting`
- `scipy/linalg/tests/test_decomp.py::TestQZ::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestQZ::test_qz_complex`
- `scipy/linalg/tests/test_decomp.py::TestQZ::test_qz_complex64`
- `scipy/linalg/tests/test_decomp.py::TestQZ::test_qz_double`
- `scipy/linalg/tests/test_decomp.py::TestQZ::test_qz_double_complex`
- `scipy/linalg/tests/test_decomp.py::TestQZ::test_qz_double_sort`
- `scipy/linalg/tests/test_decomp.py::TestQZ::test_qz_single`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_empty[0-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_empty[0-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_empty[2-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_r`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_random`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_random_complex`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_random_complex_economic`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_random_tall`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_random_trap`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_random_trap_economic`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex128-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[complex64-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float32-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_shape_dtype[float64-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_simple_fat`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_simple_tall`
- `scipy/linalg/tests/test_decomp.py::TestRQ::test_simple_trap`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_crash_2609`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_simple_overdet`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_simple_overdet_complex`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_simple_underdet`
- `scipy/linalg/tests/test_decomp.py::TestSVDVals::test_simple_underdet_complex`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_crash_1580`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_degenerate`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-0-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-0-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-0-float32]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-0-float]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-0-int]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-2-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-2-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-2-float32]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-2-float]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[0-2-int]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[2-0-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[2-0-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[2-0-float32]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[2-0-float]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_empty[2-0-int]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_gh_5039`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_random`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_random_complex`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex128-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[complex64-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float32-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_shape_dtype[float64-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_simple_overdet`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_simple_singular`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESDD::test_simple_underdet`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_crash_1580`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_degenerate`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-0-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-0-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-0-float32]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-0-float]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-0-int]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-2-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-2-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-2-float32]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-2-float]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[0-2-int]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[2-0-complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[2-0-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[2-0-float32]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[2-0-float]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_empty[2-0-int]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_gh_5039`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_random`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_random_complex`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex128-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[complex64-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float32-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-0-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-0-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-0-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-1-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-1-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-1-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-2-0]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-2-1]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_shape_dtype[float64-2-2]`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_simple_complex`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_simple_overdet`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_simple_singular`
- `scipy/linalg/tests/test_decomp.py::TestSVD_GESVD::test_simple_underdet`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_check_finite`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_empty[float]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_empty[int]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[complex128-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[complex128-real]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[complex64-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[complex64-real]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[float32-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[float32-real]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[float64-complex]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_custom[float64-real]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex128-complex-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex128-complex-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex128-real-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex128-real-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex64-complex-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex64-complex-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex64-real-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[complex64-real-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float32-complex-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float32-complex-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float32-real-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float32-real-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float64-complex-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float64-complex-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float64-real-iuc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_gh_13137_sort_str[float64-real-ouc]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_simple`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_sort[<lambda>-expected_diag4]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_sort[iuc-expected_diag2]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_sort[lhp-expected_diag0]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_sort[ouc-expected_diag3]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_sort[rhp-expected_diag1]`
- `scipy/linalg/tests/test_decomp.py::TestSchur::test_sort_errors`
- `scipy/linalg/tests/test_decomp.py::test_aligned_mem`
- `scipy/linalg/tests/test_decomp.py::test_aligned_mem_complex`
- `scipy/linalg/tests/test_decomp.py::test_aligned_mem_float`
- `scipy/linalg/tests/test_decomp.py::test_orth`
- `scipy/linalg/tests/test_decomp.py::test_orth_empty[complex64]`
- `scipy/linalg/tests/test_decomp.py::test_orth_empty[complex]`
- `scipy/linalg/tests/test_decomp.py::test_orth_empty[float32]`
- `scipy/linalg/tests/test_decomp.py::test_orth_empty[float]`
- `scipy/linalg/tests/test_decomp.py::test_orth_empty[int]`
- `scipy/linalg/tests/test_decomp.py::test_orth_memory_efficiency`
- `scipy/linalg/tests/test_decomp.py::test_subspace_angles`
- `scipy/linalg/tests/test_decomp.py::test_svd_gesdd_nofegfault`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #21462: ENH: linalg.eig: support batched input

#### Reference issue
Follow-up to gh-21446
Toward gh-21466

#### What does this implement/fix?
This adds support for n-dimensional batch input to `linalg.eig`.

#### Additional information
~~I'll write more to motivate this PR shortly.~~ (Done - see gh-21466). A few things to keep in mind:

- Addition of batch support in compiled code would provide speed and memory improvements, but this will take some time. In the meantime, the decorator introduced in this PR can help keep the `linalg` API more self-consistent and consistent with the NumPy API.
- I've included a test for `eig`, but I would really appreciate it if someone else would be willing to write a more general property-based test. In `stats`, we have standard tests for the `axis`, `nan_policy`, and `keepdims` arguments that are more thorough than ad hoc tests previously included for these features.
- The decorator can also add support for array-API compatible arrays if desired. In `stats`, we've also used a decorator to help standardize documentation and input validation. In `linalg`, it might be useful to standardize notes about common arguments like `overwrite_` and `check_finite` and implement standard shape/dtype checks.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

````diff
diff --git a/doc/Makefile b/doc/Makefile
index 36ad778a0040e119cdfc355c6d9f117b64f7a2e8..ff7950101df6906c56675ae0fc2dd0ed844f159f 100644
--- a/doc/Makefile
+++ b/doc/Makefile
@@ -117,7 +117,6 @@ html-build:
 convert-notebooks:
 	$(PYTHON) convert_notebooks.py
 
-
 coverage: build version-check
 	mkdir -p build/coverage build/doctrees
 	$(SPHINXBUILD) -b coverage $(ALLSPHINXOPTS) build/coverage $(FILES)
diff --git a/doc/convert_notebooks.py b/doc/convert_notebooks.py
index 40376cb2e2718e3bc719c0a09fa5feb1b72f4f5b..09532adab972f9932c9c1947fc392e2fd5039060 100644
--- a/doc/convert_notebooks.py
+++ b/doc/convert_notebooks.py
@@ -40,6 +40,7 @@ if __name__ == '__main__':
     os.makedirs(os.path.expanduser(_contents_path), exist_ok=True)
 
     md_files = glob.glob("source/tutorial/stats/*.md")
+    md_files += glob.glob("source/tutorial/*.md")
     is_dirty = call_jupytext(
         md_files,
         _contents_path,
diff --git a/doc/source/tutorial/linalg.rst b/doc/source/tutorial/linalg.rst
index 2c0068bbe23afdb3a78e70008c5c2134fe8d2597..52f0026c8b6aa0a5158b688669604ec3af075503 100644
--- a/doc/source/tutorial/linalg.rst
+++ b/doc/source/tutorial/linalg.rst
@@ -956,3 +956,21 @@ Van der Monde         `numpy.vander`                     Create a Van der Monde
 
 
 For examples of the use of these functions, see their respective docstrings.
+
+Advanced Features
+-----------------
+
+Batch Support
+^^^^^^^^^^^^^
+Some of SciPy's linear algebra functions can process batches of scalars, 1D-, or
+2D-arrays given N-d array input.
+For example, a linear algebra function that typically accepts a (2D) matrix may accept
+an array of shape ``(4, 3, 2)``, which it would interpret as a batch of four 3-by-2
+matrices. In this case, we say that the the *core shape* of the input is (3, 2) and the
+*batch shape* is ``(4,)``. Likewise, a linear algebra function that typically accepts
+a (1D) vector would treat a ``(4, 3, 2)`` array as a ``(4, 3)`` batch of vectors,
+in which case the *core shape* of the input is ``(2,)`` and the *batch shape* is
+``(4, 3)``. The length of the core shape is also referred to as the *core dimension*.
+In these cases, the final shape of the output is the batch shape of the input
+concatenated with the core shape of the output (i.e., the shape of the output when
+the batch shape of the input is ``()``). For more information, see :doc:`linalg_batch`.
diff --git a/doc/source/tutorial/linalg_batch.md b/doc/source/tutorial/linalg_batch.md
new file mode 100644
index 0000000000000000000000000000000000000000..62f42b4de33cc5523e89cc2ab9a533fdc7c57154
--- /dev/null
+++ b/doc/source/tutorial/linalg_batch.md
@@ -0,0 +1,153 @@
+---
+jupytext:
+  text_representation:
+    extension: .md
+    format_name: myst
+    format_version: 0.13
+    jupytext_version: 1.16.4
+kernelspec:
+  display_name: Python 3 (ipykernel)
+  language: python
+  name: python3
+orphan: true
+---
+
+```{eval-rst}
+.. jupyterlite:: ../_contents/linalg_batch.ipynb
+   :new_tab: True
+```
+
+(linalg_batch)=
+# Batched Linear Operations
+
+Some of SciPy's linear algebra functions support N-dimensional array input. These operations have not been mathematically generalized to higher-order tensors; rather, the indicated operation is performed on a *batch* (or "stack") of input scalars, vectors, and/or matrices.
+
+Consider the `linalg.det` function, which maps a matrix to a scalar.
+
+```{code-cell} ipython3
+import numpy as np
+from scipy import linalg
+A = np.eye(3)
+linalg.det(A)
+```
+
+Sometimes we need the determinant of a batch of matrices of the same dimensionality.
+
+```{code-cell} ipython3
+batch = [i*np.eye(3) for i in range(1, 4)]
+batch
+```
+
+We could perform the operation for each element of the batch in a loop or list comprehension:
+
+```{code-cell} ipython3
+[linalg.det(A) for A in batch]
+```
+
+However, just as we might use NumPy broadcasting and vectorization rules to create the batch of matrices in the first place:
+
+```{code-cell} ipython3
+i = np.arange(1, 4).reshape(-1, 1, 1)
+batch = i * np.eye(3)
+batch
+```
+
+we might also wish to perform the determinant operation on all of the matrices in one function call.
+
+```{code-cell} ipython3
+linalg.det(batch)
+```
+
+In SciPy, we prefer the term "batch" instead of "stack" because the idea is generalized to N-dimensional batches. Suppose the input is a 2 x 4 batch of 3 x 3 matrices.
+
+```{code-cell} ipython3
+batch_shape = (2, 4)
+i = np.arange(np.prod(batch_shape)).reshape(*batch_shape, 1, 1)
+input = i * np.eye(3)
+```
+
+In this case, we say that the *batch shape* is `(2, 4)`, and the *core shape* of the input is `(3, 3)`. The net shape of the input is the sum (concatenation) of the batch shape and core shape.
+
+```{code-cell} ipython3
+input.shape
+```
+
+Since each 3 x 3 matrix is converted to a zero-dimensional scalar, we say that the core shape of the outuput is `()`. The shape of the output is the sum of the batch shape and core shape, so the result is a 2 x 4 array.
+
+```{code-cell} ipython3
+output = linalg.det(input)
+output
+```
+
+```{code-cell} ipython3
+output.shape
+```
+
+Not all linear algebra functions map to scalars. For instance, the {func}`scipy.linalg.expm` function maps from a matrix to a matrix with the same shape.
+
+```{code-cell} ipython3
+A = np.eye(3)
+linalg.expm(A)
+```
+
+In this case, the core shape of the output is `(3, 3)`, so with a batch shape of `(2, 4)`, we expect an output of shape `(2, 4, 3, 3)`.
+
+```{code-cell} ipython3
+output = linalg.expm(input)
+output.shape
+```
+
+Generalization of these rules to functions with multiple inputs and outputs is straightforward. For instance, the {func}`scipy.linalg.eig` function produces two outputs by default, a vector and a matrix.
+
+```{code-cell} ipython3
+evals, evecs = linalg.eig(A)
+evals.shape, evecs.shape
+```
+
+In this case, the core shape of the output vector is `(3,)` and the core shape of the output matrix is `(3, 3)`. The shape of each output is the batch shape plus the core shape as before.
+
+```{code-cell} ipython3
+evals, evecs = linalg.eig(input)
+evals.shape, evecs.shape
+```
+
+When there is more than one input, there is no complication if the input shapes are identical.
+
+```{code-cell} ipython3
+evals, evecs = linalg.eig(input, b=input)
+evals.shape, evecs.shape
+```
+
+The rules when the shapes are not identical follow logically. Each input can have its own batch shape as long as the shapes are broadcastable according to [NumPy's broadcasting rules](#array-broadcasting-in-numpy). The net batch shape is the broadcasted shape of the individual batch shapes, and the shape of each output is the net batch shape plus its core shape.
+
+```{code-cell} ipython3
+rng = np.random.default_rng(2859239482)
+
+# Define input core shapes
+m = 3
+core_shape_a = (m, m)
+core_shape_b = (m, m)
+
+# Define broadcastable batch shapes
+batch_shape_a = (2, 4)
+batch_shape_b = (5, 1, 4)
+
+# Define output core shapes
+core_shape_evals = (m,)
+core_shape_evecs = (m, m)
+
+# Predict shapes of outputs: broadcast batch shapes,
+# and append output core shapes
+net_batch_shape = np.broadcast_shapes(batch_shape_a, batch_shape_b)
+output_shape_evals = net_batch_shape + core_shape_evals
+output_shape_evecs = net_batch_shape + core_shape_evecs
+output_shape_evals, output_shape_evecs
+```
+
+```{code-cell} ipython3
+# Check predictions
+input_a = rng.random(batch_shape_a + core_shape_a)
+input_b = rng.random(batch_shape_b + core_shape_b)
+evals, evecs = linalg.eig(input_a, b=input_b)
+evals.shape, evecs.shape
+```
diff --git a/scipy/_lib/_util.py b/scipy/_lib/_util.py
index 4a1307d0a221bbcf1dd283b21f9f61c29359e591..a70317c6400fc9eca6b288ef5bf9329dd2c14410 100644
--- a/scipy/_lib/_util.py
+++ b/scipy/_lib/_util.py
@@ -1174,3 +1174,97 @@ def _dict_formatter(d, n=0, mplus=1, sorter=None):
                              formatter={'float_kind': _float_formatter_10}):
             s = str(d)
     return s
+
+
+def _apply_over_batch(*argdefs):
+    """
+    Factory for decorator that applies a function over batched arguments.
+
+    Array arguments may have any number of core dimensions (typically 0,
+    1, or 2) and any broadcastable batch shapes. There may be any
+    number of array outputs of any number of dimensions. Assumptions
+    right now - which are satisfied by all functions of interest in `linalg` -
+    are that all array inputs are consecutive keyword or positional arguments,
+    and that the wrapped function returns either a single array or a tuple of
+    arrays. It's only as general as it needs to be right now - it can be extended.
+
+    Parameters
+    ----------
+    *argdefs : tuple of (str, int)
+        Definitions of array arguments: the keyword name of the argument, and
+        the number of core dimensions.
+
+    Example:
+    --------
+    `linalg.eig` accepts two matrices as the first two arguments `a` and `b`, where
+    `b` is optional, and returns one array or a tuple of arrays, depending on the
+    values of other positional or keyword arguments. To generate a wrapper that applies
+    the function over batches of `a` and optionally `b` :
+
+    >>> _apply_over_batch(('a', 2), ('b', 2))
+    """
+    names, ndims = list(zip(*argdefs))
+    n_arrays = len(names)
+
+    def decorator(f):
+        @functools.wraps(f)
+        def wrapper(*args, **kwargs):
+            args = list(args)
+
+            # Ensure all arrays in `arrays`, other arguments in `other_args`/`kwargs`
+            arrays, other_args = args[:n_arrays], args[n_arrays:]
+            for i, name in enumerate(names):
+                if name in kwargs:
+                    if i + 1 <= len(args):
+                        raise ValueError(f'{f.__name__}() got multiple values '
+                                         f'for argument `{name}`.')
+                    else:
+                        arrays.append(kwargs.pop(name))
+
+            # Determine core and batch shapes
+            batch_shapes = []
+            core_shapes = []
+            for i, (array, ndim) in enumerate(zip(arrays, ndims)):
+                array = None if array is None else np.asarray(array)
+                shape = () if array is None else array.shape
+                arrays[i] = array
+                batch_shapes.append(shape[:-ndim] if ndim > 0 else shape)
+                core_shapes.append(shape[-ndim:] if ndim > 0 else shape)
+
+            # Early exit if call is not batched
+            if not any(batch_shapes):
+                return f(*arrays, *other_args, **kwargs)
+
+            # Determine broadcasted batch shape
+            batch_shape = np.broadcast_shapes(*batch_shapes)  # Gives OK error message
+
+            # Broadcast arrays to appropriate shape
+            for i, (array, core_shape) in enumerate(zip(arrays, core_shapes)):
+                if array is None:
+                    continue
+                arrays[i] = np.broadcast_to(array, batch_shape + core_shape)
+
+            # Main loop
+            results = []
+            for index in np.ndindex(batch_shape):
+                result = f(*(array[index] for array in arrays), *other_args, **kwargs)
+                # Assume `result` is either a tuple or single array. This is easily
+                # generalized by allowing the contributor to pass an `unpack_result`
+                # callable to the decorator factory.
+                result = (result,) if not isinstance(result, tuple) else result
+                results.append(result)
+            results = list(zip(*results))
+
+            # Reshape results
+            for i, result in enumerate(results):
+                result = np.stack(result)
+                core_shape = result.shape[1:]
+                results[i] = np.reshape(result, batch_shape + core_shape)
+
+            # Assume `result` should be a single array if there is only one element or
+            # a `tuple` otherwise. This is easily generalized by allowing the
+            # contributor to pass an `pack_result` callable to the decorator factory.
+            return results[0] if len(results) == 1 else results
+
+        return wrapper
+    return decorator
diff --git a/scipy/linalg/_decomp.py b/scipy/linalg/_decomp.py
index c520d6b04b6bf0a22c4fcad62d98a17faea7c9fd..1062368644074ab5c8164878e118d244c9caf2e3 100644
--- a/scipy/linalg/_decomp.py
+++ b/scipy/linalg/_decomp.py
@@ -21,7 +21,7 @@ from numpy import (array, isfinite, inexact, nonzero, iscomplexobj,
                    flatnonzero, conj, asarray, argsort, empty,
                    iscomplex, zeros, einsum, eye, inf)
 # Local imports
-from scipy._lib._util import _asarray_validated
+from scipy._lib._util import _asarray_validated, _apply_over_batch
 from ._misc import LinAlgError, _datacopied, norm
 from .lapack import get_lapack_funcs, _compute_lwork
 
@@ -111,6 +111,7 @@ def _geneig(a1, b1, left, right, overwrite_a, overwrite_b,
     return w, vr
 
 
+@_apply_over_batch(('a', 2), ('b', 2))
 def eig(a, b=None, left=False, right=True, overwrite_a=False,
         overwrite_b=False, check_finite=True, homogeneous_eigvals=False):
     """
@@ -123,6 +124,11 @@ def eig(a, b=None, left=False, right=True, overwrite_a=False,
 
     where ``.H`` is the Hermitian conjugation.
 
+    The documentation is written assuming array arguments are of specified
+    "core" shapes. However, array argument(s) of this function may have additional
+    "batch" dimensions prepended to the core shape. In this case, the array is treated
+    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.
+
     Parameters
     ----------
     a : (M, M) array_like
````

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/linalg/tests/test_decomp.py b/scipy/linalg/tests/test_decomp.py
index 605496721f8eec7a522fbba0a77ed33d6c1fdeaf..fadacd4b51ff76b5a37b8245059d0f93f2728e69 100644
--- a/scipy/linalg/tests/test_decomp.py
+++ b/scipy/linalg/tests/test_decomp.py
@@ -404,6 +404,36 @@ class TestEig:
         assert vr.shape == (0, 0)
         assert vr.dtype == vr_n.dtype
 
+    @pytest.mark.parametrize("include_B", [False, True])
+    @pytest.mark.parametrize("left", [False, True])
+    @pytest.mark.parametrize("right", [False, True])
+    @pytest.mark.parametrize("homogeneous_eigvals", [False, True])
+    @pytest.mark.parametrize("dtype", [np.float32, np.complex128])
+    def test_nd_input(self, include_B, left, right, homogeneous_eigvals, dtype):
+        batch_shape = (3, 2)
+        core_shape = (4, 4)
+        rng = np.random.default_rng(3249823598235)
+        A = rng.random(batch_shape + core_shape).astype(dtype)
+        B = rng.random(batch_shape + core_shape).astype(dtype)
+        kwargs = dict(right=right, homogeneous_eigvals=homogeneous_eigvals)
+
+        if include_B:
+            res = eig(A, b=B, left=left, **kwargs)
+        else:
+            res = eig(A, left=left, **kwargs)
+
+        for i in range(batch_shape[0]):
+            for j in range(batch_shape[1]):
+                if include_B:
+                    ref = eig(A[i, j], b=B[i, j], left=left, **kwargs)
+                else:
+                    ref = eig(A[i, j], left=left, **kwargs)
+
+                if left or right:
+                    for k in range(len(ref)):
+                        assert_allclose(res[k][i, j], ref[k])
+                else:
+                    assert_allclose(res[i, j], ref)
 
 
 class TestEigBanded:
```

## Validation

```json
{
 "test_files": [
  "scipy/linalg/tests/test_decomp.py"
 ],
 "collected_before": 561,
 "collected_after": 561,
 "outcomes_before": {
  "PASSED": 526,
  "FAILED": 32,
  "SKIPPED": 2,
  "XFAIL": 1
 },
 "outcomes_after": {
  "PASSED": 558,
  "SKIPPED": 2,
  "XFAIL": 1
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "t[complex128-False-False-False-True]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-False-True-False]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-False-True-True]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-False-False]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-False-True]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-True-False]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-False-True-True-True]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-False-False]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-False-True]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-True-False]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-False-True-True]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-False-False]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-False-True]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-True-False]\nFAILED scipy/linalg/tests/test_decomp.py::TestEig::test_nd_input[complex128-True-True-True-True]\n============ 32 failed, 526 passed, 2 skipped, 1 xfailed in 20.25s =============",
 "tail_after": "_decomp.py::TestNullSpace::test_null_space_options[gesvd-False-True]\nPASSED scipy/linalg/tests/test_decomp.py::TestNullSpace::test_null_space_options[gesvd-False-False]\nPASSED scipy/linalg/tests/test_decomp.py::test_subspace_angles\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array0x0real\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array2x2_real\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array2x2_complex\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array3x3_real\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_single_array3x3_complex\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_random_1d_stacked_arrays\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_random_2d_stacked_arrays\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_low_dimensionality_error\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_not_square_error\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_swapped_v_w_error\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_non_associated_error\nPASSED scipy/linalg/tests/test_decomp.py::TestCDF2RDF::test_not_conjugate_pairs\nSKIPPED [2] scipy/linalg/tests/test_decomp.py:1142: 64-bit LAPACK required\nXFAIL scipy/linalg/tests/test_decomp.py::test_lapack_misaligned - reason: [NOTRUN] Ticket #1152, triggers a segfault in rare cases.\n================== 558 passed, 2 skipped, 1 xfailed in 11.68s ==================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

# scipy__scipy-20382

[back to the list](README.md) -- **MAINT: lint: enforce `numpy as np` alias**

| field | value |
|---|---|
| pull request | [scipy/scipy#20382](https://github.com/scipy/scipy/pull/20382) (created 2024-04-03, merged 2024-04-03) |
| ChaCo lists | full, ablation |
| status | **not-fail-to-pass** -- no developer test fails before the change and passes after (1926 pass on both sides) |
| base commit | [`bd15d2426647`](https://github.com/scipy/scipy/commit/bd15d2426647732b0888afd1cf9edf0838b3e1c0) (2024-04-03), first parent of the merge commit |
| merge commit | [`a0c834099ba5`](https://github.com/scipy/scipy/commit/a0c834099ba53d51041079e6f70108f46e837104) |
| issues closed | none |
| version | 1.14 |
| image | `f2p-chaco/scipy__scipy-20382:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-20382.Dockerfile) |
| source files (`patch`) | `scipy/constants/_constants.py`, `scipy/linalg/blas.py`, `scipy/linalg/lapack.py`, `tools/lint.toml` |
| test files (`test_patch`) | `scipy/linalg/tests/test_lapack.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (1926)

<details><summary>show</summary>

- `scipy/linalg/tests/test_lapack.py::TestBlockedQR::test_geqrt_gemqrt`
- `scipy/linalg/tests/test_lapack.py::TestBlockedQR::test_tpqrt_tpmqrt`
- `scipy/linalg/tests/test_lapack.py::TestDlasd4::test_sing_val_update`
- `scipy/linalg/tests/test_lapack.py::TestDpotr::test_gh_2691`
- `scipy/linalg/tests/test_lapack.py::TestFlapackSimple::test_gebal`
- `scipy/linalg/tests/test_lapack.py::TestFlapackSimple::test_gehrd`
- `scipy/linalg/tests/test_lapack.py::TestFlapackSimple::test_lange`
- `scipy/linalg/tests/test_lapack.py::TestFlapackSimple::test_trsyl`
- `scipy/linalg/tests/test_lapack.py::TestHetrd::test_hetrd[1-float32-complex64]`
- `scipy/linalg/tests/test_lapack.py::TestHetrd::test_hetrd[1-float64-complex128]`
- `scipy/linalg/tests/test_lapack.py::TestHetrd::test_hetrd[3-float32-complex64]`
- `scipy/linalg/tests/test_lapack.py::TestHetrd::test_hetrd[3-float64-complex128]`
- `scipy/linalg/tests/test_lapack.py::TestHetrd::test_hetrd_with_zero_dim_array[complex128]`
- `scipy/linalg/tests/test_lapack.py::TestHetrd::test_hetrd_with_zero_dim_array[complex64]`
- `scipy/linalg/tests/test_lapack.py::TestLapack::test_clapack`
- `scipy/linalg/tests/test_lapack.py::TestLapack::test_flapack`
- `scipy/linalg/tests/test_lapack.py::TestLeastSquaresSolvers::test_gels`
- `scipy/linalg/tests/test_lapack.py::TestLeastSquaresSolvers::test_gelsd`
- `scipy/linalg/tests/test_lapack.py::TestLeastSquaresSolvers::test_gelss`
- `scipy/linalg/tests/test_lapack.py::TestLeastSquaresSolvers::test_gelsy`
- `scipy/linalg/tests/test_lapack.py::TestRegression::test_ticket_1645`
- `scipy/linalg/tests/test_lapack.py::TestSytrd::test_sytrd[1-float32]`
- `scipy/linalg/tests/test_lapack.py::TestSytrd::test_sytrd[1-float64]`
- `scipy/linalg/tests/test_lapack.py::TestSytrd::test_sytrd[3-float32]`
- `scipy/linalg/tests/test_lapack.py::TestSytrd::test_sytrd[3-float64]`
- `scipy/linalg/tests/test_lapack.py::TestSytrd::test_sytrd_with_zero_dim_array[float32]`
- `scipy/linalg/tests/test_lapack.py::TestSytrd::test_sytrd_with_zero_dim_array[float64]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_invalid_argument_raises_exception[Invalid-N-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_invalid_argument_raises_exception[U-Invalid-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_invalid_argument_raises_exception[U-N-Invalid]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_invalid_matrix_shapes[5-5-0-5]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_invalid_matrix_shapes[5-5-3-5]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_nag_example_f07vef_f07vsf[complex128]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_nag_example_f07vef_f07vsf[complex64]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_nag_example_f07vef_f07vsf[float32]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_nag_example_f07vef_f07vsf[float64]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-complex128-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-complex128-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-complex128-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-complex64-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-complex64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-complex64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-float32-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-float32-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-float64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-L-float64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-complex128-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-complex128-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-complex128-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-complex64-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-complex64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-complex64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-float32-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-float32-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-float64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[N-U-float64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-complex128-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-complex128-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-complex128-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-complex64-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-complex64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-complex64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-float32-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-float32-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-float64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-L-float64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-complex128-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-complex128-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-complex128-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-complex64-C]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-complex64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-complex64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-float32-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-float32-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-float64-N]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_random_matrices[U-U-float64-T]`
- `scipy/linalg/tests/test_lapack.py::TestTbtrs::test_zero_element_in_diagonal`
- `scipy/linalg/tests/test_lapack.py::test_geequ`
- `scipy/linalg/tests/test_lapack.py::test_gees_trexc[complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gees_trexc[complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gees_trexc[float32]`
- `scipy/linalg/tests/test_lapack.py::test_gees_trexc[float64]`
- `scipy/linalg/tests/test_lapack.py::test_gees_trsen[complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gees_trsen[complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gees_trsen[float32]`
- `scipy/linalg/tests/test_lapack.py::test_gees_trsen[float64]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_NAG[A0-sva_expect0-u_expect0-v_expect0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_edge_arguments[float32]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_edge_arguments[float64]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-0-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-1-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-2-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-0-3-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-0-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-1-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-2-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[0-1-3-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-0-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-1-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-2-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-0-3-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-0-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-1-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-2-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-0-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-1-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-2-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-0-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-0-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-0-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-0-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-1-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-1-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-1-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-1-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-2-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-2-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-2-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-2-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-3-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-3-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-3-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-3-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-4-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-4-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-4-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-4-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-5-float32-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-5-float32-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-5-float64-size0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_general[1-1-3-3-5-float64-size1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_invalid_job_arguments[kwargs0]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_invalid_job_arguments[kwargs1]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_invalid_job_arguments[kwargs2]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_invalid_job_arguments[kwargs3]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_invalid_job_arguments[kwargs4]`
- `scipy/linalg/tests/test_lapack.py::test_gejsv_invalid_job_arguments[kwargs5]`
- `scipy/linalg/tests/test_lapack.py::test_generalized_eigh_lworks[he-gv]`
- `scipy/linalg/tests/test_lapack.py::test_generalized_eigh_lworks[he-gvx]`
- `scipy/linalg/tests/test_lapack.py::test_generalized_eigh_lworks[sy-gv]`
- `scipy/linalg/tests/test_lapack.py::test_generalized_eigh_lworks[sy-gvx]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape0-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape0-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape0-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape0-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape1-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape1-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape1-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape1-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape2-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape2-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape2-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrf_lwork[shape2-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size0-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size0-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size0-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size0-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size1-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size1-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size1-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size1-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size2-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size2-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size2-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp[matrix_size2-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_errors_with_empty_array`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape0-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape0-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape0-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape0-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape1-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape1-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape1-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape1-float64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape2-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape2-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape2-float32]`
- `scipy/linalg/tests/test_lapack.py::test_geqrfp_lwork[shape2-float64]`
- `scipy/linalg/tests/test_lapack.py::test_getc2_gesc2`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgexc[complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgexc[complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgexc[float32]`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgexc[float64]`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgsen[complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgsen[complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgsen[float32]`
- `scipy/linalg/tests/test_lapack.py::test_gges_tgsen[float64]`
- `scipy/linalg/tests/test_lapack.py::test_gglse`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-False-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-False-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-False-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-False-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-True-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-True-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-True-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[F-True-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-False-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-False-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-False-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-False-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-True-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-True-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-True-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx[N-True-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_NAG[du0-d0-dl0-b0-x0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_NAG[du1-d1-dl1-b1-x1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-complex128_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-complex128_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-complex64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-complex64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-float32_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-float32_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-float64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-False-float64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-complex128_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-complex128_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-complex64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-complex64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-float32_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-float32_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-float64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[F-True-float64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-complex128_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-complex128_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-complex64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-complex64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-float32_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-float32_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-float64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-False-float64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-complex128_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-complex128_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-complex64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-complex64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-float32_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-float32_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-float64_0]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_incompatible_size[N-True-float64_1]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-0-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-0-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-0-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-0-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-1-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-1-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-1-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[F-1-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-0-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-0-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-0-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-0-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-1-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-1-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-1-float32]`
- `scipy/linalg/tests/test_lapack.py::test_gtsvx_error_singular[N-1-float64]`
- `scipy/linalg/tests/test_lapack.py::test_gttrf_gttrs[complex128]`
- `scipy/linalg/tests/test_lapack.py::test_gttrf_gttrs[complex64]`
- `scipy/linalg/tests/test_lapack.py::test_gttrf_gttrs[float32]`
- `scipy/linalg/tests/test_lapack.py::test_gttrf_gttrs[float64]`
- `scipy/linalg/tests/test_lapack.py::test_gttrf_gttrs_NAG_f07cdf_f07cef_f07crf_f07csf[du0-d0-dl0-du_exp0-d_exp0-du2_exp0-ipiv_exp0-b0-x0]`
- `scipy/linalg/tests/test_lapack.py::test_gttrf_gttrs_NAG_f07cdf_f07cef_f07crf_f07csf[du1-d1-dl1-du_exp1-d_exp1-du2_exp1-ipiv_exp1-b1-x1]`
- `scipy/linalg/tests/test_lapack.py::test_hegst`
- `scipy/linalg/tests/test_lapack.py::test_lapack_documented`
- `scipy/linalg/tests/test_lapack.py::test_larfg_larf`
- `scipy/linalg/tests/test_lapack.py::test_lartg`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd[complex128]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd[complex64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd[float32]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd[float64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1-float32]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1-float64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[10-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[10-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[10-float32]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[10-float64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[100-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[100-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[100-float32]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[100-float64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1000-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1000-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1000-float32]`
- `scipy/linalg/tests/test_lapack.py::test_orcsd_uncsd_lwork[1000-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ormrz_unmrz`
- `scipy/linalg/tests/test_lapack.py::test_pftrf`
- `scipy/linalg/tests/test_lapack.py::test_pftri`
- `scipy/linalg/tests/test_lapack.py::test_pftrs`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[complex128-False]`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[complex128-True]`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[complex64-False]`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[complex64-True]`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[float32-False]`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[float32-True]`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[float64-False]`
- `scipy/linalg/tests/test_lapack.py::test_pptrs_pptri_pptrf_ppsv_ppcon[float64-True]`
- `scipy/linalg/tests/test_lapack.py::test_pstf2`
- `scipy/linalg/tests/test_lapack.py::test_pstrf`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[0-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[0-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[0-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[0-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[1-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[1-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[1-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[1-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[2-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[2-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[2-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr[2-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_NAG_f08jgf[2-d0-e0-d_expect0-z_expect0]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[0-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[0-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[0-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[0-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[1-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[1-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[1-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[1-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[2-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[2-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[2-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_non_spd[2-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[0-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[0-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[0-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[0-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[1-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[1-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[1-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[1-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[2-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[2-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[2-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_error_singular[2-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[0-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[0-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[0-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[0-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[1-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[1-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[1-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[1-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[2-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[2-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[2-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pteqr_raise_error_wrong_shape[2-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[F-<lambda>-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[F-<lambda>-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[F-<lambda>-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[F-<lambda>-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[N-<lambda>-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[N-<lambda>-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[N-<lambda>-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx[N-<lambda>-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_NAG[d0-e0-b0-x0]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_NAG[d1-e1-b1-x1]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[F-<lambda>-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[F-<lambda>-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[F-<lambda>-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[F-<lambda>-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[N-<lambda>-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[N-<lambda>-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[N-<lambda>-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_error_raise_errors[N-<lambda>-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[F-<lambda>-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[F-<lambda>-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[F-<lambda>-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[F-<lambda>-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[N-<lambda>-complex128-float64]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[N-<lambda>-complex64-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[N-<lambda>-float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_ptsvx_non_SPD_singular[N-<lambda>-float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs[float32-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs[float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs[float64-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs[float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_NAG[d0-e0-d_expect0-e_expect0-b0-x_expect0]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_NAG[d1-e1-d_expect1-e_expect1-b1-x_expect1]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_incompatible_shape[float32-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_incompatible_shape[float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_incompatible_shape[float64-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_incompatible_shape[float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_singular_nonSPD[float32-complex64]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_singular_nonSPD[float32-float32]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_singular_nonSPD[float64-complex128]`
- `scipy/linalg/tests/test_lapack.py::test_pttrf_pttrs_errors_singular_nonSPD[float64-float64]`
- `scipy/linalg/tests/test_lapack.py::test_rot`
- `scipy/linalg/tests/test_lapack.py::test_sfrk_hfrk`
- `scipy/linalg/tests/test_lapack.py::test_sgesdd_lwork_bug_workaround`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[he-ev]`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[he-evd]`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[he-evr]`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[he-evx]`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[sy-ev]`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[sy-evd]`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[sy-evr]`
- `scipy/linalg/tests/test_lapack.py::test_standard_eigh_lworks[sy-evx]`
- `scipy/linalg/tests/test_lapack.py::test_sycon_hecon`
- `scipy/linalg/tests/test_lapack.py::test_syconv`
- `scipy/linalg/tests/test_lapack.py::test_syequb`
- `scipy/linalg/tests/test_lapack.py::test_sygst`
- `scipy/linalg/tests/test_lapack.py::test_tfsm`
- `scipy/linalg/tests/test_lapack.py::test_tfttr_trttf`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[0-N-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[0-N-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[0-T-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[0-T-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[1-N-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[1-N-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[1-T-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[1-T-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[2-N-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[2-N-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[2-T-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[2-T-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[3-N-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[3-N-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[3-T-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[3-T-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[4-N-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[4-N-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[4-T-float32]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl[4-T-float64]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl_NAG[float32-a0-b0-c0-d0-e0-f0-rans0-lans0]`
- `scipy/linalg/tests/test_lapack.py::test_tgsyl_NAG[float64-a0-b0-c0-d0-e0-f0-rans0-lans0]`
- `scipy/linalg/tests/test_lapack.py::test_tpttr_trttp`
- `scipy/linalg/tests/test_lapack.py::test_trexc_NAG[t0-expect0-2-1]`
- `scipy/linalg/tests/test_lapack.py::test_trexc_NAG[t1-expect1-1-4]`
- `scipy/linalg/tests/test_lapack.py::test_trsen_NAG[t0-q0-expect0-select0-1.75-3.22]`
- `scipy/linalg/tests/test_lapack.py::test_trsen_NAG[t1-q1-expect1-select1-1.02-0.182]`
- `scipy/linalg/tests/test_lapack.py::test_tzrzf`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #20382: MAINT: lint: enforce `numpy as np` alias

#### Reference issue


#### What does this implement/fix?


Enforce `numpy` alias, as discussed in https://github.com/scipy/scipy/pull/20367#issuecomment-2033998396

#### Additional information

The lint rule works, the proof is the additional violations it picks up. I wonder what's the rational behind importing `numpy` as `_np`? The latest change is 8 years ago, so I think it might be an old convention. 

Happy to fix them too if it's fine to fix.

@lucascolley Can you review this PR, please? Thank you very much.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/constants/_constants.py b/scipy/constants/_constants.py
index fa379828ddd62bedc92f2e0e81b51ce550ca90fd..666690d47a836c27d9386172ede7ecc26068884c 100644
--- a/scipy/constants/_constants.py
+++ b/scipy/constants/_constants.py
@@ -13,7 +13,7 @@ import math as _math
 from typing import TYPE_CHECKING, Any
 
 from ._codata import value as _cd
-import numpy as _np
+import numpy as np
 
 if TYPE_CHECKING:
     import numpy.typing as npt
@@ -271,13 +271,13 @@ def convert_temperature(
     """
     # Convert from `old_scale` to Kelvin
     if old_scale.lower() in ['celsius', 'c']:
-        tempo = _np.asanyarray(val) + zero_Celsius
+        tempo = np.asanyarray(val) + zero_Celsius
     elif old_scale.lower() in ['kelvin', 'k']:
-        tempo = _np.asanyarray(val)
+        tempo = np.asanyarray(val)
     elif old_scale.lower() in ['fahrenheit', 'f']:
-        tempo = (_np.asanyarray(val) - 32) * 5 / 9 + zero_Celsius
+        tempo = (np.asanyarray(val) - 32) * 5 / 9 + zero_Celsius
     elif old_scale.lower() in ['rankine', 'r']:
-        tempo = _np.asanyarray(val) * 5 / 9
+        tempo = np.asanyarray(val) * 5 / 9
     else:
         raise NotImplementedError("%s scale is unsupported: supported scales "
                                   "are Celsius, Kelvin, Fahrenheit, and "
@@ -329,7 +329,7 @@ def lambda2nu(lambda_: npt.ArrayLike) -> Any:
     array([  2.99792458e+08,   1.00000000e+00])
 
     """
-    return c / _np.asanyarray(lambda_)
+    return c / np.asanyarray(lambda_)
 
 
 def nu2lambda(nu: npt.ArrayLike) -> Any:
@@ -359,4 +359,4 @@ def nu2lambda(nu: npt.ArrayLike) -> Any:
     array([  2.99792458e+08,   1.00000000e+00])
 
     """
-    return c / _np.asanyarray(nu)
+    return c / np.asanyarray(nu)
diff --git a/scipy/linalg/blas.py b/scipy/linalg/blas.py
index c42190ed453a6d4d460ca077eb2d1bf72b7aab00..c943460e6bafcd9a382586d5a5155357382ea596 100644
--- a/scipy/linalg/blas.py
+++ b/scipy/linalg/blas.py
@@ -207,7 +207,7 @@ BLAS Level 3 functions
 
 __all__ = ['get_blas_funcs', 'find_best_blas_type']
 
-import numpy as _np
+import numpy as np
 import functools
 
 from scipy.linalg import _fblas
@@ -243,10 +243,10 @@ _type_score.update({x: 2 for x in 'iIlLqQd'})
 _type_score.update({'F': 3, 'D': 4, 'g': 2, 'G': 4})
 
 # Final mapping to the actual prefixes and dtypes
-_type_conv = {1: ('s', _np.dtype('float32')),
-              2: ('d', _np.dtype('float64')),
-              3: ('c', _np.dtype('complex64')),
-              4: ('z', _np.dtype('complex128'))}
+_type_conv = {1: ('s', np.dtype('float32')),
+              2: ('d', np.dtype('float64')),
+              3: ('c', np.dtype('complex64')),
+              4: ('z', np.dtype('complex128'))}
 
 # some convenience alias for complex functions
 _blas_alias = {'cnrm2': 'scnrm2', 'znrm2': 'dznrm2',
@@ -294,7 +294,7 @@ def find_best_blas_type(arrays=(), dtype=None):
     ('d', dtype('float64'), True)
 
     """
-    dtype = _np.dtype(dtype)
+    dtype = np.dtype(dtype)
     max_score = _type_score.get(dtype.char, 5)
     prefer_fortran = False
 
@@ -318,7 +318,7 @@ def find_best_blas_type(arrays=(), dtype=None):
 
     # Get the LAPACK prefix and the corresponding dtype if not fall back
     # to 'd' and double precision float.
-    prefix, dtype = _type_conv.get(max_score, ('d', _np.dtype('float64')))
+    prefix, dtype = _type_conv.get(max_score, ('d', np.dtype('float64')))
 
     return prefix, dtype, prefer_fortran
 
@@ -335,7 +335,7 @@ def _get_funcs(names, arrays, dtype,
 
     funcs = []
     unpack = False
-    dtype = _np.dtype(dtype)
+    dtype = np.dtype(dtype)
     module1 = (cmodule, cmodule_name)
     module2 = (fmodule, fmodule_name)
 
@@ -362,9 +362,9 @@ def _get_funcs(names, arrays, dtype,
         func.module_name, func.typecode = module_name, prefix
         func.dtype = dtype
         if not ilp64:
-            func.int_dtype = _np.dtype(_np.intc)
+            func.int_dtype = np.dtype(np.intc)
         else:
-            func.int_dtype = _np.dtype(_np.int64)
+            func.int_dtype = np.dtype(np.int64)
         func.prefix = prefix  # Backward compatibility
         funcs.append(func)
 
diff --git a/scipy/linalg/lapack.py b/scipy/linalg/lapack.py
index 57b0f65138b36dc9542f429dc73f88b6aac03004..487ff5ad6efb61e1d2dcc0a2f51b13cc96889c49 100644
--- a/scipy/linalg/lapack.py
+++ b/scipy/linalg/lapack.py
@@ -822,7 +822,7 @@ All functions
 # Author: Pearu Peterson, March 2002
 #
 
-import numpy as _np
+import numpy as np
 from .blas import _get_funcs, _memoize_get_funcs
 from scipy.linalg import _flapack
 from re import compile as regex_compile
@@ -975,8 +975,8 @@ def get_lapack_funcs(names, arrays=(), dtype=None, ilp64=False):
                           ilp64=True)
 
 
-_int32_max = _np.iinfo(_np.int32).max
-_int64_max = _np.iinfo(_np.int64).max
+_int32_max = np.iinfo(np.int32).max
+_int64_max = np.iinfo(np.int64).max
 
 
 def _compute_lwork(routine, *args, **kwargs):
@@ -1020,10 +1020,10 @@ def _check_work_float(value, dtype, int_dtype):
     carefully for single-precision types.
     """
 
-    if dtype == _np.float32 or dtype == _np.complex64:
+    if dtype == np.float32 or dtype == np.complex64:
         # Single-precision routine -- take next fp value to work
         # around possible truncation in LAPACK code
-        value = _np.nextafter(value, _np.inf, dtype=_np.float32)
+        value = np.nextafter(value, np.inf, dtype=np.float32)
 
     value = int(value)
     if int_dtype.itemsize == 4:
diff --git a/tools/lint.toml b/tools/lint.toml
index 2f04d356026f5e00b5a5d5a418a5da072aeae1e3..69f7e9e2e812aad3fc6f7e40136ac8bd7ebf008f 100644
--- a/tools/lint.toml
+++ b/tools/lint.toml
@@ -10,7 +10,8 @@ target-version = "py39"
 # Also, `PGH004` which checks for blanket (non-specific) `noqa`s
 # and `B028` which checks that warnings include the `stacklevel` keyword.
 # `B028` added in gh-19623.
-select = ["E", "F", "PGH004", "UP", "B028"]
+# `ICN001` added in gh-20382 to enforce common conventions for imports
+select = ["E", "F", "PGH004", "UP", "B028", "ICN001"]
 ignore = ["E741"]
 
 # Allow unused variables when underscore-prefixed.
@@ -26,6 +27,9 @@ dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"
 "scipy/linalg/_generate_pyx.py" = ["E501"]
 "scipy/spatial/transform/_rotation.pyi" = ["E501"]
 
+[lint.flake8-import-conventions.aliases]
+numpy = "np"
+
 [lint.mccabe]
 # Unlike Flake8, default to a complexity level of 10.
 max-complexity = 10
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/linalg/tests/test_lapack.py b/scipy/linalg/tests/test_lapack.py
index ba419b2ede86589607872c0471b303aa7d76defe..0102e2893eab69d8313a503e55a0f3329b048570 100644
--- a/scipy/linalg/tests/test_lapack.py
+++ b/scipy/linalg/tests/test_lapack.py
@@ -59,8 +59,14 @@ def test_lapack_documented():
         pytest.skip('lapack.__doc__ is None')
     names = set(lapack.__doc__.split())
     ignore_list = {
-        'absolute_import', 'clapack', 'division', 'find_best_lapack_type',
-        'flapack', 'print_function', 'HAS_ILP64',
+        "absolute_import",
+        "clapack",
+        "division",
+        "find_best_lapack_type",
+        "flapack",
+        "print_function",
+        "HAS_ILP64",
+        "np",
     }
     missing = list()
     for name in dir(lapack):
```

## Validation

```json
{
 "image_head": "bd15d2426647732b0888afd1cf9edf0838b3e1c0",
 "patch_applies": true,
 "test_files": [
  "scipy/linalg/tests/test_lapack.py"
 ],
 "collected_before": 1927,
 "collected_after": 1927,
 "outcomes_before": {
  "PASSED": 1926,
  "SKIPPED": 1
 },
 "outcomes_after": {
  "PASSED": 1926,
  "SKIPPED": 1
 },
 "exit_before": 0,
 "exit_after": 0,
 "tail_before": "\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-T-float64]\nSKIPPED [1] scipy/linalg/tests/test_lapack.py:1754: Failing on some OpenBLAS version, see gh-12276\n======================= 1926 passed, 1 skipped in 9.83s ========================",
 "tail_after": "\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[0-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[1-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[2-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[3-T-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-N-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-N-float64]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-T-float32]\nPASSED scipy/linalg/tests/test_lapack.py::test_tgsyl[4-T-float64]\nSKIPPED [1] scipy/linalg/tests/test_lapack.py:1754: Failing on some OpenBLAS version, see gh-12276\n======================= 1926 passed, 1 skipped in 8.70s ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

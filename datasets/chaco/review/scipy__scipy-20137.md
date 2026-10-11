# scipy__scipy-20137

[back to the list](README.md) -- **ENH: stats.pearsonr: add support for `axis` argument**

| field | value |
|---|---|
| pull request | [scipy/scipy#20137](https://github.com/scipy/scipy/pull/20137) (created 2024-02-22, merged 2024-03-21) |
| ChaCo lists | full, ablation, f2p30 |
| status | **runnable** -- 5 developer test(s) flip; oracle reproduces it |
| base commit | [`cd60e810c174`](https://github.com/scipy/scipy/commit/cd60e810c17442f71ab7f7788eccd1013fc265f1) (2024-03-20), first parent of the merge commit |
| merge commit | [`ceea3e316ab7`](https://github.com/scipy/scipy/commit/ceea3e316ab78e3477004da0c26236105fe3b4d5) |
| issues closed | none |
| version | 1.14 |
| image | `f2p-chaco/scipy__scipy-20137:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-20137.Dockerfile) |
| source files (`patch`) | `scipy/stats/_morestats.py`, `scipy/stats/_stats_py.py` |
| test files (`test_patch`) | `scipy/stats/tests/test_stats.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (5)

- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_axis01[0]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_axis01[1]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_axis_None`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_nd_input_validation`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_nd_special_cases`

## PASS_TO_PASS (954)

<details><summary>show</summary>

- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_bad_inputs`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_dtypes`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_r`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_scholar`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_scholar3`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_constant_input`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_nan_policy_omit`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_nan_policy_propogate`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_nan_policy_raise`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_alternative_error`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_default`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_distribution_error`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_distribution_norm`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_empty_imput`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_nan_input_omit`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_nan_input_propagate`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_nan_input_raise`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_normal_dist`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_one_sided`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_return_nan`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_two_sided`
- `scipy/stats/tests/test_stats.py::TestCdfDistanceValidation::test_distinct_value_and_weight_lengths`
- `scipy/stats/tests/test_stats.py::TestCdfDistanceValidation::test_empty_distribution`
- `scipy/stats/tests/test_stats.py::TestCdfDistanceValidation::test_inf_weight`
- `scipy/stats/tests/test_stats.py::TestCdfDistanceValidation::test_negative_weights`
- `scipy/stats/tests/test_stats.py::TestCdfDistanceValidation::test_zero_weight`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_fisher`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[fisher-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[fisher-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[fisher-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[mudholkar_george-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[mudholkar_george-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[mudholkar_george-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[pearson-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[pearson-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[pearson-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[stouffer-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[stouffer-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[stouffer-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[tippett-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[tippett-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[tippett-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_mudholkar_george`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_mudholkar_george_equal_fisher_pearson_average`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_pearson`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[fisher]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[mudholkar_george]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[pearson]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[stouffer]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[tippett]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_stouffer`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_stouffer2`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_tippett`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_weighted_stouffer`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_weighted_stouffer2`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_basic`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_basic_example[greater-0.1629000687684--0.6785654158217636-1-1]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_basic_example[greater-0.8370999312316--0.985600937290653-1.0--1]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_basic_example[less-0.1629000687684--1.0-0.6785654158217636--1]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_basic_example[less-0.8370999312316--1-0.985600937290653-1]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_basic_example[two-sided-0.325800137536--0.814938968841-0.99230697523-1]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_basic_example[two-sided-0.325800137536--0.992306975236-0.81493896884--1]`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_complex_data`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_constant_input`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_extremely_large_input_values`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_invalid_method`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_len1`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_length3_r_exactly_negative_one`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_length_two_neg2`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_length_two_pos1`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_near_constant_input`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_negative_correlation_pvalue_gh17795`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pBIGBIG`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pBIGHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pBIGLITTLE`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pBIGROUND`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pBIGTINY`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pHUGEHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pHUGEROUND`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pHUGETINY`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pLITTLEHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pLITTLELITTLE`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pLITTLEROUND`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pLITTLETINY`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pROUNDROUND`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pTINYROUND`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pTINYTINY`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pXBIG`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pXHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pXLITTLE`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pXROUND`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pXTINY`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pXX`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_pearsonr_result_attributes`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_r_almost_exactly_neg1`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_r_almost_exactly_pos1`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_unequal_lengths`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_very_large_input_values`
- `scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_very_small_input_values`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_alternative`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_alternative_nan_policy[greater]`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_alternative_nan_policy[less]`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_alternative_nan_policy[two-sided]`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_corr_1`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_empty_arrays`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_gh_11111`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_gh_issue_6061_windows_overflow`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_index_error`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_nan_policies`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_normal_draws`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_omit_paired_value`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_spearmanr_vs_r`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_tie0`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_tie1`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_tie2`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_ties_axis_1`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr2::test_unequal_lengths`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_1d_vs_2d`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_1d_vs_2d_nans`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_3cols`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_gh_8111`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_gh_9103`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_nan_policy`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_nan_policy_bug_12411`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_nan_policy_bug_12458`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_ndim_too_high`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sBIGBIG`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sBIGHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sBIGLITTLE`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sBIGROUND`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sBIGTINY`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sHUGEHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sHUGEROUND`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sHUGETINY`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sLITTLEHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sLITTLELITTLE`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sLITTLEROUND`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sLITTLETINY`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sROUNDROUND`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sTINYROUND`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sTINYTINY`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sXBIG`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sXHUGE`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sXLITTLE`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sXROUND`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sXTINY`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_sXX`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_scalar`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_spearmanr_result_attributes`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_uneven_2d_shapes`
- `scipy/stats/tests/test_stats.py::TestCorrSpearmanr::test_uneven_lengths`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_axis_none`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_ddof`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_empty`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_numbers`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_result_attributes`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_scalar`
- `scipy/stats/tests/test_stats.py::TestEnergyDistance::test_combine_weights`
- `scipy/stats/tests/test_stats.py::TestEnergyDistance::test_inf_values`
- `scipy/stats/tests/test_stats.py::TestEnergyDistance::test_same_distribution`
- `scipy/stats/tests/test_stats.py::TestEnergyDistance::test_shift`
- `scipy/stats/tests/test_stats.py::TestEnergyDistance::test_simple`
- `scipy/stats/tests/test_stats.py::TestEnergyDistance::test_zero_weight`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[20-0.2]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[20-0.499999999999]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[20-0.500000000001]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[20-0.5]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[20-0.8]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.2]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.499999999999]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.500000000001]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.5]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.8]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_maximum`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_minimum`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_monotonicity_in_alpha[2000]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_monotonicity_in_alpha[20]`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_same_as_mean`
- `scipy/stats/tests/test_stats.py::TestExpectile::test_weights`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_2d_inputs[-1]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_2d_inputs[-2]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_2d_inputs[0]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_2d_inputs[1]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_3d_inputs`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_all_length_one`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_axis_error`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_bad_shapes`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_basic`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_constant_input[a0-b0-expected0]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_constant_input[a1-b1-expected1]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_known_exact`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_large_integer_array`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_length0_1d_error`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_length0_2d_error`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_nist`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_result_attributes`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_too_few_inputs[args0]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_too_few_inputs[args1]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_trivial`
- `scipy/stats/tests/test_stats.py::TestFindRepeats::test_basic`
- `scipy/stats/tests/test_stats.py::TestFindRepeats::test_empty_result`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_basic`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_gh3014`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_gh4130`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_gh9231`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_large_numbers`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_less_greater`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_precise`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_raises`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_result[greater]`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_result[less]`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_result[two-sided]`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_row_or_col_zero`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_0`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_1d_array`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_1d_array0`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_1d_list`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_1d_list0`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_1d_list_neg`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_2d_array`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_2d_axis0`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_2d_axis1`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_2d_list`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_large_values`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_weights_1d_array`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_weights_1d_list`
- `scipy/stats/tests/test_stats.py::TestGeoMean::test_weights_masked_1d_array`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_1d_array`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_1d_numeric_array_like_input`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_3d_array`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_3d_array_axis_0`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_3d_array_axis_1`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_3d_array_axis_2`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_3d_array_axis_type_tuple`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_ddof_equal_to_number_of_observations`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_masked_3d_array`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_propagates_nan_values`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_raises_value_error_inf_entry`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_raises_value_error_negative_entry`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_raises_value_error_non_array_like_input`
- `scipy/stats/tests/test_stats.py::TestGeometricStandardDeviation::test_raises_value_error_zero_entry`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_0`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_1d_array`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_1d_array_with_negative_value`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_1d_array_with_zero`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_1d_list`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_2d_array`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_2d_axis0`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_2d_axis0_with_zero`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_2d_axis1`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_2d_axis1_with_zero`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_2d_list`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_weights_1d_list`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_weights_2d_array_axis0`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_weights_2d_array_axis1`
- `scipy/stats/tests/test_stats.py::TestHarMean::test_weights_masked_1d_array`
- `scipy/stats/tests/test_stats.py::TestIQR::test_2D`
- `scipy/stats/tests/test_stats.py::TestIQR::test_api`
- `scipy/stats/tests/test_stats.py::TestIQR::test_axis`
- `scipy/stats/tests/test_stats.py::TestIQR::test_basic`
- `scipy/stats/tests/test_stats.py::TestIQR::test_constant`
- `scipy/stats/tests/test_stats.py::TestIQR::test_empty`
- `scipy/stats/tests/test_stats.py::TestIQR::test_interpolation`
- `scipy/stats/tests/test_stats.py::TestIQR::test_keepdims`
- `scipy/stats/tests/test_stats.py::TestIQR::test_nanpolicy`
- `scipy/stats/tests/test_stats.py::TestIQR::test_rng`
- `scipy/stats/tests/test_stats.py::TestIQR::test_scalarlike`
- `scipy/stats/tests/test_stats.py::TestIQR::test_scale`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_axis`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_jarque_bera_array_like`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_jarque_bera_size`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_jarque_bera_stats`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_agree_with_r`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_known_examples`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_ks1samp_allpaths`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[greater-6-6-1-ks_1samp]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[greater-6-6-1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[less-7-7--1-ks_1samp]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[less-7-7--1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[two-sided-6-6-1-ks_1samp]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[two-sided-6-6-1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[two-sided-7-7--1-ks_1samp]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_location_sign[two-sided-7-7--1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSOneSample::test_namedtuple_attributes`
- `scipy/stats/tests/test_stats.py::TestKSTest::test_agree_with_ks_1samp`
- `scipy/stats/tests/test_stats.py::TestKSTest::test_namedtuple_attributes`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test100_100`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test100_110`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testEqualSizes`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testLarge`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testLargeBoth`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testMediumBoth`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testMiddlingBoth`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testNamedAttributes`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testRepeatedValues`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testSmall`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testTwoVsFour`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::testTwoVsThree`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_argument_checking`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_gh11184`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_gh12218`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[greater-5.9-5.9-1-ks_2samp]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[greater-5.9-5.9-1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[less-6.1-6.0--1-ks_2samp]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[less-6.1-6.0--1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[two-sided-5.9-5.9-1-ks_2samp]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[two-sided-5.9-5.9-1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[two-sided-6.1-6.0--1-ks_2samp]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_location_sign[two-sided-6.1-6.0--1-kstest]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_some_code_paths`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_warnings_gh_14019`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c0[greater-0.1666666666667-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c0[greater-1-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c0[less-0.1666666666667-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c0[less-1-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c0[two-sided-0.3333333333333-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c0[two-sided-0.3333333333333-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c1[greater-0.1666666666667-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c1[greater-0.9583333333333-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c1[less-0.1666666666667-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c1[less-0.9583333333333-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c1[two-sided-0.3333333333333-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_c1[two-sided-0.3333333333333-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171[greater-0.0597194664903-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171[greater-0.9624118165785-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171[less-0.0597194664903-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171[less-0.9624118165785-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171[two-sided-0.1194389329806-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171[two-sided-0.1194389329806-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171b[greater-0.246236925303-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171b[greater-0.755634083327-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171b[less-0.246236925303-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171b[less-0.755634083327-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171b[two-sided-0.4924738506059-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171b[two-sided-0.4924738506059-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171c[greater-0.01535692653267-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171c[greater-0.9847475308925-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171c[less-0.01535692653267-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171c[less-0.9847475308925-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171c[two-sided-0.03071385306533-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_lt_171c[two-sided-0.03071385306533-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n1[greater-nan-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n1[greater-nan-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n1[less-nan-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n1[less-nan-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n1[two-sided-nan-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n1[two-sided-nan-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n2[greater-0.5-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n2[greater-1-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n2[less-0.5-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n2[less-1-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n2[two-sided-1-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_n2[two-sided-1-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlation[greater-0.5916666666667-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlation[greater-0.5916666666667-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlation[less-0.5916666666667-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlation[less-0.5916666666667-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlation[two-sided-1-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlation[two-sided-1-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlationb[greater-0.5475694444444-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlationb[greater-0.5475694444444-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlationb[less-0.5475694444444-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlationb[less-0.5475694444444-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlationb[two-sided-1-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_against_R_no_correlationb[two-sided-1-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_gt_171[greater-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_gt_171[greater-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_gt_171[less-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_gt_171[less-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_gt_171[two-sided-False]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_gt_171[two-sided-True]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_kendalltau_alternative_asymptotic`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_nan_policy[greater-asymptotic]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_nan_policy[greater-exact]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_nan_policy[less-asymptotic]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_nan_policy[less-exact]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_nan_policy[two-sided-asymptotic]`
- `scipy/stats/tests/test_stats.py::TestKendallTauAlternative::test_nan_policy[two-sided-exact]`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_another_tie`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_basic`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_empty`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_kruskal_result_attributes`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_large_no_samples`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_nan_policy`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_simple`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_simple_tie`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_three_groups`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_infty`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_lowsamples`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_nans`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_notndarray`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_reps[-1]`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_reps[1]`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_shape`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_error_wrongdisttype`
- `scipy/stats/tests/test_stats.py::TestMGCErrorWarnings::test_warns_reps`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_alias`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_dist_perm`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_fived[linear-0.184-0.001]`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_fived[nonlinear-0.019-0.117]`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_oned[independence--0.0094-0.78]`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_oned[linear-0.97-0.001]`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_oned[nonlinear-0.163-0.001]`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_pvalue_literature`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_random_state`
- `scipy/stats/tests/test_stats.py::TestMGCStat::test_workers`
- `scipy/stats/tests/test_stats.py::TestMannWhitneyU::test_mannwhitneyu_no_correct_one_sided`
- `scipy/stats/tests/test_stats.py::TestMannWhitneyU::test_mannwhitneyu_no_correct_two_sided`
- `scipy/stats/tests/test_stats.py::TestMannWhitneyU::test_mannwhitneyu_one_sided`
- `scipy/stats/tests/test_stats.py::TestMannWhitneyU::test_mannwhitneyu_ones`
- `scipy/stats/tests/test_stats.py::TestMannWhitneyU::test_mannwhitneyu_result_attributes`
- `scipy/stats/tests/test_stats.py::TestMannWhitneyU::test_mannwhitneyu_two_sided`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_axis_and_nan`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_center_mean_with_nan[1-expected0]`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_center_mean_with_nan[None-4.5]`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_center_not_callable`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_mad_nan_omit`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_median_abs_deviation`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_nan_policy_omit_with_inf`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_nan_policy_with_axis[omit-expected0]`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_nan_policy_with_axis[propagate-expected1]`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_size_zero_with_axis[0]`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_size_zero_with_axis[1]`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_size_zero_with_axis[2]`
- `scipy/stats/tests/test_stats.py::TestMedianAbsDeviation::test_size_zero_with_axis[None]`
- `scipy/stats/tests/test_stats.py::TestMode::test_axes`
- `scipy/stats/tests/test_stats.py::TestMode::test_basic`
- `scipy/stats/tests/test_stats.py::TestMode::test_empty`
- `scipy/stats/tests/test_stats.py::TestMode::test_gh16955[omit]`
- `scipy/stats/tests/test_stats.py::TestMode::test_gh16955[propagate]`
- `scipy/stats/tests/test_stats.py::TestMode::test_gh17214[z0]`
- `scipy/stats/tests/test_stats.py::TestMode::test_gh17214[z1]`
- `scipy/stats/tests/test_stats.py::TestMode::test_gh9955`
- `scipy/stats/tests/test_stats.py::TestMode::test_keepdims`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_nan`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_result_attributes`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_shape_gh_9955[axis0]`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_shape_gh_9955[axis1]`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_shape_gh_9955[axis2]`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_shape_gh_9955[axis3]`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_shape_gh_9955[axis4]`
- `scipy/stats/tests/test_stats.py::TestMode::test_mode_shape_gh_9955[axis5]`
- `scipy/stats/tests/test_stats.py::TestMode::test_nan_policy_propagate_gh_9815`
- `scipy/stats/tests/test_stats.py::TestMode::test_negative_axes_gh_15375[axis0]`
- `scipy/stats/tests/test_stats.py::TestMode::test_negative_axes_gh_15375[axis1]`
- `scipy/stats/tests/test_stats.py::TestMode::test_negative_axes_gh_15375[axis2]`
- `scipy/stats/tests/test_stats.py::TestMode::test_negative_axes_gh_15375[axis3]`
- `scipy/stats/tests/test_stats.py::TestMode::test_raise_non_numeric_gh18254`
- `scipy/stats/tests/test_stats.py::TestMode::test_scalar`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[False-data0]`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[False-data1]`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[False-data2]`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[False-data3]`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[True-data0]`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[True-data1]`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[True-data2]`
- `scipy/stats/tests/test_stats.py::TestMode::test_smallest_equal[True-data3]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[0-1-complex128]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[0-1-float32]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[0-1-float64]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[1-0-complex128]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[1-0-float32]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[1-0-float64]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_empty_1d`
- `scipy/stats/tests/test_stats.py::TestMoments::test_kurtosis`
- `scipy/stats/tests/test_stats.py::TestMoments::test_kurtosis_array_scalar`
- `scipy/stats/tests/test_stats.py::TestMoments::test_kurtosis_constant_value`
- `scipy/stats/tests/test_stats.py::TestMoments::test_kurtosis_propagate_nan`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_accuracy`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_empty_order`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_propagate_nan`
- `scipy/stats/tests/test_stats.py::TestMoments::test_precision_loss_gh15554`
- `scipy/stats/tests/test_stats.py::TestMoments::test_rename_moment_order`
- `scipy/stats/tests/test_stats.py::TestMoments::test_skew_constant_value`
- `scipy/stats/tests/test_stats.py::TestMoments::test_skew_propagate_nan`
- `scipy/stats/tests/test_stats.py::TestMoments::test_skewness`
- `scipy/stats/tests/test_stats.py::TestMoments::test_skewness_scalar`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_Ames_assay`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[117-0.9997817843373017-True-exact-data10]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[12332-0.7722477197436702-False-asymptotic-data2]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[12805-0.3886487053947608-False-asymptotic-data0]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[197-0.9619432897162209-True-exact-data6]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[217-0.9693058575034678-True-exact-data8]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[241-0.9622210164861476-True-exact-data5]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[266-4.121656378600823e-05-False-exact-data3]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[332-0.9566400920502488-True-exact-data4]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[395-0.991530289351305-True-exact-data9]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[423-0.9590458306880073-True-exact-data7]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy2[49140-0.02888978556179862-False-asymptotic-data1]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[117-0.9997817843373017-True-exact-data10]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[12332-0.7722477197436702-False-asymptotic-data2]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[12805-0.3886487053947608-False-asymptotic-data0]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[197-0.9619432897162209-True-exact-data6]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[217-0.9693058575034678-True-exact-data8]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[241-0.9622210164861476-True-exact-data5]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[266-4.121656378600823e-05-False-exact-data3]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[332-0.9566400920502488-True-exact-data4]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[395-0.991530289351305-True-exact-data9]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[423-0.9590458306880073-True-exact-data7]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_accuracy[49140-0.02888978556179862-False-asymptotic-data1]`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_input_validation`
- `scipy/stats/tests/test_stats.py::TestPageTrendTest::test_options`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_boundaries[mean-result1]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_boundaries[rank-result0]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_boundaries[strict-result2]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_boundaries[weak-result3]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_inf[mean-result1]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_inf[rank-result0]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_inf[strict-result2]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_inf[weak-result3]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers[mean-35]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers[rank-40]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers[strict-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers[weak-40]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_missing[mean-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_missing[rank-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_missing[strict-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_missing[weak-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_multiple3[mean-45]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_multiple3[rank-50]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_multiple3[strict-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_large_numbers_multiple3[weak-60]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_missing[mean-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_missing[rank-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_missing[strict-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_missing[weak-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple2[mean-40]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple2[rank-45]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple2[strict-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple2[weak-50]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple3[mean-45]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple3[rank-50]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple3[strict-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_multiple3[weak-60]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_fail[raise-a0-score0-The`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_fail[raise-a0-score0-The input contains nan values]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_fail[raise-a1-score1-The`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_fail[raise-a1-score1-The input contains nan values]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_ok[omit-a4-score4-result4]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_ok[omit-a5-score5-result5]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_ok[omit-a6-score6-result6]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_ok[propagate-a0-1-nan]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_ok[propagate-a1-1-nan]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_ok[propagate-a2-score2-result2]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nans_ok[propagate-a3-score3-result3]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nd[shape0]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nd[shape1]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nd[shape2]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_nd[shape3]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_unique[mean-35]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_unique[rank-40]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_unique[strict-30]`
- `scipy/stats/tests/test_stats.py::TestPercentileOfScore::test_unique[weak-40]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_1d_array`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_1d_array_with_negative_value`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_1d_array_with_zero`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_1d_list`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_2d_axisnone[a0--0.5]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_2d_axisnone[a1-0.5]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_2d_list_axis0[a0--0.5]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_2d_list_axis0[a1-0.5]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_2d_list_axis1[a0--0.5]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_2d_list_axis1[a1-0.5]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_bad_exponent`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_weights_1d_list`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_weights_2d_array[0-gmean-0]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_weights_2d_array[1-hmean--1]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_weights_2d_array[None-wpmean_reference-9.87654321]`
- `scipy/stats/tests/test_stats.py::TestPowMean::test_weights_masked_1d_array`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_axis`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic_masked`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_ddof_broadcasting`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_power_divergence_gh_12282`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_power_divergence_result_attributes`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_R_ci_quantile[0.25-0.95--inf-1.39096812846378-less]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_R_ci_quantile[0.3-0.95-1.22140275816017-1.476980793882643-two-sided]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_R_ci_quantile[0.5-0.9-1.506817785112854-1.803988415397857-two-sided]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_R_ci_quantile[0.8-0.9-2.117000016612675-inf-greater]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_R_pvalue[1.2-0.3-two-sided-0.01515567517648]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_R_pvalue[1.8-0.5-two-sided-0.1109183496606]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_match_conover_examples`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.9-greater-continuous]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.9-greater-discrete]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.9-less-continuous]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.9-less-discrete]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.95-greater-continuous]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.95-greater-discrete]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.95-less-continuous]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_pval_ci_match[0.95-less-discrete]`
- `scipy/stats/tests/test_stats.py::TestQuantileTest::test_quantile_test_iv`
- `scipy/stats/tests/test_stats.py::TestRankSums::test_input_validation`
- `scipy/stats/tests/test_stats.py::TestRankSums::test_ranksums_named_results`
- `scipy/stats/tests/test_stats.py::TestRankSums::test_ranksums_result_attributes[greater]`
- `scipy/stats/tests/test_stats.py::TestRankSums::test_ranksums_result_attributes[less]`
- `scipy/stats/tests/test_stats.py::TestRankSums::test_ranksums_result_attributes[two-sided]`
- `scipy/stats/tests/test_stats.py::TestRatioUniforms::test_consistency`
- `scipy/stats/tests/test_stats.py::TestRegression::test_compare_to_polyfit`
- `scipy/stats/tests/test_stats.py::TestRegression::test_empty_input`
- `scipy/stats/tests/test_stats.py::TestRegression::test_identical_x`
- `scipy/stats/tests/test_stats.py::TestRegression::test_linregress`
- `scipy/stats/tests/test_stats.py::TestRegression::test_linregressBIGX`
- `scipy/stats/tests/test_stats.py::TestRegression::test_linregress_result_attributes`
- `scipy/stats/tests/test_stats.py::TestRegression::test_nan_input`
- `scipy/stats/tests/test_stats.py::TestRegression::test_nist_norris`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regressXX`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regressZEROX`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_against_R`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_alternative`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_shape_error`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_simple`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_simple_negative_cor`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_simple_onearg_cols`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_simple_onearg_rows`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_two_inputs`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_two_inputs_horizontal_line`
- `scipy/stats/tests/test_stats.py::TestSEM::test_sem`
- `scipy/stats/tests/test_stats.py::TestScoreatpercentile::test_axis`
- `scipy/stats/tests/test_stats.py::TestScoreatpercentile::test_basic`
- `scipy/stats/tests/test_stats.py::TestScoreatpercentile::test_empty`
- `scipy/stats/tests/test_stats.py::TestScoreatpercentile::test_exception`
- `scipy/stats/tests/test_stats.py::TestScoreatpercentile::test_fraction`
- `scipy/stats/tests/test_stats.py::TestScoreatpercentile::test_lower_higher`
- `scipy/stats/tests/test_stats.py::TestScoreatpercentile::test_sequence_per`
- `scipy/stats/tests/test_stats.py::TestSigmaClip::test_sigmaclip1`
- `scipy/stats/tests/test_stats.py::TestSigmaClip::test_sigmaclip2`
- `scipy/stats/tests/test_stats.py::TestSigmaClip::test_sigmaclip3`
- `scipy/stats/tests/test_stats.py::TestSigmaClip::test_sigmaclip_result_attributes`
- `scipy/stats/tests/test_stats.py::TestSigmaClip::test_std_zero`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_alternative`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[greater]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[less]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[two-sided]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_iv`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_onesample`
- `scipy/stats/tests/test_stats.py::TestTrim::test_trim1`
- `scipy/stats/tests/test_stats.py::TestTrim::test_trim_mean`
- `scipy/stats/tests/test_stats.py::TestTrim::test_trimboth`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tmax`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tmean`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tmin`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tsem`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tstd`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tvar`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistance::test_collapse`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistance::test_combine_weights`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistance::test_inf_values`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistance::test_same_distribution`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistance::test_shift`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistance::test_simple`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistance::test_zero_weight`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-12-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-12-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-12-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-17-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-17-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-17-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-8-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-8-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[23-8-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-12-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-12-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-12-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-17-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-17-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-17-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-8-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-8-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[3-8-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-12-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-12-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-12-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-17-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-17-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-17-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-8-38]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-8-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_collapse_nD[5-8-9]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_error_code`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_inf_values`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-10-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-10-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-10-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-15-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-15-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-15-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-20-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-20-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[1-20-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-10-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-10-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-10-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-15-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-15-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-15-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-20-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-20-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[3-20-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-10-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-10-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-10-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-15-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-15-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-15-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-20-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-20-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_multi_dim_nD[5-20-20]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[1-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[1-1]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[1-300]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[10-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[10-1]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[10-300]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[300-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[300-1]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[300-300]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-13-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-13-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-13-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-19-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-19-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-19-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-7-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-7-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[2-7-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-13-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-13-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-13-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-19-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-19-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-19-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-7-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-7-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[4-7-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-13-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-13-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-13-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-19-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-19-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-19-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-7-13]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-7-19]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_orthogonal_nD[7-7-7]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_published_values`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-3-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-3-35]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-3-4]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-4-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-4-35]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-4-4]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-7-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-7-35]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[10-7-4]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-3-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-3-35]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-3-4]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-4-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-4-35]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-4-4]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-7-15]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-7-35]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_same_distribution_nD[5-7-4]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-16-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-16-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-16-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-32-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-32-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-32-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-8-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-8-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[1-8-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-16-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-16-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-16-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-32-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-32-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-32-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-8-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-8-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[2-8-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-16-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-16-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-16-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-32-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-32-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-32-8]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-8-16]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-8-32]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_zero_weight_nD[6-8-8]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_gzscore_masked_array`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_gzscore_normal_array`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap[x0-y0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap[x1-y1]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_axis`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_ddof`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit[0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit[2]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit_with_axis[0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit_with_axis[2]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_raise`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_2d_all_nan`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_2d_all_nan_row`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_axis`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_1d`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_2d`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_2d_nan_policy_omit`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_ddof`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_empty_input[x0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_empty_input[x1]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_masked_element_0_gh19039`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_omit`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_omit_with_ddof`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_propagate`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_raise`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-False-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-False-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-False-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-True-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-True-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-True-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-False-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-False-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-False-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_ttest_many_dims[equal_var-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_ttest_many_dims[equal_var-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_ttest_many_dims[equal_var-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_ttest_many_dims[unequal_var-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_ttest_many_dims[unequal_var-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_ttest_many_dims[unequal_var-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_exact_alternative`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_exact_distribution`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_exact_selection`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutation_check_inputs`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutation_check_p_values`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutation_nanpolicy`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a0-b0-update0-p_d0]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a1-b1-update1-p_d1]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a2-b2-update2-0.000999000999000999]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a3-b3-update3-0.000999000999000999]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a4-b4-update4-p_d4]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a5-b5-update5-p_d5]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a6-b6-update6-0.000999000999000999]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a7-b7-update7-p_d7]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a8-b8-update8-0.3333333333333333]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_permutations[a9-b9-update9-p_d9]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_randperm_alternative`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_ttest_ind_randperm_alternative2`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_alternatives[greater-0.9985605452443--4.2461168970325]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_alternatives[less-0.001439454755672--4.2461168970325]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_compare_SAS`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_equal_var`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_errors_unsupported`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_trim_bounds_error[-0.2]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_trim_bounds_error[0.5]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_trim_bounds_error[1]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_ttest_compare_r[a0-b0-0.5361949075312673--0.6864951273557258-0.2]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_ttest_compare_r[a1-b1-0.00998909252078421-4.591598691181999-0.2]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_ttest_compare_r[a2-b2-0.10512380092302633-2.832256715395378-0.32]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_ttest_compare_r[a3-b3-0.002878909511344--4.2461168970325-0.2]`
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_ttest_compare_r[a4-b4-0.005293305834235--3.0983317739483-0.2]`
- `scipy/stats/tests/test_stats.py::test__broadcast_concatenate`
- `scipy/stats/tests/test_stats.py::test_binomtest`
- `scipy/stats/tests/test_stats.py::test_binomtest2`
- `scipy/stats/tests/test_stats.py::test_binomtest3`
- `scipy/stats/tests/test_stats.py::test_chiquare_data_types_attributes[1000000-int32]`
- `scipy/stats/tests/test_stats.py::test_chiquare_data_types_attributes[200-uint8]`
- `scipy/stats/tests/test_stats.py::test_chisquare_masked_arrays`
- `scipy/stats/tests/test_stats.py::test_cumfreq`
- `scipy/stats/tests/test_stats.py::test_friedmanchisquare`
- `scipy/stats/tests/test_stats.py::test_gh5686`
- `scipy/stats/tests/test_stats.py::test_gh_chisquare_12282`
- `scipy/stats/tests/test_stats.py::test_kendall_tau_large`
- `scipy/stats/tests/test_stats.py::test_kendalltau`
- `scipy/stats/tests/test_stats.py::test_kendalltau_deprecations`
- `scipy/stats/tests/test_stats.py::test_kendalltau_gh18139_overflow`
- `scipy/stats/tests/test_stats.py::test_kendalltau_nan_2nd_arg`
- `scipy/stats/tests/test_stats.py::test_kendalltau_vs_mstats_basic`
- `scipy/stats/tests/test_stats.py::test_kurtosistest_too_few_samples`
- `scipy/stats/tests/test_stats.py::test_normalitytests`
- `scipy/stats/tests/test_stats.py::test_obrientransform`
- `scipy/stats/tests/test_stats.py::test_pointbiserial`
- `scipy/stats/tests/test_stats.py::test_power_divergence_against_cressie_read_data`
- `scipy/stats/tests/test_stats.py::test_relfreq`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[ks_1samp-args1]`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[ks_2samp-args2]`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[kstest-args3]`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[wilcoxon-args0]`
- `scipy/stats/tests/test_stats.py::test_segfault_issue_9710`
- `scipy/stats/tests/test_stats.py::test_skewtest_too_few_samples`
- `scipy/stats/tests/test_stats.py::test_theilslopes`
- `scipy/stats/tests/test_stats.py::test_ttest_1samp_new`
- `scipy/stats/tests/test_stats.py::test_ttest_1samp_popmean_array`
- `scipy/stats/tests/test_stats.py::test_ttest_ci_iv[ttest_1samp-args0]`
- `scipy/stats/tests/test_stats.py::test_ttest_ci_iv[ttest_rel-args1]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_axis_size_zero[b0-expected_shape0]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_axis_size_zero[b1-expected_shape1]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_empty_1d_returns_nan`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_from_stats_inputs_zero`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_nan_2nd_arg`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_nonaxis_size_zero`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_nonaxis_size_zero_different_lengths`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_with_uneq_var`
- `scipy/stats/tests/test_stats.py::test_ttest_rel`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_axis_size_zero[b0-expected_shape0]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_axis_size_zero[b1-expected_shape1]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_ci_1d[greater]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_ci_1d[less]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_ci_1d[two-sided]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_empty_1d_returns_nan`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_nan_2nd_arg`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_nonaxis_size_zero`
- `scipy/stats/tests/test_stats.py::test_ttest_single_observation`
- `scipy/stats/tests/test_stats.py::test_weightedtau`
- `scipy/stats/tests/test_stats.py::test_weightedtau_vs_quadratic`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #20137: ENH: stats.pearsonr: add support for `axis` argument

#### Reference issue
Closes gh-9307

#### What does this implement/fix?
This adds native support for an `axis` argument to `pearsonr`, greatly improving the speed of vectorized calls (e.g. [pairwise comparisons](https://stackoverflow.com/questions/62817623/improve-speed-of-scipy-pearson-correlation-for-many-pairwise-calculations/78025304#78025304)).

#### Additional information
~~Failing existing tests pending resolution of gh-20136.~~ Worked around it.
~~Needs new tests of `axis`.~~ Added.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/stats/_morestats.py b/scipy/stats/_morestats.py
index 8da9345041842106da5f05164155f65c3142e9b9..13d6824f746183d90734541fe060775cd0412288 100644
--- a/scipy/stats/_morestats.py
+++ b/scipy/stats/_morestats.py
@@ -1250,6 +1250,12 @@ def boxcox_normmax(
     6.000...
     """
     x = np.asarray(x)
+
+    if np.any(~np.isfinite(x) | (x < 0)):
+        message = ("The `x` argument of `boxcox_normmax` must contain "
+                   "only positive, finite, real numbers.")
+        raise ValueError(message)
+
     end_msg = "exceed specified `ymax`."
     if isinstance(ymax, _BigFloat):
         dtype = x.dtype if np.issubdtype(x.dtype, np.floating) else np.float64
@@ -1321,15 +1327,7 @@ def boxcox_normmax(
 
     optimfunc = methods[method]
 
-    try:
-        res = optimfunc(x)
-    except ValueError as e:
-        if "infs or NaNs" in str(e):
-            message = ("The `x` argument of `boxcox_normmax` must contain "
-                       "only positive, finite, real numbers.")
-            raise ValueError(message) from e
-        else:
-            raise e
+    res = optimfunc(x)
 
     if res is None:
         message = ("The `optimizer` argument of `boxcox_normmax` must return "
diff --git a/scipy/stats/_stats_py.py b/scipy/stats/_stats_py.py
index a0bcb13c74b2b1b9bb75dd1ecad59dbab08ac249..3add2952f4f711721614170ba67664d272251026 100644
--- a/scipy/stats/_stats_py.py
+++ b/scipy/stats/_stats_py.py
@@ -45,7 +45,9 @@ from scipy._lib._util import (check_random_state, MapWrapper, _get_nan,
                               AxisError)
 
 import scipy.special as special
-from scipy import linalg
+# Import unused here but needs to stay until end of deprecation periode
+# See https://github.com/scipy/scipy/issues/15765#issuecomment-1875564522
+from scipy import linalg  # noqa: F401
 from . import distributions
 from . import _mstats_basic as mstats_basic
 from ._stats_mstats_common import (_find_repeats, linregress, theilslopes,
@@ -4347,13 +4349,11 @@ def _pearsonr_fisher_ci(r, n, confidence_level, alternative):
     Fisher's transformation is used to compute the confidence interval
     (https://en.wikipedia.org/wiki/Fisher_transformation).
     """
-    if r == 1:
-        zr = np.inf
-    elif r == -1:
-        zr = -np.inf
-    else:
+
+    with np.errstate(divide='ignore'):
         zr = np.arctanh(r)
 
+    ones = np.ones_like(r)
     if n > 3:
         se = np.sqrt(1 / (n - 3))
         if alternative == "two-sided":
@@ -4366,28 +4366,28 @@ def _pearsonr_fisher_ci(r, n, confidence_level, alternative):
             h = special.ndtri(confidence_level)
             zhi = zr + h*se
             rhi = np.tanh(zhi)
-            rlo = -1.0
+            rlo = -ones
         else:
             # alternative == "greater":
             h = special.ndtri(confidence_level)
             zlo = zr - h*se
             rlo = np.tanh(zlo)
-            rhi = 1.0
+            rhi = ones
     else:
-        rlo, rhi = -1.0, 1.0
+        rlo, rhi = -ones, ones
 
     return ConfidenceInterval(low=rlo, high=rhi)
 
 
-def _pearsonr_bootstrap_ci(confidence_level, method, x, y, alternative):
+def _pearsonr_bootstrap_ci(confidence_level, method, x, y, alternative, axis):
     """
     Compute the confidence interval for Pearson's R using the bootstrap.
     """
-    def statistic(x, y):
-        statistic, _ = pearsonr(x, y)
+    def statistic(x, y, axis):
+        statistic, _ = pearsonr(x, y, axis=axis)
         return statistic
 
-    res = bootstrap((x, y), statistic, confidence_level=confidence_level,
+    res = bootstrap((x, y), statistic, confidence_level=confidence_level, axis=axis,
                     paired=True, alternative=alternative, **method._asdict())
     # for one-sided confidence intervals, bootstrap gives +/- inf on one side
     res.confidence_interval = np.clip(res.confidence_interval, -1, 1)
@@ -4419,12 +4419,13 @@ class PearsonRResult(PearsonRResultBase):
         coefficient `statistic` for the given confidence level.
 
     """
-    def __init__(self, statistic, pvalue, alternative, n, x, y):
+    def __init__(self, statistic, pvalue, alternative, n, x, y, axis):
         super().__init__(statistic, pvalue)
         self._alternative = alternative
         self._n = n
         self._x = x
         self._y = y
+        self._axis = axis
 
         # add alias for consistency with other correlation functions
         self.correlation = statistic
@@ -4475,8 +4476,8 @@ class PearsonRResult(PearsonRResultBase):
                https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
         """
         if isinstance(method, BootstrapMethod):
-            ci = _pearsonr_bootstrap_ci(confidence_level, method,
-                                        self._x, self._y, self._alternative)
+            ci = _pearsonr_bootstrap_ci(confidence_level, method, self._x, self._y,
+                                        self._alternative, self._axis)
         elif method is None:
             ci = _pearsonr_fisher_ci(self.statistic, self._n, confidence_level,
                                      self._alternative)
@@ -4486,7 +4487,7 @@ class PearsonRResult(PearsonRResultBase):
             raise ValueError(message)
         return ci
 
-def pearsonr(x, y, *, alternative='two-sided', method=None):
+def pearsonr(x, y, *, alternative='two-sided', method=None, axis=0):
     r"""
     Pearson correlation coefficient and p-value for testing non-correlation.
 
@@ -4508,10 +4509,15 @@ def pearsonr(x, y, *, alternative='two-sided', method=None):
 
     Parameters
     ----------
-    x : (N,) array_like
+    x : array_like
         Input array.
-    y : (N,) array_like
+    y : array_like
         Input array.
+    axis : int or None, default
+        Axis along which to perform the calculation. Default is 0.
+        If None, ravel both arrays before performing the calculation.
+
+        .. versionadded:: 1.13.0
     alternative : {'two-sided', 'greater', 'less'}, optional
         Defines the alternative hypothesis. Default is 'two-sided'.
         The following options are available:
@@ -4669,6 +4675,24 @@ def pearsonr(x, y, *, alternative='two-sided', method=None):
     >>> res.confidence_interval(confidence_level=0.9, method=method)
     ConfidenceInterval(low=-0.9983163756488651, high=-0.22771001702132443)  # may vary
 
+    If N-dimensional arrays are provided, multiple tests are performed in a
+    single call according to the same conventions as most `scipy.stats` functions:
+
+    >>> rng = np.random.default_rng(2348246935601934321)
+    >>> x = rng.standard_normal((8, 15))
+    >>> y = rng.standard_normal((8, 15))
+    >>> stats.pearsonr(x, y, axis=0).statistic.shape  # between corresponding columns
+    (15,)
+    >>> stats.pearsonr(x, y, axis=1).statistic.shape  # between corresponding rows
+    (8,)
+
+    To perform all pairwise comparisons between slices of the arrays,
+    use standard NumPy broadcasting techniques. For instance, to compute the
+    correlation between all pairs of rows:
+
+    >>> stats.pearsonr(x[:, np.newaxis, :], y, axis=-1).statistic.shape
+    (8, 8)
+
     There is a linear dependence between x and y if y = a + b*x + e, where
     a,b are constants and e is a random error term, assumed to be independent
     of x. For simplicity, assume that x is standard normal, a=0, b=1 and let
@@ -4716,85 +4740,111 @@ def pearsonr(x, y, *, alternative='two-sided', method=None):
     than zero which happens in about half of the cases if we sample x and y.
 
     """
-    n = len(x)
-    if n != len(y):
-        raise ValueError('x and y must have the same length.')
+    x = np.asarray(x)
+    y = np.asarray(y)
+
+    if axis is None:
+        x = x.ravel()
+        y = y.ravel()
+        axis = -1
+
+    axis_int = int(axis)
+    if axis_int != axis:
+        raise ValueError('`axis` must be an integer.')
+    axis = axis_int
+
+    n = x.shape[axis]
+    if n != y.shape[axis]:
+        raise ValueError('`x` and `y` must have the same length along `axis`.')
 
     if n < 2:
-        raise ValueError('x and y must have length at least 2.')
+        raise ValueError('`x` and `y` must have length at least 2.')
 
-    x = np.asarray(x)
-    y = np.asarray(y)
+    try:
+        x, y = np.broadcast_arrays(x, y)
+    except ValueError as e:
+        message = '`x` and `y` must be broadcastable.'
+        raise ValueError(message) from e
 
-    if (np.issubdtype(x.dtype, np.complexfloating)
-            or np.issubdtype(y.dtype, np.complexfloating)):
+    x = np.moveaxis(x, axis, -1)
+    y = np.moveaxis(y, axis, -1)
+    axis = -1
+
+    dtype = np.result_type(x.dtype, y.dtype)
+    if np.issubdtype(dtype, np.integer):
+        dtype = np.float64
+
+    if np.issubdtype(dtype, np.complexfloating):
         raise ValueError('This function does not support complex data')
 
+    x = x.astype(dtype, copy=False)
+    y = y.astype(dtype, copy=False)
+    threshold = np.finfo(dtype).eps ** 0.75
+
     # If an input is constant, the correlation coefficient is not defined.
-    if (x == x[0]).all() or (y == y[0]).all():
+    const_x = (x == x[..., [0]]).all(axis=-1)
+    const_y = (y == y[..., [0]]).all(axis=-1)
+    const_xy = const_x | const_y
+    if np.any(const_xy):
         msg = ("An input array is constant; the correlation coefficient "
                "is not defined.")
         warnings.warn(stats.ConstantInputWarning(msg), stacklevel=2)
-        result = PearsonRResult(statistic=np.nan, pvalue=np.nan, n=n,
-                                alternative=alternative, x=x, y=y)
-        return result
 
     if isinstance(method, PermutationMethod):
-        def statistic(y):
-            statistic, _ = pearsonr(x, y, alternative=alternative)
+        def statistic(y, axis):
+            statistic, _ = pearsonr(x, y, axis=axis, alternative=alternative)
             return statistic
 
         res = permutation_test((y,), statistic, permutation_type='pairings',
-                               alternative=alternative, **method._asdict())
+                               axis=axis, alternative=alternative, **method._asdict())
 
         return PearsonRResult(statistic=res.statistic, pvalue=res.pvalue, n=n,
-                              alternative=alternative, x=x, y=y)
+                              alternative=alternative, x=x, y=y, axis=axis)
     elif isinstance(method, MonteCarloMethod):
-        def statistic(x, y):
-            statistic, _ = pearsonr(x, y, alternative=alternative)
+        def statistic(x, y, axis):
+            statistic, _ = pearsonr(x, y, axis=axis, alternative=alternative)
             return statistic
 
         if method.rvs is None:
             rng = np.random.default_rng()
             method.rvs = rng.normal, rng.normal
 
-        res = monte_carlo_test((x, y,), statistic=statistic,
+        res = monte_carlo_test((x, y,), statistic=statistic, axis=axis,
                                alternative=alternative, **method._asdict())
 
         return PearsonRResult(statistic=res.statistic, pvalue=res.pvalue, n=n,
-                              alternative=alternative, x=x, y=y)
+                              alternative=alternative, x=x, y=y, axis=axis)
     elif method is not None:
         message = ('`method` must be an instance of `PermutationMethod`,'
                    '`MonteCarloMethod`, or None.')
         raise ValueError(message)
 
-    # dtype is the data type for the calculations.  This expression ensures
-    # that the data type is at least 64 bit floating point.  It might have
-    # more precision if the input is, for example, np.longdouble.
-    dtype = type(1.0 + x[0] + y[0])
-
     if n == 2:
-        r = dtype(np.sign(x[1] - x[0])*np.sign(y[1] - y[0]))
-        result = PearsonRResult(statistic=r, pvalue=1.0, n=n,
-                                alternative=alternative, x=x, y=y)
+        r = (np.sign(x[..., 1] - x[..., 0])*np.sign(y[..., 1] - y[..., 0]))[()]
+        result = PearsonRResult(statistic=r, pvalue=np.ones_like(r)[()], n=n,
+                                alternative=alternative, x=x, y=y, axis=axis)
         return result
 
-    xmean = x.mean(dtype=dtype)
-    ymean = y.mean(dtype=dtype)
+    xmean = x.mean(axis=axis, keepdims=True)
+    ymean = y.mean(axis=axis, keepdims=True)
+    xm = x - xmean
+    ym = y - ymean
 
-    # By using `astype(dtype)`, we ensure that the intermediate calculations
-    # use at least 64 bit floating point.
-    xm = x.astype(dtype) - xmean
-    ym = y.astype(dtype) - ymean
-
-    # Unlike np.linalg.norm or the expression sqrt((xm*xm).sum()),
-    # scipy.linalg.norm(xm) does not overflow if xm is, for example,
+    # scipy.linalg.norm(xm) avoids premature overflow when xm is e.g.
     # [-5e210, 5e210, 3e200, -3e200]
-    normxm = linalg.norm(xm)
-    normym = linalg.norm(ym)
-
-    threshold = 1e-13
-    if normxm < threshold*abs(xmean) or normym < threshold*abs(ymean):
+    # but not when `axis` is provided, so scale manually. scipy.linalg.norm
+    # also raises an error with NaN input rather than returning NaN, so
+    # use np.linalg.norm.
+    xmax = np.max(np.abs(xm), axis=axis, keepdims=True)
+    ymax = np.max(np.abs(ym), axis=axis, keepdims=True)
+    with np.errstate(invalid='ignore'):
+        normxm = xmax * np.linalg.norm(xm/xmax, axis=axis, keepdims=True)
+        normym = ymax * np.linalg.norm(ym/ymax, axis=axis, keepdims=True)
+
+    nconst_x = np.any(normxm < threshold*abs(xmean), axis=axis)
+    nconst_y = np.any(normym < threshold*abs(ymean), axis=axis)
+    nconst_xy = nconst_x | nconst_y
+    if np.any(nconst_xy & (~const_xy)):
         # If all the values in x (likewise y) are very close to the mean,
         # the loss of precision that occurs in the subtraction xm = x - xmean
         # might result in large errors in r.
@@ -4802,20 +4852,23 @@ def pearsonr(x, y, *, alternative='two-sided', method=None):
                "correlation coefficient may be inaccurate.")
         warnings.warn(stats.NearConstantInputWarning(msg), stacklevel=2)
 
-    r = np.dot(xm/normxm, ym/normym)
+    with np.errstate(invalid='ignore', divide='ignore'):
+        r = np.sum(xm/normxm * ym/normym, axis=axis)
 
     # Presumably, if abs(r) > 1, then it is only some small artifact of
     # floating point arithmetic.
-    r = max(min(r, 1.0), -1.0)
+    one = np.asarray(1, dtype=dtype)
+    r = np.asarray(np.clip(r, -one, one))
+    r[const_xy] = _get_nan(r)
 
     # As explained in the docstring, the distribution of `r` under the null
     # hypothesis is the beta distribution on (-1, 1) with a = b = n/2 - 1.
-    ab = n/2 - 1
-    dist = stats.beta(ab, ab, loc=-1, scale=2)
+    ab, loc, scale = np.asarray([n/2 - 1, -1, 2], dtype=dtype)
+    dist = stats.beta(ab, ab, loc=loc, scale=scale)
     pvalue = _get_pvalue(r, dist, alternative)
 
-    return PearsonRResult(statistic=r, pvalue=pvalue, n=n,
-                          alternative=alternative, x=x, y=y)
+    return PearsonRResult(statistic=r, pvalue=pvalue.astype(dtype), n=n,
+                          alternative=alternative, x=x, y=y, axis=axis)
 
 
 def fisher_exact(table, alternative='two-sided'):
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/stats/tests/test_stats.py b/scipy/stats/tests/test_stats.py
index a1600a95e560933438cc3ca245f36f117407fe0f..ab7e2ed71e0d7ecc5495ac265a16d109d11f8874 100644
--- a/scipy/stats/tests/test_stats.py
+++ b/scipy/stats/tests/test_stats.py
@@ -401,7 +401,7 @@ class TestCorrPearsonr:
         # See https://github.com/scipy/scipy/issues/9353
         x = [0.004434375, 0.004756007, 0.003911996, 0.0038005, 0.003409971]
         y = [2.48e-188, 7.41e-181, 4.09e-208, 2.08e-223, 2.66e-245]
-        r, p = stats.pearsonr(x,y)
+        r, p = stats.pearsonr(x, y)
 
         # The expected values were computed using mpmath with 80 digits
         # of precision.
@@ -516,30 +516,30 @@ class TestCorrPearsonr:
     @pytest.mark.parametrize('method', ('permutation', 'monte_carlo'))
     def test_resampling_pvalue(self, method, alternative):
         rng = np.random.default_rng(24623935790378923)
-        size = 100 if method == 'permutation' else 1000
+        size = (2, 100) if method == 'permutation' else (2, 1000)
         x = rng.normal(size=size)
         y = rng.normal(size=size)
         methods = {'permutation': stats.PermutationMethod(random_state=rng),
                    'monte_carlo': stats.MonteCarloMethod(rvs=(rng.normal,)*2)}
         method = methods[method]
-        res = stats.pearsonr(x, y, alternative=alternative, method=method)
-        ref = stats.pearsonr(x, y, alternative=alternative)
+        res = stats.pearsonr(x, y, alternative=alternative, method=method, axis=-1)
+        ref = stats.pearsonr(x, y, alternative=alternative, axis=-1)
         assert_allclose(res.statistic, ref.statistic, rtol=1e-15)
         assert_allclose(res.pvalue, ref.pvalue, rtol=1e-2, atol=1e-3)
 
     @pytest.mark.xslow
     @pytest.mark.parametrize('alternative', ('less', 'greater', 'two-sided'))
     def test_bootstrap_ci(self, alternative):
-        rng = np.random.default_rng(24623935790378923)
-        x = rng.normal(size=100)
-        y = rng.normal(size=100)
-        res = stats.pearsonr(x, y, alternative=alternative)
+        rng = np.random.default_rng(2462935790378923)
+        x = rng.normal(size=(2, 100))
+        y = rng.normal(size=(2, 100))
+        res = stats.pearsonr(x, y, alternative=alternative, axis=-1)
 
         method = stats.BootstrapMethod(random_state=rng)
         res_ci = res.confidence_interval(method=method)
         ref_ci = res.confidence_interval()
 
-        assert_allclose(res_ci, ref_ci, atol=1e-2)
+        assert_allclose(res_ci, ref_ci, atol=1.5e-2)
 
     def test_invalid_method(self):
         message = "`method` must be an instance of..."
@@ -550,6 +550,89 @@ class TestCorrPearsonr:
         with pytest.raises(ValueError, match=message):
             res.confidence_interval(method="exact")
 
+    @pytest.mark.parametrize('axis', [0, 1])
+    def test_axis01(self, axis):
+        rng = np.random.default_rng(38572345825)
+        shape = (9, 10)
+        x, y = rng.normal(size=(2,) + shape)
+        res = stats.pearsonr(x, y, axis=axis)
+        ci = res.confidence_interval()
+        if axis == 0:
+            x, y = x.T, y.T
+        for i in range(x.shape[0]):
+            res_i = stats.pearsonr(x[i], y[i])
+            ci_i = res_i.confidence_interval()
+            assert_allclose(res.statistic[i], res_i.statistic)
+            assert_allclose(res.pvalue[i], res_i.pvalue)
+            assert_allclose(ci.low[i], ci_i.low)
+            assert_allclose(ci.high[i], ci_i.high)
+
+    def test_axis_None(self):
+        rng = np.random.default_rng(38572345825)
+        shape = (9, 10)
+        x, y = rng.normal(size=(2,) + shape)
+        res = stats.pearsonr(x, y, axis=None)
+        ci = res.confidence_interval()
+        ref = stats.pearsonr(x.ravel(), y.ravel())
+        ci_ref = ref.confidence_interval()
+        assert_allclose(res.statistic, ref.statistic)
+        assert_allclose(res.pvalue, ref.pvalue)
+        assert_allclose(ci, ci_ref)
+
+    def test_nd_input_validation(self):
+        x, y = np.ones((2, 2, 5))
+        message = '`axis` must be an integer.'
+        with pytest.raises(ValueError, match=message):
+            stats.pearsonr(x, y, axis=1.5)
+
+        message = '`x` and `y` must have the same length along `axis`'
+        with pytest.raises(ValueError, match=message):
+            stats.pearsonr(x, np.ones((2, 1)), axis=1)
+
+        message = '`x` and `y` must have length at least 2.'
+        with pytest.raises(ValueError, match=message):
+            stats.pearsonr(*np.ones((2, 2, 1)), axis=1)
+
+        message = '`x` and `y` must be broadcastable.'
+        with pytest.raises(ValueError, match=message):
+            stats.pearsonr(x, np.ones((3, 5)), axis=1)
+
+    def test_nd_special_cases(self):
+        rng = np.random.default_rng(34989235492245)
+        x0, y0 = rng.random((2, 3, 5))
+
+        message = 'An input array is constant'
+        with pytest.warns(stats.ConstantInputWarning, match=message):
+            x = x0.copy()
+            x[0] = 1
+            res = stats.pearsonr(x, y0, axis=1)
+            ci = res.confidence_interval()
+            np.testing.assert_equal(res.statistic[0], np.nan)
+            np.testing.assert_equal(res.pvalue[0], np.nan)
+            np.testing.assert_equal(ci.low[0], np.nan)
+            np.testing.assert_equal(ci.high[0], np.nan)
+            assert not np.any(np.isnan(res.statistic[1:]))
+            assert not np.any(np.isnan(res.pvalue[1:]))
+            assert not np.any(np.isnan(ci.low[1:]))
+            assert not np.any(np.isnan(ci.high[1:]))
+
+        message = 'An input array is nearly constant'
+        with pytest.warns(stats.NearConstantInputWarning, match=message):
+            x[0, 0] = 1 + 1e-15
+            stats.pearsonr(x, y0, axis=1)
+
+        # length 2 along axis
+        x = [[1, 2], [1, 2], [2, 1], [2, 1]]
+        y = [[1, 2], [2, 1], [1, 2], [2, 1]]
+        res = stats.pearsonr(x, y, axis=-1)
+        ci = res.confidence_interval()
+        assert_allclose(res.statistic, [1, -1, -1, 1])
+        assert_allclose(res.pvalue, 1)
+        assert_allclose(ci.low, -1)
+        assert_allclose(ci.high, 1)
+        assert (res.pvalue.shape == res.statistic.shape
+                == ci.low.shape == ci.high.shape)
+
 
 class TestFisherExact:
     """Some tests to show that fisher_exact() works correctly.
```

## Validation

```json
{
 "image_head": "cd60e810c17442f71ab7f7788eccd1013fc265f1",
 "patch_applies": true,
 "test_files": [
  "scipy/stats/tests/test_stats.py"
 ],
 "collected_before": 976,
 "collected_after": 976,
 "outcomes_before": {
  "PASSED": 954,
  "SKIPPED": 14,
  "FAILED": 5,
  "XFAIL": 3
 },
 "outcomes_after": {
  "PASSED": 959,
  "SKIPPED": 14,
  "XFAIL": 3
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "ests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.5]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.500000000001]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.8]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_monotonicity_in_alpha[20]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_monotonicity_in_alpha[2000]\nSKIPPED [14] scipy/conftest.py:51: very slow test; set environment variable SCIPY_XSLOW=1 to run it\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-two-sided] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-less] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-greater] - reason: Discrepancy in `main`; needs further investigation.\nFAILED scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_axis01[0] - Ty...\nFAILED scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_axis01[1] - Ty...\nFAILED scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_axis_None - Ty...\nFAILED scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_nd_input_validation\nFAILED scipy/stats/tests/test_stats.py::TestCorrPearsonr::test_nd_special_cases\n======= 5 failed, 952 passed, 14 skipped, 3 xfailed in 139.83s (0:02:19) =======",
 "tail_after": ".5]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[20-0.500000000001]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[20-0.8]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.2]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.499999999999]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.5]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.500000000001]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_expectile_properties[2000-0.8]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_monotonicity_in_alpha[20]\nPASSED scipy/stats/tests/test_stats.py::TestExpectile::test_monotonicity_in_alpha[2000]\nSKIPPED [14] scipy/conftest.py:51: very slow test; set environment variable SCIPY_XSLOW=1 to run it\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-two-sided] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-less] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-greater] - reason: Discrepancy in `main`; needs further investigation.\n============ 957 passed, 14 skipped, 3 xfailed in 137.52s (0:02:17) ============",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

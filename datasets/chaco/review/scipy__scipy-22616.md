# scipy__scipy-22616

[back to the list](README.md) -- **ENH: stats: use `vecdot` and `nonzero` where appropriate**

| field | value |
|---|---|
| pull request | [scipy/scipy#22616](https://github.com/scipy/scipy/pull/22616) (created 2025-03-02, merged 2025-03-04) |
| ChaCo lists | full, ablation |
| status | **not-fail-to-pass** -- no developer test fails before the change and passes after (1205 pass on both sides) |
| base commit | [`be136acf77f2`](https://github.com/scipy/scipy/commit/be136acf77f2950d6bf62742781bb1841c502dab) (2025-03-04), first parent of the merge commit |
| merge commit | [`0dec1d661e10`](https://github.com/scipy/scipy/commit/0dec1d661e109beda6fa40eb01342f328d5e185e) |
| issues closed | none |
| version | 1.16 |
| image | `f2p-chaco/scipy__scipy-22616:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-22616.Dockerfile) |
| source files (`patch`) | `scipy/_lib/_util.py`, `scipy/stats/_kde.py`, `scipy/stats/_stats_py.py` |
| test files (`test_patch`) | `scipy/stats/tests/test_stats.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (1205)

<details><summary>show</summary>

- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_bad_inputs`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_dtypes`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_r`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_scholar`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_compare_scholar3`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_constant_input`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_nan_policy_omit`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_nan_policy_propagate`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_nan_policy_raise`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_too_small_inputs[case0]`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_too_small_inputs[case1]`
- `scipy/stats/tests/test_stats.py::TestAlexanderGovern::test_too_small_inputs[case2]`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_alternative_error`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_default`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_distribution_error`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_distribution_norm`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_empty_imput[kwarg_update0]`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_empty_imput[kwarg_update1]`
- `scipy/stats/tests/test_stats.py::TestBrunnerMunzel::test_brunnermunzel_empty_imput[kwarg_update2]`
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
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chiquare_data_types_attributes[numpy-1000000-int32]`
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chiquare_data_types_attributes[numpy-200-uint8]`
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chisquare_12282a[numpy]`
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chisquare_12282b[numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-0-fisher]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-0-mudholkar_george]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-0-pearson]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-0-stouffer]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-0-tippett]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-1-fisher]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-1-mudholkar_george]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-1-pearson]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-1-stouffer]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[numpy-1-tippett]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-fisher-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-fisher-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-fisher-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-mudholkar_george-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-mudholkar_george-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-mudholkar_george-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-pearson-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-pearson-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-pearson-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-stouffer-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-stouffer-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-stouffer-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-tippett-all]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-tippett-random]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[numpy-tippett-single]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[numpy-fisher-14.83716180549625-0.02156175132483465]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[numpy-mudholkar_george-6.828712071641684-0.01654551838539527]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[numpy-pearson--1.179737662212887-0.022126300085691275]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[numpy-stouffer-2.131790594240385-0.01651203260896294]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[numpy-tippett-0.01-0.02970100000000002]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[numpy-fisher]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[numpy-mudholkar_george]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[numpy-pearson]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[numpy-stouffer]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[numpy-tippett]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_weighted_stouffer[numpy-weights0-2.131790594240385-0.01651203260896294]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_weighted_stouffer[numpy-weights1-1.051815015753598-0.1464422142261314]`
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
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_axis_none[numpy]`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_ddof[numpy]`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_empty[numpy]`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_nan_policy_other[numpy]`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_numbers[numpy]`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_result_attributes`
- `scipy/stats/tests/test_stats.py::TestDescribe::test_describe_scalar[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_equal_var_input_validation`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_known_exact`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_large_integer_array`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_length0_1d_error`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_length0_2d_error`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_nist`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_result_attributes`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_too_few_inputs[args0]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_too_few_inputs[args1]`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_trivial`
- `scipy/stats/tests/test_stats.py::TestFOneWay::test_unequal_var`
- `scipy/stats/tests/test_stats.py::TestFindRepeats::test_basic`
- `scipy/stats/tests/test_stats.py::TestFindRepeats::test_empty_result`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_basic`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_gh3014`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_gh4130`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_gh9231`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_input_validation_edge_cases_rxc`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_large_numbers`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_less_greater`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_precise`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_raises`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_resampling_2x2`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_resampling_rxc`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_result[greater]`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_result[less]`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_result[two-sided]`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_row_or_col_zero`
- `scipy/stats/tests/test_stats.py::TestGMean::test_0[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_1d_neg[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_1d_with_0[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_2d[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_2d_axis0[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_2d_axis1[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_large_values[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_weights_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_weights_1d_list[numpy]`
- `scipy/stats/tests/test_stats.py::TestGMean::test_weights_masked_1d_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_1d_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_1d_numeric_array_like_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_0[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_1[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_2[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_type_tuple[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_ddof_equal_to_number_of_observations[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_propagates_nan_values[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_raises_value_error_non_numeric_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[numpy--1]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[numpy-0]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[numpy-inf]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[numpy-nan]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_0[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_1d_with_negative_value[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_1d_with_zero[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_2d[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_2d_axis0[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_2d_axis0_with_zero[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_2d_axis1[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_2d_axis1_with_zero[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_weights_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_weights_1d_list[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_weights_2d_axis0[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_weights_2d_axis1[numpy]`
- `scipy/stats/tests/test_stats.py::TestHMean::test_weights_masked_1d_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestIQR::test_2D`
- `scipy/stats/tests/test_stats.py::TestIQR::test_api`
- `scipy/stats/tests/test_stats.py::TestIQR::test_axis`
- `scipy/stats/tests/test_stats.py::TestIQR::test_basic`
- `scipy/stats/tests/test_stats.py::TestIQR::test_constant`
- `scipy/stats/tests/test_stats.py::TestIQR::test_empty[x0]`
- `scipy/stats/tests/test_stats.py::TestIQR::test_empty[x1]`
- `scipy/stats/tests/test_stats.py::TestIQR::test_interpolation`
- `scipy/stats/tests/test_stats.py::TestIQR::test_keepdims`
- `scipy/stats/tests/test_stats.py::TestIQR::test_nanpolicy`
- `scipy/stats/tests/test_stats.py::TestIQR::test_rng`
- `scipy/stats/tests/test_stats.py::TestIQR::test_scalarlike`
- `scipy/stats/tests/test_stats.py::TestIQR::test_scale`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_axis[numpy]`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_jarque_bera_against_R[numpy]`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_jarque_bera_array_like[numpy]`
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_jarque_bera_too_few_observations[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestKSTest::test_pm_inf_gh20386`
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
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_argument_checking[case0]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_argument_checking[case1]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_argument_checking[case2]`
- `scipy/stats/tests/test_stats.py::TestKSTwoSamples::test_gh11184`
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
- `scipy/stats/tests/test_stats.py::TestKruskal::test_no_args_gh20661`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_simple`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_simple_tie`
- `scipy/stats/tests/test_stats.py::TestKruskal::test_three_groups`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_kurtosis[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_kurtosis_array_scalar`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_kurtosis_constant_value[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_kurtosis_nan_policy`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_kurtosis_propagate_nan`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-False--1]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-False-0]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-False-2]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-False-None]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-True--1]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-True-0]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-True-2]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-False-True-None]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-False--1]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-False-0]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-False-2]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-False-None]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-True--1]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-True-0]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-True-2]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[numpy-True-True-None]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_against_R[numpy-greater]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_against_R[numpy-less]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_against_R[numpy-two-sided]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_gh9033_regression[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_intuitive[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_kurtosistest_too_few_observations[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_axis_iv[1.5]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_axis_iv[a`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_axis_iv[a duck]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_axis_iv[axis1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_axis_iv[inf]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_axis_iv[nan]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_dtype`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_dtype_iv`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_dtype_iv_non_numeric`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[False-False-1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[False-False-4]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[False-False-order2]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[False-True-1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[False-True-4]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[False-True-order2]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[True-False-1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[True-False-4]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[True-False-order2]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[True-True-1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[True-True-4]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_lmoment[True-True-order2]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[-1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[0]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[1.5]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[a`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[a duck]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[inf]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[nan]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[order1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[order7]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_order_iv[order8]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_sorted_iv[1.5]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_sorted_iv[a`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_sorted_iv[a duck]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_sorted_iv[inf]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_sorted_iv[nan]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_sorted_iv[sorted1]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_standardize_iv[1.5]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_standardize_iv[a`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_standardize_iv[a duck]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_standardize_iv[inf]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_standardize_iv[nan]`
- `scipy/stats/tests/test_stats.py::TestLMoment::test_standardize_iv[standardize1]`
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
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[numpy-0-1-complex128]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[numpy-0-1-float32]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[numpy-0-1-float64]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[numpy-1-0-complex128]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[numpy-1-0-float32]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[numpy-1-0-float64]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment[numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_accuracy`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0--1-0]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0--1-1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0--1-2]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0--1-3]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-0-0]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-0-1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-0-2]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-0-3]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-1-0]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-1-1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-1-2]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-0-1-3]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None--1-0]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None--1-1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None--1-2]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None--1-3]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-0-0]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-0-1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-0-2]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-0-3]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-1-0]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-1-1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-1-2]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[numpy-None-1-3]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[numpy-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[numpy-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[numpy-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[numpy-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[numpy-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[numpy-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-0-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-0-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-0-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-0-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-0-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-0-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-1-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-1-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-1-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-1-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-1-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-1-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-2-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-2-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-2-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-2-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-2-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-2-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-3-0-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-3-0-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-3-1-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-3-1-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-3-None-10]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[numpy-3-None-size1]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_empty_order[numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_propagate_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_nan_policy`
- `scipy/stats/tests/test_stats.py::TestMoments::test_rename_moment_order[numpy]`
- `scipy/stats/tests/test_stats.py::TestNormalTest::test_against_R[numpy-two-sided]`
- `scipy/stats/tests/test_stats.py::TestNormalTest::test_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestNormalTest::test_too_few_observations[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_1d_with_negative_value[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_1d_with_zero[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis0[numpy-a0--0.5]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis0[numpy-a1-0.5]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis1[numpy-a0--0.5]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis1[numpy-a1-0.5]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axisnone[numpy-a0--0.5]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axisnone[numpy-a1-0.5]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_bad_exponent[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_1d_list[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_2d[numpy-0-gmean-0]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_2d[numpy-1-hmean--1]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_2d[numpy-None-wpmean_reference-9.87654321]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_masked_1d_array[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-greater-0]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-greater-1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-greater-None]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-less-0]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-less-1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-less-None]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-two-sided-0]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-two-sided-1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[numpy-two-sided-None]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_axis01[numpy-0]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_axis01[numpy-1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_axis_None[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[numpy-greater-0.1629000687684--0.6785654158217636-1-1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[numpy-greater-0.8370999312316--0.985600937290653-1.0--1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[numpy-less-0.1629000687684--1.0-0.6785654158217636--1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[numpy-less-0.8370999312316--1-0.985600937290653-1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[numpy-two-sided-0.325800137536--0.814938968841-0.99230697523-1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[numpy-two-sided-0.325800137536--0.992306975236-0.81493896884--1]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_bootstrap_ci[numpy-greater]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_bootstrap_ci[numpy-less]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_bootstrap_ci[numpy-two-sided]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_constant_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_different_dimensionality[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_extremely_large_input_values[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_input_validation[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length3_r_exactly_negative_one[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length_two_constant_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length_two_neg1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length_two_pos1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_nd_input_validation[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_nd_special_cases[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_near_constant_input[numpy-float32]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_near_constant_input[numpy-float64]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_negative_correlation_pvalue_gh17795[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_pearsonr_result_attributes[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_r_almost_exactly_neg1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_r_almost_exactly_pos1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-monte_carlo-greater]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-monte_carlo-less]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-monte_carlo-two-sided]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-monte_carlo2-greater]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-monte_carlo2-less]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-monte_carlo2-two-sided]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-permutation-greater]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-permutation-less]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[numpy-permutation-two-sided]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_very_large_input_values[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_very_small_input_values[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pBIGBIG`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pBIGHUGE`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pBIGLITTLE`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pBIGROUND`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pBIGTINY`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pHUGEHUGE`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pHUGEROUND`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pHUGETINY`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pLITTLEHUGE`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pLITTLELITTLE`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pLITTLEROUND`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pLITTLETINY`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pROUNDROUND`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pTINYROUND`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pTINYTINY`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pXBIG`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pXHUGE`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pXLITTLE`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pXROUND`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pXTINY`
- `scipy/stats/tests/test_stats.py::TestPearsonrWilkinson::test_pXX`
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
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_axis[numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat0-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat0-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat0-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat0-case3]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat1-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat1-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat1-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat1-case3]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat2-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat2-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat2-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat2-case3]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat3-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat3-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat3-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat3-case3]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat4-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat4-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat4-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat4-case3]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat5-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat5-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat5-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat5-case3]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat6-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat6-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat6-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[numpy-lambda_stat6-case3]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_ddof_broadcasting[numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat0-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat0-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat0-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat1-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat1-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat1-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat2-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat2-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat2-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat3-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat3-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat3-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat4-case0]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat4-case1]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[numpy-lambda_stat4-case2]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_power_divergence_against_cressie_read_data[numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_power_divergence_gh_12282[numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_power_divergence_result_attributes[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_simple`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_simple_negative_cor`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_two_inputs`
- `scipy/stats/tests/test_stats.py::TestRegression::test_regress_two_inputs_horizontal_line`
- `scipy/stats/tests/test_stats.py::TestSEM::test_sem[numpy]`
- `scipy/stats/tests/test_stats.py::TestSEM::test_sem_nan_policy[numpy]`
- `scipy/stats/tests/test_stats.py::TestSEM::test_sem_scalar[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestSkew::test_empty_1d[numpy-kurtosis]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_empty_1d[numpy-skew]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_nan_policy`
- `scipy/stats/tests/test_stats.py::TestSkew::test_precision_loss_gh15554[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skew_constant_value[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skew_propagate_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skewness[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skewness_scalar`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-False--1]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-False-0]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-False-2]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-False-None]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-True--1]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-True-0]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-True-2]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[numpy-True-None]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_against_R[numpy-greater]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_against_R[numpy-less]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_against_R[numpy-two-sided]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_intuitive[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_skewtest_too_few_observations[numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_alternative[numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[numpy-greater]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[numpy-less]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[numpy-two-sided]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_iv[numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_onesample[numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_onesample_nan_policy[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrim::test_trim1`
- `scipy/stats/tests/test_stats.py::TestTrim::test_trim_mean`
- `scipy/stats/tests/test_stats.py::TestTrim::test_trimboth`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tax_scalar_and_nanpolicy[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tmax[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tmean[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tmin[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tmin_scalar_and_nanpolicy[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tsem[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tstd[numpy]`
- `scipy/stats/tests/test_stats.py::TestTrimmedStats::test_tvar[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[1-50]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[10-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[10-1]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[10-50]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[50-10]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[50-1]`
- `scipy/stats/tests/test_stats.py::TestWassersteinDistanceND::test_optimization_vs_analytical[50-50]`
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
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_complex_gh22404[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_dtype[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_empty[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_integer[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_nan_policy[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_non_broadcastable[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_special_cases[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-None--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-None-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-None-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-None-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-True--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-True-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-True-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-False-True-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-None--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-None-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-None-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-None-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-True--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-True-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-True-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[numpy-True-True-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_complex_gh22404[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_dtype[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_empty[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_integer[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_nan_policy[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_special_cases[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-False--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-False-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-False-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-False-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-True--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-True-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-True-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-0-True-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-False--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-False-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-False-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-False-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-True--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-True-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-True-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-True-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-False--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-False-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-False-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-False-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-True--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-True-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-True-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-0-True-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-False--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-False-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-False-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-False-axis3]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-True--1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-True-1]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-True-None]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-propagate-1-True-axis3]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_complex_gh22404[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_degenerate_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_gzscore_masked_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_gzscore_normal_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap[numpy-x0-y0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap[numpy-x1-y1]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_axis[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_ddof[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit[numpy-0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit[numpy-2]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit_with_axis[numpy-0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit_with_axis[numpy-2]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_raise[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_2d_all_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_2d_all_nan_row[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_axis[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_2d[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_2d_nan_policy_omit[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_ddof[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_empty_input[numpy-x0]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_empty_input[numpy-x1]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_masked_element_0_gh19039[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_omit[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_omit_with_ddof[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_propagate[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_raise[numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0-False-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0-False-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0-False-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0-True-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0-True-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0-True-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-False-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-False-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-False-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_monte_carlo_method[shape0-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_monte_carlo_method[shape0-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_monte_carlo_method[shape0-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_monte_carlo_method[shape1-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_monte_carlo_method[shape1-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_monte_carlo_method[shape1-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_method[shape0-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_method[shape0-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_method[shape0-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_method[shape1-greater]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_method[shape1-less]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_method[shape1-two-sided]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_not_implement_for_xp[numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_resampling_input_validation`
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
- `scipy/stats/tests/test_stats.py::Test_ttest_trim::test_permutation_not_implement_for_xp[numpy]`
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
- `scipy/stats/tests/test_stats.py::test_chk_asarray[numpy]`
- `scipy/stats/tests/test_stats.py::test_cumfreq`
- `scipy/stats/tests/test_stats.py::test_friedmanchisquare`
- `scipy/stats/tests/test_stats.py::test_gh5686[numpy]`
- `scipy/stats/tests/test_stats.py::test_kendall_tau_large`
- `scipy/stats/tests/test_stats.py::test_kendalltau`
- `scipy/stats/tests/test_stats.py::test_kendalltau_gh18139_overflow`
- `scipy/stats/tests/test_stats.py::test_kendalltau_nan_2nd_arg`
- `scipy/stats/tests/test_stats.py::test_kendalltau_vs_mstats_basic`
- `scipy/stats/tests/test_stats.py::test_obrientransform`
- `scipy/stats/tests/test_stats.py::test_pointbiserial`
- `scipy/stats/tests/test_stats.py::test_relfreq`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[ks_1samp-args1]`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[ks_2samp-args2]`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[kstest-args3]`
- `scipy/stats/tests/test_stats.py::test_rename_mode_method[wilcoxon-args0]`
- `scipy/stats/tests/test_stats.py::test_segfault_issue_9710`
- `scipy/stats/tests/test_stats.py::test_theilslopes`
- `scipy/stats/tests/test_stats.py::test_ttest_1samp_new[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_1samp_new_omit[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_1samp_popmean_array[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ci_iv[ttest_1samp-args0]`
- `scipy/stats/tests/test_stats.py::test_ttest_ci_iv[ttest_rel-args1]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_axis_size_zero[numpy-b0-expected_shape0]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_axis_size_zero[numpy-b1-expected_shape1]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_empty_1d_returns_nan[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_from_stats_inputs_zero[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_nan_2nd_arg`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_nan_policy`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_nonaxis_size_zero[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_nonaxis_size_zero_different_lengths[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_scalar`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_with_uneq_var[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_zero_division[numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_axis_size_zero[b0-expected_shape0]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_axis_size_zero[b1-expected_shape1]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_ci_1d[greater]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_ci_1d[less]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_ci_1d[two-sided]`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_empty_1d_returns_nan`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_nan_2nd_arg`
- `scipy/stats/tests/test_stats.py::test_ttest_rel_nonaxis_size_zero`
- `scipy/stats/tests/test_stats.py::test_ttest_uniform_pvalues[numpy]`
- `scipy/stats/tests/test_stats.py::test_weightedtau`
- `scipy/stats/tests/test_stats.py::test_weightedtau_vs_quadratic`

</details>

## Problem statement (what the agent may be shown)

````text
Pull request #22616: ENH: stats: use `vecdot` and `nonzero` where appropriate

#### Reference issue
https://github.com/scipy/scipy/pull/22611#discussion_r1976530805
gh-22462 

#### What does this implement/fix?
There are pretty substantial performance arguments for using `vecdot(x, y)` instead of `sum(x, y)`, so I think it's worth using, especially when it's conceptually clear.

```python3
import numpy as np
rng = np.random.default_rng(325943759872345)
x = rng.random(1000)
y = rng.random(1000)

%timeit np.sum(x * y)
8.45 μs ± 3.87 μs per loop (mean ± std. dev. of 7 runs, 100,000 loops each)

%timeit np.vecdot(x, y)
# 1.16 μs ± 9.92 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)
```

While I was at it, I thought it would be worth using `count_nonzero` when we're counting booleans, especially for very long slices.
```python3
mask = x > 0.5

%timeit np.sum(mask)
# 4.21 μs ± 94.4 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)

%timeit np.count_nonzero(mask)
# 432 ns ± 2.54 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)
```

#### Additional information
There are currently some gotchas to using `vecdot` that we need to watch out for, especially when the backend is not NumPy; see data-apis/array-api#910.

This just covers `_stats_py.py` for now. 

What do we want to do for things like `np.sum(x * y * z)`, where we might get a performance improvement, but may not be an improvement conceptually?
````

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/_lib/_util.py b/scipy/_lib/_util.py
index 70bf535f40226c746fed753f3467ce674d41a52a..e3349d73b09ab4abe75099b1ef390e554666d62c 100644
--- a/scipy/_lib/_util.py
+++ b/scipy/_lib/_util.py
@@ -1347,3 +1347,15 @@ def _apply_over_batch(*argdefs):
 
         return wrapper
     return decorator
+
+
+def np_vecdot(x1, x2, /, *, axis=-1):
+    # `np.vecdot` has advantages (e.g. see gh-22462), so let's use it when
+    # available. As functions are translated to Array API, `np_vecdot` can be
+    # replaced with `xp.vecdot`.
+    if np.__version__ > "2.0":
+        return np.vecdot(x1, x2, axis=axis)
+    else:
+        # of course there are other fancy ways of doing this (e.g. `einsum`)
+        # but let's keep it simple since it's temporary
+        return np.sum(x1 * x2, axis=axis)
diff --git a/scipy/stats/_kde.py b/scipy/stats/_kde.py
index 564969c9f080297116a3ea826df0adbc55001d2e..a360994d433f5e9ae705876423fd847ed34cce1c 100644
--- a/scipy/stats/_kde.py
+++ b/scipy/stats/_kde.py
@@ -19,7 +19,7 @@
 
 # SciPy imports.
 from scipy import linalg, special
-from scipy._lib._util import check_random_state
+from scipy._lib._util import check_random_state, np_vecdot
 
 from numpy import (asarray, atleast_2d, reshape, zeros, newaxis, exp, pi,
                    sqrt, ravel, power, atleast_1d, squeeze, sum, transpose,
@@ -210,7 +210,7 @@ class gaussian_kde:
                 raise ValueError("`weights` input should be one-dimensional.")
             if len(self._weights) != self.n:
                 raise ValueError("`weights` input should be of length n")
-            self._neff = 1/sum(self._weights**2)
+            self._neff = 1/np_vecdot(self._weights, self._weights)
 
         # This can be converted to a warning once gh-10205 is resolved
         if self.d > self.n:
@@ -324,8 +324,8 @@ class gaussian_kde:
         sqrt_det = np.prod(np.diagonal(sum_cov_chol[0]))
         norm_const = power(2 * pi, sum_cov.shape[0] / 2.0) * sqrt_det
 
-        energies = sum(diff * tdiff, axis=0) / 2.0
-        result = sum(exp(-energies)*self.weights, axis=0) / norm_const
+        energies = np_vecdot(diff, tdiff, axis=0) / 2.0
+        result = np_vecdot(exp(-energies), self.weights, axis=0) / norm_const
 
         return result
 
@@ -359,9 +359,8 @@ class gaussian_kde:
         normalized_low = ravel((low - self.dataset) / stdev)
         normalized_high = ravel((high - self.dataset) / stdev)
 
-        value = np.sum(self.weights*(
-                        special.ndtr(normalized_high) -
-                        special.ndtr(normalized_low)))
+        delta = special.ndtr(normalized_high) - special.ndtr(normalized_low)
+        value = np_vecdot(self.weights, delta)
         return value
 
     def integrate_box(self, low_bounds, high_bounds, maxpts=None, *, rng=None):
@@ -392,8 +391,7 @@ class gaussian_kde:
             high, lower_limit=low, cov=self.covariance, maxpts=maxpts,
             rng=rng
         )
-        # XXX: xp.linalg.vecdot is much faster than (a*b).sum(axis=-1)
-        return (values * self.weights).sum(axis=-1)
+        return np_vecdot(values, self.weights, axis=-1)
 
     def integrate_kde(self, other):
         """
@@ -435,8 +433,8 @@ class gaussian_kde:
             diff = large.dataset - mean
             tdiff = linalg.cho_solve(sum_cov_chol, diff)
 
-            energies = sum(diff * tdiff, axis=0) / 2.0
-            result += sum(exp(-energies)*large.weights, axis=0)*small.weights[i]
+            energies = np_vecdot(diff, tdiff, axis=0) / 2.0
+            result += np_vecdot(exp(-energies), large.weights, axis=0)*small.weights[i]
 
         sqrt_det = np.prod(np.diagonal(sum_cov_chol[0]))
         norm_const = power(2 * pi, sum_cov.shape[0] / 2.0) * sqrt_det
@@ -699,7 +697,7 @@ class gaussian_kde:
         try:
             return self._neff
         except AttributeError:
-            self._neff = 1/sum(self.weights**2)
+            self._neff = 1/np_vecdot(self.weights, self.weights)
             return self._neff
 
 
diff --git a/scipy/stats/_stats_py.py b/scipy/stats/_stats_py.py
index 083abc016479f81ab36e6ed6b295a8917d6989f2..11e8a3cae151be2b65095dc95907ce89f618e1a4 100644
--- a/scipy/stats/_stats_py.py
+++ b/scipy/stats/_stats_py.py
@@ -44,7 +44,7 @@ from scipy.optimize import milp, LinearConstraint
 from scipy._lib._array_api import is_lazy_array, xp_ravel
 from scipy._lib._util import (check_random_state, _get_nan,
                               _rename_parameter, _contains_nan,
-                              AxisError, _lazywhere)
+                              AxisError, _lazywhere, np_vecdot)
 from scipy._lib.deprecation import _deprecate_positional_args
 
 import scipy.special as special
@@ -3992,16 +3992,14 @@ def f_oneway(*samples, axis=0, equal_var=True):
 
         # calculate adjusted grand mean
         # "... and $\hat{y} = \sum w_t y_t / \sum w_t$. When all..."
-        y_hat = np.sum(w_t * y_t, axis=0) / np.sum(w_t, axis=0)
+        y_hat = np_vecdot(w_t, y_t, axis=0) / np.sum(w_t, axis=0)
 
         # adjust f statistic
         # ref.[4] p.334 eq.29
-        numerator = np.sum(w_t * (y_t - y_hat)**2, axis=0) / (k - 1)
+        numerator =  np_vecdot(w_t, (y_t - y_hat)**2, axis=0) / (k - 1)
         denominator = (
                 1 + 2 * (k - 2) / (k**2 - 1) *
-                np.sum((1 / (n_t - 1)) *
-                       (1 - w_t / s_w_t)**2,
-                       axis=0)
+                np_vecdot(1 / (n_t - 1), (1 - w_t / s_w_t)**2, axis=0)
         )
         f = numerator / denominator
 
@@ -4013,8 +4011,7 @@ def f_oneway(*samples, axis=0, equal_var=True):
         # ref.[4] p.334 eq.30
         hat_f2 = (
                 (k**2 - 1) /
-                (3 * np.sum((1 / (n_t - 1)) *
-                            (1 - w_t / s_w_t)**2, axis=0))
+                (3 * np_vecdot(1 / (n_t - 1), (1 - w_t / s_w_t)**2, axis=0))
         )
 
         # calculate p value
@@ -4166,6 +4163,7 @@ def alexandergovern(*samples, nan_policy='propagate', axis=0):
     weights = inv_sq_se / np.sum(inv_sq_se, axis=0, keepdims=True)
 
     # (3) determine variance-weighted estimate of the common mean
+    # Consider replacing with vecdot when data-apis/array-api#910 is resolved
     var_w = np.sum(weights * means, axis=0, keepdims=True)
 
     # (4) determine one-sample t statistic for each group
@@ -4185,7 +4183,7 @@ def alexandergovern(*samples, nan_policy='propagate', axis=0):
           (b**2*10 + 8*b*c**4 + 1000*b)))
 
     # (9) calculate statistic
-    A = np.sum(z**2, axis=0)
+    A = np_vecdot(z, z, axis=0)
 
     # "[the p value is determined from] central chi-square random deviates
     # with k - 1 degrees of freedom". Alexander, Govern (94)
@@ -8858,9 +8856,11 @@ def brunnermunzel(x, y, alternative="two-sided", distribution="t",
     rankx_mean = np.mean(rankx)
     ranky_mean = np.mean(ranky)
 
-    Sx = np.sum(np.power(rankcx - rankx - rankcx_mean + rankx_mean, 2.0))
+    temp_x = rankcx - rankx - rankcx_mean + rankx_mean
+    Sx = np_vecdot(temp_x, temp_x)
     Sx /= nx - 1
-    Sy = np.sum(np.power(rankcy - ranky - rankcy_mean + ranky_mean, 2.0))
+    temp_y = rankcy - ranky - rankcy_mean + ranky_mean
+    Sy = np_vecdot(temp_y, temp_y)
     Sy /= ny - 1
 
     wbfn = nx * ny * (rankcy_mean - rankcx_mean)
@@ -9054,8 +9054,7 @@ def combine_pvalues(pvalues, method='fisher', weights=None, *, axis=0):
 
         norm = _SimpleNormal()
         Zi = norm.isf(pvalues)
-        # could use `einsum` or clever `matmul` for performance,
-        # but this is the most readable
+        # Consider `vecdot` when data-apis/array-api#910 is resolved
         statistic = (xp.sum(weights * Zi, axis=axis)
                      / xp_vector_norm(weights, axis=axis))
         pval = _get_pvalue(statistic, norm, alternative="greater", xp=xp)
@@ -9478,8 +9477,8 @@ def quantile_test(x, *, q=0, p=0.5, alternative='two-sided'):
     # "We will use two test statistics in this test. Let T1 equal "
     # "the number of observations less than or equal to x*, and "
     # "let T2 equal the number of observations less than x*."
-    T1 = (X <= x_star).sum()
-    T2 = (X < x_star).sum()
+    T1 = np.count_nonzero(X <= x_star)
+    T2 = np.count_nonzero(X < x_star)
 
     # "The null distribution of the test statistics T1 and T2 is "
     # "the binomial distribution, with parameters n = sample size, and "
@@ -9997,11 +9996,10 @@ def _cdf_distance(p, u_values, v_values, u_weights=None, v_weights=None):
     # If p = 1 or p = 2, we avoid using np.power, which introduces an overhead
     # of about 15%.
     if p == 1:
-        return np.sum(np.multiply(np.abs(u_cdf - v_cdf), deltas))
+        return np_vecdot(np.abs(u_cdf - v_cdf), deltas)
     if p == 2:
-        return np.sqrt(np.sum(np.multiply(np.square(u_cdf - v_cdf), deltas)))
-    return np.power(np.sum(np.multiply(np.power(np.abs(u_cdf - v_cdf), p),
-                                       deltas)), 1/p)
+        return np.sqrt(np_vecdot(np.square(u_cdf - v_cdf), deltas))
+    return np.power(np_vecdot(np.power(np.abs(u_cdf - v_cdf), p), deltas), 1/p)
 
 
 def _validate_distribution(values, weights):
@@ -10120,7 +10118,7 @@ def _sum_of_squares(a, axis=0):
 
     """
     a, axis = _chk_asarray(a, axis)
-    return np.sum(a*a, axis)
+    return np_vecdot(a, a, axis=axis)
 
 
 def _square_of_sums(a, axis=0):
@@ -10503,7 +10501,7 @@ def _br(x, *, r=0):
     x = np.triu(x)
     j = np.arange(n, dtype=x.dtype)
     n = np.asarray(n, dtype=x.dtype)[()]
-    return (np.sum(special.binom(j, r[:, np.newaxis])*x, axis=-1)
+    return (np_vecdot(special.binom(j, r[:, np.newaxis]), x, axis=-1)
             / special.binom(n-1, r) / n)
 
 
@@ -10593,7 +10591,7 @@ def lmoment(sample, order=None, *, axis=0, sorted=False, standardize=True):
     n = sample.shape[-1]
     bk[..., n:] = 0  # remove NaNs due to n_moments > n
 
-    lmoms = np.sum(prk * bk, axis=-1)
+    lmoms = np_vecdot(prk, bk, axis=-1)
     if standardize and n_moments > 2:
         lmoms[2:] /= lmoms[1]
 
@@ -10917,6 +10915,7 @@ def _xp_mean(x, /, *, axis=None, weights=None, keepdims=False, nan_policy='propa
     if weights is None:
         return xp.mean(x, axis=axis, keepdims=keepdims)
 
+    # consider using `vecdot` if `axis` tuple support is added (data-apis/array-api#910)
     norm = xp.sum(weights, axis=axis)
     wsum = xp.sum(x * weights, axis=axis)
     with np.errstate(divide='ignore', invalid='ignore'):
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/stats/tests/test_stats.py b/scipy/stats/tests/test_stats.py
index 18457e03eafb736c7b0b0c1cd592b47e1e53e9da..54d7887f4a8892a25f65dfca92ce3e3dfee53c58 100644
--- a/scipy/stats/tests/test_stats.py
+++ b/scipy/stats/tests/test_stats.py
@@ -7941,13 +7941,10 @@ class TestFOneWay:
 
     def test_known_exact(self):
         # Another trivial dataset for which the exact F and p can be
-        # calculated.
+        # calculated on most platforms
         F, p = stats.f_oneway([2], [2], [2, 3, 4])
-        # The use of assert_equal might be too optimistic, but the calculation
-        # in this case is trivial enough that it is likely to go through with
-        # no loss of precision.
-        assert_equal(F, 3/5)
-        assert_equal(p, 5/8)
+        assert_allclose(F, 3/5, rtol=1e-15)  # assert_equal fails on some CI platforms
+        assert_allclose(p, 5/8, rtol=1e-15)
 
     def test_large_integer_array(self):
         a = np.array([655, 788], dtype=np.uint16)
```

## Validation

```json
{
 "test_files": [
  "scipy/stats/tests/test_stats.py"
 ],
 "collected_before": 1223,
 "collected_after": 1223,
 "outcomes_before": {
  "PASSED": 1205,
  "SKIPPED": 15,
  "XFAIL": 3
 },
 "outcomes_after": {
  "PASSED": 1205,
  "SKIPPED": 15,
  "XFAIL": 3
 },
 "exit_before": 0,
 "exit_after": 0,
 "tail_before": "var_basic[numpy-omit-1-True--1]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-True-axis3]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_special_cases[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_nan_policy[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_empty[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_dtype[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_integer[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_complex_gh22404[numpy]\nPASSED scipy/stats/tests/test_stats.py::test_chk_asarray[numpy]\nSKIPPED [12] scipy/conftest.py:72: very slow test; set environment variable SCIPY_XSLOW=1 to run it\nSKIPPED [2] scipy/stats/tests/test_stats.py:6552: `alternative` not available for `normaltest`\nSKIPPED [1] scipy/stats/tests/test_stats.py:9715: These parameters *are* compatible with NumPy\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-True-two-sided] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-True-less] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-True-greater] - reason: Discrepancy in `main`; needs further investigation.\n================= 1199 passed, 15 skipped, 3 xfailed in 36.10s =================",
 "tail_after": "var_basic[numpy-omit-1-True--1]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[numpy-omit-1-True-axis3]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_special_cases[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_nan_policy[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_empty[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_dtype[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_integer[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_complex_gh22404[numpy]\nPASSED scipy/stats/tests/test_stats.py::test_chk_asarray[numpy]\nSKIPPED [12] scipy/conftest.py:72: very slow test; set environment variable SCIPY_XSLOW=1 to run it\nSKIPPED [2] scipy/stats/tests/test_stats.py:6552: `alternative` not available for `normaltest`\nSKIPPED [1] scipy/stats/tests/test_stats.py:9715: These parameters *are* compatible with NumPy\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-True-two-sided] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-True-less] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[numpy-0.2-True-greater] - reason: Discrepancy in `main`; needs further investigation.\n================= 1199 passed, 15 skipped, 3 xfailed in 34.96s =================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

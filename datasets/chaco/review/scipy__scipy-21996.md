# scipy__scipy-21996

[back to the list](README.md) -- **ENH: `stats.fisher_exact`: extend to `R x C` tables**

| field | value |
|---|---|
| pull request | [scipy/scipy#21996](https://github.com/scipy/scipy/pull/21996) (created 2024-12-04, merged 2024-12-05) |
| ChaCo lists | full, ablation |
| status | **runnable** -- 4 developer test(s) flip; oracle reproduces it |
| base commit | [`3c7071929278`](https://github.com/scipy/scipy/commit/3c707192927890207f719b887543640d3f6f3fdc) (2024-12-05), first parent of the merge commit |
| merge commit | [`b658ecc2d59a`](https://github.com/scipy/scipy/commit/b658ecc2d59a338c6ad4a2c489de905349a267bc) |
| issues closed | none |
| version | 1.15 |
| image | `f2p-chaco/scipy__scipy-21996:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-21996.Dockerfile) |
| source files (`patch`) | `scipy/stats/_stats_py.py`, `scipy/stats/contingency.py` |
| test files (`test_patch`) | `scipy/stats/tests/test_stats.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (4)

- `scipy/stats/tests/test_stats.py::TestFisherExact::test_input_validation_edge_cases_rxc`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_raises`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_resampling_2x2`
- `scipy/stats/tests/test_stats.py::TestFisherExact::test_resampling_rxc`

## PASS_TO_PASS (1191)

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
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chiquare_data_types_attributes[1000000-int32-numpy]`
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chiquare_data_types_attributes[200-uint8-numpy]`
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chisquare_12282a[numpy]`
- `scipy/stats/tests/test_stats.py::TestChisquare::test_chisquare_12282b[numpy]`
- `scipy/stats/tests/test_stats.py::TestChisquareMA::test_chisquare_masked_arrays`
- `scipy/stats/tests/test_stats.py::TestChisquareMA::test_deprecation_warning`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[0-fisher-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[0-mudholkar_george-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[0-pearson-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[0-stouffer-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[0-tippett-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[1-fisher-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[1-mudholkar_george-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[1-pearson-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[1-stouffer-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_axis[1-tippett-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[fisher-all-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[fisher-random-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[fisher-single-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[mudholkar_george-all-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[mudholkar_george-random-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[mudholkar_george-single-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[pearson-all-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[pearson-random-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[pearson-single-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[stouffer-all-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[stouffer-random-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[stouffer-single-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[tippett-all-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[tippett-random-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_monotonicity[tippett-single-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[fisher-14.83716180549625-0.02156175132483465-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[mudholkar_george-6.828712071641684-0.01654551838539527-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[pearson--1.179737662212887-0.022126300085691275-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[stouffer-2.131790594240385-0.01651203260896294-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_reference_values[tippett-0.01-0.02970100000000002-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[fisher-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[mudholkar_george-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[pearson-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[stouffer-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_result[tippett-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_weighted_stouffer[weights0-2.131790594240385-0.01651203260896294-numpy]`
- `scipy/stats/tests/test_stats.py::TestCombinePvalues::test_weighted_stouffer[weights1-1.051815015753598-0.1464422142261314-numpy]`
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
- `scipy/stats/tests/test_stats.py::TestGSTD::test_1d_array`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_1d_numeric_array_like_input`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_0`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_1`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_2`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_3d_array_axis_type_tuple`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_ddof_equal_to_number_of_observations`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_masked_3d_array`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_propagates_nan_values`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_raises_value_error_non_numeric_input`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[-1]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[0]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[inf]`
- `scipy/stats/tests/test_stats.py::TestGSTD::test_returns_nan_invalid_value[nan]`
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
- `scipy/stats/tests/test_stats.py::TestJarqueBera::test_jarque_bera_size[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-False--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-False-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-False-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-False-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-True-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-True-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[False-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-False--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-False-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-False-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-False-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-True-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-True-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosis::test_vectorization[True-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_against_R[greater-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_against_R[less-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_against_R[two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_gh9033_regression[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_intuitive[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_kurtosistest_too_few_observations[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestKurtosisTest::test_too_small[numpy]`
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
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[0-1-complex128-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[0-1-float32-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[0-1-float64-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[1-0-complex128-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[1-0-float32-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_constant_moments[1-0-float64-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment[numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_accuracy`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0--1-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0--1-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0--1-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0--1-3-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-0-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-0-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-0-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-0-3-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-1-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-1-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-1-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[0-1-3-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None--1-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None--1-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None--1-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None--1-3-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-0-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-0-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-0-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-0-3-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-1-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-1-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-1-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_array_api[None-1-3-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[0-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[0-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[1-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[1-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[None-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_array_moment[None-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-0-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-0-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-1-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-1-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-None-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[0-None-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-0-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-0-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-1-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-1-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-None-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[1-None-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-0-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-0-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-1-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-1-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-None-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[2-None-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-0-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-0-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-1-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-1-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-None-10-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_center_scalar_moment[3-None-size1-numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_empty_order[numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_moment_propagate_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestMoments::test_nan_policy`
- `scipy/stats/tests/test_stats.py::TestMoments::test_rename_moment_order[numpy]`
- `scipy/stats/tests/test_stats.py::TestNormalTest::test_against_R[two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::TestNormalTest::test_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestNormalTest::test_too_small[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_1d_with_negative_value[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_1d_with_zero[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis0[a0--0.5-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis0[a1-0.5-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis1[a0--0.5-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axis1[a1-0.5-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axisnone[a0--0.5-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_2d_axisnone[a1-0.5-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_bad_exponent[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_1d_list[numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_2d[0-gmean-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_2d[1-hmean--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPMean::test_weights_2d[None-wpmean_reference-9.87654321-numpy]`
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
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[greater-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[greater-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[greater-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[less-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[less-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[less-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[two-sided-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[two-sided-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_array_api[two-sided-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_axis01[0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_axis01[1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_axis_None[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[greater-0.1629000687684--0.6785654158217636-1-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[greater-0.8370999312316--0.985600937290653-1.0--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[less-0.1629000687684--1.0-0.6785654158217636--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[less-0.8370999312316--1-0.985600937290653-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[two-sided-0.325800137536--0.814938968841-0.99230697523-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_basic_example[two-sided-0.325800137536--0.992306975236-0.81493896884--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_bootstrap_ci[greater-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_bootstrap_ci[less-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_bootstrap_ci[two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_constant_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_extremely_large_input_values[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_input_validation[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length3_r_exactly_negative_one[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length_two_constant_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length_two_neg1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_length_two_pos1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_nd_input_validation[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_nd_special_cases[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_near_constant_input[float32-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_near_constant_input[float64-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_negative_correlation_pvalue_gh17795[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_pearsonr_result_attributes[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_r_almost_exactly_neg1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_r_almost_exactly_pos1[numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[monte_carlo-greater-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[monte_carlo-less-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[monte_carlo-two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[monte_carlo2-greater-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[monte_carlo2-less-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[monte_carlo2-two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[permutation-greater-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[permutation-less-numpy]`
- `scipy/stats/tests/test_stats.py::TestPearsonr::test_resampling_pvalue[permutation-two-sided-numpy]`
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
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat0-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat0-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat0-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat0-case3-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat1-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat1-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat1-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat1-case3-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat2-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat2-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat2-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat2-case3-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat3-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat3-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat3-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat3-case3-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat4-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat4-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat4-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat4-case3-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat5-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat5-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat5-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat5-case3-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat6-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat6-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat6-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_basic[lambda_stat6-case3-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_ddof_broadcasting[numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat0-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat0-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat0-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat1-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat1-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat1-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat2-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat2-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat2-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat3-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat3-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat3-case2-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat4-case0-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat4-case1-numpy]`
- `scipy/stats/tests/test_stats.py::TestPowerDivergence::test_empty_cases[lambda_stat4-case2-numpy]`
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
- `scipy/stats/tests/test_stats.py::TestRegression::test_one_arg_deprecation`
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
- `scipy/stats/tests/test_stats.py::TestSkew::test_empty_1d[kurtosis-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_empty_1d[skew-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_nan_policy`
- `scipy/stats/tests/test_stats.py::TestSkew::test_precision_loss_gh15554[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skew_constant_value[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skew_propagate_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skewness[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_skewness_scalar`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[False--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[False-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[False-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[False-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[True-0-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[True-2-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkew::test_vectorization[True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_against_R[greater-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_against_R[less-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_against_R[two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_intuitive[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_skewtest_too_few_observations[numpy]`
- `scipy/stats/tests/test_stats.py::TestSkewTest::test_too_small[numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_alternative[numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[greater-numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[less-numpy]`
- `scipy/stats/tests/test_stats.py::TestStudentTest::test_1samp_ci_1d[two-sided-numpy]`
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
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_dtype[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_empty[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_integer[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_nan_policy[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_non_broadcastable[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_special_cases[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-None--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-None-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-None-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-None-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-True-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[False-True-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-None--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-None-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-None-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-None-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-True-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Mean::test_xp_mean_basic[True-True-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_dtype[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_empty[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_integer[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_nan_policy[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_special_cases[numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-False--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-False-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-False-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-False-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-True-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-0-True-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-False--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-False-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-False-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-False-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-True-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-True-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-False--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-False-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-False-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-False-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-True-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-0-True-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-False--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-False-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-False-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-False-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-True--1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-True-1-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-True-None-numpy]`
- `scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[propagate-1-True-axis3-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_degenerate_input[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_gzscore_masked_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_gzscore_normal_array[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap[x0-y0-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap[x1-y1-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_axis[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_ddof[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit[0-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit[2-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit_with_axis[0-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_omit_with_axis[2-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zmap_nan_policy_raise[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_2d_all_nan[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_2d_all_nan_row[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_axis[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_1d[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_2d[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_constant_input_2d_nan_policy_omit[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_ddof[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_empty_input[x0-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_empty_input[x1-numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_masked_element_0_gh19039[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_omit[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_omit_with_ddof[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_propagate[numpy]`
- `scipy/stats/tests/test_stats.py::TestZmapZscore::test_zscore_nan_raise[numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-False-greater-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-False-less-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-False-two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-True-greater-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-True-less-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0-True-two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-False-greater-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-False-less-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-False-two-sided-numpy]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[-1-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-basic]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-permutations]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_common::test_nans_on_axis[0-trim]`
- `scipy/stats/tests/test_stats.py::Test_ttest_ind_permutations::test_permutation_not_implement_for_xp[numpy]`
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
- `scipy/stats/tests/test_stats.py::test_ttest_ind_axis_size_zero[b0-expected_shape0-numpy]`
- `scipy/stats/tests/test_stats.py::test_ttest_ind_axis_size_zero[b1-expected_shape1-numpy]`
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

```text
Pull request #21996: ENH: `stats.fisher_exact`: extend to `R x C` tables

#### Reference issue
Follow-up to gh-20989, gh-15618
Closes gh-7099

#### What does this implement/fix?
This extends `fisher_exact` to two-dimensional tables with shapes other than `(2, 2)`. As the notes of `fisher_exact` already explained, there is more than one choice of statistic associated with Fisher's exact test; here, we use the PMF of [`scipy.stats.random_table`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.random_table.html) (with the marginals of the observed table) as the statistic. The p-value - the percentage of tables with the observed marginals that produce a statistic at least as extreme (small) as the observed table - is determined via either a permutation or Monte Carlo approach. Although the two approaches are exactly equivalent in this case, both may be valuable: the Monte Carlo approach is much faster because it uses `scipy.stats.random_table` to sample the tables, but the permutation approach *can* perform a deterministic exact test for sufficiently small tables. Both approaches are exact or almost exact in a long-run sense.

#### Additional information
I'll need to check the behavior for 1 x C and R x 1 tables and maybe add some edge case handling for those.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/stats/_stats_py.py b/scipy/stats/_stats_py.py
index f4d78f4efa36615d5d250c313d6a599ebaa070e1..1b766051267302e5e31455c57e4e5b5cb855c77e 100644
--- a/scipy/stats/_stats_py.py
+++ b/scipy/stats/_stats_py.py
@@ -4670,26 +4670,39 @@ def pearsonr(x, y, *, alternative='two-sided', method=None, axis=0):
                           alternative=alternative, x=x, y=y, axis=axis)
 
 
-def fisher_exact(table, alternative='two-sided'):
-    """Perform a Fisher exact test on a 2x2 contingency table.
+def fisher_exact(table, alternative=None, *, method=None):
+    """Perform a Fisher exact test on a contingency table.
 
-    The null hypothesis is that the true odds ratio of the populations
+    For a 2x2 table,
+    the null hypothesis is that the true odds ratio of the populations
     underlying the observations is one, and the observations were sampled
     from these populations under a condition: the marginals of the
-    resulting table must equal those of the observed table. The statistic
-    returned is the unconditional maximum likelihood estimate of the odds
+    resulting table must equal those of the observed table.
+    The statistic is the unconditional maximum likelihood estimate of the odds
     ratio, and the p-value is the probability under the null hypothesis of
     obtaining a table at least as extreme as the one that was actually
-    observed. There are other possible choices of statistic and two-sided
+    observed.
+
+    For other table sizes, or if `method` is provided, the null hypothesis
+    is that the rows and columns of the tables have fixed sums and are
+    independent; i.e., the table was sampled from a `scipy.stats.random_table`
+    distribution with the observed marginals. The statistic is the
+    probability mass of this distribution evaluated at `table`, and the
+    p-value is the percentage of the population of tables with statistic at
+    least as extreme (small) as that of `table`. There is only one alternative
+    hypothesis available: the rows and columns are not independent.
+
+    There are other possible choices of statistic and two-sided
     p-value definition associated with Fisher's exact test; please see the
     Notes for more information.
 
     Parameters
     ----------
     table : array_like of ints
-        A 2x2 contingency table.  Elements must be non-negative integers.
+        A contingency table.  Elements must be non-negative integers.
     alternative : {'two-sided', 'less', 'greater'}, optional
-        Defines the alternative hypothesis.
+        Defines the alternative hypothesis for 2x2 tables; unused for other
+        table sizes.
         The following options are available (default is 'two-sided'):
 
         * 'two-sided': the odds ratio of the underlying population is not one
@@ -4699,13 +4712,29 @@ def fisher_exact(table, alternative='two-sided'):
 
         See the Notes for more details.
 
+    method : ResamplingMethod, optional
+        Defines the method used to compute the p-value.
+        If `method` is an instance of `PermutationMethod`/`MonteCarloMethod`,
+        the p-value is computed using
+        `scipy.stats.permutation_test`/`scipy.stats.monte_carlo_test` with the
+        provided configuration options and other appropriate settings.
+        Note that if `method` is an instance of `MonteCarloMethod`, the ``rvs``
+        attribute must be left unspecified; Monte Carlo samples are always drawn
+        using the ``rvs`` method of `scipy.stats.random_table`.
+        Otherwise, the p-value is computed as documented in the notes.
+
+        .. versionadded:: 1.15.0
+
     Returns
     -------
     res : SignificanceResult
         An object containing attributes:
 
         statistic : float
-            This is the prior odds ratio, not a posterior estimate.
+            For a 2x2 table with default `method`, this is the odds ratio - the
+            prior odds ratio not a posterior estimate. In all other cases, this
+            is the probability density of obtaining the observed table under the
+            null hypothesis of independence with marginals fixed.
         pvalue : float
             The probability under the null hypothesis of obtaining a
             table at least as extreme as the one that was actually observed.
@@ -4713,7 +4742,7 @@ def fisher_exact(table, alternative='two-sided'):
     Raises
     ------
     ValueError
-        If `table` is not a 2x2 contingency table with non-negative entries.
+        If `table` is not two-dimensional or has negative entries.
 
     See Also
     --------
@@ -4846,17 +4875,32 @@ def fisher_exact(table, alternative='two-sided'):
     >>> res.pvalue
     0.034965034965034975
 
+    For tables with shape other than ``(2, 2)``, provide an instance of
+    `scipy.stats.MonteCarloMethod` or `scipy.stats.PermutationMethod` for the
+    `method` parameter:
+
+    >>> import numpy as np
+    >>> from scipy.stats import MonteCarloMethod
+    >>> rng = np.random.default_rng(4507195762371367)
+    >>> method = MonteCarloMethod(rng=rng)
+    >>> fisher_exact([[8, 2, 3], [1, 5, 4]], method=method)
+    SignificanceResult(statistic=np.float64(0.005782), pvalue=np.float64(0.0603))
+
     For a more detailed example, see :ref:`hypothesis_fisher_exact`.
     """
     hypergeom = distributions.hypergeom
     # int32 is not enough for the algorithm
     c = np.asarray(table, dtype=np.int64)
-    if not c.shape == (2, 2):
-        raise ValueError("The input `table` must be of shape (2, 2).")
+    if not c.ndim == 2:
+        raise ValueError("The input `table` must have two dimensions.")
 
     if np.any(c < 0):
         raise ValueError("All values in `table` must be nonnegative.")
 
+    if not c.shape == (2, 2) or method is not None:
+        return _fisher_exact_rxc(c, alternative, method)
+    alternative = 'two-sided' if alternative is None else alternative
+
     if 0 in c.sum(axis=0) or 0 in c.sum(axis=1):
         # If both values in a row or column are zero, the p-value is 1 and
         # the odds ratio is NaN.
@@ -4913,6 +4957,98 @@ def fisher_exact(table, alternative='two-sided'):
     return SignificanceResult(oddsratio, pvalue)
 
 
+def _fisher_exact_rxc(table, alternative, method):
+    if alternative is not None:
+        message = ('`alternative` must be the default (None) unless '
+                  '`table` has shape `(2, 2)` and `method is None`.')
+        raise ValueError(message)
+
+    if table.size == 0:
+        raise ValueError("`table` must have at least one row and one column.")
+
+    if table.shape[0] == 1 or table.shape[1] == 1 or np.all(table == 0):
+        # Only one such table with those marginals
+        return SignificanceResult(1.0, 1.0)
+
+    if method is None:
+        method = stats.MonteCarloMethod()
+
+    if isinstance(method, stats.PermutationMethod):
+        res = _fisher_exact_permutation_method(table, method)
+    elif isinstance(method, stats.MonteCarloMethod):
+        res = _fisher_exact_monte_carlo_method(table, method)
+    else:
+        message = (f'`{method=}` not recognized; if provided, `method` must be an '
+                   'instance of `PermutationMethod` or `MonteCarloMethod`.')
+        raise ValueError(message)
+
+    return SignificanceResult(np.clip(res.statistic, None, 1.0), res.pvalue)
+
+
+def _fisher_exact_permutation_method(table, method):
+    x, y = _untabulate(table)
+    colsums = np.sum(table, axis=0)
+    rowsums = np.sum(table, axis=1)
+    X = stats.random_table(rowsums, colsums)
+
+    # `permutation_test` with `permutation_type='pairings' permutes the order of `x`,
+    # which pairs observations in `x` with different observations in `y`.
+    def statistic(x):
+        # crosstab the resample and compute the statistic
+        table = stats.contingency.crosstab(x, y)[1]
+        return X.pmf(table)
+
+    # tables with *smaller* probability mass are considered to be more extreme
+    return stats.permutation_test((x,), statistic, permutation_type='pairings',
+                                  alternative='less', **method._asdict())
+
+
+def _fisher_exact_monte_carlo_method(table, method):
+    method = method._asdict()
+
+    if method.pop('rvs', None) is not None:
+        message = ('If the `method` argument of `fisher_exact` is an '
+                   'instance of `MonteCarloMethod`, its `rvs` attribute '
+                   'must be unspecified. Use the `MonteCarloMethod` `rng` argument '
+                   'to control the random state.')
+        raise ValueError(message)
+    rng = np.random.default_rng(method.pop('rng', None))
+
+    # `random_table.rvs` produces random contingency tables with the given marginals
+    # under the null hypothesis of independence
+    shape = table.shape
+    colsums = np.sum(table, axis=0)
+    rowsums = np.sum(table, axis=1)
+    totsum = np.sum(table)
+    X = stats.random_table(rowsums, colsums, seed=rng)
+
+    def rvs(size):
+        n_resamples = size[0]
+        return X.rvs(size=n_resamples).reshape(size)
+
+    # axis signals to `monte_carlo_test` that statistic is vectorized, but we know
+    # how it will pass the table(s), so we don't need to use `axis` explicitly.
+    def statistic(table, axis):
+        shape_ = (-1,) + shape if table.size > totsum else shape
+        return X.pmf(table.reshape(shape_))
+
+    # tables with *smaller* probability mass are considered to be more extreme
+    return stats.monte_carlo_test(table.ravel(), rvs, statistic,
+                                  alternative='less', **method)
+
+
+def _untabulate(table):
+    # converts a contingency table to paired samples indicating the
+    # correspondence between row and column indices
+    r, c = table.shape
+    x, y = [], []
+    for i in range(r):
+        for j in range(c):
+            x.append([i] * table[i, j])
+            y.append([j] * table[i, j])
+    return np.concatenate(x), np.concatenate(y)
+
+
 def spearmanr(a, b=None, axis=0, nan_policy='propagate',
               alternative='two-sided'):
     r"""Calculate a Spearman correlation coefficient with associated p-value.
diff --git a/scipy/stats/contingency.py b/scipy/stats/contingency.py
index 270fd8ae6d171c5ac9f78d76c1037714638d9b98..809df62e3cdaa2887fab2164afbe01e496ac6315 100644
--- a/scipy/stats/contingency.py
+++ b/scipy/stats/contingency.py
@@ -24,7 +24,7 @@ Functions for creating and analyzing contingency tables.
 from functools import reduce
 import math
 import numpy as np
-from ._stats_py import power_divergence
+from ._stats_py import power_divergence, _untabulate
 from ._relative_risk import relative_risk
 from ._crosstab import crosstab
 from ._odds_ratio import odds_ratio
@@ -178,6 +178,9 @@ def chi2_contingency(observed, correction=True, lambda_=None, *, method=None):
         `scipy.stats.permutation_test`/`scipy.stats.monte_carlo_test` with the
         provided configuration options and other appropriate settings.
         Otherwise, the p-value is computed as documented in the notes.
+        Note that if `method` is an instance of `MonteCarloMethod`, the ``rvs``
+        attribute must be left unspecified; Monte Carlo samples are always drawn
+        using the ``rvs`` method of `scipy.stats.random_table`.
 
         .. versionadded:: 1.15.0
 
@@ -375,18 +378,6 @@ def _chi2_resampling_methods(observed, expected, correction, lambda_, method):
     return Chi2ContingencyResult(res.statistic, res.pvalue, np.nan, expected)
 
 
-def _untabulate(table):
-    # converts a contingency table to paired samples indicating the
-    # correspondence between row and column indices
-    r, c = table.shape
-    x, y = [], []
-    for i in range(r):
-        for j in range(c):
-            x.append([i] * table[i, j])
-            y.append([j] * table[i, j])
-    return np.concatenate(x), np.concatenate(y)
-
-
 def _chi2_permutation_method(observed, expected, method):
     x, y = _untabulate(observed)
     # `permutation_test` with `permutation_type='pairings' permutes the order of `x`,
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/stats/tests/test_stats.py b/scipy/stats/tests/test_stats.py
index eada574af2431d5e8a35dee15d214a9e68e29d48..db1a9341a7d525c96019bff60d37ae7d1402a34d 100644
--- a/scipy/stats/tests/test_stats.py
+++ b/scipy/stats/tests/test_stats.py
@@ -886,9 +886,10 @@ class TestFisherExact:
         assert_approx_equal(res, 0.2751, significant=4)
 
     def test_raises(self):
-        # test we raise an error for wrong shape of input.
-        assert_raises(ValueError, stats.fisher_exact,
-                      np.arange(6).reshape(2, 3))
+        # test we raise an error for wrong number of dimensions.
+        message = "The input `table` must have two dimensions."
+        with pytest.raises(ValueError, match=message):
+            stats.fisher_exact(np.arange(6))
 
     def test_row_or_col_zero(self):
         tables = ([[0, 0], [5, 10]],
@@ -945,6 +946,102 @@ class TestFisherExact:
         res = stats.fisher_exact(table, alternative=alternative)
         assert_equal((res.statistic, res.pvalue), res)
 
+    def test_input_validation_edge_cases_rxc(self):
+        rng = np.random.default_rng(2345783457834572345)
+        table = np.asarray([[2, 7], [8, 2]])
+
+        message = r"`alternative` must be the default \(None\) unless..."
+        with pytest.raises(ValueError, match=message):
+            method = stats.PermutationMethod(rng=rng)
+            stats.fisher_exact(table, method=method, alternative='less')
+
+        message = "...not recognized; if provided, `method` must be an..."
+        with pytest.raises(ValueError, match=message):
+            method = stats.BootstrapMethod(rng=rng)
+            stats.fisher_exact(table, method=method)
+
+        message = "If the `method` argument of `fisher_exact` is an..."
+        with pytest.raises(ValueError, match=message):
+            method = stats.MonteCarloMethod(rvs=stats.norm.rvs)
+            stats.fisher_exact(table, method=method)
+
+        message = "`table` must have at least one row and one column."
+        with pytest.raises(ValueError, match=message):
+            stats.fisher_exact(np.zeros((0, 1)))
+
+        # Specical case: when there is only one table with given marginals, the
+        # PMF of that case is 1.0, so the p-value is 1.0
+        np.testing.assert_equal(stats.fisher_exact([[1, 2, 3]]), (1, 1))
+        np.testing.assert_equal(stats.fisher_exact([[1], [2], [3]]), (1, 1))
+        np.testing.assert_equal(stats.fisher_exact(np.zeros((2, 3))), (1, 1))
+
+
+
+    @pytest.mark.fail_slow(10)
+    @pytest.mark.slow()
+    def test_resampling_2x2(self):
+        rng = np.random.default_rng(2345783457834572345)
+        table = np.asarray([[2, 7], [8, 2]])
+        ref = stats.fisher_exact(table)
+        ref_pvalue = ref.pvalue
+        ref_stat = stats.random_table(table.sum(axis=1), table.sum(axis=0)).pmf(table)
+
+        method = stats.MonteCarloMethod(rng=rng)
+        res = stats.fisher_exact(table, method=method)
+        assert_allclose(res.pvalue, ref_pvalue, atol=0.0025)
+        assert_equal(res.statistic, ref_stat)
+
+        method = stats.PermutationMethod(rng=rng)
+        res = stats.fisher_exact(table, method=method)
+        assert_allclose(res.pvalue, ref.pvalue, atol=0.0025)
+        assert_equal(res.statistic, ref_stat)
+
+    @pytest.mark.fail_slow(10)
+    @pytest.mark.slow()
+    def test_resampling_rxc(self):
+        # Compare against R fisher.exact
+        # options(digits=16)
+        # MP6 < - rbind(
+        #     c(1, 2, 2, 1, 1, 0, 1),
+        #     c(2, 0, 0, 2, 3, 0, 0),
+        #     c(0, 1, 1, 1, 2, 7, 3),
+        #     c(1, 1, 2, 0, 0, 0, 1),
+        #     c(0, 1, 1, 1, 1, 0, 0))
+        # fisher.test(MP6)
+
+        table = [[1, 2, 2, 1, 1, 0, 1],
+                 [2, 0, 0, 2, 3, 0, 0],
+                 [0, 1, 1, 1, 2, 7, 3],
+                 [1, 1, 2, 0, 0, 0, 1],
+                 [0, 1, 1, 1, 1, 0, 0]]
+        table = np.asarray(table)
+
+        ref_pvalue = 0.03928964365533
+        rng = np.random.default_rng(3928964365533)
+
+        method = stats.PermutationMethod(rng=rng)
+        res = stats.fisher_exact(table, method=method)
+        assert_allclose(res.pvalue, ref_pvalue, atol=5e-4)
+
+        method = stats.MonteCarloMethod(rng=rng, n_resamples=99999)
+        res = stats.fisher_exact(table, method=method)
+        assert_allclose(res.pvalue, ref_pvalue, atol=5e-4)
+
+    @pytest.mark.xslow()
+    def test_resampling_exact_2x2(self):
+        # Test that exact permutation p-value matches result of `fisher_exact`
+        rng = np.random.default_rng(2345783457834572345)
+        method = stats.PermutationMethod(rng=rng)
+
+        for a in range(1, 3):
+            for b in range(1, 3):
+                for c in range(1, 3):
+                    for d in range(1, 4):
+                        table = np.asarray([[a, b], [c, d]])
+                        ref = stats.fisher_exact(table)
+                        res = stats.fisher_exact(table, method=method)
+                        assert_allclose(res.pvalue, ref.pvalue, atol=1e-14)
+
 
 class TestCorrSpearmanr:
     """ W.II.D. Compute a correlation matrix on all the variables.
```

## Validation

```json
{
 "test_files": [
  "scipy/stats/tests/test_stats.py"
 ],
 "collected_before": 1213,
 "collected_after": 1213,
 "outcomes_before": {
  "PASSED": 1191,
  "FAILED": 4,
  "SKIPPED": 15,
  "XFAIL": 3
 },
 "outcomes_after": {
  "PASSED": 1195,
  "SKIPPED": 15,
  "XFAIL": 3
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "XP_Var::test_nan_policy[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_empty[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_dtype[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_integer[numpy]\nPASSED scipy/stats/tests/test_stats.py::test_chk_asarray[numpy]\nSKIPPED [12] scipy/conftest.py:81: very slow test; set environment variable SCIPY_XSLOW=1 to run it\nSKIPPED [2] scipy/stats/tests/test_stats.py:6608: `alternative` not available for `normaltest`\nSKIPPED [1] scipy/stats/tests/test_stats.py:9724: These parameters *are* compatible with NumPy\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-two-sided-numpy] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-less-numpy] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-greater-numpy] - reason: Discrepancy in `main`; needs further investigation.\nFAILED scipy/stats/tests/test_stats.py::TestFisherExact::test_raises - Assert...\nFAILED scipy/stats/tests/test_stats.py::TestFisherExact::test_input_validation_edge_cases_rxc\nFAILED scipy/stats/tests/test_stats.py::TestFisherExact::test_resampling_2x2\nFAILED scipy/stats/tests/test_stats.py::TestFisherExact::test_resampling_rxc\n============ 4 failed, 1185 passed, 15 skipped, 3 xfailed in 35.21s ============",
 "tail_after": "mit-1-True-1-numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-True--1-numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_xp_var_basic[omit-1-True-axis3-numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_special_cases[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_nan_policy[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_empty[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_dtype[numpy]\nPASSED scipy/stats/tests/test_stats.py::TestXP_Var::test_integer[numpy]\nPASSED scipy/stats/tests/test_stats.py::test_chk_asarray[numpy]\nSKIPPED [12] scipy/conftest.py:81: very slow test; set environment variable SCIPY_XSLOW=1 to run it\nSKIPPED [2] scipy/stats/tests/test_stats.py:6608: `alternative` not available for `normaltest`\nSKIPPED [1] scipy/stats/tests/test_stats.py:9724: These parameters *are* compatible with NumPy\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-two-sided-numpy] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-less-numpy] - reason: Discrepancy in `main`; needs further investigation.\nXFAIL scipy/stats/tests/test_stats.py::Test_ttest_CI::test_confidence_interval[0.2-True-greater-numpy] - reason: Discrepancy in `main`; needs further investigation.\n================= 1189 passed, 15 skipped, 3 xfailed in 37.42s =================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

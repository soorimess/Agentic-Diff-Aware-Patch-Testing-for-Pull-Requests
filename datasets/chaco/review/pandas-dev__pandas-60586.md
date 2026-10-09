# pandas-dev__pandas-60586

[back to the list](README.md) -- **Backport PR #60584 on branch 2.3.x (TST: Address matplotlib 3.10 deprecation of vert=)**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#60586](https://github.com/pandas-dev/pandas/pull/60586) (created 2024-12-17, merged 2024-12-18) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 3 developer test(s) flip; oracle reproduces it |
| base commit | [`3362822db000`](https://github.com/pandas-dev/pandas/commit/3362822db00076222d3875a86b5f5625799d8862) (2024-12-17), first parent of the merge commit |
| merge commit | [`eb22bf8f9c19`](https://github.com/pandas-dev/pandas/commit/eb22bf8f9c194a96b6d7583504ab7ca217238881) |
| issues closed | none |
| version | 2.3 |
| image | `f2p-chaco/pandas-dev__pandas-60586:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-60586.Dockerfile) |
| source files (`patch`) | `pandas/plotting/_matplotlib/boxplot.py`, `pandas/plotting/_matplotlib/tools.py` |
| test files (`test_patch`) | `pandas/tests/plotting/frame/test_frame.py`, `pandas/tests/plotting/test_boxplot_method.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (3)

- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_group_xlabel_ylabel[vert0]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_xlabel_ylabel[vert0]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_plot_xlabel_ylabel[vert0]`

## PASS_TO_PASS (427)

<details><summary>show</summary>

- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[box]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[density]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[hist]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[kde]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_all_invalid_plot_data[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_area_lim[False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_area_lim[True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_area_sharey_dont_overwrite`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bad_label`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_barwidth[False-bar-get_width]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_barwidth[False-barh-get_height]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_barwidth[True-bar-get_width]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_barwidth[True-barh-get_height]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_bottom_left_bottom`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_bottom_left_left`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_bottom_left_subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_categorical[CategoricalIndex]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_categorical[Index]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_linewidth[False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_linewidth[True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_linewidth_subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_nan`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_bar_nan_stacked`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_barh_barwidth_subplots[bar-get_width]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_barh_barwidth_subplots[barh-get_height]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_return_type_invalid`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_return_type_invalid_type[axes]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_return_type_invalid_type[both]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_return_type_invalid_type[dict]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_series`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_series_positions`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_df_grid_settings`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_df_gridspec_patterns_boxed`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_df_gridspec_patterns_vert_horiz`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_donot_overwrite_index_name`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_asymmetrical`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot[kwargs0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot[kwargs1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot[kwargs2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_bar`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_column_name[\u8aa4\u5dee]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_column_name[yerr]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr[y_err0-bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr[y_err0-barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr[y_err0-line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr[y_err1-bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr[y_err1-barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr[y_err1-line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[0.2-0.2-bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[0.2-0.2-barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[0.2-0.2-line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[y_err0-x_err0-bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[y_err0-x_err0-barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[y_err0-x_err0-line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[y_err1-x_err1-bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[y_err1-x_err1-barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr[y_err1-x_err1-line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr_subplots[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr_subplots[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_different_yerr_xerr_subplots[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_external_typeerror`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_external_valueerror`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_yerr_array`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_scatter`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_scatter_color`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_timeseries[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_timeseries[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_timeseries[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_with_integer_column_names`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_with_partial_columns_box[<lambda>]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_with_partial_columns_box[DataFrame]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_with_partial_columns_dti`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_with_partial_columns_kind[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_with_partial_columns_kind[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[density]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[hist]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[kde]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot[pie]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[123-subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[123-subplots should be a bool or an iterable]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[a-each`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[a-each entry should be a list/tuple]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[subplots2-each`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[subplots2-each entry should be a list/tuple]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[subplots3-each`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_bad_input[subplots3-each entry should be a list/tuple]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_duplicated_column`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_invalid_column_name`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_invalid_kind[box]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_invalid_kind[hexbin]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_invalid_kind[scatter]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_multiindex_notimplemented`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_nonunique_cols_notimplemented`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_group_subplot_series_notimplemented`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hexbin_basic`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hexbin_basic_subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hexbin_cmap[kwargs0-BuGn]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hexbin_cmap[kwargs1-cubehelix]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hexbin_cmap[kwargs2-YlGn]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hexbin_with_c[None]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hexbin_with_c[std]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_df`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_df_coord[data0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_df_coord[data1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_df_orientation`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_df_series`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_df_series_cumulative`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_df_series_cumulative_density`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_weights[weights0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_hist_weights[weights1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_implicit_label`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_df[bar-kwargs1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_df[hexbin-kwargs5]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_df[hist-kwargs2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_df[line-kwargs0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_df[pie-kwargs3]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_df[scatter-kwargs4]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_series[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_series[hist]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_series[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_integer_array_plot_series[pie]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_kind`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_logscale[loglog]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_logscale[logx]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_logscale[logy]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_xy_args[x0-A-a]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_xy_args[x1-y1-lbl1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_xy_args_dup_cols[A-B]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_invalid_xy_args_dup_cols[x1-B]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kde_df`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kde_df_logy`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kde_df_rot`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kde_df_subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kde_missing_vals`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[box]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[density]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[hist]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[kde]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways_x_y[hexbin]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_kind_both_ways_x_y[scatter]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df[idx0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df[idx1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df_stacked[idx0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df_stacked[idx1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df_stacked_area[kwargs0-idx0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df_stacked_area[kwargs0-idx1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df_stacked_area[kwargs1-idx0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_nan_df_stacked_area[kwargs1-idx1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked[-1-area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked[-1-line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked[1-area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked[1-line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked_mixed`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked_positive_idx[area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked_positive_idx[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked_sep_df[area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_area_stacked_sep_df[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_label_none`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_lim[kwargs0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_lim[kwargs1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_line_lim_subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_logscales[True-log]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_logscales[sym-symlog]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[box]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[density]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[hexbin]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[hist]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[kde]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[pie]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_memory_leak[scatter]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_negative_log`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nonnumeric_exclude`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nullable_int_plot[cols0-A-B]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nullable_int_plot[cols1-A-B]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nullable_int_plot[cols2-C-A]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nullable_int_plot[cols3-A-C]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nullable_int_plot[cols4-B-C]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nullable_int_plot[cols5-A-D]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_nullable_int_plot[cols6-A-E]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[area0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[area1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[box]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[density]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[hist]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[kde]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_partially_invalid_plot_data_numeric[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_period_compat`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_pie_df[2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_pie_df[Y]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_pie_df_err`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_pie_df_labels_colors`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_pie_df_nan`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_pie_df_subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plain_axes`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plain_axes_df`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plain_axes_make_axes_locatable`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plain_axes_make_inset_axes`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_bar[kwargs0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_bar[kwargs1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_bar[kwargs2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_bar[kwargs3]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_bar_int_col`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_bar_ticks`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_barh_ticks`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_int_columns`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_multiindex`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_multiindex_unicode`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_no_numeric_data`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_no_rows`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_no_warning`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_other_args[kwargs0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_other_args[kwargs1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_other_args[kwargs2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_other_args[kwargs3]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_passed_ax`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter[1-2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter[x-y]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_error`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_shape`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_c[0-1-2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_c[x-y-z]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_c_array`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_c_props`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_categorical_data[x-y]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_categorical_data[y-x]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_categorical_data[y-y]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_norm`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_with_s`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_scatter_without_norm`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_single_column_bar[None]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_single_column_bar[layout1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_subplots`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_subplots_negative_layout`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_subplots_use_index`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_tick_props`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_title`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_visible_ax`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_xy`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_xy_figsize_and_title`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_xy_int_cols`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_raise_error_on_datetime_time_data`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatter_unknown_colormap`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_color_by_categorical[categories0-False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_color_by_categorical[categories0-True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_color_by_categorical[categories1-False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_color_by_categorical[categories1-True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_datetime_data[0-1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_datetime_data[dates-vals]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col0-0-1-False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col0-0-1-True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col0-a-b-False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col0-a-b-True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col1-0-1-False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col1-0-1-True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col1-a-b-False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_scatterplot_object_data[b_col1-a-b-True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_secondary_axis_font_size[bar]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_secondary_axis_font_size[barh]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_secondary_axis_font_size[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_secondary_y[False]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_secondary_y[True]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_sharex_and_ax`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_sharex_false_and_ax`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_sharey_and_ax`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_sharey_and_ax_tight`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_specified_props_kwd_plot_box[boxprops-boxes]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_specified_props_kwd_plot_box[capprops-caps]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_specified_props_kwd_plot_box[medianprops-medians]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_specified_props_kwd_plot_box[whiskerprops-whiskers]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_style_by_column[markers0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_style_by_column[markers1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_style_by_column[markers2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_style_by_column[markers3]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_table`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_unordered_ts`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_unsorted_index[float64]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_unsorted_index[int64]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_unsorted_index_lims[df0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_unsorted_index_lims[df1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_unsorted_index_lims_x_y`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_x_multiindex_values_ticks`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_x_string_values_ticks`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xcompat`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xcompat_plot_params`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xcompat_plot_params_context_manager`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xcompat_plot_params_x_compat`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xcompat_plot_period`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[hexbin-None-None]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[hexbin-None-Y`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[hexbin-None-Y Label]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[hexbin-X`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[hexbin-X Label-None]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[hexbin-X Label-Y Label]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[scatter-None-None]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[scatter-None-Y`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[scatter-None-Y Label]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[scatter-X`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[scatter-X Label-None]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_plane_plot[scatter-X Label-Y Label]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[area-None--1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[area-None--]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[area-None--new]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[area-None--new_label4]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[area-old-old-new]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[bar-None--1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[bar-None--]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[bar-None--new]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[bar-None--new_label4]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[bar-old-old-new]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[line-None--1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[line-None--]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[line-None--new]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[line-None--new_label4]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlabel_ylabel_dataframe_single_plot[line-old-old-new]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlim_plot_line[area]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlim_plot_line[line]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xlim_plot_line_correctly_in_mixed_plot_type`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xy_args_integer[0-1-colnames0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_xy_args_integer[1-0-colnames1]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_y_listlike[0-y2-lbl2-colors2]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_y_listlike[A-y0-lbl0-colors0]`
- `pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_y_listlike[A-y1-lbl1-colors1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_legacy1`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_legacy1_return_type`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_legacy2`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_legacy2_return_type`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_legacy3[False-None-1-layout1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_legacy3[True-UserWarning-3-layout0]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_multiindex_column`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_fontsize`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_groupby_boxplot_object`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_groupby_boxplot_subplots_false[None-expected_xticklabel4]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_groupby_boxplot_subplots_false[col1-expected_xticklabel1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_groupby_boxplot_subplots_false[col3-expected_xticklabel3]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_groupby_boxplot_subplots_false[v-expected_xticklabel0]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_groupby_boxplot_subplots_false[v1-expected_xticklabel2]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_axes_shape_cols_groupby[-1-3]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_axes_shape_cols_groupby[4-4]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_axes_shape_rows[-1-3]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_axes_shape_rows[4-4]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_needs_by`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_positive_layout`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_positive_layout_axes[category-4-2]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_positive_layout_axes[classroom-3-2]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_positive_layout_axes[gender-2-1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_shape`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_too_small`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_visible[category-True]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_visible[height-False]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_visible[weight-True]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_works[-1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_layout_works[2]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_multiple_axes`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_multiple_axes_ax_error`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_multiple_axes_on_fig`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type_arg[axes]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type_arg[both]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type_arg[dict]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type_arg_duplcate_cats[axes]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type_arg_duplcate_cats[both]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type_arg_duplcate_cats[dict]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_box_return_type_groupby`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_plot_fignums`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_grouped_plot_fignums_excluded_col`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_axis_limits`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_axis_limits_two_rows`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_empty_column`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_group_no_xlabel_ylabel[vert1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_group_xlabel_ylabel[vert1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs0-None]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs1-None]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs2-UserWarning]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs3-None]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs4-UserWarning]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs5-UserWarning]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs6-None]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1[kwargs7-UserWarning]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy1_series`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy2`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy2_by_none`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy2_with_ax`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy2_with_ax_return_type`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_legacy2_with_multi_col`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_numeric_data`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_return_type_legacy`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_return_type_legacy_return_type[axes]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_return_type_legacy_return_type[both]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_return_type_legacy_return_type[dict]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_return_type_none`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_xlabel_ylabel[vert1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_color_kwd[colors_kwd0-expected0]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_color_kwd[colors_kwd1-expected1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_color_kwd[r-expected2]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_color_kwd_errors[dict_colors0-invalid`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_color_kwd_errors[dict_colors0-invalid key 'invalid_key']`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_colors_in_theme[dark_background-expected0]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_colors_in_theme[default-expected1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_figsize`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_fontsize`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_plot_box[vert0]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_plot_box[vert1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_plot_xlabel_ylabel[vert1]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_specified_props_kwd[boxprops-boxes]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_specified_props_kwd[capprops-caps]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_specified_props_kwd[medianprops-medians]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_specified_props_kwd[whiskerprops-whiskers]`
- `pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_stacked_boxplot_set_axis`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #60586: Backport PR #60584 on branch 2.3.x (TST: Address matplotlib 3.10 deprecation of vert=)

Backport PR #60584: TST: Address matplotlib 3.10 deprecation of vert=
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/pandas/plotting/_matplotlib/boxplot.py b/pandas/plotting/_matplotlib/boxplot.py
index d2b76decaa75d3e7adc9792763db4e276e514ff1..80f0349b205e6072abeb63c4727a1efa060b2d36 100644
--- a/pandas/plotting/_matplotlib/boxplot.py
+++ b/pandas/plotting/_matplotlib/boxplot.py
@@ -7,6 +7,7 @@ from typing import (
 )
 import warnings
 
+import matplotlib as mpl
 from matplotlib.artist import setp
 import numpy as np
 
@@ -20,6 +21,7 @@ from pandas.core.dtypes.missing import remove_na_arraylike
 
 import pandas as pd
 import pandas.core.common as com
+from pandas.util.version import Version
 
 from pandas.io.formats.printing import pprint_thing
 from pandas.plotting._matplotlib.core import (
@@ -54,7 +56,8 @@ def _set_ticklabels(ax: Axes, labels: list[str], is_vertical: bool, **kwargs) ->
     ticks = ax.get_xticks() if is_vertical else ax.get_yticks()
     if len(ticks) != len(labels):
         i, remainder = divmod(len(ticks), len(labels))
-        assert remainder == 0, remainder
+        if Version(mpl.__version__) < Version("3.10"):
+            assert remainder == 0, remainder
         labels *= i
     if is_vertical:
         ax.set_xticklabels(labels, **kwargs)
diff --git a/pandas/plotting/_matplotlib/tools.py b/pandas/plotting/_matplotlib/tools.py
index 898b5b25e7b0171e4b41106bf340e7fbc3bbb735..98441c5afbaa47bfdfd7db27f33ef91c90332088 100644
--- a/pandas/plotting/_matplotlib/tools.py
+++ b/pandas/plotting/_matplotlib/tools.py
@@ -57,7 +57,7 @@ def format_date_labels(ax: Axes, rot) -> None:
     fig = ax.get_figure()
     if fig is not None:
         # should always be a Figure but can technically be None
-        maybe_adjust_figure(fig, bottom=0.2)
+        maybe_adjust_figure(fig, bottom=0.2)  # type: ignore[arg-type]
 
 
 def table(
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/plotting/frame/test_frame.py b/pandas/tests/plotting/frame/test_frame.py
index 4ca4067214bbd20e56065bf74d6851e926679b88..33366b4eabba5b4827b8710fb6edc27f3754d5e7 100644
--- a/pandas/tests/plotting/frame/test_frame.py
+++ b/pandas/tests/plotting/frame/test_frame.py
@@ -1059,28 +1059,43 @@ class TestDataFramePlots:
         tm.assert_numpy_array_equal(ax.xaxis.get_ticklocs(), positions)
         assert len(ax.lines) == 7 * len(numeric_cols)
 
+    @pytest.mark.filterwarnings("ignore:set_ticklabels:UserWarning")
+    @pytest.mark.xfail(
+        Version(mpl.__version__) >= Version("3.10"),
+        reason="Fails starting with matplotlib 3.10",
+    )
     def test_boxplot_vertical(self, hist_df):
         df = hist_df
         numeric_cols = df._get_numeric_data().columns
         labels = [pprint_thing(c) for c in numeric_cols]
 
         # if horizontal, yticklabels are rotated
-        ax = df.plot.box(rot=50, fontsize=8, vert=False)
+        kwargs = (
+            {"vert": False}
+            if Version(mpl.__version__) < Version("3.10")
+            else {"orientation": "horizontal"}
+        )
+        ax = df.plot.box(rot=50, fontsize=8, **kwargs)
         _check_ticks_props(ax, xrot=0, yrot=50, ylabelsize=8)
         _check_text_labels(ax.get_yticklabels(), labels)
         assert len(ax.lines) == 7 * len(numeric_cols)
 
-    @pytest.mark.filterwarnings("ignore:Attempt:UserWarning")
+    @pytest.mark.filterwarnings("ignore::UserWarning")
+    @pytest.mark.xfail(
+        Version(mpl.__version__) >= Version("3.10"),
+        reason="Fails starting with matplotlib version 3.10",
+    )
     def test_boxplot_vertical_subplots(self, hist_df):
         df = hist_df
         numeric_cols = df._get_numeric_data().columns
         labels = [pprint_thing(c) for c in numeric_cols]
+        kwargs = (
+            {"vert": False}
+            if Version(mpl.__version__) < Version("3.10")
+            else {"orientation": "horizontal"}
+        )
         axes = _check_plot_works(
-            df.plot.box,
-            default_axes=True,
-            subplots=True,
-            vert=False,
-            logx=True,
+            df.plot.box, default_axes=True, subplots=True, logx=True, **kwargs
         )
         _check_axes_shape(axes, axes_num=3, layout=(1, 3))
         _check_ax_scales(axes, xaxis="log")
@@ -1088,12 +1103,22 @@ class TestDataFramePlots:
             _check_text_labels(ax.get_yticklabels(), [label])
             assert len(ax.lines) == 7
 
+    @pytest.mark.filterwarnings("ignore:set_ticklabels:UserWarning")
+    @pytest.mark.xfail(
+        Version(mpl.__version__) >= Version("3.10"),
+        reason="Fails starting with matplotlib 3.10",
+    )
     def test_boxplot_vertical_positions(self, hist_df):
         df = hist_df
         numeric_cols = df._get_numeric_data().columns
         labels = [pprint_thing(c) for c in numeric_cols]
         positions = np.array([3, 2, 8])
-        ax = df.plot.box(positions=positions, vert=False)
+        kwargs = (
+            {"vert": False}
+            if Version(mpl.__version__) < Version("3.10")
+            else {"orientation": "horizontal"}
+        )
+        ax = df.plot.box(positions=positions, **kwargs)
         _check_text_labels(ax.get_yticklabels(), labels)
         tm.assert_numpy_array_equal(ax.yaxis.get_ticklocs(), positions)
         assert len(ax.lines) == 7 * len(numeric_cols)
diff --git a/pandas/tests/plotting/test_boxplot_method.py b/pandas/tests/plotting/test_boxplot_method.py
index 76f7fa1f22eec4bdb7464619226352c918d31a02..e1b03a34086c03c01d7fa6cd4b3158a444d17e09 100644
--- a/pandas/tests/plotting/test_boxplot_method.py
+++ b/pandas/tests/plotting/test_boxplot_method.py
@@ -1,5 +1,7 @@
 """ Test cases for .boxplot method """
 
+from __future__ import annotations
+
 import itertools
 import string
 
@@ -22,6 +24,7 @@ from pandas.tests.plotting.common import (
     _check_ticks_props,
     _check_visible,
 )
+from pandas.util.version import Version
 
 from pandas.io.formats.printing import pprint_thing
 
@@ -35,6 +38,17 @@ def _check_ax_limits(col, ax):
     assert y_max >= col.max()
 
 
+if Version(mpl.__version__) < Version("3.10"):
+    verts: list[dict[str, bool | str]] = [{"vert": False}, {"vert": True}]
+else:
+    verts = [{"orientation": "horizontal"}, {"orientation": "vertical"}]
+
+
+@pytest.fixture(params=verts)
+def vert(request):
+    return request.param
+
+
 class TestDataFramePlots:
     def test_stacked_boxplot_set_axis(self):
         # GH2980
@@ -315,7 +329,7 @@ class TestDataFramePlots:
 
         assert result[expected][0].get_color() == "C1"
 
-    @pytest.mark.parametrize("vert", [True, False])
+    @pytest.mark.filterwarnings("ignore:set_ticklabels:UserWarning")
     def test_plot_xlabel_ylabel(self, vert):
         df = DataFrame(
             {
@@ -325,11 +339,11 @@ class TestDataFramePlots:
             }
         )
         xlabel, ylabel = "x", "y"
-        ax = df.plot(kind="box", vert=vert, xlabel=xlabel, ylabel=ylabel)
+        ax = df.plot(kind="box", xlabel=xlabel, ylabel=ylabel, **vert)
         assert ax.get_xlabel() == xlabel
         assert ax.get_ylabel() == ylabel
 
-    @pytest.mark.parametrize("vert", [True, False])
+    @pytest.mark.filterwarnings("ignore:set_ticklabels:UserWarning")
     def test_plot_box(self, vert):
         # GH 54941
         rng = np.random.default_rng(2)
@@ -338,14 +352,14 @@ class TestDataFramePlots:
 
         xlabel, ylabel = "x", "y"
         _, axs = plt.subplots(ncols=2, figsize=(10, 7), sharey=True)
-        df1.plot.box(ax=axs[0], vert=vert, xlabel=xlabel, ylabel=ylabel)
-        df2.plot.box(ax=axs[1], vert=vert, xlabel=xlabel, ylabel=ylabel)
+        df1.plot.box(ax=axs[0], xlabel=xlabel, ylabel=ylabel, **vert)
+        df2.plot.box(ax=axs[1], xlabel=xlabel, ylabel=ylabel, **vert)
         for ax in axs:
             assert ax.get_xlabel() == xlabel
             assert ax.get_ylabel() == ylabel
         mpl.pyplot.close()
 
-    @pytest.mark.parametrize("vert", [True, False])
+    @pytest.mark.filterwarnings("ignore:set_ticklabels:UserWarning")
     def test_boxplot_xlabel_ylabel(self, vert):
         df = DataFrame(
             {
@@ -355,11 +369,11 @@ class TestDataFramePlots:
             }
         )
         xlabel, ylabel = "x", "y"
-        ax = df.boxplot(vert=vert, xlabel=xlabel, ylabel=ylabel)
+        ax = df.boxplot(xlabel=xlabel, ylabel=ylabel, **vert)
         assert ax.get_xlabel() == xlabel
         assert ax.get_ylabel() == ylabel
 
-    @pytest.mark.parametrize("vert", [True, False])
+    @pytest.mark.filterwarnings("ignore:set_ticklabels:UserWarning")
     def test_boxplot_group_xlabel_ylabel(self, vert):
         df = DataFrame(
             {
@@ -369,14 +383,20 @@ class TestDataFramePlots:
             }
         )
         xlabel, ylabel = "x", "y"
-        ax = df.boxplot(by="group", vert=vert, xlabel=xlabel, ylabel=ylabel)
+        ax = df.boxplot(by="group", xlabel=xlabel, ylabel=ylabel, **vert)
         for subplot in ax:
             assert subplot.get_xlabel() == xlabel
             assert subplot.get_ylabel() == ylabel
         mpl.pyplot.close()
 
-    @pytest.mark.parametrize("vert", [True, False])
-    def test_boxplot_group_no_xlabel_ylabel(self, vert):
+    @pytest.mark.filterwarnings("ignore:set_ticklabels:UserWarning")
+    def test_boxplot_group_no_xlabel_ylabel(self, vert, request):
+        if Version(mpl.__version__) >= Version("3.10") and vert == {
+            "orientation": "horizontal"
+        }:
+            request.applymarker(
+                pytest.mark.xfail(reason=f"{vert} fails starting with matplotlib 3.10")
+            )
         df = DataFrame(
             {
                 "a": np.random.default_rng(2).standard_normal(10),
@@ -384,9 +404,14 @@ class TestDataFramePlots:
                 "group": np.random.default_rng(2).choice(["group1", "group2"], 10),
             }
         )
-        ax = df.boxplot(by="group", vert=vert)
+        ax = df.boxplot(by="group", **vert)
         for subplot in ax:
-            target_label = subplot.get_xlabel() if vert else subplot.get_ylabel()
+            target_label = (
+                subplot.get_xlabel()
+                if vert == {"vert": True}  # noqa: PLR1714
+                or vert == {"orientation": "vertical"}
+                else subplot.get_ylabel()
+            )
             assert target_label == pprint_thing(["group"])
         mpl.pyplot.close()
```

## Validation

```json
{
 "test_files": [
  "pandas/tests/plotting/frame/test_frame.py",
  "pandas/tests/plotting/test_boxplot_method.py"
 ],
 "collected_before": 436,
 "collected_after": 436,
 "outcomes_before": {
  "PASSED": 427,
  "XFAIL": 6,
  "FAILED": 3
 },
 "outcomes_after": {
  "PASSED": 430,
  "XFAIL": 6
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": " changed in 3.6.0\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_vertical - Fails starting with matplotlib 3.10\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_vertical_subplots - Fails starting with matplotlib version 3.10\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_vertical_positions - Fails starting with matplotlib 3.10\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_iterator - Iterator is consumed\nXFAIL pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_group_no_xlabel_ylabel[vert0] - {'orientation': 'horizontal'} fails starting with matplotlib 3.10\nXPASS pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_area_lim[True] - 2020-12-01 this has been failing periodically on the ymin==0 assertion for a week or so.\nXPASS pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_area_lim[False] - 2020-12-01 this has been failing periodically on the ymin==0 assertion for a week or so.\nFAILED pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_plot_xlabel_ylabel[vert0]\nFAILED pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_xlabel_ylabel[vert0]\nFAILED pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_group_xlabel_ylabel[vert0]\n====== 3 failed, 416 passed, 6 xfailed, 2 xpassed, 26 warnings in 52.60s =======",
 "tail_after": "klabel4]\nPASSED pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_groupby_boxplot_object\nPASSED pandas/tests/plotting/test_boxplot_method.py::TestDataFrameGroupByPlots::test_boxplot_multiindex_column\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_plot_invalid_arg - Api changed in 3.6.0\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_vertical - Fails starting with matplotlib 3.10\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_vertical_subplots - Fails starting with matplotlib version 3.10\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_boxplot_vertical_positions - Fails starting with matplotlib 3.10\nXFAIL pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_errorbar_plot_iterator - Iterator is consumed\nXFAIL pandas/tests/plotting/test_boxplot_method.py::TestDataFramePlots::test_boxplot_group_no_xlabel_ylabel[vert0] - {'orientation': 'horizontal'} fails starting with matplotlib 3.10\nXPASS pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_area_lim[True] - 2020-12-01 this has been failing periodically on the ymin==0 assertion for a week or so.\nXPASS pandas/tests/plotting/frame/test_frame.py::TestDataFramePlots::test_area_lim[False] - 2020-12-01 this has been failing periodically on the ymin==0 assertion for a week or so.\n=========== 419 passed, 6 xfailed, 2 xpassed, 26 warnings in 46.28s ============",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

# scipy__scipy-22969

[back to the list](README.md) -- **MAINT: stats.make_distribution: fix most remaining discrete distribution specific issues**

| field | value |
|---|---|
| pull request | [scipy/scipy#22969](https://github.com/scipy/scipy/pull/22969) (created 2025-05-10, merged 2025-05-13) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 3 developer test(s) flip; oracle reproduces it |
| base commit | [`2e683251bf95`](https://github.com/scipy/scipy/commit/2e683251bf95078001e1dd4b94a2fa93ee9b2426) (2025-05-13), first parent of the merge commit |
| merge commit | [`4c5e1ea1952f`](https://github.com/scipy/scipy/commit/4c5e1ea1952f83208e0ca7843b23a47867f60202) |
| issues closed | none |
| version | 1.16 |
| image | `f2p-chaco/scipy__scipy-22969:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-22969.Dockerfile) |
| source files (`patch`) | `scipy/stats/_discrete_distns.py`, `scipy/stats/_distribution_infrastructure.py` |
| test files (`test_patch`) | `scipy/stats/tests/test_continuous.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (3)

- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[128-distdata128]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[129-distdata129]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[139-distdata139]`

## PASS_TO_PASS (318)

<details><summary>show</summary>

- `scipy/stats/tests/test_continuous.py::TestAttributes::test_cache_policy`
- `scipy/stats/tests/test_continuous.py::TestAttributes::test_iv_policy`
- `scipy/stats/tests/test_continuous.py::TestAttributes::test_shapes`
- `scipy/stats/tests/test_continuous.py::TestAttributes::test_tol`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_complement_safe[ccdf]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_complement_safe[cdf]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ccdf-methods13-x-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ccdf-methods13-x-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ccdf-methods13-x-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ccdf-methods13-x-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ccdf-methods13-x-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[cdf-methods11-x-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[cdf-methods11-x-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[cdf-methods11-x-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[cdf-methods11-x-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[cdf-methods11-x-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[entropy-methods0-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[entropy-methods0-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[entropy-methods0-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[entropy-methods0-None-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[entropy-methods0-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[iccdf-methods15-p-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[iccdf-methods15-p-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[iccdf-methods15-p-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[iccdf-methods15-p-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[iccdf-methods15-p-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ilogccdf-methods14-logp-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ilogccdf-methods14-logp-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ilogccdf-methods14-logp-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ilogccdf-methods14-logp-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[ilogccdf-methods14-logp-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[kurtosis-methods7-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[kurtosis-methods7-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[kurtosis-methods7-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[kurtosis-methods7-None-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[kurtosis-methods7-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logccdf-methods12-x-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logccdf-methods12-x-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logccdf-methods12-x-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logccdf-methods12-x-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logccdf-methods12-x-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logcdf-methods10-x-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logcdf-methods10-x-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logcdf-methods10-x-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logcdf-methods10-x-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logcdf-methods10-x-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logentropy-methods1-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logentropy-methods1-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logentropy-methods1-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logentropy-methods1-None-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logentropy-methods1-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logpdf-methods9-x-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logpdf-methods9-x-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logpdf-methods9-x-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logpdf-methods9-x-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[logpdf-methods9-x-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mean-methods4-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mean-methods4-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mean-methods4-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mean-methods4-None-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mean-methods4-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[median-methods2-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[median-methods2-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[median-methods2-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[median-methods2-None-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[median-methods2-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mode-methods3-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mode-methods3-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mode-methods3-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[mode-methods3-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[pdf-methods8-x-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[pdf-methods8-x-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[pdf-methods8-x-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[pdf-methods8-x-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[pdf-methods8-x-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[skewness-methods6-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[skewness-methods6-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[skewness-methods6-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[skewness-methods6-None-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[skewness-methods6-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[variance-methods5-None-Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[variance-methods5-None-Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[variance-methods5-None-StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[variance-methods5-None-Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_funcs[variance-methods5-None-_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_icomplement_safe[ccdf]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_icomplement_safe[cdf]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_logcdf2_safe`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_logentropy_safe`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_logexp_safe[logccdf]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_logexp_safe[logcdf]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_plot`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_subtraction_safe`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_support_moments_sample[Binomial]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_support_moments_sample[Normal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_support_moments_sample[StandardNormal]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_support_moments_sample[Uniform]`
- `scipy/stats/tests/test_continuous.py::TestDistributions::test_support_moments_sample[_LogUniform]`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_ContinuousDistribution__repr__`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_ContinuousDistribution_set_invalid_nan`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_Domain`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_Parameter`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_RealParameter_uncommon_dtypes[float16-float16]`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_RealParameter_uncommon_dtypes[int16-float64]`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_fiinfo`
- `scipy/stats/tests/test_continuous.py::TestFullCoverage::test_generate_domain_support`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_multiple_parameterizations[0.5-0.5]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_multiple_parameterizations[0.5-a1]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_multiple_parameterizations[b1-0.5]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_multiple_parameterizations[b1-a1]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_variable_support[-1]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_variable_support[0]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_variable_support[1]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_custom_variable_support[c3]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_input_validation`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_repr_str_docs`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[0-distdata0]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[1-distdata1]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[10-distdata10]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[101-distdata101]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[102-distdata102]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[103-distdata103]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[104-distdata104]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[105-distdata105]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[106-distdata106]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[107-distdata107]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[108-distdata108]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[109-distdata109]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[11-distdata11]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[110-distdata110]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[111-distdata111]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[112-distdata112]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[114-distdata114]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[115-distdata115]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[116-distdata116]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[117-distdata117]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[118-distdata118]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[119-distdata119]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[12-distdata12]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[120-distdata120]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[121-distdata121]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[122-distdata122]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[123-distdata123]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[124-distdata124]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[125-distdata125]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[126-distdata126]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[127-distdata127]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[13-distdata13]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[130-distdata130]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[131-distdata131]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[132-distdata132]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[133-distdata133]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[134-distdata134]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[135-distdata135]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[136-distdata136]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[138-distdata138]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[14-distdata14]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[140-distdata140]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[141-distdata141]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[142-distdata142]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[15-distdata15]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[16-distdata16]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[17-distdata17]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[18-distdata18]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[19-distdata19]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[2-distdata2]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[22-distdata22]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[23-distdata23]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[24-distdata24]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[25-distdata25]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[26-distdata26]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[27-distdata27]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[28-distdata28]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[30-distdata30]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[31-distdata31]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[32-distdata32]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[33-distdata33]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[34-distdata34]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[35-distdata35]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[36-distdata36]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[37-distdata37]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[39-distdata39]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[4-distdata4]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[40-distdata40]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[42-distdata42]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[43-distdata43]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[44-distdata44]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[45-distdata45]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[46-distdata46]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[47-distdata47]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[48-distdata48]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[49-distdata49]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[5-distdata5]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[50-distdata50]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[51-distdata51]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[52-distdata52]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[54-distdata54]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[59-distdata59]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[6-distdata6]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[63-distdata63]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[64-distdata64]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[65-distdata65]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[66-distdata66]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[67-distdata67]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[68-distdata68]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[69-distdata69]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[7-distdata7]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[70-distdata70]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[71-distdata71]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[72-distdata72]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[73-distdata73]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[74-distdata74]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[75-distdata75]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[76-distdata76]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[77-distdata77]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[78-distdata78]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[79-distdata79]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[8-distdata8]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[80-distdata80]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[81-distdata81]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[82-distdata82]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[84-distdata84]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[85-distdata85]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[86-distdata86]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[87-distdata87]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[88-distdata88]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[9-distdata9]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[91-distdata91]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[92-distdata92]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[94-distdata94]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[95-distdata95]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[96-distdata96]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[97-distdata97]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[98-distdata98]`
- `scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[99-distdata99]`
- `scipy/stats/tests/test_continuous.py::TestMixture::test_basic[shape0]`
- `scipy/stats/tests/test_continuous.py::TestMixture::test_basic[shape1]`
- `scipy/stats/tests/test_continuous.py::TestMixture::test_default_weights`
- `scipy/stats/tests/test_continuous.py::TestMixture::test_input_validation`
- `scipy/stats/tests/test_continuous.py::TestMixture::test_inverse`
- `scipy/stats/tests/test_continuous.py::TestMixture::test_properties`
- `scipy/stats/tests/test_continuous.py::TestOrderStatistic::test_composition_gh22037`
- `scipy/stats/tests/test_continuous.py::TestOrderStatistic::test_order_statistic`
- `scipy/stats/tests/test_continuous.py::TestOrderStatistic::test_support_gh22037`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist0]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist10]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist11]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist12]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist13]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist14]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist15]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist16]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist17]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist1]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist2]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist3]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist4]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist5]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist6]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist7]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist8]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_executable[dist9]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist0]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist1]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist2]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist3]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist4]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist5]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist6]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist7]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist8]`
- `scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist9]`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_ContinuousDistribution_only`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_abs`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_abs_finite_support`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_arithmetic_operators`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_exp_pow[exp]`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_exp_pow[pow]`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_loc_scale`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_log`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_monotonic_transforms`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_pow`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_reciprocal[-1]`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_reciprocal[1]`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_reciprocal[2]`
- `scipy/stats/tests/test_continuous.py::TestTransforms::test_truncate`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[0-1-inclusive0]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[0-1-inclusive1]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[0-1-inclusive2]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[0-1-inclusive3]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[3-1-inclusive0]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[3-1-inclusive1]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[3-1-inclusive2]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_function_endpoints[3-1-inclusive3]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_simple[-inf]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_simple[3.141592653589793]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_contains_simple[x0]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_iv`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_str2`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_str[case0]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_str[case1]`
- `scipy/stats/tests/test_continuous.py::Test_RealInterval::test_symbols_gh22137`
- `scipy/stats/tests/test_continuous.py::test_input_validation`
- `scipy/stats/tests/test_continuous.py::test_rng_deepcopy_pickle`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Generator-sample-dist_shape0-x_shape0-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Generator-sample-dist_shape0-x_shape1-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Generator-sample-dist_shape1-x_shape0-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Generator-sample-dist_shape1-x_shape1-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Halton-sample-dist_shape0-x_shape0-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Halton-sample-dist_shape0-x_shape1-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Halton-sample-dist_shape1-x_shape0-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Halton-sample-dist_shape1-x_shape1-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Sobol-sample-dist_shape0-x_shape0-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Sobol-sample-dist_shape0-x_shape1-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Sobol-sample-dist_shape1-x_shape0-Normal]`
- `scipy/stats/tests/test_continuous.py::test_sample_against_cdf[Sobol-sample-dist_shape1-x_shape1-Normal]`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #22969: MAINT: stats.make_distribution: fix most remaining discrete distribution specific issues

#### Reference issue
gh-22312

#### What does this implement/fix?
gh-22312 added a new discrete distribution infrastructure and a way to use the infrastructure with existing discrete distributions, but there were distribution-specific issues that precluded use with some distributions. This resolves those issues for `nchypergeom_fisher`, `nchypergeom_fisher`, and `zipfian`. It also runs tests properly on `betanbinom`, `zipf`, and `logser`.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/stats/_discrete_distns.py b/scipy/stats/_discrete_distns.py
index 1e3340506e37e096b9626c888781cda2497838f6..ac12ef17aa3d72738aef845c3d1bacc3bcb6a228 100644
--- a/scipy/stats/_discrete_distns.py
+++ b/scipy/stats/_discrete_distns.py
@@ -1371,12 +1371,13 @@ def _gen_harmonic_leq1(n, a):
     """Generalized harmonic number, a <= 1"""
     if not np.size(n):
         return n
-    n_max = np.max(n)  # loop starts at maximum of all n
+    n_max = np.nanmax(n)  # loop starts at maximum of all n
     out = np.zeros_like(a, dtype=float)
     # add terms of harmonic series; starting from smallest to avoid roundoff
     for i in np.arange(n_max, 0, -1, dtype=float):
         mask = i <= n  # don't add terms after nth
         out[mask] += 1/i**a[mask]
+    out[np.isnan(n)] = np.nan
     return out
 
 
@@ -1871,9 +1872,9 @@ class _nchypergeom_gen(rv_discrete):
     def _argcheck(self, M, n, N, odds):
         M, n = np.asarray(M), np.asarray(n),
         N, odds = np.asarray(N), np.asarray(odds)
-        cond1 = (M.astype(int) == M) & (M >= 0)
-        cond2 = (n.astype(int) == n) & (n >= 0)
-        cond3 = (N.astype(int) == N) & (N >= 0)
+        cond1 = (~np.isnan(M)) & (M.astype(int) == M) & (M >= 0)
+        cond2 = (~np.isnan(n)) & (n.astype(int) == n) & (n >= 0)
+        cond3 = (~np.isnan(N)) & (N.astype(int) == N) & (N >= 0)
         cond4 = odds > 0
         cond5 = N <= M
         cond6 = n <= M
@@ -1883,6 +1884,8 @@ class _nchypergeom_gen(rv_discrete):
 
         @_vectorize_rvs_over_shapes
         def _rvs1(M, n, N, odds, size, random_state):
+            if np.isnan(M) | np.isnan(n) | np.isnan(N):
+                return np.full(size, np.nan)
             length = np.prod(size)
             urn = _PyStochasticLib3()
             rv_gen = getattr(urn, self.rvs_name)
@@ -1900,15 +1903,19 @@ class _nchypergeom_gen(rv_discrete):
 
         @np.vectorize
         def _pmf1(x, M, n, N, odds):
+            if np.isnan(x) | np.isnan(M) | np.isnan(n) | np.isnan(N):
+                return np.nan
             urn = self.dist(N, n, M, odds, 1e-12)
             return urn.probability(x)
 
         return _pmf1(x, M, n, N, odds)
 
-    def _stats(self, M, n, N, odds, moments):
+    def _stats(self, M, n, N, odds, moments='mv'):
 
         @np.vectorize
         def _moments1(M, n, N, odds):
+            if np.isnan(M) | np.isnan(n) | np.isnan(N):
+                return np.nan, np.nan
             urn = self.dist(N, n, M, odds, 1e-12)
             return urn.moments()
 
diff --git a/scipy/stats/_distribution_infrastructure.py b/scipy/stats/_distribution_infrastructure.py
index 13b8380c5a951387261d45dc2478af1a3ab14c3e..94b2243d177bf684f26da14c9721a10325c5ef38 100644
--- a/scipy/stats/_distribution_infrastructure.py
+++ b/scipy/stats/_distribution_infrastructure.py
@@ -3856,8 +3856,7 @@ def make_distribution(dist):
 
         `make_distribution` does not work perfectly with all instances of
         `rv_continuous`. Known failures include `levy_stable`, `vonmises`,
-        `hypergeom`, `nchypergeom_fisher`, `nchypergeom_wallenius`,
-        `poisson_binom`; and some methods of some distributions
+        `hypergeom`, `poisson_binom`, and 'skellam'. Some methods of some distributions
         will not support array shape parameters.
 
     Parameters
@@ -4066,8 +4065,7 @@ def make_distribution(dist):
 
     """
     if dist in {stats.levy_stable, stats.vonmises, stats.hypergeom,
-                stats.nchypergeom_fisher, stats.nchypergeom_wallenius,
-                stats.poisson_binom}:
+                stats.poisson_binom, stats.skellam}:
         raise NotImplementedError(f"`{dist.name}` is not supported.")
 
     if isinstance(dist, stats.rv_continuous | stats.rv_discrete):
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/stats/tests/test_continuous.py b/scipy/stats/tests/test_continuous.py
index 5132d54eebf814058a06203b08244c4549ffc99e..2be327145c2e1883a682f6938247c8384999415f 100644
--- a/scipy/stats/tests/test_continuous.py
+++ b/scipy/stats/tests/test_continuous.py
@@ -1113,7 +1113,7 @@ class TestMakeDistribution:
                 'johnsonsb', 'kappa4', 'ksone', 'kstwo', 'kstwobign', 'norminvgauss',
                 'powerlognorm', 'powernorm', 'recipinvgauss', 'studentized_range',
                 'vonmises_line', # continuous
-                'betanbinom', 'zipf', 'logser', 'skellam'}  # discrete
+                'skellam'}  # discrete
         if not int(os.environ.get('SCIPY_XSLOW', '0')) and distname in slow:
             pytest.skip('Skipping as XSLOW')
 
@@ -1122,25 +1122,24 @@ class TestMakeDistribution:
             'vonmises',               # circular distribution; shouldn't work
             'poisson_binom',          # vector shape parameter
             'hypergeom',              # distribution functions need interpolation
-            'nchypergeom_fisher',     # distribution functions don't accept NaN
-            'nchypergeom_wallenius',  # distribution functions don't accept NaN
-            'skellam',                # during `entropy`, Fatal Python error: Aborted!
-            'zipfian',                # during init, value error due to unexpected nans
+            'skellam',                # gh-22956 (_ncx2_pdf crashes with extreme input)
         }:
             return
 
         # skip single test, mostly due to slight disagreement
         custom_tolerances = {'ksone': 1e-5, 'kstwo': 1e-5}  # discontinuous PDF
         skip_entropy = {'kstwobign', 'pearson3'}  # tolerance issue
-        skip_skewness = {'exponpow', 'ksone'}  # tolerance issue
-        skip_kurtosis = {'chi', 'exponpow', 'invgamma',  # tolerance issue
-                         'johnsonsb', 'ksone', 'kstwo'}  # tolerance issue
+        skip_skewness = {'exponpow', 'ksone', 'nchypergeom_wallenius'}  # tolerance
+        skip_kurtosis = {'chi', 'exponpow', 'invgamma',  # tolerance
+                         'johnsonsb', 'ksone', 'kstwo',  # tolerance
+                         'nchypergeom_wallenius'}  # tolerance
         skip_logccdf = {'arcsine', 'skewcauchy', 'trapezoid', 'triang'}  # tolerance
         skip_raw = {2: {'alpha', 'foldcauchy', 'halfcauchy', 'levy', 'levy_l'},
                     3: {'pareto'},  # stats.pareto is just wrong
                     4: {'invgamma'}}  # tolerance issue
-        skip_standardized = {'exponpow', 'ksone'}  # tolerances
-        skip_median = {'nhypergeom', 'yulesimon'}  # nan mismatch
+        skip_standardized = {'exponpow', 'ksone', 'nchypergeom_wallenius'}  # tolerances
+        skip_median = {'nhypergeom', 'yulesimon',  # nan mismatch
+                       'betanbinom', 'zipf', 'logser'}  # median 0th element
 
         dist = getattr(stats, distname)
         params = dict(zip(dist.shapes.split(', '), distdata[1])) if dist.shapes else {}
@@ -1195,10 +1194,14 @@ class TestMakeDistribution:
                 if distname not in skip_standardized:
                     assert_allclose(X.moment(order, kind='standardized'),
                                     Y.stats('mvsk'[order-1]), rtol=rtol, atol=atol)
-            seed = 845298245687345
-            assert_allclose(X.sample(shape=10, rng=seed),
-                            Y.rvs(size=10, random_state=np.random.default_rng(seed)),
-                            rtol=rtol)
+            if isinstance(dist, stats.rv_continuous):
+                # For discrete distributions, these won't agree at the far left end
+                # of the support, and the new infrastructure is slow there (for now).
+                seed = 845298245687345
+                assert_allclose(X.sample(shape=10, rng=seed),
+                                Y.rvs(size=10,
+                                      random_state=np.random.default_rng(seed)),
+                                rtol=rtol)
 
     def test_custom(self):
         rng = np.random.default_rng(7548723590230982)
```

## Validation

```json
{
 "test_files": [
  "scipy/stats/tests/test_continuous.py"
 ],
 "collected_before": 343,
 "collected_after": 343,
 "outcomes_before": {
  "PASSED": 318,
  "SKIPPED": 22,
  "FAILED": 3
 },
 "outcomes_after": {
  "PASSED": 321,
  "SKIPPED": 22
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "[dist3]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist4]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist5]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist6]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist7]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist8]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist9]\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_input_validation\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_basic[shape0]\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_basic[shape1]\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_default_weights\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_properties\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_inverse\nSKIPPED [1] scipy/stats/tests/test_continuous.py:251: Mode is not unique; `method`s disagree.\nSKIPPED [21] scipy/stats/tests/test_continuous.py:1118: Skipping as XSLOW\nFAILED scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[128-distdata128]\nFAILED scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[129-distdata129]\nFAILED scipy/stats/tests/test_continuous.py::TestMakeDistribution::test_rv_generic[139-distdata139]\n============= 3 failed, 318 passed, 22 skipped in 71.34s (0:01:11) =============",
 "tail_after": "ts/tests/test_continuous.py::TestReprs::test_not_too_long[dist0]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist1]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist2]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist3]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist4]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist5]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist6]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist7]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist8]\nPASSED scipy/stats/tests/test_continuous.py::TestReprs::test_not_too_long[dist9]\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_input_validation\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_basic[shape0]\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_basic[shape1]\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_default_weights\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_properties\nPASSED scipy/stats/tests/test_continuous.py::TestMixture::test_inverse\nSKIPPED [1] scipy/stats/tests/test_continuous.py:251: Mode is not unique; `method`s disagree.\nSKIPPED [21] scipy/stats/tests/test_continuous.py:1118: Skipping as XSLOW\n================== 321 passed, 22 skipped in 66.93s (0:01:06) ==================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

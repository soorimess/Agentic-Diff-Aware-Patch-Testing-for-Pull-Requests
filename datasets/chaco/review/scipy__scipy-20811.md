# scipy__scipy-20811

[back to the list](README.md) -- **ENH: ndimage: extend filter axes support to remaining filters (`generic_filter`, etc.)**

| field | value |
|---|---|
| pull request | [scipy/scipy#20811](https://github.com/scipy/scipy/pull/20811) (created 2024-05-27, merged 2024-09-11) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 25 developer test(s) flip; oracle reproduces it |
| base commit | [`46344fe55327`](https://github.com/scipy/scipy/commit/46344fe55327d7a3d9b6dd0f7ce081cbaa96dc7b) (2024-09-10), first parent of the merge commit |
| merge commit | [`9aa1dbafd0a6`](https://github.com/scipy/scipy/commit/9aa1dbafd0a68a8cd5cfd9fc1ad8e502475b1a49) |
| issues closed | none |
| version | 1.15 |
| image | `f2p-chaco/scipy__scipy-20811:latest` -- [Dockerfile](../dockerfiles/scipy__scipy-20811.Dockerfile) |
| source files (`patch`) | `scipy/ndimage/_filters.py` |
| test files (`test_patch`) | `scipy/ndimage/tests/test_filters.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (25)

- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_derivative_filter_axes[gaussian_gradient_magnitude-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_derivative_filter_axes[gaussian_laplace-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_derivative_filter_axes[laplace-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes10-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes11-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes12-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes13-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes14-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes15-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes17-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes18-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes19-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes20-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes21-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes9-numpy]`

## PASS_TO_PASS (2237)

<details><summary>show</summary>

- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate01[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate01_overlap[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate02[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate03[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate04[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate05[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate06[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate07[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate08[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate09[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate10[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate11[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate12[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate13[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate14[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate15[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate16[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate17[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate18[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate19[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex128-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex128-complex64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex128-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input[complex64-complex64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel[complex128-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel[complex128-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel[complex64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel[complex64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel_cval[complex128-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel_cval[complex128-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel_cval[complex64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_and_kernel_cval[complex64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex128-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex128-complex64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex128-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_input_cval[complex64-complex64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex128-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel[complex64-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex128-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate1d_complex_kernel_cval[complex64-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate20[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate21[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate22[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate23[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate24[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate25[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate26[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex128-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex128-complex64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex128-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input[complex64-complex64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel[complex128-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel[complex128-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel[complex64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel[complex64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel_cval[complex128-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel_cval[complex128-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel_cval[complex64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_input_and_kernel_cval[complex64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex128-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel[complex64-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex128-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[constant-complex64-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex128-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_cval[grid-constant-complex64-uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[float32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[float32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[float64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[float64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[int8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint16-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint16-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint32-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint32-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint8-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_complex_kernel_invalid_cval[uint8-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes0-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes1-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes10-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes11-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes12-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes13-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes14-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes2-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes3-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes4-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes5-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes6-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes7-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes8-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin0-axes9-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes0-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes1-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes10-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes11-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes12-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes13-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes14-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes2-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes3-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes4-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes5-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes6-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes7-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes8-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-complex128-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-complex128-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-complex64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-complex64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-float32-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-float32-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-float64-convolve-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_convolve_axes[origin1-axes9-float64-correlate-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_correlate_mode_sequence[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend01[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend01[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend01[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend01[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend01[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend02[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend02[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend02[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend02[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend02[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend03[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend03[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend03[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend03[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend03[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend04[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend04[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend04[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend04[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend04[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend05[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend05[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend05[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend05[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend05[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend06[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend06[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend06[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend06[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend06[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend07[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend07[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend07[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend07[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend07[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend08[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend08[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend08[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend08[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend08[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend09[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend09[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend09[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend09[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend09[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend10[constant-expected_value4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend10[mirror-expected_value3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend10[nearest-expected_value0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend10[reflect-expected_value2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_extend10[wrap-expected_value1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes0-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes0-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes0-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes0-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes0-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes0-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes0-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes1-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes1-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes1-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes1-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes1-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes1-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes1-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes10-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes10-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes10-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes10-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes10-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes10-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes10-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes11-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes11-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes11-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes11-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes11-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes11-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes11-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes12-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes12-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes12-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes12-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes12-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes12-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes12-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes13-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes13-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes13-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes13-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes13-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes13-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes13-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes14-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes14-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes14-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes14-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes14-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes14-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes14-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes15-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes15-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes15-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes15-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes15-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes15-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes15-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes16-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes16-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes16-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes16-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes16-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes16-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes16-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes17-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes17-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes17-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes17-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes17-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes17-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes17-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes18-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes18-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes18-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes18-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes18-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes18-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes18-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes19-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes19-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes19-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes19-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes19-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes19-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes19-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes2-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes2-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes2-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes2-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes2-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes2-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes2-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes20-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes20-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes20-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes20-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes20-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes20-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes20-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes21-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes21-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes21-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes21-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes21-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes21-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes21-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes3-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes3-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes3-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes3-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes3-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes3-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes3-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes4-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes4-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes4-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes4-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes4-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes4-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes4-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes5-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes5-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes5-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes5-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes5-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes5-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes5-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes6-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes6-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes6-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes6-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes6-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes6-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes6-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes7-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes7-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes7-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes7-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes7-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes7-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes7-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes8-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes8-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes8-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes8-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes8-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes8-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes8-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes9-gaussian_filter-extra_args0-0-1.0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes9-maximum_filter-extra_args3-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes9-median_filter-extra_args4-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes9-minimum_filter-extra_args2-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes9-percentile_filter-extra_args6-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes9-rank_filter-extra_args5-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes[axes9-uniform_filter-extra_args1-1-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes0-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes0-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes0-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes0-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes0-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes0-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes0-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes1-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes1-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes1-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes1-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes1-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes1-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes1-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes10-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes10-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes10-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes10-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes10-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes10-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes10-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes11-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes11-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes11-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes11-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes11-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes11-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes11-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes12-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes12-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes12-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes12-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes12-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes12-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes12-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes13-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes13-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes13-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes13-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes13-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes13-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes13-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes14-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes14-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes14-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes14-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes14-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes14-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes14-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes2-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes2-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes2-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes2-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes2-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes2-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes2-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes3-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes3-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes3-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes3-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes3-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes3-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes3-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes4-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes4-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes4-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes4-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes4-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes4-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes4-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes5-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes5-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes5-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes5-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes5-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes5-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes5-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes6-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes6-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes6-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes6-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes6-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes6-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes6-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes7-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes7-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes7-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes7-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes7-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes7-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes7-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes8-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes8-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes8-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes8-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes8-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes8-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes8-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes9-gaussian_filter-0-1.0-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes9-maximum_filter-1-3-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes9-median_filter-1-3-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes9-minimum_filter-1-3-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes9-percentile_filter-1-3-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes9-rank_filter-1-3-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_axes_kwargs[axes9-uniform_filter-1-3-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-convolve-args0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-correlate-args1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-gaussian_filter-args2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-maximum_filter-args5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-median_filter-args6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-minimum_filter-args4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-percentile_filter-args8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-rank_filter-args7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes0-uniform_filter-args3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-convolve-args0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-correlate-args1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-gaussian_filter-args2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-maximum_filter-args5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-median_filter-args6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-minimum_filter-args4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-percentile_filter-args8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-rank_filter-args7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes1-uniform_filter-args3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-convolve-args0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-correlate-args1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-gaussian_filter-args2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-maximum_filter-args5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-median_filter-args6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-minimum_filter-args4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-percentile_filter-args8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-rank_filter-args7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes2-uniform_filter-args3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-convolve-args0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-correlate-args1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-gaussian_filter-args2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-maximum_filter-args5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-median_filter-args6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-minimum_filter-args4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-percentile_filter-args8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-rank_filter-args7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_axes[axes3-uniform_filter-args3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes0-convolve-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes0-correlate-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes0-maximum_filter-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes0-median_filter-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes0-minimum_filter-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes0-percentile_filter-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes0-rank_filter-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes1-convolve-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes1-correlate-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes1-maximum_filter-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes1-median_filter-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes1-minimum_filter-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes1-percentile_filter-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes1-rank_filter-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes2-convolve-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes2-correlate-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes2-maximum_filter-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes2-median_filter-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes2-minimum_filter-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes2-percentile_filter-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[False-axes2-rank_filter-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes0-convolve-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes0-correlate-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes0-maximum_filter-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes0-median_filter-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes0-minimum_filter-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes0-percentile_filter-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes0-rank_filter-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes1-convolve-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes1-correlate-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes1-maximum_filter-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes1-median_filter-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes1-minimum_filter-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes1-percentile_filter-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes1-rank_filter-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes2-convolve-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes2-correlate-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes2-maximum_filter-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes2-median_filter-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes2-minimum_filter-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes2-percentile_filter-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_invalid_footprint_ndim[True-axes2-rank_filter-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[convolve-kwargs14-origin-0-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[convolve-kwargs14-origin-0-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[correlate-kwargs13-origin-0-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[correlate-kwargs13-origin-0-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs0-radius-3-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs0-radius-3-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs1-mode-constant-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs1-mode-constant-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs2-sigma-1.0-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs2-sigma-1.0-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs3-order-0-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[gaussian_filter-kwargs3-order-0-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[maximum_filter-kwargs10-size-3-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[maximum_filter-kwargs10-size-3-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[maximum_filter-kwargs11-mode-constant-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[maximum_filter-kwargs11-mode-constant-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[maximum_filter-kwargs12-origin-0-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[maximum_filter-kwargs12-origin-0-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[minimum_filter-kwargs7-size-3-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[minimum_filter-kwargs7-size-3-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[minimum_filter-kwargs8-mode-constant-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[minimum_filter-kwargs8-mode-constant-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[minimum_filter-kwargs9-origin-0-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[minimum_filter-kwargs9-origin-0-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[uniform_filter-kwargs4-size-3-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[uniform_filter-kwargs4-size-3-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[uniform_filter-kwargs5-mode-constant-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[uniform_filter-kwargs5-mode-constant-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[uniform_filter-kwargs6-origin-0-1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_tuple_length_mismatch[uniform_filter-kwargs6-origin-0-3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_weights_subset_axes_origins[convolve-kwargs0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_weights_subset_axes_origins[correlate-kwargs1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_weights_subset_axes_origins[maximum_filter-kwargs3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_weights_subset_axes_origins[median_filter-kwargs4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_weights_subset_axes_origins[minimum_filter-kwargs2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_weights_subset_axes_origins[percentile_filter-kwargs6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_filter_weights_subset_axes_origins[rank_filter-kwargs5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gauss01[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gauss02[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gauss03[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gauss04[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gauss05[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gauss06[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gauss_memory_overlap[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude01[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude01[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude02[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude02[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude02[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude02[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_gradient_magnitude02[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace01[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace01[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace02[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace02[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace02[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace02[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_gaussian_laplace02[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter01[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter1d01[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_gradient_magnitude01[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_laplace01[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace01[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace01[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace02[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace02[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace02[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace02[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_laplace02[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter01[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter02[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter03[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter04[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter05[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter06[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter07[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter08[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_maximum_filter09[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter01[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter02[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter03[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter04[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter05[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter05_overlap[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter06[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter07[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter08[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minimum_filter09[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes10-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes11-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes12-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes13-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes14-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[maximum_filter-kwargs1-axes9-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes10-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes11-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes12-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes13-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes14-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[median_filter-kwargs2-axes9-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes10-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes11-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes12-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes13-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes14-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[minimum_filter-kwargs0-axes9-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes10-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes11-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes12-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes13-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes14-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[percentile_filter-kwargs4-axes9-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes0-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes1-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes10-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes11-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes12-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes13-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes14-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes2-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes3-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes4-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes5-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes6-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes7-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_minmax_nonseparable_axes[rank_filter-kwargs3-axes9-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt01[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt02[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt03[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_prewitt04[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank01[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank02[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank03[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank04[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank05[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank06[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank06_overlap[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank07[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank08[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank09[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank10[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank11[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank12[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank13[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank14[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_rank15[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel01[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel02[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel03[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_sobel04[uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform01[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform01_complex[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform02[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform03[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform04[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform05[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[float64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[int8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint16-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint32-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint64-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-float32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-float64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-int16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-int32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-int64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-int8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-uint16-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-uint32-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-uint64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06[uint8-uint8-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06_complex[complex128-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06_complex[complex128-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06_complex[complex64-complex128-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_uniform06_complex[complex64-complex64-numpy]`
- `scipy/ndimage/tests/test_filters.py::TestThreading::test_correlate1d[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestThreading::test_correlate[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestThreading::test_median_filter[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestThreading::test_minmax_filter[numpy]`
- `scipy/ndimage/tests/test_filters.py::TestThreading::test_uniform_filter1d[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_bad_convolve_and_correlate_origins[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_byte_order_median[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_footprint_all_zeros[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_gaussian_filter[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_gaussian_kernel1d[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_gaussian_radius[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_gaussian_radius_invalid[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_gaussian_truncate[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_gh_5430[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_minmaximum_filter1d[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes_gaussian_gradient_magnitude[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes_gaussian_laplace[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes_laplace[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes_prewitt[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes_sequentially[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes_sobel[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_multiple_modes_uniform[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_orders_gauss[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_rank_filter_noninteger_rank[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_size_footprint_both_set[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_ticket_701[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_uniform_filter1d_roundoff_errors[numpy]`
- `scipy/ndimage/tests/test_filters.py::test_valid_origins[numpy]`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #20811: ENH: ndimage: extend filter axes support to remaining filters (`generic_filter`, etc.)

This MR includes the commits from #20809, so that one should be reviewed and merged first.

#### What does this implement/fix?

This is the second of two MRs that finish extending axes support to the remaining functions in the `_filters` submodule of ndimage. We added this support to several functions in 1.11 (#18016, #18261, #18305), but I did not complete the final set of functions at that time. This MR handles the functions `generic_filter`, `laplace`, `gaussian_laplace` and `gaussian_gradient_magnitude`.

cc @mdhaber as having reviewed prior, related MRs
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/scipy/ndimage/_filters.py b/scipy/ndimage/_filters.py
index d937e0a9ae762cb74f2bccc66c4e2e6ab0c85ed8..95f22d267cc4e0e0c52882d4aeb03de61cc6c088 100644
--- a/scipy/ndimage/_filters.py
+++ b/scipy/ndimage/_filters.py
@@ -553,7 +553,8 @@ def sobel(input, axis=-1, output=None, mode="reflect", cval=0.0):
 def generic_laplace(input, derivative2, output=None, mode="reflect",
                     cval=0.0,
                     extra_arguments=(),
-                    extra_keywords=None):
+                    extra_keywords=None,
+                    *, axes=None):
     """
     N-D Laplace filter using a provided second derivative function.
 
@@ -572,6 +573,9 @@ def generic_laplace(input, derivative2, output=None, mode="reflect",
     %(cval)s
     %(extra_keywords)s
     %(extra_arguments)s
+    axes : tuple of int or None
+        The axes over which to apply the filter. If a `mode` tuple is
+        provided, its length must match the number of axes.
 
     Returns
     -------
@@ -583,7 +587,7 @@ def generic_laplace(input, derivative2, output=None, mode="reflect",
         extra_keywords = {}
     input = np.asarray(input)
     output = _ni_support._get_output(output, input)
-    axes = list(range(input.ndim))
+    axes = _ni_support._check_axes(axes, input.ndim)
     if len(axes) > 0:
         modes = _ni_support._normalize_sequence(mode, len(axes))
         derivative2(input, axes[0], output, modes[0], cval,
@@ -598,7 +602,7 @@ def generic_laplace(input, derivative2, output=None, mode="reflect",
 
 
 @_ni_docstrings.docfiller
-def laplace(input, output=None, mode="reflect", cval=0.0):
+def laplace(input, output=None, mode="reflect", cval=0.0, *, axes=None):
     """N-D Laplace filter based on approximate second derivatives.
 
     Parameters
@@ -607,6 +611,9 @@ def laplace(input, output=None, mode="reflect", cval=0.0):
     %(output)s
     %(mode_multiple)s
     %(cval)s
+    axes : tuple of int or None
+        The axes over which to apply the filter. If a `mode` tuple is
+        provided, its length must match the number of axes.
 
     Returns
     -------
@@ -629,12 +636,12 @@ def laplace(input, output=None, mode="reflect", cval=0.0):
     """
     def derivative2(input, axis, output, mode, cval):
         return correlate1d(input, [1, -2, 1], axis, output, mode, cval, 0)
-    return generic_laplace(input, derivative2, output, mode, cval)
+    return generic_laplace(input, derivative2, output, mode, cval, axes=axes)
 
 
 @_ni_docstrings.docfiller
 def gaussian_laplace(input, sigma, output=None, mode="reflect",
-                     cval=0.0, **kwargs):
+                     cval=0.0, *, axes=None, **kwargs):
     """Multidimensional Laplace filter using Gaussian second derivatives.
 
     Parameters
@@ -647,6 +654,9 @@ def gaussian_laplace(input, sigma, output=None, mode="reflect",
     %(output)s
     %(mode_multiple)s
     %(cval)s
+    axes : tuple of int or None
+        The axes over which to apply the filter. If `sigma` or `mode` tuples
+        are provided, their length must match the number of axes.
     Extra keyword arguments will be passed to gaussian_filter().
 
     Returns
@@ -680,15 +690,27 @@ def gaussian_laplace(input, sigma, output=None, mode="reflect",
         return gaussian_filter(input, sigma, order, output, mode, cval,
                                **kwargs)
 
+    axes = _ni_support._check_axes(axes, input.ndim)
+    num_axes = len(axes)
+    sigma = _ni_support._normalize_sequence(sigma, num_axes)
+    if num_axes < input.ndim:
+        # set sigma = 0 for any axes not being filtered
+        sigma_temp = [0,] * input.ndim
+        for s, ax in zip(sigma, axes):
+            sigma_temp[ax] = s
+        sigma = sigma_temp
+
     return generic_laplace(input, derivative2, output, mode, cval,
                            extra_arguments=(sigma,),
-                           extra_keywords=kwargs)
+                           extra_keywords=kwargs,
+                           axes=axes)
 
 
 @_ni_docstrings.docfiller
 def generic_gradient_magnitude(input, derivative, output=None,
                                mode="reflect", cval=0.0,
-                               extra_arguments=(), extra_keywords=None):
+                               extra_arguments=(), extra_keywords=None,
+                               *, axes=None):
     """Gradient magnitude using a provided gradient function.
 
     Parameters
@@ -709,6 +731,9 @@ def generic_gradient_magnitude(input, derivative, output=None,
     %(cval)s
     %(extra_keywords)s
     %(extra_arguments)s
+    axes : tuple of int or None
+        The axes over which to apply the filter. If a `mode` tuple is
+        provided, its length must match the number of axes.
 
     Returns
     -------
@@ -720,7 +745,7 @@ def generic_gradient_magnitude(input, derivative, output=None,
         extra_keywords = {}
     input = np.asarray(input)
     output = _ni_support._get_output(output, input)
-    axes = list(range(input.ndim))
+    axes = _ni_support._check_axes(axes, input.ndim)
     if len(axes) > 0:
         modes = _ni_support._normalize_sequence(mode, len(axes))
         derivative(input, axes[0], output, modes[0], cval,
@@ -740,7 +765,8 @@ def generic_gradient_magnitude(input, derivative, output=None,
 
 @_ni_docstrings.docfiller
 def gaussian_gradient_magnitude(input, sigma, output=None,
-                                mode="reflect", cval=0.0, **kwargs):
+                                mode="reflect", cval=0.0, *, axes=None,
+                                **kwargs):
     """Multidimensional gradient magnitude using Gaussian derivatives.
 
     Parameters
@@ -753,6 +779,9 @@ def gaussian_gradient_magnitude(input, sigma, output=None,
     %(output)s
     %(mode_multiple)s
     %(cval)s
+    axes : tuple of int or None
+        The axes over which to apply the filter. If `sigma` or `mode` tuples
+        are provided, their length must match the number of axes.
     Extra keyword arguments will be passed to gaussian_filter().
 
     Returns
@@ -784,7 +813,7 @@ def gaussian_gradient_magnitude(input, sigma, output=None,
 
     return generic_gradient_magnitude(input, derivative, output, mode,
                                       cval, extra_arguments=(sigma,),
-                                      extra_keywords=kwargs)
+                                      extra_keywords=kwargs, axes=axes)
 
 
 def _correlate_or_convolve(input, weights, output, mode, cval, origin,
@@ -1772,7 +1801,7 @@ def generic_filter1d(input, function, filter_size, axis=-1,
 @_ni_docstrings.docfiller
 def generic_filter(input, function, size=None, footprint=None,
                    output=None, mode="reflect", cval=0.0, origin=0,
-                   extra_arguments=(), extra_keywords=None):
+                   extra_arguments=(), extra_keywords=None, *, axes=None):
     """Calculate a multidimensional filter using the given function.
 
     At each element the provided function is called. The input values
@@ -1791,6 +1820,12 @@ def generic_filter(input, function, size=None, footprint=None,
     %(origin_multiple)s
     %(extra_arguments)s
     %(extra_keywords)s
+    axes : tuple of int or None, optional
+        If None, `input` is filtered along all axes. Otherwise,
+        `input` is filtered along the specified axes. When `axes` is
+        specified, any tuples used for `size` or `origin` must match the length
+        of `axes`. The ith entry in any of these tuples corresponds to the ith
+        entry in `axes`.
 
     Returns
     -------
@@ -1877,23 +1912,31 @@ def generic_filter(input, function, size=None, footprint=None,
     input = np.asarray(input)
     if np.iscomplexobj(input):
         raise TypeError('Complex type not supported')
-    origins = _ni_support._normalize_sequence(origin, input.ndim)
+    axes = _ni_support._check_axes(axes, input.ndim)
+    num_axes = len(axes)
     if footprint is None:
         if size is None:
             raise RuntimeError("no footprint or filter size provided")
-        sizes = _ni_support._normalize_sequence(size, input.ndim)
+        sizes = _ni_support._normalize_sequence(size, num_axes)
         footprint = np.ones(sizes, dtype=bool)
     else:
         footprint = np.asarray(footprint, dtype=bool)
+
+    # expand origins, footprint if num_axes < input.ndim
+    footprint = _expand_footprint(input.ndim, axes, footprint)
+    origins = _expand_origin(input.ndim, axes, origin)
+
     fshape = [ii for ii in footprint.shape if ii > 0]
     if len(fshape) != input.ndim:
-        raise RuntimeError('filter footprint array has incorrect shape.')
+        raise RuntimeError(f"footprint.ndim ({footprint.ndim}) "
+                           f"must match len(axes) ({num_axes})")
     for origin, lenf in zip(origins, fshape):
         if (lenf // 2 + origin < 0) or (lenf // 2 + origin >= lenf):
             raise ValueError('invalid origin')
     if not footprint.flags.contiguous:
         footprint = footprint.copy()
     output = _ni_support._get_output(output, input)
+
     mode = _ni_support._extend_mode_to_code(mode)
     _nd_image.generic_filter(input, function, footprint, output, mode,
                              cval, origins, extra_arguments, extra_keywords)
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/scipy/ndimage/tests/test_filters.py b/scipy/ndimage/tests/test_filters.py
index 04603b83ec5e5436ce0ddfb97c33d77a8c008e52..b22fc76a3a0c29b89c7ae82be247a39f071202a2 100644
--- a/scipy/ndimage/tests/test_filters.py
+++ b/scipy/ndimage/tests/test_filters.py
@@ -917,11 +917,74 @@ class TestNdimageFilters:
 
         # result should be equivalent to sigma=0.0/size=1 on unfiltered axes
         axes = xp.asarray(axes)
-        all_sizes = (size if ax in (axes % array.ndim) else size0
-                     for ax in range(array.ndim))
+        all_sizes = tuple(size if ax in (axes % array.ndim) else size0
+                          for ax in range(array.ndim))
         expected = filter_func(array, *extra_args, all_sizes)
         xp_assert_close(output, expected)
 
+    @skip_xp_backends("cupy",
+                      reasons=["these filters do not yet have axes support"])
+    @pytest.mark.parametrize(('filter_func', 'kwargs'),
+                             [(ndimage.laplace, {}),
+                              (ndimage.gaussian_gradient_magnitude,
+                               {"sigma": 1.0}),
+                              (ndimage.gaussian_laplace, {"sigma": 0.5})])
+    def test_derivative_filter_axes(self, xp, filter_func, kwargs):
+        array = xp.arange(6 * 8 * 12, dtype=xp.float64)
+        array = xp.reshape(array, (6, 8, 12))
+
+        # duplicate axes raises an error
+        with pytest.raises(ValueError, match="axes must be unique"):
+            filter_func(array, axes=(1, 1), **kwargs)
+
+        # compare results to manually looping over the non-filtered axes
+        output = filter_func(array, axes=(1, 2), **kwargs)
+        expected = xp.empty_like(output)
+        expected = []
+        for i in range(array.shape[0]):
+            expected.append(filter_func(array[i, ...], **kwargs))
+        expected = xp.stack(expected, axis=0)
+        xp_assert_close(output, expected)
+
+        output = filter_func(array, axes=(0, -1), **kwargs)
+        expected = []
+        for i in range(array.shape[1]):
+            expected.append(filter_func(array[:, i, :], **kwargs))
+        expected = xp.stack(expected, axis=1)
+        xp_assert_close(output, expected)
+
+        output = filter_func(array, axes=(1), **kwargs)
+        expected = []
+        for i in range(array.shape[0]):
+            exp_inner = []
+            for j in range(array.shape[2]):
+                exp_inner.append(filter_func(array[i, :, j], **kwargs))
+            expected.append(xp.stack(exp_inner, axis=-1))
+        expected = xp.stack(expected, axis=0)
+        xp_assert_close(output, expected)
+
+    @skip_xp_backends("cupy",
+                      reasons=["generic_filter does not yet have axes support"])
+    @pytest.mark.parametrize(
+        'axes',
+        tuple(itertools.combinations(range(-3, 3), 1))
+        + tuple(itertools.combinations(range(-3, 3), 2))
+        + ((0, 1, 2),))
+    def test_generic_filter_axes(self, xp, axes):
+        array = xp.arange(6 * 8 * 12, dtype=xp.float64)
+        array = xp.reshape(array, (6, 8, 12))
+        size = 3
+        if len(set(ax % array.ndim for ax in axes)) != len(axes):
+            # parametrized cases with duplicate axes raise an error
+            with pytest.raises(ValueError, match="axes must be unique"):
+                ndimage.generic_filter(array, np.amax, size=size, axes=axes)
+            return
+
+        # choose np.amax as the function so we can compare to maximum_filter
+        output = ndimage.generic_filter(array, np.amax, size=size, axes=axes)
+        expected = ndimage.maximum_filter(array, size=size, axes=axes)
+        xp_assert_close(output, expected)
+
     @skip_xp_backends("cupy",
                       reasons=["https://github.com/cupy/cupy/pull/8339"])
     @pytest.mark.parametrize('func', [ndimage.correlate, ndimage.convolve])
@@ -1020,6 +1083,7 @@ class TestNdimageFilters:
         expected = filter_func(array, *args, size_3d, **kwargs)
         xp_assert_close(output, expected)
 
+
     @pytest.mark.parametrize("filter_func, kwargs",
                              [(ndimage.convolve, {}),
                               (ndimage.correlate, {}),
```

## Validation

```json
{
 "test_files": [
  "scipy/ndimage/tests/test_filters.py"
 ],
 "collected_before": 2262,
 "collected_after": 2262,
 "outcomes_before": {
  "PASSED": 2237,
  "FAILED": 25
 },
 "outcomes_after": {
  "PASSED": 2262
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes8-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes9-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes10-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes11-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes12-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes13-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes14-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes15-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes16-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes17-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes18-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes19-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes20-numpy]\nFAILED scipy/ndimage/tests/test_filters.py::TestNdimageFilters::test_generic_filter_axes[axes21-numpy]\n======================= 25 failed, 2237 passed in 14.11s =======================",
 "tail_after": "est_multiple_modes_gaussian_laplace[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_multiple_modes_gaussian_gradient_magnitude[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_multiple_modes_uniform[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_gaussian_truncate[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_gaussian_radius[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_gaussian_radius_invalid[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::TestThreading::test_correlate1d[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::TestThreading::test_correlate[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::TestThreading::test_median_filter[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::TestThreading::test_uniform_filter1d[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::TestThreading::test_minmax_filter[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_minmaximum_filter1d[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_uniform_filter1d_roundoff_errors[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_footprint_all_zeros[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_gaussian_filter[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_rank_filter_noninteger_rank[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_size_footprint_both_set[numpy]\nPASSED scipy/ndimage/tests/test_filters.py::test_byte_order_median[numpy]\n============================= 2262 passed in 9.93s =============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

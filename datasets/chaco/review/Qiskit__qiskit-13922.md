# Qiskit__qiskit-13922

[back to the list](README.md) -- **Better MCX Decomposition with logarithmic Toffoli Depth**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#13922](https://github.com/Qiskit/qiskit/pull/13922) (created 2025-02-25, merged 2025-03-25) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 423 developer test(s) flip; oracle reproduces it |
| base commit | [`d67c8182b67d`](https://github.com/Qiskit/qiskit/commit/d67c8182b67d9ddc79a871b8d9424d2111b8ecbe) (2025-03-25), first parent of the merge commit |
| merge commit | [`fbdf95081264`](https://github.com/Qiskit/qiskit/commit/fbdf95081264209b6cc483b2f92264128e2cc281) |
| issues closed | none |
| version | 2.1 |
| image | `f2p-chaco/qiskit__qiskit-13922:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-13922.Dockerfile) |
| source files (`patch`) | `qiskit/synthesis/__init__.py`, `qiskit/synthesis/multi_controlled/__init__.py`, `qiskit/synthesis/multi_controlled/mcx_synthesis.py`, `releasenotes/notes/better_mcx_synthesis-7e6e265147bc1d33.yaml` |
| test files (`test_patch`) | `test/python/synthesis/test_multi_controlled_synthesis.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (423)

- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_c3x`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_c4x`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_001`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_002`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_003`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_004`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_005`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_006`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_007`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_008`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_009`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_010`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_011`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_012`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_013`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_014`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_015`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_016`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_017`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_018`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_019`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_020`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_021`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_022`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_023`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_024`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_025`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_026`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_027`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_028`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_029`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_030`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_031`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_032`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_033`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_034`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_035`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_036`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_037`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_038`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_039`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_040`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_041`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_042`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_043`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_044`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_045`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_046`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_047`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_048`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_049`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_050`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_051`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_052`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_053`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_054`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_055`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_056`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_057`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_058`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_059`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_060`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_061`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_062`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_063`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_064`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_065`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_066`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_067`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_068`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_069`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_070`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_071`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_072`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_073`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_074`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_075`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_076`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_077`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_078`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_079`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_080`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_081`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_082`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_083`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_084`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_085`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_086`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_087`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_088`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_089`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_090`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_091`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_092`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_093`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_094`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_095`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_096`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_097`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_098`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_099`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_100`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_101`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_102`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_103`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_104`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_105`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_106`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_107`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_108`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_109`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_110`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_111`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_112`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_113`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_114`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_115`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_116`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_117`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_118`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_119`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_120`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_121`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_122`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_123`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_124`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_125`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_create_mc_gates_126`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_b95_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_b95_2_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_b95_3_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_b95_4_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_b95_5_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_b95_6_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_kg24_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_kg24_2_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_kg24_3_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_kg24_4_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_kg24_5_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_clean_kg24_6_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_dirty_kg24_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_dirty_kg24_2_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_dirty_kg24_3_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_dirty_kg24_4_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_dirty_kg24_5_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_1_dirty_kg24_6_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_clean_kg24_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_clean_kg24_2_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_clean_kg24_3_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_clean_kg24_4_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_clean_kg24_5_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_clean_kg24_6_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_dirty_kg24_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_dirty_kg24_2_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_dirty_kg24_3_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_dirty_kg24_4_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_dirty_kg24_5_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_2_dirty_kg24_6_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_gray_code_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_gray_code_2_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_gray_code_3_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_gray_code_4_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_gray_code_5_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_gray_code_6_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_clean_m15_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_clean_m15_2_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_clean_m15_3_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_clean_m15_4_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_dirty_i15_1_1`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_dirty_i15_2_2`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_dirty_i15_3_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_dirty_i15_4_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_dirty_i15_5_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_n_dirty_i15_6_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_1_1`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_2_2`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_3_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_4_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_5_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_6_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_7_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCorrectness::test_mcx_noaux_v24_8_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_c3x_cx_count`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_c4x_cx_count`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_1`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_2`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_4`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_6`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_7`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_8`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mc_rotation_gates_cx_count_9`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcu_noaux_cx_count_1_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcu_noaux_cx_count_2_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcu_noaux_cx_count_3_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_clean_b95_cx_count_1_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_clean_b95_cx_count_2_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_clean_b95_cx_count_3_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_clean_kg24_cx_count_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_clean_kg24_cx_count_2_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_clean_kg24_cx_count_3_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_clean_kg24_cx_count_4_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_dirty_kg24_cx_count_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_dirty_kg24_cx_count_2_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_dirty_kg24_cx_count_3_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_1_dirty_kg24_cx_count_4_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_clean_kg24_cx_count_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_clean_kg24_cx_count_2_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_clean_kg24_cx_count_3_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_clean_kg24_cx_count_4_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_dirty_kg24_cx_count_1_3`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_dirty_kg24_cx_count_2_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_dirty_kg24_cx_count_3_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_2_dirty_kg24_cx_count_4_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_01`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_02`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_03`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_04`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_05`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_06`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_07`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_08`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_09`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_11`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_12`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_13`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_14`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_16`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_17`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_18`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_19`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_20`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_21`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_22`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_23`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_24`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_25`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_26`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_27`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_28`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_29`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_30`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_31`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_32`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_33`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_34`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_35`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_36`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_37`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_38`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_39`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_40`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_41`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_42`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_43`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_44`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_45`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_46`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_47`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_48`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_49`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_50`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_51`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_52`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_53`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_54`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_equiv_noaux_cx_count_55`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_n_clean_m15_cx_count_1_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_n_clean_m15_cx_count_2_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_n_clean_m15_cx_count_3_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_n_dirty_i15_cx_count_1_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_n_dirty_i15_cx_count_2_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_n_dirty_i15_cx_count_3_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_noaux_v24_cx_count_1_5`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_noaux_v24_cx_count_2_10`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_mcx_noaux_v24_cx_count_3_15`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_001`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_002`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_003`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_004`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_005`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_006`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_007`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_008`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_009`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_010`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_011`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_012`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_013`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_014`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_015`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_016`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_017`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_018`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_019`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_020`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_021`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_022`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_023`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_024`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_025`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_026`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_027`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_028`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_029`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_030`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_031`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_032`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_033`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_034`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_035`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_036`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_037`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_038`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_039`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_040`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_041`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_042`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_043`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_044`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_045`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_046`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_047`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_048`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_049`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_050`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_051`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_052`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_053`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_054`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_055`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_056`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_057`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_058`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_059`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_060`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_061`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_062`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_063`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_064`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_065`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_066`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_067`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_068`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_069`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_070`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_071`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_072`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_073`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_074`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_075`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_076`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_077`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_078`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_079`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_080`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_081`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_082`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_083`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_084`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_085`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_086`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_087`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_088`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_089`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_090`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_091`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_092`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_093`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_094`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_095`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_096`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_097`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_098`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_099`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_100`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_101`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_102`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_103`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_104`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_105`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_106`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_107`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_108`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_109`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_110`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_111`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_112`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_113`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_114`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_115`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_116`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_117`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_118`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_119`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_120`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_121`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_122`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_123`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_124`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_125`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_126`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_127`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_128`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_129`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_130`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_131`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_132`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_133`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_134`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_135`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_136`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_137`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_138`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_139`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_140`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_141`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_142`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_143`
- `test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_144`

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #13922: Better MCX Decomposition with logarithmic Toffoli Depth

### Summary
Implement four new multi-controlled-x synthesis functions: `synth_mcx_1_clean_kg24`, `synth_mcx_1_dirty_kg24`, `synth_mcx_2_clean_kg24`, `synth_mcx_2_dirty_kg24` as discussed in #13913.

### Details and comments
Once implementations are confirmed, these should be added to the HLS transpiler synthesis plugin.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/synthesis/__init__.py b/qiskit/synthesis/__init__.py
index a41bc042aa9b70f79c36792a630ed356a6e6c586..ea33904fe81676ea858afa557a68b9bffbee9943 100644
--- a/qiskit/synthesis/__init__.py
+++ b/qiskit/synthesis/__init__.py
@@ -127,6 +127,10 @@ Multi Controlled Synthesis
 ==========================
 
 .. autofunction:: synth_mcmt_vchain
+.. autofunction:: synth_mcx_1_clean_kg24
+.. autofunction:: synth_mcx_1_dirty_kg24
+.. autofunction:: synth_mcx_2_clean_kg24
+.. autofunction:: synth_mcx_2_dirty_kg24
 .. autofunction:: synth_mcx_n_dirty_i15
 .. autofunction:: synth_mcx_n_clean_m15
 .. autofunction:: synth_mcx_1_clean_b95
@@ -220,6 +224,10 @@ from .two_qubit.two_qubit_decompose import (
 )
 from .multi_controlled import (
     synth_mcmt_vchain,
+    synth_mcx_1_clean_kg24,
+    synth_mcx_1_dirty_kg24,
+    synth_mcx_2_clean_kg24,
+    synth_mcx_2_dirty_kg24,
     synth_mcx_n_dirty_i15,
     synth_mcx_n_clean_m15,
     synth_mcx_1_clean_b95,
diff --git a/qiskit/synthesis/multi_controlled/__init__.py b/qiskit/synthesis/multi_controlled/__init__.py
index 0fa29553e7edfdccd015b2921d21e24ffbba97f0..bf1022ec8ff4cccffc3d55872bc1d4ec4dfc5567 100644
--- a/qiskit/synthesis/multi_controlled/__init__.py
+++ b/qiskit/synthesis/multi_controlled/__init__.py
@@ -14,6 +14,10 @@
 
 from .mcmt_vchain import synth_mcmt_vchain
 from .mcx_synthesis import (
+    synth_mcx_1_clean_kg24,
+    synth_mcx_1_dirty_kg24,
+    synth_mcx_2_clean_kg24,
+    synth_mcx_2_dirty_kg24,
     synth_mcx_n_dirty_i15,
     synth_mcx_n_clean_m15,
     synth_mcx_1_clean_b95,
diff --git a/qiskit/synthesis/multi_controlled/mcx_synthesis.py b/qiskit/synthesis/multi_controlled/mcx_synthesis.py
index a75c778c1bbdc2ac8f540e09ea7379f2bc18c726..c44b409f754c1c63279ab7bbbb891b3fecadceeb 100644
--- a/qiskit/synthesis/multi_controlled/mcx_synthesis.py
+++ b/qiskit/synthesis/multi_controlled/mcx_synthesis.py
@@ -12,11 +12,12 @@
 
 """Module containing multi-controlled circuits synthesis with and without ancillary qubits."""
 
+from __future__ import annotations
 from math import ceil
 import numpy as np
 
-from qiskit.circuit import QuantumRegister
-from qiskit.circuit.quantumcircuit import QuantumCircuit
+from qiskit.exceptions import QiskitError
+from qiskit.circuit.quantumcircuit import QuantumCircuit, QuantumRegister, AncillaRegister
 from qiskit.circuit.library.standard_gates import (
     HGate,
     CU1Gate,
@@ -305,6 +306,350 @@ def synth_mcx_noaux_v24(num_ctrl_qubits: int) -> QuantumCircuit:
     return qc
 
 
+def _linear_depth_ladder_ops(num_ladder_qubits: int) -> tuple[QuantumCircuit, list[int]]:
+    r"""
+    Helper function to create linear-depth ladder operations used in Khattar and Gidney's MCX synthesis.
+    In particular, this implements Step-1 and Step-2 on Fig. 3 of [1] except for the first and last
+    CCX gates.
+
+    Args:
+        num_ladder_qubits: No. of qubits involved in the ladder operation.
+
+    Returns:
+        A tuple consisting of the linear-depth ladder circuit and the index of control qubit to
+        apply the final CCX gate.
+
+    Raises:
+        QiskitError: If num_ladder_qubits <= 2.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    if num_ladder_qubits <= 2:
+        raise QiskitError("n_ctrls >= 3 to use MCX ladder. Otherwise, use CCX")
+
+    n = num_ladder_qubits + 1
+    qc = QuantumCircuit(n)
+    qreg = list(range(n))
+
+    # up-ladder
+    for i in range(2, n - 2, 2):
+        qc.ccx(qreg[i + 1], qreg[i + 2], qreg[i])
+        qc.x(qreg[i])
+
+    # down-ladder
+    if n % 2 != 0:
+        a, b, target = n - 3, n - 5, n - 6
+    else:
+        a, b, target = n - 1, n - 4, n - 5
+
+    if target > 0:
+        qc.ccx(qreg[a], qreg[b], qreg[target])
+        qc.x(qreg[target])
+
+    for i in range(target, 2, -2):
+        qc.ccx(qreg[i], qreg[i - 1], qreg[i - 2])
+        qc.x(qreg[i - 2])
+
+    mid_second_ctrl = 1 + max(0, 6 - n)
+    final_ctrl = qreg[mid_second_ctrl] - 1
+    return qc, final_ctrl
+
+
+def synth_mcx_1_kg24(num_ctrl_qubits: int, clean: bool = True) -> QuantumCircuit:
+    r"""
+    Synthesize a multi-controlled X gate with :math:`k` controls using :math:`1` ancillary qubit as
+    described in Sec. 5 of [1].
+
+    Args:
+        num_ctrl_qubits: The number of control qubits.
+        clean: If True, the ancilla is clean, otherwise it is dirty.
+
+    Returns:
+        The synthesized quantum circuit.
+
+    Raises:
+        QiskitError: If num_ctrl_qubits <= 2.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    if num_ctrl_qubits <= 2:
+        raise QiskitError("kg24 synthesis requires at least 3 control qubits. Use CCX directly.")
+
+    q_controls = QuantumRegister(num_ctrl_qubits, name="ctrl")
+    q_target = QuantumRegister(1, name="targ")
+    q_ancilla = AncillaRegister(1, name="anc")
+    qc = QuantumCircuit(q_controls, q_target, q_ancilla, name="mcx_linear_depth")
+
+    ladder_ops, final_ctrl = _linear_depth_ladder_ops(num_ctrl_qubits)
+    qc.ccx(q_controls[0], q_controls[1], q_ancilla)  #                  # create cond. clean ancilla
+    qc.compose(ladder_ops, q_ancilla[:] + q_controls[:], inplace=True)  # up-ladder
+    qc.ccx(q_ancilla, q_controls[final_ctrl], q_target)  #              # target
+    qc.compose(  #                                                      # down-ladder
+        ladder_ops.inverse(),
+        q_ancilla[:] + q_controls[:],
+        inplace=True,
+    )
+    qc.ccx(q_controls[0], q_controls[1], q_ancilla)
+
+    if not clean:
+        # perform toggle-detection if ancilla is dirty
+        qc.compose(ladder_ops, q_ancilla[:] + q_controls[:], inplace=True)
+        qc.ccx(q_ancilla, q_controls[final_ctrl], q_target)
+        qc.compose(ladder_ops.inverse(), q_ancilla[:] + q_controls[:], inplace=True)
+
+    return qc
+
+
+def synth_mcx_1_clean_kg24(num_ctrl_qubits: int) -> QuantumCircuit:
+    r"""
+    Synthesize a multi-controlled X gate with :math:`k` controls using :math:`1` clean ancillary qubit
+    producing a circuit with :math:`2k-3` Toffoli gates and depth :math:`O(k)` as described in
+    Sec. 5.1 of [1].
+
+    Args:
+        num_ctrl_qubits: The number of control qubits.
+
+    Returns:
+        The synthesized quantum circuit.
+
+    Raises:
+        QiskitError: If num_ctrl_qubits <= 2.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    return synth_mcx_1_kg24(num_ctrl_qubits, clean=True)
+
+
+def synth_mcx_1_dirty_kg24(num_ctrl_qubits: int) -> QuantumCircuit:
+    r"""
+    Synthesize a multi-controlled X gate with :math:`k` controls using :math:`1` dirty ancillary qubit
+    producing a circuit with :math:`4k-8` Toffoli gates and depth :math:`O(k)` as described in
+    Sec. 5.3 of [1].
+
+    Args:
+        num_ctrl_qubits: The number of control qubits.
+
+    Returns:
+        The synthesized quantum circuit.
+
+    Raises:
+        QiskitError: If num_ctrl_qubits <= 2.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    return synth_mcx_1_kg24(num_ctrl_qubits, clean=False)
+
+
+def _n_parallel_ccx_x(n: int) -> QuantumCircuit:
+    r"""
+    Construct a quantum circuit for creating n-condionally clean ancillae using 3n qubits. This
+    implements Fig. 4a of [1]. The order of returned qubits is qr_a, qr_a, qr_target.
+
+    Args:
+        n: Number of conditionally clean ancillae to create.
+
+    Returns:
+        QuantumCircuit: The quantum circuit for creating n-condionally clean ancillae.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    n_qubits = 3 * n
+    q = QuantumRegister(n_qubits, name="q")
+    qc = QuantumCircuit(q, name=f"ccxn_{n}")
+    qr_a, qr_b, qr_target = q[:n], q[n : 2 * n], q[2 * n :]
+    qc.x(qr_target)
+    qc.ccx(qr_a, qr_b, qr_target)
+
+    return qc
+
+
+def _build_logn_depth_ccx_ladder(
+    ancilla_idx: int, ctrls: list[int], skip_cond_clean: bool = False
+) -> tuple[QuantumCircuit, list[int]]:
+    r"""
+    Helper function to build a log-depth ladder compose of CCX and X gates as shown in Fig. 4b of [1].
+
+    Args:
+        ancilla_idx: Index of the ancillary qubit.
+        ctrls: List of control qubits.
+        skip_cond_clean: If True, do not include the conditionally clean ancilla (step 1 and 5 in
+            Fig. 4b of [1]).
+
+    Returns:
+        A tuple consisting of the log-depth ladder circuit of conditionally clean ancillae and the
+        list of indices of control qubit to apply the linear-depth MCX gate.
+
+    Raises:
+        QiskitError: If no. of qubits in parallel CCX + X gates are not the same.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    qc = QuantumCircuit(len(ctrls) + 1)
+    anc = [ancilla_idx]
+    final_ctrls = []
+
+    while len(ctrls) > 1:
+        next_batch_len = min(len(anc) + 1, len(ctrls))
+        ctrls, nxt_batch = ctrls[next_batch_len:], ctrls[:next_batch_len]
+        new_anc = []
+        while len(nxt_batch) > 1:
+            ccx_n = len(nxt_batch) // 2
+            st = int(len(nxt_batch) % 2)
+            ccx_x, ccx_y, ccx_t = (
+                nxt_batch[st : st + ccx_n],
+                nxt_batch[st + ccx_n :],
+                anc[-ccx_n:],
+            )
+            if not len(ccx_x) == len(ccx_y) == ccx_n >= 1:
+                raise QiskitError(
+                    f"Invalid CCX gate parameters: {len(ccx_x)=} != {len(ccx_y)=} != {len(ccx_n)=}"
+                )
+            if ccx_t != [ancilla_idx]:
+                qc.compose(_n_parallel_ccx_x(ccx_n), ccx_x + ccx_y + ccx_t, inplace=True)
+            else:
+                if not skip_cond_clean:
+                    qc.ccx(ccx_x[0], ccx_y[0], ccx_t[0])  #  # create conditionally clean ancilla
+            new_anc += nxt_batch[st:]  #                     # newly created cond. clean ancilla
+            nxt_batch = ccx_t + nxt_batch[:st]
+            anc = anc[:-ccx_n]
+
+        anc = sorted(anc + new_anc)
+        final_ctrls += nxt_batch
+
+    final_ctrls += ctrls
+    final_ctrls = sorted(final_ctrls)
+    return qc, final_ctrls[:-1]  # exclude ancilla
+
+
+def synth_mcx_2_kg24(num_ctrl_qubits: int, clean: bool = True) -> QuantumCircuit:
+    r"""
+    Synthesize a multi-controlled X gate with :math:`k` controls using :math:`2` ancillary qubits.
+    as described in Sec. 5 of [1].
+
+    Args:
+        num_ctrl_qubits: The number of control qubits.
+        clean: If True, the ancilla is clean, otherwise it is dirty.
+
+    Returns:
+        The synthesized quantum circuit.
+
+    Raises:
+        QiskitError: If num_ctrl_qubits <= 2.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    if num_ctrl_qubits <= 2:
+        raise QiskitError("kg24 synthesis requires at least 3 control qubits. Use CCX directly.")
+
+    q_control = QuantumRegister(num_ctrl_qubits, name="ctrl")
+    q_target = QuantumRegister(1, name="targ")
+    q_ancilla = AncillaRegister(2, name="anc")
+    qc = QuantumCircuit(q_control, q_target, q_ancilla, name="mcx_logn_depth")
+
+    ladder_ops, final_ctrls = _build_logn_depth_ccx_ladder(
+        num_ctrl_qubits, list(range(num_ctrl_qubits))
+    )
+    qc.compose(ladder_ops, q_control[:] + [q_ancilla[0]], inplace=True)
+    if len(final_ctrls) == 1:  # Already a toffoli
+        qc.ccx(q_ancilla[0], q_control[final_ctrls[0]], q_target)
+    else:
+        mid_mcx = synth_mcx_1_clean_kg24(len(final_ctrls) + 1)
+        qc.compose(
+            mid_mcx,
+            [q_ancilla[0]]
+            + q_control[final_ctrls]
+            + q_target[:]
+            + [q_ancilla[1]],  # ctrls, targ, anc
+            inplace=True,
+        )
+    qc.compose(ladder_ops.inverse(), q_control[:] + [q_ancilla[0]], inplace=True)
+
+    if not clean:
+        # perform toggle-detection if ancilla is dirty
+        ladder_ops_new, final_ctrls = _build_logn_depth_ccx_ladder(
+            num_ctrl_qubits, list(range(num_ctrl_qubits)), skip_cond_clean=True
+        )
+        qc.compose(ladder_ops_new, q_control[:] + [q_ancilla[0]], inplace=True)
+        if len(final_ctrls) == 1:
+            qc.ccx(q_ancilla[0], q_control[final_ctrls[0]], q_target)
+        else:
+            qc.compose(
+                mid_mcx,
+                [q_ancilla[0]] + q_control[final_ctrls] + q_target[:] + [q_ancilla[1]],
+                inplace=True,
+            )
+        qc.compose(ladder_ops_new.inverse(), q_control[:] + [q_ancilla[0]], inplace=True)
+
+    return qc
+
+
+def synth_mcx_2_clean_kg24(num_ctrl_qubits: int) -> QuantumCircuit:
+    r"""
+    Synthesize a multi-controlled X gate with :math:`k` controls using :math:`2` clean ancillary qubits
+    producing a circuit with :math:`2k-3` Toffoli gates and depth :math:`O(\log(k))` as described in
+    Sec. 5.2 of [1].
+
+    Args:
+        num_ctrl_qubits: The number of control qubits.
+
+    Returns:
+        The synthesized quantum circuit.
+
+    Raises:
+        QiskitError: If num_ctrl_qubits <= 2.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    return synth_mcx_2_kg24(num_ctrl_qubits, clean=True)
+
+
+def synth_mcx_2_dirty_kg24(num_ctrl_qubits: int) -> QuantumCircuit:
+    r"""
+    Synthesize a multi-controlled X gate with :math:`k` controls using :math:`2` dirty ancillary qubits
+    producing a circuit with :math:`4k-8` Toffoli gates and depth :math:`O(\log(k))` as described in
+    Sec. 5.4 of [1].
+
+    Args:
+        num_ctrl_qubits: The number of control qubits.
+
+    Returns:
+        The synthesized quantum circuit.
+
+    Raises:
+        QiskitError: If num_ctrl_qubits <= 2.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    return synth_mcx_2_kg24(num_ctrl_qubits, clean=False)
+
+
 def synth_c3x() -> QuantumCircuit:
     """Efficient synthesis of 3-controlled X-gate."""
 
diff --git a/releasenotes/notes/better_mcx_synthesis-7e6e265147bc1d33.yaml b/releasenotes/notes/better_mcx_synthesis-7e6e265147bc1d33.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..9a79a706f750a05c8aec31bad0cbaaf7ca2073b4
--- /dev/null
+++ b/releasenotes/notes/better_mcx_synthesis-7e6e265147bc1d33.yaml
@@ -0,0 +1,21 @@
+---
+features_synthesis:
+  - |
+    Added new decompositions for :class:`.MCXGate` utilizing clean ancillae, improving circuit
+    depth and efficiency:
+    
+    * :func:`.synth_mcx_1_clean_kg24`, using 1 additional clean ancilla qubit
+    * :func:`.synth_mcx_1_dirty_kg24`, using 1 additional dirty ancilla qubit
+    * :func:`.synth_mcx_2_clean_kg24`, using 2 additional clean ancillary qubits
+    * :func:`.synth_mcx_2_dirty_kg24`, using 2 additional dirty ancillary qubits
+
+    Example usage:
+
+    .. code-block:: python
+        
+        from qiskit.synthesis.multi_controlled import synth_mcx_1_clean_kg24
+        
+        n_ctrls = 10
+        qc = synth_mcx_1_clean_kg24(n_ctrls)
+        qc.draw()
+
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/synthesis/test_multi_controlled_synthesis.py b/test/python/synthesis/test_multi_controlled_synthesis.py
index ac24f4ce282ad637fd91d599cfd6d9c7dbb7c442..ec148787feadd82016a8c6fcb53c29c1a1a1094b 100644
--- a/test/python/synthesis/test_multi_controlled_synthesis.py
+++ b/test/python/synthesis/test_multi_controlled_synthesis.py
@@ -43,6 +43,10 @@ from qiskit.synthesis.multi_controlled import (
     synth_mcx_n_dirty_i15,
     synth_mcx_n_clean_m15,
     synth_mcx_1_clean_b95,
+    synth_mcx_1_clean_kg24,
+    synth_mcx_1_dirty_kg24,
+    synth_mcx_2_clean_kg24,
+    synth_mcx_2_dirty_kg24,
     synth_mcx_gray_code,
     synth_mcx_noaux_v24,
     synth_c3x,
@@ -134,6 +138,42 @@ class TestMCSynthesisCorrectness(QiskitTestCase):
             XGate(), num_ctrl_qubits, synthesized_circuit, clean_ancillas=True
         )
 
+    @data(3, 4, 5, 6, 7, 8)
+    def test_mcx_1_clean_kg24(self, num_ctrl_qubits: int):
+        """Test synth_mcx_1_clean_kg24 by comparing synthesized and expected matrices."""
+        # Note: the method requires at least 3 control qubits
+        synthesized_circuit = synth_mcx_1_clean_kg24(num_ctrl_qubits)
+        self.assertSynthesisCorrect(
+            XGate(), num_ctrl_qubits, synthesized_circuit, clean_ancillas=True
+        )
+
+    @data(3, 4, 5, 6, 7, 8)
+    def test_mcx_1_dirty_kg24(self, num_ctrl_qubits: int):
+        """Test synth_mcx_1_dirty_kg24 by comparing synthesized and expected matrices."""
+        # Note: the method requires at least 3 control qubits
+        synthesized_circuit = synth_mcx_1_dirty_kg24(num_ctrl_qubits)
+        self.assertSynthesisCorrect(
+            XGate(), num_ctrl_qubits, synthesized_circuit, clean_ancillas=False
+        )
+
+    @data(3, 4, 5, 6, 7, 8)
+    def test_mcx_2_clean_kg24(self, num_ctrl_qubits: int):
+        """Test synth_mcx_2_clean_kg24 by comparing synthesized and expected matrices."""
+        # Note: the method requires at least 3 control qubits
+        synthesized_circuit = synth_mcx_2_clean_kg24(num_ctrl_qubits)
+        self.assertSynthesisCorrect(
+            XGate(), num_ctrl_qubits, synthesized_circuit, clean_ancillas=True
+        )
+
+    @data(3, 4, 5, 6, 7, 8)
+    def test_mcx_2_dirty_kg24(self, num_ctrl_qubits: int):
+        """Test synth_mcx_2_dirty_kg24 by comparing synthesized and expected matrices."""
+        # Note: the method requires at least 3 control qubits
+        synthesized_circuit = synth_mcx_2_dirty_kg24(num_ctrl_qubits)
+        self.assertSynthesisCorrect(
+            XGate(), num_ctrl_qubits, synthesized_circuit, clean_ancillas=False
+        )
+
     @data(3, 4, 5, 6, 7, 8)
     def test_mcx_gray_code(self, num_ctrl_qubits: int):
         """Test synth_mcx_gray_code by comparing synthesized and expected matrices."""
@@ -232,6 +272,46 @@ class TestMCSynthesisCounts(QiskitTestCase):
         # The bound from the documentation of synth_mcx_1_clean_b95
         self.assertLessEqual(cx_count, 16 * num_ctrl_qubits - 8)
 
+    @data(3, 5, 10, 15)
+    def test_mcx_1_clean_kg24_cx_count(self, num_ctrl_qubits: int):
+        """Test synth_mcx_1_clean_kg24 bound on CX count."""
+        synthesized_circuit = synth_mcx_1_clean_kg24(num_ctrl_qubits)
+        transpiled_circuit = self.pm.run(synthesized_circuit)
+        cx_count = transpiled_circuit.count_ops()["cx"]
+        # Based on the bound from the Sec 5.1 of arXiv:2407.17966, assuming Toffoli decomposition
+        # requires 6 CX gates.
+        self.assertLessEqual(cx_count, 12 * num_ctrl_qubits - 18)
+
+    @data(3, 5, 10, 15)
+    def test_mcx_1_dirty_kg24_cx_count(self, num_ctrl_qubits: int):
+        """Test synth_mcx_1_dirty_kg24 bound on CX count."""
+        synthesized_circuit = synth_mcx_1_dirty_kg24(num_ctrl_qubits)
+        transpiled_circuit = self.pm.run(synthesized_circuit)
+        cx_count = transpiled_circuit.count_ops()["cx"]
+        ## Based on the bound from the Sec 5.3 of arXiv:2407.17966, assuming Toffoli decomposition
+        # requires 6 CX gates.
+        self.assertLessEqual(cx_count, 24 * num_ctrl_qubits - 48)
+
+    @data(3, 5, 10, 15)
+    def test_mcx_2_clean_kg24_cx_count(self, num_ctrl_qubits: int):
+        """Test synth_mcx_2_clean_kg24 bound on CX count."""
+        synthesized_circuit = synth_mcx_2_clean_kg24(num_ctrl_qubits)
+        transpiled_circuit = self.pm.run(synthesized_circuit)
+        cx_count = transpiled_circuit.count_ops()["cx"]
+        # Based on the bound from the Sec 5.2 of arXiv:2407.17966, assuming Toffoli decomposition
+        # requires 6 CX gates.
+        self.assertLessEqual(cx_count, 12 * num_ctrl_qubits - 18)
+
+    @data(3, 5, 10, 15)
+    def test_mcx_2_dirty_kg24_cx_count(self, num_ctrl_qubits: int):
+        """Test synth_mcx_2_dirty_kg24 bound on CX count."""
+        synthesized_circuit = synth_mcx_2_dirty_kg24(num_ctrl_qubits)
+        transpiled_circuit = self.pm.run(synthesized_circuit)
+        cx_count = transpiled_circuit.count_ops()["cx"]
+        # Based on the bound from the Sec 5.4 of arXiv:2407.17966, assuming Toffoli decomposition
+        # requires 6 CX gates.
+        self.assertLessEqual(cx_count, 24 * num_ctrl_qubits - 48)
+
     def test_c3x_cx_count(self):
         """Test synth_c3x bound on CX count."""
         synthesized_circuit = synth_c3x()
```

## Validation

```json
{
 "test_files": [
  "test/python/synthesis/test_multi_controlled_synthesis.py"
 ],
 "collected_before": 424,
 "collected_after": 423,
 "outcomes_before": {
  "ERROR": 424
 },
 "outcomes_after": {
  "PASSED": 423
 },
 "exit_before": 2,
 "exit_after": 0,
 "tail_before": "============================= test session starts ==============================\nplatform linux -- Python 3.11.17, pytest-8.1.2, pluggy-1.5.0 -- /usr/local/bin/python\nhypothesis profile 'default' -> database=DirectoryBasedExampleDatabase(PosixPath('/testbed/.hypothesis/examples'))\nrootdir: /testbed\nconfigfile: pyproject.toml\nplugins: hypothesis-6.130.4\ncollecting ... collected 0 items / 1 error\n\n==================================== ERRORS ====================================\n__ ERROR collecting test/python/synthesis/test_multi_controlled_synthesis.py ___\nImportError while importing test module '/testbed/test/python/synthesis/test_multi_controlled_synthesis.py'.\nHint: make sure your test modules/packages have valid Python names.\nTraceback:\n/usr/local/lib/python3.11/importlib/__init__.py:126: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\ntest/python/synthesis/test_multi_controlled_synthesis.py:42: in <module>\n    from qiskit.synthesis.multi_controlled import (\nE   ImportError: cannot import name 'synth_mcx_1_clean_kg24' from 'qiskit.synthesis.multi_controlled' (/testbed/qiskit/synthesis/multi_controlled/__init__.py)\n=========================== short test summary info ============================\nERROR test/python/synthesis/test_multi_controlled_synthesis.py\n!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!\n=============================== 1 error in 2.76s ===============================",
 "tail_after": "t_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_133\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_134\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_135\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_136\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_137\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_138\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_139\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_140\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_141\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_142\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_143\nPASSED test/python/synthesis/test_multi_controlled_synthesis.py::TestMCSynthesisCounts::test_small_mc_gates_cx_count_144\n================ 423 passed, 1658 warnings in 92.76s (0:01:32) =================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

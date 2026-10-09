# Qiskit__qiskit-14143

[back to the list](README.md) -- **HLS plugin for new MCX Decompositions**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#14143](https://github.com/Qiskit/qiskit/pull/14143) (created 2025-04-01, merged 2025-04-07) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 151 developer test(s) flip; oracle reproduces it |
| base commit | [`f72eb246bdb4`](https://github.com/Qiskit/qiskit/commit/f72eb246bdb45c0728c903ef68bce810e402df4d) (2025-04-07), first parent of the merge commit |
| merge commit | [`a6a2fcd7ab03`](https://github.com/Qiskit/qiskit/commit/a6a2fcd7ab03e55edf8c880d011334a3e1a6e23b) |
| issues closed | none |
| version | 2.1 |
| image | `f2p-chaco/qiskit__qiskit-14143:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-14143.Dockerfile) |
| source files (`patch`) | `pyproject.toml`, `qiskit/transpiler/passes/synthesis/hls_plugins.py`, `releasenotes/notes/add-new-mcx-plugins-2177db9195e2b680.yaml` |
| test files (`test_patch`) | `test/python/transpiler/test_high_level_synthesis.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (151)

- `test/python/transpiler/test_high_level_synthesis.py::TestAnnotatedSynthesisPlugins::test_conjugate_reduction_applies_1`
- `test/python/transpiler/test_high_level_synthesis.py::TestAnnotatedSynthesisPlugins::test_conjugate_reduction_applies_2`
- `test/python/transpiler/test_high_level_synthesis.py::TestAnnotatedSynthesisPlugins::test_conjugate_reduction_not_applies_1`
- `test/python/transpiler/test_high_level_synthesis.py::TestAnnotatedSynthesisPlugins::test_conjugate_reduction_not_applies_2`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_ancilla_arguments`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_ancilla_noop`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_ancilla_reset_1_True`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_ancilla_reset_2_False`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_ancilla_state_maintained`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_both_basis_gates_and_plugin_specified`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_coupling_map_gets_passed_to_plugins`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_default_config`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_multiple_methods`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_multiple_methods_short_form`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_no_config`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_non_default_config`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_qubits_get_passed_to_plugins`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_skip_synthesis_with_empty_methods_list`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_synth_fails_definition_exists`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_synthesis_returns_none`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_synthesis_using_alternate_form`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_synthesis_using_alternate_short_form`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_target_gets_passed_to_plugins`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_track_global_phase`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_use_default_on_unspecified_is_false`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisInterface::test_use_default_on_unspecified_is_true`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_annotated_circuit`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_annotated_circuit_with_phase`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_annotated_gate`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_annotated_rec`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_annotated_rec_with_control_states`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_annotated_with_empty_modifiers`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_circuit_with_mcx`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_circuit_with_mcx_def`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_circuit_with_mcx_def_rec`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_circuit_with_recursive_def`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_circuit_with_recursive_def2`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_circuit_with_recursive_def3`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_control_basic_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_control_clifford`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_control_custom_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_control_high_level_object`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_definition_with_annotations`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_definition_with_high_level_objects`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_inverse_basic_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_inverse_clifford`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_inverse_custom_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_inverse_high_level_object`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_multiple_controls`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_multiple_powers`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_nested_controls`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_nested_controls_permutation`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_nested_inverses`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_nested_inverses_permutation`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_nested_powers`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_nested_powers_permutation`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_power_custom_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_power_float_basic_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_power_float_clifford`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_power_high_level_object`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_power_negint_basic_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_power_posint_basic_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_power_posint_clifford`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_reordered_modifiers`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_simple_circuit`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_simple_circuit2`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_three_inverses`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_transpile_control_high_level_object`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_transpile_inverse_high_level_object`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_transpile_power_high_level_object`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisModifiers::test_two_inverses`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_controlled_cx`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_controlled_cz`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_controlled_qft`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_controlled_qft_adder`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_controlled_x`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_controlled_z`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_recursively_controlled_cx`
- `test/python/transpiler/test_high_level_synthesis.py::TestHighLevelSynthesisQuality::test_recursively_controlled_cz`
- `test/python/transpiler/test_high_level_synthesis.py::TestKMSSynthesisLinearFunctionPlugin::test_invert_and_transpose`
- `test/python/transpiler/test_high_level_synthesis.py::TestKMSSynthesisLinearFunctionPlugin::test_unfortunate_name`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_annotated_mcx`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_applicability`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_01_n_clean_m15`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_02_n_dirty_i15`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_07_1_clean_b95`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_08_noaux_v24`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_09_gray_code`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_10_default`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_01_n_clean_m15`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_02_n_dirty_i15`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_07_1_clean_b95`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_08_noaux_v24`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_09_gray_code`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_10_default`
- `test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_supported_names`
- `test/python/transpiler/test_high_level_synthesis.py::TestPMHSynthesisLinearFunctionPlugin::test_invert_and_transpose`
- `test/python/transpiler/test_high_level_synthesis.py::TestPMHSynthesisLinearFunctionPlugin::test_plugin_selection_all`
- `test/python/transpiler/test_high_level_synthesis.py::TestPMHSynthesisLinearFunctionPlugin::test_plugin_selection_all_with_metrix`
- `test/python/transpiler/test_high_level_synthesis.py::TestPMHSynthesisLinearFunctionPlugin::test_section_size`
- `test/python/transpiler/test_high_level_synthesis.py::TestPMHSynthesisLinearFunctionPlugin::test_unfortunate_name`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_correctness_1_default`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_correctness_2_rustiq`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_rustiq_preserve_order`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_rustiq_upto_options`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_rustiq_upto_phase`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_rustiq_with_parameterized_angles`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_supported_names`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_trivial_rotations_1_default`
- `test/python/transpiler/test_high_level_synthesis.py::TestPauliEvolutionSynthesisPlugins::test_trivial_rotations_2_rustiq`
- `test/python/transpiler/test_high_level_synthesis.py::TestQFTSynthesisPlugins::test_qft_line_plugin_annotated_qft_1_line`
- `test/python/transpiler/test_high_level_synthesis.py::TestQFTSynthesisPlugins::test_qft_line_plugin_annotated_qft_2_full`
- `test/python/transpiler/test_high_level_synthesis.py::TestQFTSynthesisPlugins::test_qft_plugins_qft_1_line`
- `test/python/transpiler/test_high_level_synthesis.py::TestQFTSynthesisPlugins::test_qft_plugins_qft_2_full`
- `test/python/transpiler/test_high_level_synthesis.py::TestQFTSynthesisPlugins::test_skip_non_qft_1_line`
- `test/python/transpiler/test_high_level_synthesis.py::TestQFTSynthesisPlugins::test_skip_non_qft_2_full`
- `test/python/transpiler/test_high_level_synthesis.py::TestQFTSynthesisPlugins::test_supported_names`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_abstract_synthesis`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_abstract_synthesis_all_permutations`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_concrete_synthesis`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_concrete_synthesis_all_permutations`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_concrete_synthesis_is_not_possible`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_concrete_synthesis_over_disconnected_qubits`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_token_swapper_in_known_plugin_names`
- `test/python/transpiler/test_high_level_synthesis.py::TestTokenSwapperPermutationPlugin::test_unfortunate_name`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_dont_unroll_a_gate_in_basis_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_dont_unroll_a_gate_in_basis_gates_with_target`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_dont_unroll_a_gate_in_eq_lib`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_if_else`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_leave_store_alone_basis`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_leave_store_alone_with_target`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_nested_control_flow`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_raise_for_opaque_not_in_eq_lib`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_raise_for_opaque_not_in_eq_lib_target_with_target`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_unroll_empty_definition`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_unroll_empty_definition_with_phase`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_unroll_gate_until_reach_basis_gates`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_unroll_gate_until_reach_basis_gates_with_target`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_unroll_twice_until_we_get_to_eqlib`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollCustomDefinitionsCompatibility::test_unroll_twice_until_we_get_to_eqlib_with_target`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_basic_unroll`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_basic_unroll_min_qubits`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_definition_unroll_parameterized`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_simple_unroll_parameterized_with_expressions`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_simple_unroll_parameterized_without_expressions`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_unroll_all_instructions`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_unroll_no_basis`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_unroll_toffoli`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_unroll_toffoli_min_qubits`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_unroll_with_clbit`
- `test/python/transpiler/test_high_level_synthesis.py::TestUnrollerCompatability::test_unrolling_parameterized_composite_gates`

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #14143: HLS plugin for new MCX Decompositions

### Summary
Add HLS passes for recently added `synth_mcx_2_clean_kg24, synth_mcx_2_dirty_kg24, synth_mcx_1_clean_kg24, synth_mcx_1_dirty_kg24` in #13922.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/pyproject.toml b/pyproject.toml
index 86c505a72db04436ca996e9945bb3c5c07021c6e..50539937f110020b5f58a69ad2e6a962f625d4de 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -86,6 +86,10 @@ sk = "qiskit.transpiler.passes.synthesis.solovay_kitaev_synthesis:SolovayKitaevS
 "linear_function.pmh" = "qiskit.transpiler.passes.synthesis.hls_plugins:PMHSynthesisLinearFunction"
 "mcx.n_dirty_i15" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesisNDirtyI15"
 "mcx.n_clean_m15" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesisNCleanM15"
+"mcx.2_clean_kg24" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesis2CleanKG24"
+"mcx.2_dirty_kg24" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesis2DirtyKG24"
+"mcx.1_clean_kg24" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesis1CleanKG24"
+"mcx.1_dirty_kg24" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesis1DirtyKG24"
 "mcx.1_clean_b95" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesis1CleanB95"
 "mcx.gray_code" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesisGrayCode"
 "mcx.noaux_v24" = "qiskit.transpiler.passes.synthesis.hls_plugins:MCXSynthesisNoAuxV24"
diff --git a/qiskit/transpiler/passes/synthesis/hls_plugins.py b/qiskit/transpiler/passes/synthesis/hls_plugins.py
index a22981d947ee6a5df91ea146e92d64930f35be8a..b477e68b8e2b384915cf6e2624bc8f5ad8617584 100644
--- a/qiskit/transpiler/passes/synthesis/hls_plugins.py
+++ b/qiskit/transpiler/passes/synthesis/hls_plugins.py
@@ -194,6 +194,26 @@ not sufficient, the corresponding synthesis method will return `None`.
       - `0`
       - `k-2`
       - at most `8*k-6` CX gates
+    * - ``"2_clean_kg24"``
+      - :class:`~.MCXSynthesis2CleanKG24`
+      - `2`
+      - `0`
+      - at most `12*k-18` CX gates
+    * - ``"2_dirty_kg24"``
+      - :class:`~.MCXSynthesis2DirtyKG24`
+      - `0`
+      - `2`
+      - at most `24*k-48` CX gates
+    * - ``"1_clean_kg24"``
+      - :class:`~.MCXSynthesis1CleanKG24`
+      - `1`
+      - `0`
+      - at most `12*k-18` CX gates
+    * - ``"1_dirty_kg24"``
+      - :class:`~.MCXSynthesis1DirtyKG24`
+      - `0`
+      - `1`
+      - at most `24*k-48` CX gates
     * - ``"1_clean_b95"``
       - :class:`~.MCXSynthesis1CleanB95`
       - `1`
@@ -212,6 +232,10 @@ not sufficient, the corresponding synthesis method will return `None`.
    MCXSynthesisNoAuxV24
    MCXSynthesisNCleanM15
    MCXSynthesisNDirtyI15
+   MCXSynthesis2CleanKG24
+   MCXSynthesis2DirtyKG24
+   MCXSynthesis1CleanKG24
+   MCXSynthesis1DirtyKG24
    MCXSynthesis1CleanB95
    MCXSynthesisDefault
 
@@ -522,7 +546,11 @@ from qiskit.synthesis.qft import (
 )
 from qiskit.synthesis.multi_controlled import (
     synth_mcx_n_dirty_i15,
+    synth_mcx_2_dirty_kg24,
+    synth_mcx_1_dirty_kg24,
     synth_mcx_n_clean_m15,
+    synth_mcx_2_clean_kg24,
+    synth_mcx_1_clean_kg24,
     synth_mcx_1_clean_b95,
     synth_mcx_gray_code,
     synth_mcx_noaux_v24,
@@ -1145,6 +1173,174 @@ class MCXSynthesis1CleanB95(HighLevelSynthesisPlugin):
         return decomposition
 
 
+class MCXSynthesis2CleanKG24(HighLevelSynthesisPlugin):
+    r"""Synthesis plugin for a multi-controlled X gate based on the paper by Khattar and
+    Gidney (2024).
+
+    See [1] for details.
+
+    The plugin name is :``mcx.2_clean_kg24`` which can be used as the key on an :class:`~.HLSConfig`
+    object to use this method with :class:`~.HighLevelSynthesis`.
+
+    For a multi-controlled X gate with :math:`k\ge 3` control qubits this synthesis method requires
+    :math:`2` additional clean ancillary qubits. The synthesized circuit consists of :math:`k + 2`
+    qubits and at most :math:`12 * k - 18` CX gates.
+
+    The plugin supports the following plugin-specific options:
+
+    * num_clean_ancillas: The number of clean ancillary qubits available.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    def run(self, high_level_object, coupling_map=None, target=None, qubits=None, **options):
+        """Run synthesis for the given MCX gate."""
+
+        if not isinstance(high_level_object, (MCXGate, C3XGate, C4XGate)):
+            # Unfortunately we occasionally have custom instructions called "mcx"
+            # which get wrongly caught by the plugin interface. A simple solution is
+            # to return None in this case, since HLS would proceed to examine
+            # their definition as it should.
+            return None
+
+        num_ctrl_qubits = high_level_object.num_ctrl_qubits
+        num_clean_ancillas = options.get("num_clean_ancillas", 0)
+
+        if num_clean_ancillas < 2:
+            return None
+
+        decomposition = synth_mcx_2_clean_kg24(num_ctrl_qubits)
+        return decomposition
+
+
+class MCXSynthesis2DirtyKG24(HighLevelSynthesisPlugin):
+    r"""Synthesis plugin for a multi-controlled X gate based on the paper by Khattar and
+    Gidney (2024).
+
+    See [1] for details.
+
+    The plugin name is :``mcx.2_dirty_kg24`` which can be used as the key on an :class:`~.HLSConfig`
+    object to use this method with :class:`~.HighLevelSynthesis`.
+
+    For a multi-controlled X gate with :math:`k\ge 3` control qubits this synthesis method requires
+    :math:`2` additional dirty ancillary qubits. The synthesized circuit consists of :math:`k + 2`
+    qubits and at most :math:`24 * k - 48` CX gates.
+
+    The plugin supports the following plugin-specific options:
+
+    * num_clean_ancillas: The number of clean ancillary qubits available.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    def run(self, high_level_object, coupling_map=None, target=None, qubits=None, **options):
+        """Run synthesis for the given MCX gate."""
+
+        if not isinstance(high_level_object, (MCXGate, C3XGate, C4XGate)):
+            # Unfortunately we occasionally have custom instructions called "mcx"
+            # which get wrongly caught by the plugin interface. A simple solution is
+            # to return None in this case, since HLS would proceed to examine
+            # their definition as it should.
+            return None
+
+        num_ctrl_qubits = high_level_object.num_ctrl_qubits
+        num_dirty_ancillas = options.get("num_dirty_ancillas", 0)
+
+        if num_dirty_ancillas < 2:
+            return None
+
+        decomposition = synth_mcx_2_dirty_kg24(num_ctrl_qubits)
+        return decomposition
+
+
+class MCXSynthesis1CleanKG24(HighLevelSynthesisPlugin):
+    r"""Synthesis plugin for a multi-controlled X gate based on the paper by Khattar and
+    Gidney (2024).
+
+    See [1] for details.
+
+    The plugin name is :``mcx.1_clean_kg24`` which can be used as the key on an :class:`~.HLSConfig`
+    object to use this method with :class:`~.HighLevelSynthesis`.
+
+    For a multi-controlled X gate with :math:`k\ge 3` control qubits this synthesis method requires
+    :math:`1` additional clean ancillary qubit. The synthesized circuit consists of :math:`k + 2`
+    qubits and at most :math:`12 * k - 18` CX gates.
+
+    The plugin supports the following plugin-specific options:
+
+    * num_clean_ancillas: The number of clean ancillary qubits available.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    def run(self, high_level_object, coupling_map=None, target=None, qubits=None, **options):
+        """Run synthesis for the given MCX gate."""
+
+        if not isinstance(high_level_object, (MCXGate, C3XGate, C4XGate)):
+            # Unfortunately we occasionally have custom instructions called "mcx"
+            # which get wrongly caught by the plugin interface. A simple solution is
+            # to return None in this case, since HLS would proceed to examine
+            # their definition as it should.
+            return None
+
+        num_ctrl_qubits = high_level_object.num_ctrl_qubits
+        num_clean_ancillas = options.get("num_clean_ancillas", 0)
+
+        if num_clean_ancillas < 1:
+            return None
+
+        decomposition = synth_mcx_1_clean_kg24(num_ctrl_qubits)
+        return decomposition
+
+
+class MCXSynthesis1DirtyKG24(HighLevelSynthesisPlugin):
+    r"""Synthesis plugin for a multi-controlled X gate based on the paper by Khattar and
+    Gidney (2024).
+
+    See [1] for details.
+
+    The plugin name is :``mcx.1_dirty_kg24`` which can be used as the key on an :class:`~.HLSConfig`
+    object to use this method with :class:`~.HighLevelSynthesis`.
+
+    For a multi-controlled X gate with :math:`k\ge 3` control qubits this synthesis method requires
+    :math:`1` additional dirty ancillary qubit. The synthesized circuit consists of :math:`k + 2`
+    qubits and at most :math:`24 * k - 48` CX gates.
+
+    The plugin supports the following plugin-specific options:
+
+    * num_clean_ancillas: The number of clean ancillary qubits available.
+
+    References:
+        1. Khattar and Gidney, Rise of conditionally clean ancillae for optimizing quantum circuits
+        `arXiv:2407.17966 <https://arxiv.org/abs/2407.17966>`__
+    """
+
+    def run(self, high_level_object, coupling_map=None, target=None, qubits=None, **options):
+        """Run synthesis for the given MCX gate."""
+
+        if not isinstance(high_level_object, (MCXGate, C3XGate, C4XGate)):
+            # Unfortunately we occasionally have custom instructions called "mcx"
+            # which get wrongly caught by the plugin interface. A simple solution is
+            # to return None in this case, since HLS would proceed to examine
+            # their definition as it should.
+            return None
+
+        num_ctrl_qubits = high_level_object.num_ctrl_qubits
+        num_dirty_ancillas = options.get("num_dirty_ancillas", 0)
+
+        if num_dirty_ancillas < 1:
+            return None
+
+        decomposition = synth_mcx_1_dirty_kg24(num_ctrl_qubits)
+        return decomposition
+
+
 class MCXSynthesisGrayCode(HighLevelSynthesisPlugin):
     r"""Synthesis plugin for a multi-controlled X gate based on the Gray code.
 
@@ -1228,27 +1424,23 @@ class MCXSynthesisDefault(HighLevelSynthesisPlugin):
 
         # Iteratively run other synthesis methods available
 
-        if (
-            decomposition := MCXSynthesisNCleanM15().run(
-                high_level_object, coupling_map, target, qubits, **options
-            )
-        ) is not None:
-            return decomposition
-
-        if (
-            decomposition := MCXSynthesisNDirtyI15().run(
-                high_level_object, coupling_map, target, qubits, **options
-            )
-        ) is not None:
-            return decomposition
-
-        if (
-            decomposition := MCXSynthesis1CleanB95().run(
-                high_level_object, coupling_map, target, qubits, **options
-            )
-        ) is not None:
-            return decomposition
+        for synthesis_method in [
+            MCXSynthesisNCleanM15,
+            MCXSynthesisNDirtyI15,
+            MCXSynthesis2CleanKG24,
+            MCXSynthesis2DirtyKG24,
+            MCXSynthesis1CleanKG24,
+            MCXSynthesis1DirtyKG24,
+            MCXSynthesis1CleanB95,
+        ]:
+            if (
+                decomposition := synthesis_method().run(
+                    high_level_object, coupling_map, target, qubits, **options
+                )
+            ) is not None:
+                return decomposition
 
+        # If no synthesis method was successful, fall back to the default
         return MCXSynthesisNoAuxV24().run(
             high_level_object, coupling_map, target, qubits, **options
         )
diff --git a/releasenotes/notes/add-new-mcx-plugins-2177db9195e2b680.yaml b/releasenotes/notes/add-new-mcx-plugins-2177db9195e2b680.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..ac5cccac897bb6043c71ce72fc92e30732dce6a0
--- /dev/null
+++ b/releasenotes/notes/add-new-mcx-plugins-2177db9195e2b680.yaml
@@ -0,0 +1,13 @@
+---
+features_transpiler:
+  - |
+    Added multiple high-level-synthesis plugins for synthesizing an :class:`.MCXGate`:
+
+    * :class:`.MCXSynthesis1CleanKG24`, based on :func:`.synth_mcx_1_clean_kg24`.
+    * :class:`.MCXSynthesis1DirtyKG24`, based on :func:`.synth_mcx_1_dirty_kg24`.
+    * :class:`.MCXSynthesis2CleanKG24`, based on :func:`.synth_mcx_2_clean_kg24`.
+    * :class:`.MCXSynthesis2DirtyKG24`, based on :func:`.synth_mcx_2_dirty_kg24`.
+
+    The :class:`.MCXSynthesisDefault` has also been updated to follow the following sequence of
+    MCX synthesizers: "mcx.n_clean_m15", "mcx.n_dirty_i15", "mcx.2_clean_kg24", "mcx.2_dirty_kg24",
+    "mcx.1_clean_kg24", "mcx.1_dirty_kg24" "mcx.1_clean_b95", "mcx.noaux_v24".
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/transpiler/test_high_level_synthesis.py b/test/python/transpiler/test_high_level_synthesis.py
index 51d74ac9f7ebbed4433610c3cce29e35a9155eb9..25ee44270553f03d26bfdf4bf7e5660ce0d9ca8b 100644
--- a/test/python/transpiler/test_high_level_synthesis.py
+++ b/test/python/transpiler/test_high_level_synthesis.py
@@ -74,6 +74,10 @@ from qiskit.transpiler.passes.synthesis.hls_plugins import (
     MCXSynthesis1CleanB95,
     MCXSynthesisNCleanM15,
     MCXSynthesisNDirtyI15,
+    MCXSynthesis2CleanKG24,
+    MCXSynthesis2DirtyKG24,
+    MCXSynthesis1CleanKG24,
+    MCXSynthesis1DirtyKG24,
     MCXSynthesisGrayCode,
     MCXSynthesisDefault,
     MCXSynthesisNoAuxV24,
@@ -2669,6 +2673,69 @@ class TestMCXSynthesisPlugins(QiskitTestCase):
             )
             self.assertIsNone(decomposition)
 
+        with self.subTest(method="2_clean_kg24", num_clean_ancillas=2, num_dirty_ancillas=0):
+            # should have a decomposition
+            decomposition = MCXSynthesis2CleanKG24().run(
+                gate, num_clean_ancillas=2, num_dirty_ancillas=0
+            )
+            self.assertIsNotNone(decomposition)
+
+        with self.subTest(method="2_clean_kg24", num_clean_ancillas=1, num_dirty_ancillas=0):
+            # should not have a decomposition
+            decomposition = MCXSynthesis2CleanKG24().run(
+                gate, num_clean_ancillas=1, num_dirty_ancillas=0
+            )
+            self.assertIsNone(decomposition)
+            decomposition = MCXSynthesis2CleanKG24().run(
+                gate, num_clean_ancillas=0, num_dirty_ancillas=0
+            )
+            self.assertIsNone(decomposition)
+
+        with self.subTest(method="2_dirty_kg24", num_clean_ancillas=0, num_dirty_ancillas=2):
+            # should have a decomposition
+            decomposition = MCXSynthesis2DirtyKG24().run(
+                gate, num_clean_ancillas=0, num_dirty_ancillas=2
+            )
+            self.assertIsNotNone(decomposition)
+
+        with self.subTest(method="2_dirty_kg24", num_clean_ancillas=0, num_dirty_ancillas=1):
+            # should not have a decomposition
+            decomposition = MCXSynthesis2DirtyKG24().run(
+                gate, num_clean_ancillas=0, num_dirty_ancillas=1
+            )
+            self.assertIsNone(decomposition)
+            decomposition = MCXSynthesis2DirtyKG24().run(
+                gate, num_clean_ancillas=0, num_dirty_ancillas=0
+            )
+            self.assertIsNone(decomposition)
+
+        with self.subTest(method="1_clean_kg24", num_clean_ancillas=1, num_dirty_ancillas=0):
+            # should have a decomposition
+            decomposition = MCXSynthesis1CleanKG24().run(
+                gate, num_clean_ancillas=1, num_dirty_ancillas=0
+            )
+            self.assertIsNotNone(decomposition)
+
+        with self.subTest(method="1_clean_kg24", num_clean_ancillas=0, num_dirty_ancillas=1):
+            # should not have a decomposition
+            decomposition = MCXSynthesis1CleanKG24().run(
+                gate, num_clean_ancillas=0, num_dirty_ancillas=1
+            )
+            self.assertIsNone(decomposition)
+
+        with self.subTest(method="1_dirty_kg24", num_clean_ancillas=0, num_dirty_ancillas=1):
+            # should have a decomposition
+            decomposition = MCXSynthesis1DirtyKG24().run(
+                gate, num_clean_ancillas=0, num_dirty_ancillas=1
+            )
+            self.assertIsNotNone(decomposition)
+        with self.subTest(method="1_dirty_kg24", num_clean_ancillas=0, num_dirty_ancillas=0):
+            # should not have a decomposition
+            decomposition = MCXSynthesis1DirtyKG24().run(
+                gate, num_clean_ancillas=0, num_dirty_ancillas=0
+            )
+            self.assertIsNone(decomposition)
+
         with self.subTest(method="1_clean_b95", num_clean_ancillas=1, num_dirty_ancillas=0):
             # should have a decomposition
             decomposition = MCXSynthesis1CleanB95().run(
@@ -2725,7 +2792,18 @@ class TestMCXSynthesisPlugins(QiskitTestCase):
             )
             self.assertIsNotNone(decomposition)
 
-    @data("n_clean_m15", "n_dirty_i15", "1_clean_b95", "noaux_v24", "gray_code", "default")
+    @data(
+        "n_clean_m15",
+        "n_dirty_i15",
+        "2_clean_kg24",
+        "2_dirty_kg24",
+        "1_clean_kg24",
+        "1_dirty_kg24",
+        "1_clean_b95",
+        "noaux_v24",
+        "gray_code",
+        "default",
+    )
     def test_mcx_plugins_correctness_from_arbitrary(self, mcx_plugin_name):
         """Test that all plugins return a correct Operator when qubits are not
         initially zero."""
@@ -2740,7 +2818,18 @@ class TestMCXSynthesisPlugins(QiskitTestCase):
         qct = hls_pass(qc)
         self.assertEqual(Operator(qc), Operator(qct))
 
-    @data("n_clean_m15", "n_dirty_i15", "1_clean_b95", "noaux_v24", "gray_code", "default")
+    @data(
+        "n_clean_m15",
+        "n_dirty_i15",
+        "2_clean_kg24",
+        "2_dirty_kg24",
+        "1_clean_kg24",
+        "1_dirty_kg24",
+        "1_clean_b95",
+        "noaux_v24",
+        "gray_code",
+        "default",
+    )
     def test_mcx_plugins_correctness_from_zero(self, mcx_plugin_name):
         """Test that all plugins return a correct Statevector when qubits are
         initially zero."""
```

## Validation

```json
{
 "test_files": [
  "test/python/transpiler/test_high_level_synthesis.py"
 ],
 "collected_before": 160,
 "collected_after": 159,
 "outcomes_before": {
  "ERROR": 160
 },
 "outcomes_after": {
  "PASSED": 151,
  "FAILED": 8
 },
 "exit_before": 2,
 "exit_after": 1,
 "tail_before": "============================= test session starts ==============================\nplatform linux -- Python 3.11.17, pytest-8.1.2, pluggy-1.5.0 -- /usr/local/bin/python\nhypothesis profile 'default' -> database=DirectoryBasedExampleDatabase(PosixPath('/testbed/.hypothesis/examples'))\nrootdir: /testbed\nconfigfile: pyproject.toml\nplugins: hypothesis-6.130.9\ncollecting ... collected 0 items / 1 error\n\n==================================== ERRORS ====================================\n_____ ERROR collecting test/python/transpiler/test_high_level_synthesis.py _____\nImportError while importing test module '/testbed/test/python/transpiler/test_high_level_synthesis.py'.\nHint: make sure your test modules/packages have valid Python names.\nTraceback:\n/usr/local/lib/python3.11/importlib/__init__.py:126: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\ntest/python/transpiler/test_high_level_synthesis.py:73: in <module>\n    from qiskit.transpiler.passes.synthesis.hls_plugins import (\nE   ImportError: cannot import name 'MCXSynthesis2CleanKG24' from 'qiskit.transpiler.passes.synthesis.hls_plugins' (/testbed/qiskit/transpiler/passes/synthesis/hls_plugins.py)\n=========================== short test summary info ============================\nERROR test/python/transpiler/test_high_level_synthesis.py\n!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!\n=============================== 1 error in 2.54s ===============================",
 "tail_after": "reduction_applies_2\nPASSED test/python/transpiler/test_high_level_synthesis.py::TestAnnotatedSynthesisPlugins::test_conjugate_reduction_not_applies_1\nPASSED test/python/transpiler/test_high_level_synthesis.py::TestAnnotatedSynthesisPlugins::test_conjugate_reduction_not_applies_2\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_03_2_clean_kg24\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_04_2_dirty_kg24\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_05_1_clean_kg24\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_arbitrary_06_1_dirty_kg24\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_03_2_clean_kg24\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_04_2_dirty_kg24\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_05_1_clean_kg24\nFAILED test/python/transpiler/test_high_level_synthesis.py::TestMCXSynthesisPlugins::test_mcx_plugins_correctness_from_zero_06_1_dirty_kg24\n================ 8 failed, 151 passed, 3217 warnings in 11.92s =================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

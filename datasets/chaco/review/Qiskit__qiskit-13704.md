# Qiskit__qiskit-13704

[back to the list](README.md) -- **Oxidize `UnitarySynthesis` path using `basis_gates`**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#13704](https://github.com/Qiskit/qiskit/pull/13704) (created 2025-01-21, merged 2025-02-17) |
| ChaCo lists | full, ablation |
| status | **broken-env** -- the developer's test files run no test on either side (nothing collected, or only collection errors): ======================= short test summary info ============================
ERROR test/python/transpiler/test_unitary_synthesis_plugin.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
========================= 2 warnings, 1 error in 2.78s ========================= |
| base commit | [`581dd3d84c95`](https://github.com/Qiskit/qiskit/commit/581dd3d84c9517df0011f0a5a2305102527d6c79) (2025-02-14), first parent of the merge commit |
| merge commit | [`26906d335a20`](https://github.com/Qiskit/qiskit/commit/26906d335a204a8b39554fc6190c15c318bd4e9c) |
| issues closed | none |
| version | 2.0 |
| image | `f2p-chaco/qiskit__qiskit-13704:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-13704.Dockerfile) |
| source files (`patch`) | `crates/accelerate/src/unitary_synthesis.rs`, `pyproject.toml`, `qiskit/transpiler/passes/synthesis/default_unitary_synth_plugin.py`, `qiskit/transpiler/passes/synthesis/unitary_synthesis.py` |
| test files (`test_patch`) | `test/python/transpiler/test_unitary_synthesis.py`, `test/python/transpiler/test_unitary_synthesis_plugin.py` |
| compiled files changed | crates/accelerate/src/unitary_synthesis.rs |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #13704: Oxidize `UnitarySynthesis` path using `basis_gates`

### Summary

This PR is a compilation of small improvements to the `UnitarySynthesis` pass, including:

1. **Performance** -> Addition of fast path (Rust) for the use case where `target is None`, all input combinations can now be run using the fast path.

2. **Fixes** ->  Fixed an oversight where the `pulse_optimize`  argument wasn't added to the fast path and therefore ignored (discovered after expanding the unit tests).

These set the stage for future refactorings of the `UnitarySynthesis` class to take better advantage of the plugin model (the default plugin is currently ignored in the fast path). 

Note that this PR touches on code that is currently actively worked on in:

- #12850 
- #13568 

And builds on top of #13706 (will need to be rebased after it's merged).

### Details and comments
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/crates/accelerate/src/unitary_synthesis.rs b/crates/accelerate/src/unitary_synthesis.rs
index 9d167c5f083a18f9ed8177e04a659880132be824..1d88f66e72de636a6e80be62d7f086924e27d217 100644
--- a/crates/accelerate/src/unitary_synthesis.rs
+++ b/crates/accelerate/src/unitary_synthesis.rs
@@ -62,53 +62,76 @@ enum DecomposerType {
 #[derive(Clone, Debug)]
 struct DecomposerElement {
     decomposer: DecomposerType,
-    gate: NormalOperation,
+    packed_op: PackedOperation,
+    params: SmallVec<[Param; 3]>,
 }
 
 #[derive(Clone, Debug)]
 struct TwoQubitUnitarySequence {
     gate_sequence: TwoQubitGateSequence,
-    decomp_gate: NormalOperation,
+    decomp_op: PackedOperation,
+    decomp_params: SmallVec<[Param; 3]>,
 }
 
-// Used in get_2q_decomposers. If the found 2q basis is a subset of GOODBYE_SET,
-// then we know TwoQubitBasisDecomposer is an ideal decomposition and there is
-// no need to bother trying the XXDecomposer.
+// These two variables are used to exit the decomposer search early in
+// `get_2q_decomposers_from_target`.
+// If the available 2q basis is a subset of GOODBYE_SET, TwoQubitBasisDecomposer provides
+// an ideal decomposition and we can exit the decomposer search. Similarly, if it is a
+// subset of PARAM_SET, TwoQubitControlledUDecomposer provides an ideal decompostion.
 static GOODBYE_SET: [&str; 3] = ["cx", "cz", "ecr"];
 static PARAM_SET: [&str; 8] = ["rzz", "rxx", "ryy", "rzx", "crx", "cry", "crz", "cphase"];
 
+/// Given a list of basis gates, find a corresponding euler basis to use.
+/// This will determine the available 1q synthesis basis for different decomposers.
+fn get_euler_basis_set(basis_list: IndexSet<&str>) -> EulerBasisSet {
+    let mut euler_basis_set: EulerBasisSet = EulerBasisSet::new();
+    EULER_BASES
+        .iter()
+        .enumerate()
+        .filter_map(|(idx, gates)| {
+            if !gates.iter().all(|gate| basis_list.contains(gate)) {
+                return None;
+            }
+            let basis = EULER_BASIS_NAMES[idx];
+            Some(basis)
+        })
+        .for_each(|basis| euler_basis_set.add_basis(basis));
+
+    if euler_basis_set.basis_supported(EulerBasis::U3)
+        && euler_basis_set.basis_supported(EulerBasis::U321)
+    {
+        euler_basis_set.remove(EulerBasis::U3);
+    }
+    if euler_basis_set.basis_supported(EulerBasis::ZSX)
+        && euler_basis_set.basis_supported(EulerBasis::ZSXX)
+    {
+        euler_basis_set.remove(EulerBasis::ZSX);
+    }
+    euler_basis_set
+}
+
+/// Given a `Target`, find an euler basis that is supported for a specific `PhysicalQubit`.
+/// This will determine the available 1q synthesis basis for different decomposers.
 fn get_target_basis_set(target: &Target, qubit: PhysicalQubit) -> EulerBasisSet {
     let mut target_basis_set: EulerBasisSet = EulerBasisSet::new();
     let target_basis_list = target.operation_names_for_qargs(Some(&smallvec![qubit]));
     match target_basis_list {
         Ok(basis_list) => {
-            EULER_BASES
-                .iter()
-                .enumerate()
-                .filter_map(|(idx, gates)| {
-                    if !gates.iter().all(|gate| basis_list.contains(gate)) {
-                        return None;
-                    }
-                    let basis = EULER_BASIS_NAMES[idx];
-                    Some(basis)
-                })
-                .for_each(|basis| target_basis_set.add_basis(basis));
+            target_basis_set = get_euler_basis_set(basis_list.into_iter().collect());
+        }
+        Err(_) => {
+            target_basis_set.support_all();
+            target_basis_set.remove(EulerBasis::U3);
+            target_basis_set.remove(EulerBasis::ZSX);
         }
-        Err(_) => target_basis_set.support_all(),
-    }
-    if target_basis_set.basis_supported(EulerBasis::U3)
-        && target_basis_set.basis_supported(EulerBasis::U321)
-    {
-        target_basis_set.remove(EulerBasis::U3);
-    }
-    if target_basis_set.basis_supported(EulerBasis::ZSX)
-        && target_basis_set.basis_supported(EulerBasis::ZSXX)
-    {
-        target_basis_set.remove(EulerBasis::ZSX);
     }
     target_basis_set
 }
 
+/// Apply synthesis output (`synth_dag`) to final `DAGCircuit` (`out_dag`).
+/// `synth_dag` is a subgraph, and the `qubit_ids` are relative to the subgraph
+///  size/orientation, so `out_qargs` is used to track the final qubit ids where
+/// it should be applied.
 fn apply_synth_dag(
     py: Python<'_>,
     out_dag: &mut DAGCircuit,
@@ -129,6 +152,10 @@ fn apply_synth_dag(
     Ok(())
 }
 
+/// Apply synthesis output (`sequence`) to final `DAGCircuit` (`out_dag`).
+/// `sequence` contains a representation of gates to be applied to a subgraph,
+/// and the `qubit_ids` are relative to the subgraph size/orientation,
+/// so `out_qargs` is used to track the final qubit ids where they should be applied.
 fn apply_synth_sequence(
     py: Python<'_>,
     out_dag: &mut DAGCircuit,
@@ -138,17 +165,17 @@ fn apply_synth_sequence(
     let mut instructions = Vec::with_capacity(sequence.gate_sequence.gates().len());
     for (gate, params, qubit_ids) in sequence.gate_sequence.gates() {
         let packed_op = match gate {
-            None => &sequence.decomp_gate.operation,
+            None => &sequence.decomp_op,
             Some(gate) => &PackedOperation::from_standard_gate(*gate),
         };
         let mapped_qargs: Vec<Qubit> = qubit_ids.iter().map(|id| out_qargs[*id as usize]).collect();
         let new_params: Option<Box<SmallVec<[Param; 3]>>> = match gate {
             Some(_) => Some(Box::new(params.iter().map(|p| Param::Float(*p)).collect())),
             None => {
-                if !sequence.decomp_gate.params.is_empty()
-                    && matches!(sequence.decomp_gate.params[0], Param::Float(_))
+                if !sequence.decomp_params.is_empty()
+                    && matches!(sequence.decomp_params[0], Param::Float(_))
                 {
-                    Some(Box::new(sequence.decomp_gate.params.clone()))
+                    Some(Box::new(sequence.decomp_params.clone()))
                 } else {
                     Some(Box::new(params.iter().map(|p| Param::Float(*p)).collect()))
                 }
@@ -201,76 +228,27 @@ fn apply_synth_sequence(
     Ok(())
 }
 
-fn synth_error(
-    py: Python<'_>,
-    synth_circuit: impl Iterator<
-        Item = (
-            String,
-            Option<SmallVec<[Param; 3]>>,
-            SmallVec<[PhysicalQubit; 2]>,
-        ),
-    >,
-    target: &Target,
-) -> f64 {
-    let (lower_bound, upper_bound) = synth_circuit.size_hint();
-    let mut gate_fidelities = match upper_bound {
-        Some(bound) => Vec::with_capacity(bound),
-        None => Vec::with_capacity(lower_bound),
-    };
-    let mut score_instruction =
-        |inst_name: &str,
-         inst_params: &Option<SmallVec<[Param; 3]>>,
-         inst_qubits: &SmallVec<[PhysicalQubit; 2]>| {
-            if let Ok(names) = target.operation_names_for_qargs(Some(inst_qubits)) {
-                for name in names {
-                    if let Ok(target_op) = target.operation_from_name(name) {
-                        let are_params_close = if let Some(params) = inst_params {
-                            params.iter().zip(target_op.params.iter()).all(|(p1, p2)| {
-                                p1.is_close(py, p2, 1e-10)
-                                    .expect("Unexpected parameter expression error.")
-                            })
-                        } else {
-                            false
-                        };
-                        let is_parametrized = target_op
-                            .params
-                            .iter()
-                            .any(|param| matches!(param, Param::ParameterExpression(_)));
-                        if target_op.operation.name() == inst_name
-                            && (is_parametrized || are_params_close)
-                        {
-                            match target[name].get(Some(inst_qubits)) {
-                                Some(Some(props)) => {
-                                    gate_fidelities.push(1.0 - props.error.unwrap_or(0.0))
-                                }
-                                _ => gate_fidelities.push(1.0),
-                            }
-                            break;
-                        }
-                    }
-                }
-            }
-        };
-
-    for (inst_name, inst_params, inst_qubits) in synth_circuit {
-        score_instruction(&inst_name, &inst_params, &inst_qubits);
-    }
-    1.0 - gate_fidelities.into_iter().product::<f64>()
-}
-
-// This is the outer-most run function. It is meant to be called from Python
-// in `UnitarySynthesis.run()`.
+/// Iterate over `DAGCircuit` to perform unitary synthesis.
+/// For each elegible gate: find decomposers, select the synthesis
+/// method with the highest fidelity score and apply decompositions. The available methods are:
+///     * 1q synthesis: OneQubitEulerDecomposer
+///     * 2q synthesis: TwoQubitBasisDecomposer, TwoQubitControlledUDecomposer, XXDecomposer (Python, only if target is provided)
+///     * 3q+ synthesis: QuantumShannonDecomposer (Python)
+/// This function is currently used in the Python `UnitarySynthesis`` transpiler pass as a replacement for the `_run_main_loop` method.
+/// It returns a new `DAGCircuit` with the different synthesized gates.
 #[pyfunction]
-#[pyo3(name = "run_default_main_loop", signature=(dag, qubit_indices, min_qubits, target, coupling_edges, approximation_degree=None, natural_direction=None))]
+#[pyo3(name = "run_main_loop", signature=(dag, qubit_indices, min_qubits, target, basis_gates, coupling_edges, approximation_degree=None, natural_direction=None, pulse_optimize=None))]
 fn py_run_main_loop(
     py: Python,
     dag: &mut DAGCircuit,
     qubit_indices: Vec<usize>,
     min_qubits: usize,
-    target: &Target,
+    target: Option<&Target>,
+    basis_gates: HashSet<String>,
     coupling_edges: HashSet<[PhysicalQubit; 2]>,
     approximation_degree: Option<f64>,
     natural_direction: Option<bool>,
+    pulse_optimize: Option<bool>,
 ) -> PyResult<DAGCircuit> {
     // We need to use the python converter because the currently available Rust conversion
     // is lossy. We need `QuantumCircuit` instances to be used in `replace_blocks`.
@@ -311,9 +289,11 @@ fn py_run_main_loop(
                     new_ids,
                     min_qubits,
                     target,
+                    basis_gates.clone(),
                     coupling_edges.clone(),
                     approximation_degree,
                     natural_direction,
+                    pulse_optimize,
                 )?;
                 new_blocks.push(dag_to_circuit.call1((res,))?);
             }
@@ -332,7 +312,7 @@ fn py_run_main_loop(
                 py_op: new_node.unbind().into(),
             };
         }
-        if !(matches!(packed_instr.op.view(), OperationRef::Unitary(_))
+        if !(packed_instr.op.name() == "unitary"
             && packed_instr.op.num_qubits() >= min_qubits as u32)
         {
             out_dag.push_back(py, packed_instr)?;
@@ -346,7 +326,14 @@ fn py_run_main_loop(
             // Run 1q synthesis
             [2, 2] => {
                 let qubit = dag.get_qargs(packed_instr.qubits)[0];
-                let target_basis_set = get_target_basis_set(target, PhysicalQubit::new(qubit.0));
+                let target_basis_set = match target {
+                    Some(target) => get_target_basis_set(target, PhysicalQubit::new(qubit.0)),
+                    None => {
+                        let basis_gates: IndexSet<&str> =
+                            basis_gates.iter().map(String::as_str).collect();
+                        get_euler_basis_set(basis_gates)
+                    }
+                };
                 let sequence = unitary_to_gate_sequence_inner(
                     unitary.view(),
                     &target_basis_set,
@@ -397,8 +384,10 @@ fn py_run_main_loop(
                     ref_qubits,
                     &coupling_edges,
                     target,
+                    basis_gates.clone(),
                     approximation_degree,
                     natural_direction,
+                    pulse_optimize,
                     &mut out_dag,
                     out_qargs,
                     apply_original_op,
@@ -406,223 +395,130 @@ fn py_run_main_loop(
             }
             // Run 3q+ synthesis
             _ => {
-                let qs_decomposition: &Bound<'_, PyAny> = imports::QS_DECOMPOSITION.get_bound(py);
-                let synth_circ = qs_decomposition.call1((unitary.into_pyarray(py),))?;
-                let synth_dag = circuit_to_dag(
-                    py,
-                    QuantumCircuitData::extract_bound(&synth_circ)?,
-                    false,
-                    None,
-                    None,
-                )?;
-                let out_qargs = dag.get_qargs(packed_instr.qubits);
-                apply_synth_dag(py, &mut out_dag, out_qargs, &synth_dag)?;
+                if basis_gates.is_empty() && target.is_none() {
+                    out_dag.push_back(py, packed_instr.clone())?;
+                } else {
+                    let qs_decomposition: &Bound<'_, PyAny> =
+                        imports::QS_DECOMPOSITION.get_bound(py);
+                    let synth_circ = qs_decomposition.call1((unitary.into_pyarray(py),))?;
+                    let synth_dag = circuit_to_dag(
+                        py,
+                        QuantumCircuitData::extract_bound(&synth_circ)?,
+                        false,
+                        None,
+                        None,
+                    )?;
+                    let out_qargs = dag.get_qargs(packed_instr.qubits);
+                    apply_synth_dag(py, &mut out_dag, out_qargs, &synth_dag)?;
+                }
             }
         }
     }
     Ok(out_dag)
 }
 
-fn run_2q_unitary_synthesis(
-    py: Python,
-    unitary: Array2<Complex64>,
-    ref_qubits: &[PhysicalQubit; 2],
-    coupling_edges: &HashSet<[PhysicalQubit; 2]>,
-    target: &Target,
+/// Return a single decomposer for the given `basis_gates`. If no decomposer is found,
+/// return `None``. If a decomposer is found, the return type will be either
+/// `DecomposerElement::TwoQubitBasis` or `DecomposerElement::TwoQubitControlledU`.
+fn get_2q_decomposer_from_basis(
+    basis_gates: IndexSet<&str>,
     approximation_degree: Option<f64>,
-    natural_direction: Option<bool>,
-    out_dag: &mut DAGCircuit,
-    out_qargs: &[Qubit],
-    mut apply_original_op: impl FnMut(&mut DAGCircuit) -> PyResult<()>,
-) -> PyResult<()> {
-    let decomposers = {
-        let decomposers_2q =
-            get_2q_decomposers_from_target(py, target, ref_qubits, approximation_degree)?;
-        decomposers_2q.unwrap_or_default()
+    pulse_optimize: Option<bool>,
+) -> PyResult<Option<DecomposerElement>> {
+    // Non-parametrized 2q basis candidates (TwoQubitBasisDecomposer)
+    let basis_names: IndexMap<&str, StandardGate> = [
+        ("cx", StandardGate::CXGate),
+        ("cz", StandardGate::CZGate),
+        ("iswap", StandardGate::ISwapGate),
+        ("ecr", StandardGate::ECRGate),
+    ]
+    .into_iter()
+    .collect();
+    // Parametrized 2q basis candidates (TwoQubitControlledUDecomposer)
+    let param_basis_names: IndexMap<&str, StandardGate> = [
+        ("rxx", StandardGate::RXXGate),
+        ("rzx", StandardGate::RZXGate),
+        ("rzz", StandardGate::RZZGate),
+        ("ryy", StandardGate::RYYGate),
+        ("cphase", StandardGate::CPhaseGate),
+        ("crx", StandardGate::CRXGate),
+        ("cry", StandardGate::CRYGate),
+        ("crz", StandardGate::CRZGate),
+    ]
+    .into_iter()
+    .collect();
+    // 1q basis (both decomposers)
+    let euler_basis = match get_euler_basis_set(basis_gates.clone())
+        .get_bases()
+        .map(|basis| basis.as_str())
+        .next()
+    {
+        Some(basis) => basis,
+        None => return Ok(None),
     };
-    // If there's a single decomposer, avoid computing synthesis score
-    if decomposers.len() == 1 {
-        let decomposer_item = decomposers.first().unwrap();
-        let preferred_dir = preferred_direction(
-            decomposer_item,
-            ref_qubits,
-            natural_direction,
-            coupling_edges,
-            target,
-        )?;
 
-        match decomposer_item.decomposer {
-            DecomposerType::TwoQubitBasis(_) => {
-                let synth = synth_su4_sequence(
-                    &unitary,
-                    decomposer_item,
-                    preferred_dir,
-                    approximation_degree,
-                )?;
-                apply_synth_sequence(py, out_dag, out_qargs, &synth)?;
-            }
-            DecomposerType::TwoQubitControlledU(_) => {
-                let synth = synth_su4_sequence(
-                    &unitary,
-                    decomposer_item,
-                    preferred_dir,
-                    approximation_degree,
-                )?;
-                apply_synth_sequence(py, out_dag, out_qargs, &synth)?;
-            }
-            DecomposerType::XX(_) => {
-                let synth = synth_su4_dag(
-                    py,
-                    &unitary,
-                    decomposer_item,
-                    preferred_dir,
-                    approximation_degree,
-                )?;
-                apply_synth_dag(py, out_dag, out_qargs, &synth)?;
-            }
-        }
-        return Ok(());
-    }
+    // Try TwoQubitControlledUDecomposer first.
+    let kak_gates: Vec<&str> = param_basis_names
+        .keys()
+        .copied()
+        .collect::<IndexSet<&str>>()
+        .intersection(&basis_gates)
+        .copied()
+        .collect();
+    if !kak_gates.is_empty() {
+        let std_gate = *param_basis_names.get(kak_gates[0]).unwrap();
+        let rxx_equivalent_gate = RXXEquivalent::Standard(std_gate);
+        if let Ok(decomposer) =
+            TwoQubitControlledUDecomposer::new_inner(rxx_equivalent_gate, euler_basis)
+        {
+            return Ok(Some(DecomposerElement {
+                decomposer: DecomposerType::TwoQubitControlledU(Box::new(decomposer)),
+                packed_op: PackedOperation::from_standard_gate(std_gate),
+                params: SmallVec::new(),
+            }));
+        };
+    };
 
-    let mut synth_errors_sequence = Vec::new();
-    let mut synth_errors_dag = Vec::new();
-    for decomposer in &decomposers {
-        let preferred_dir = preferred_direction(
-            decomposer,
-            ref_qubits,
-            natural_direction,
-            coupling_edges,
-            target,
+    // If there is no suitable TwoQubitControlledUDecomposer, try TwoQubitBasisDecomposer.
+    let kak_gates: Vec<&str> = basis_names
+        .keys()
+        .copied()
+        .collect::<IndexSet<&str>>()
+        .intersection(&basis_gates)
+        .copied()
+        .collect();
+    if !kak_gates.is_empty() {
+        let std_gate = *basis_names.get(kak_gates[0]).unwrap();
+        let decomposer = TwoQubitBasisDecomposer::new_inner(
+            std_gate.name().to_string(),
+            std_gate.matrix(&[]).unwrap().view(),
+            approximation_degree.unwrap_or(1.0),
+            euler_basis,
+            pulse_optimize,
         )?;
-        match &decomposer.decomposer {
-            DecomposerType::TwoQubitBasis(_) => {
-                let sequence =
-                    synth_su4_sequence(&unitary, decomposer, preferred_dir, approximation_degree)?;
-                let scoring_info =
-                    sequence
-                        .gate_sequence
-                        .gates()
-                        .iter()
-                        .map(|(gate, params, qubit_ids)| {
-                            let inst_qubits =
-                                qubit_ids.iter().map(|q| ref_qubits[*q as usize]).collect();
-                            match gate {
-                                Some(gate) => (
-                                    gate.name().to_string(),
-                                    Some(params.iter().map(|p| Param::Float(*p)).collect()),
-                                    inst_qubits,
-                                ),
-                                None => (
-                                    sequence.decomp_gate.operation.name().to_string(),
-                                    Some(params.iter().map(|p| Param::Float(*p)).collect()),
-                                    inst_qubits,
-                                ),
-                            }
-                        });
-                let synth_error_from_target = synth_error(py, scoring_info, target);
-                synth_errors_sequence.push((sequence, synth_error_from_target));
-            }
-            DecomposerType::TwoQubitControlledU(_) => {
-                let sequence =
-                    synth_su4_sequence(&unitary, decomposer, preferred_dir, approximation_degree)?;
-                let scoring_info =
-                    sequence
-                        .gate_sequence
-                        .gates()
-                        .iter()
-                        .map(|(gate, params, qubit_ids)| {
-                            let inst_qubits =
-                                qubit_ids.iter().map(|q| ref_qubits[*q as usize]).collect();
-                            match gate {
-                                Some(gate) => (
-                                    gate.name().to_string(),
-                                    Some(params.iter().map(|p| Param::Float(*p)).collect()),
-                                    inst_qubits,
-                                ),
-                                None => (
-                                    sequence.decomp_gate.operation.name().to_string(),
-                                    Some(params.iter().map(|p| Param::Float(*p)).collect()),
-                                    inst_qubits,
-                                ),
-                            }
-                        });
-                let synth_error_from_target = synth_error(py, scoring_info, target);
-                synth_errors_sequence.push((sequence, synth_error_from_target));
-            }
-            DecomposerType::XX(_) => {
-                let synth_dag = synth_su4_dag(
-                    py,
-                    &unitary,
-                    decomposer,
-                    preferred_dir,
-                    approximation_degree,
-                )?;
-                let scoring_info = synth_dag
-                    .topological_op_nodes()
-                    .expect("Unexpected error in dag.topological_op_nodes()")
-                    .map(|node| {
-                        let NodeType::Operation(inst) = &synth_dag[node] else {
-                            unreachable!("DAG node must be an instruction")
-                        };
-                        let inst_qubits = synth_dag
-                            .get_qargs(inst.qubits)
-                            .iter()
-                            .map(|q| ref_qubits[q.0 as usize])
-                            .collect();
-                        (
-                            inst.op.name().to_string(),
-                            inst.params.clone().map(|boxed| *boxed),
-                            inst_qubits,
-                        )
-                    });
-                let synth_error_from_target = synth_error(py, scoring_info, target);
-                synth_errors_dag.push((synth_dag, synth_error_from_target));
-            }
-        }
+        return Ok(Some(DecomposerElement {
+            decomposer: DecomposerType::TwoQubitBasis(Box::new(decomposer)),
+            packed_op: PackedOperation::from_standard_gate(std_gate),
+            params: SmallVec::new(),
+        }));
     }
-
-    let synth_sequence = synth_errors_sequence
-        .iter()
-        .enumerate()
-        .min_by(|error1, error2| error1.1 .1.partial_cmp(&error2.1 .1).unwrap())
-        .map(|(index, _)| &synth_errors_sequence[index]);
-
-    let synth_dag = synth_errors_dag
-        .iter()
-        .enumerate()
-        .min_by(|error1, error2| error1.1 .1.partial_cmp(&error2.1 .1).unwrap())
-        .map(|(index, _)| &synth_errors_dag[index]);
-
-    match (synth_sequence, synth_dag) {
-        (None, None) => apply_original_op(out_dag)?,
-        (Some((sequence, _)), None) => apply_synth_sequence(py, out_dag, out_qargs, sequence)?,
-        (None, Some((dag, _))) => apply_synth_dag(py, out_dag, out_qargs, dag)?,
-        (Some((sequence, sequence_error)), Some((dag, dag_error))) => {
-            if sequence_error > dag_error {
-                apply_synth_dag(py, out_dag, out_qargs, dag)?
-            } else {
-                apply_synth_sequence(py, out_dag, out_qargs, sequence)?
-            }
-        }
-    };
-    Ok(())
+    Ok(None)
 }
 
+/// Return a list of decomposers for the given `target`. If no decomposer is found,
+/// return `None``. The list can contain any `DecomposerElement`. This function
+/// will exit early if an ideal decomposition is found.
 fn get_2q_decomposers_from_target(
     py: Python,
     target: &Target,
     qubits: &[PhysicalQubit; 2],
     approximation_degree: Option<f64>,
+    pulse_optimize: Option<bool>,
 ) -> PyResult<Option<Vec<DecomposerElement>>> {
+    // Store elegible basis gates (1q and 2q) with corresponding qargs (PhysicalQubit)
     let qubits: SmallVec<[PhysicalQubit; 2]> = SmallVec::from_buf(*qubits);
     let reverse_qubits: SmallVec<[PhysicalQubit; 2]> = qubits.iter().rev().copied().collect();
-    let mut available_2q_basis: IndexMap<&str, NormalOperation> = IndexMap::new();
-    let mut available_2q_props: IndexMap<&str, (Option<f64>, Option<f64>)> = IndexMap::new();
-    let mut available_2q_param_basis: IndexMap<&str, NormalOperation> = IndexMap::new();
-    let mut available_2q_param_props: IndexMap<&str, (Option<f64>, Option<f64>)> = IndexMap::new();
-
     let mut qubit_gate_map = IndexMap::new();
-
     match target.operation_names_for_qargs(Some(&qubits)) {
         Ok(direct_keys) => {
             qubit_gate_map.insert(&qubits, direct_keys);
@@ -641,13 +537,17 @@ fn get_2q_decomposers_from_target(
         }
     }
 
-    #[inline]
-    fn check_parametrized_gate(op: &NormalOperation) -> bool {
-        // The gate counts as parametrized if there is any
-        // non-float parameter
-        !op.params.iter().all(|p| matches!(p, Param::Float(_)))
-    }
+    // Define available 1q basis
+    let available_1q_basis: IndexSet<&str> = IndexSet::from_iter(
+        get_target_basis_set(target, qubits[0])
+            .get_bases()
+            .map(|basis| basis.as_str()),
+    );
 
+    // Define available 2q basis (setting apart parametrized 2q gates)
+    let mut available_2q_basis: IndexMap<&str, (NormalOperation, Option<f64>)> = IndexMap::new();
+    let mut available_2q_param_basis: IndexMap<&str, (NormalOperation, Option<f64>)> =
+        IndexMap::new();
     for (q_pair, gates) in qubit_gate_map {
         for key in gates {
             match target.operation_from_name(key) {
@@ -661,49 +561,44 @@ fn get_2q_decomposers_from_target(
                     if op.operation.num_qubits() != 2 {
                         continue;
                     }
-                    if check_parametrized_gate(op) {
-                        available_2q_param_basis.insert(key, op.clone());
-                        if target.contains_key(key) {
-                            available_2q_param_props.insert(
-                                key,
+                    // Add to param_basis if the gate parameters aren't bound (not Float)
+                    if !op.params.iter().all(|p| matches!(p, Param::Float(_))) {
+                        available_2q_param_basis.insert(
+                            key,
+                            (
+                                op.clone(),
                                 match &target[key].get(Some(q_pair)) {
-                                    Some(Some(props)) => (props.duration, props.error),
-                                    _ => (None, None),
+                                    Some(Some(props)) => props.error,
+                                    _ => None,
                                 },
-                            );
-                        } else {
-                            continue;
-                        }
+                            ),
+                        );
                     }
-                    available_2q_basis.insert(key, op.clone());
-                    if target.contains_key(key) {
-                        available_2q_props.insert(
-                            key,
+                    available_2q_basis.insert(
+                        key,
+                        (
+                            op.clone(),
                             match &target[key].get(Some(q_pair)) {
-                                Some(Some(props)) => (props.duration, props.error),
-                                _ => (None, None),
+                                Some(Some(props)) => props.error,
+                                _ => None,
                             },
-                        );
-                    } else {
-                        continue;
-                    }
+                        ),
+                    );
                 }
                 _ => continue,
             }
         }
     }
-
     if available_2q_basis.is_empty() && available_2q_param_basis.is_empty() {
         return Err(QiskitError::new_err(
             "Target has no gates available on qubits to synthesize over.",
         ));
     }
 
-    let target_basis_set = get_target_basis_set(target, qubits[0]);
-    let available_1q_basis: IndexSet<&str> =
-        IndexSet::from_iter(target_basis_set.get_bases().map(|basis| basis.as_str()));
+    // If there are available 2q gates, start search for decomposers:
     let mut decomposers: Vec<DecomposerElement> = Vec::new();
 
+    // Step 1: Try TwoQubitBasisDecomposers
     #[inline]
     fn is_supercontrolled(op: &NormalOperation) -> bool {
         match op.operation.matrix(&op.params) {
@@ -715,29 +610,15 @@ fn get_2q_decomposers_from_target(
             }
         }
     }
-
-    #[inline]
-    fn is_controlled(op: &NormalOperation) -> bool {
-        match op.operation.matrix(&op.params) {
-            None => false,
-            Some(unitary_matrix) => {
-                let kak = TwoQubitWeylDecomposition::new_inner(unitary_matrix.view(), None, None)
-                    .unwrap();
-                relative_eq!(kak.b(), 0.0) && relative_eq!(kak.c(), 0.0)
-            }
-        }
-    }
-
-    let supercontrolled_basis: IndexMap<&str, NormalOperation> = available_2q_basis
+    let supercontrolled_basis: IndexMap<&str, (NormalOperation, Option<f64>)> = available_2q_basis
         .iter()
-        .filter(|(_, v)| is_supercontrolled(v))
-        .map(|(k, v)| (*k, v.clone()))
+        .filter(|(_, (gate, _))| is_supercontrolled(gate))
+        .map(|(k, (gate, props))| (*k, (gate.clone(), *props)))
         .collect();
-
     for basis_1q in &available_1q_basis {
-        for (basis_2q, gate) in supercontrolled_basis.iter() {
-            let mut basis_2q_fidelity: f64 = match available_2q_props.get(basis_2q) {
-                Some(&(_, Some(e))) => 1.0 - e,
+        for (_, (gate, props)) in supercontrolled_basis.iter() {
+            let mut basis_2q_fidelity: f64 = match props {
+                Some(error) => 1.0 - error,
                 _ => 1.0,
             };
             if let Some(approx_degree) = approximation_degree {
@@ -748,31 +629,28 @@ fn get_2q_decomposers_from_target(
                 gate.operation.matrix(&gate.params).unwrap().view(),
                 basis_2q_fidelity,
                 basis_1q,
-                None,
+                pulse_optimize,
             )?;
 
             decomposers.push(DecomposerElement {
                 decomposer: DecomposerType::TwoQubitBasis(Box::new(decomposer)),
-                gate: gate.clone(),
+                packed_op: gate.operation.clone(),
+                params: gate.params.clone(),
             });
         }
     }
-
-    // If our 2q basis gates are a subset of cx, ecr, or cz then we know TwoQubitBasisDecomposer
-    // is an ideal decomposition and there is no need to try other decomposers
-    let available_basis_set: IndexSet<&str> = available_2q_basis.keys().copied().collect();
-
-    #[inline]
-    fn check_goodbye(basis_set: &IndexSet<&str>) -> bool {
-        !basis_set.is_empty() && basis_set.iter().all(|gate| GOODBYE_SET.contains(gate))
-    }
-
-    if check_goodbye(&available_basis_set) {
+    // If the 2q basis gates are a subset of GOODBYE_SET, exit here.
+    if available_2q_basis
+        .keys()
+        .all(|gate| GOODBYE_SET.contains(gate))
+        && !available_2q_basis.is_empty()
+    {
         return Ok(Some(decomposers));
     }
 
+    // Step 2: Try TwoQubitControlledUDecomposers
     for basis_1q in &available_1q_basis {
-        for (_basis_2q, gate) in available_2q_param_basis.iter() {
+        for (_, (gate, _)) in available_2q_param_basis.iter() {
             let rxx_equivalent_gate = if let Some(std_gate) = gate.operation.try_standard_gate() {
                 RXXEquivalent::Standard(std_gate)
             } else {
@@ -790,42 +668,46 @@ fn get_2q_decomposers_from_target(
                 Ok(decomposer) => {
                     decomposers.push(DecomposerElement {
                         decomposer: DecomposerType::TwoQubitControlledU(Box::new(decomposer)),
-                        gate: gate.clone(),
+                        packed_op: gate.operation.clone(),
+                        params: gate.params.clone(),
                     });
                 }
                 Err(_) => continue,
             };
         }
     }
-
-    // If our 2q basis gates are a subset of PARAM_SET, then we will use the TwoQubitControlledUDecomposer
-    // and there is no need to try other decomposers
-
-    let available_basis_param_set: IndexSet<&str> =
-        available_2q_param_basis.keys().copied().collect();
-
-    #[inline]
-    fn check_parametrized_goodbye(basis_set: &IndexSet<&str>) -> bool {
-        !basis_set.is_empty() && basis_set.iter().all(|gate| PARAM_SET.contains(gate))
-    }
-
-    if check_parametrized_goodbye(&available_basis_param_set) {
+    // If the 2q basis gates are a subset of PARAM_SET, exit here
+    if available_2q_param_basis
+        .keys()
+        .all(|gate| PARAM_SET.contains(gate))
+        && !available_2q_param_basis.is_empty()
+    {
         return Ok(Some(decomposers));
     }
 
-    // Let's now look for possible controlled decomposers (i.e. XXDecomposer)
-    let controlled_basis: IndexMap<&str, NormalOperation> = available_2q_basis
+    // Step 3: Try XXDecomposers (Python)
+    #[inline]
+    fn is_controlled(op: &NormalOperation) -> bool {
+        match op.operation.matrix(&op.params) {
+            None => false,
+            Some(unitary_matrix) => {
+                let kak = TwoQubitWeylDecomposition::new_inner(unitary_matrix.view(), None, None)
+                    .unwrap();
+                relative_eq!(kak.b(), 0.0) && relative_eq!(kak.c(), 0.0)
+            }
+        }
+    }
+    let controlled_basis: IndexMap<&str, (NormalOperation, Option<f64>)> = available_2q_basis
         .iter()
-        .filter(|(_, v)| is_controlled(v))
-        .map(|(k, v)| (*k, v.clone()))
+        .filter(|(_, (gate, _))| is_controlled(gate))
+        .map(|(k, (gate, props))| (*k, (gate.clone(), *props)))
         .collect();
     let mut pi2_basis: Option<&str> = None;
     let xx_embodiments: &Bound<'_, PyAny> = imports::XX_EMBODIMENTS.get_bound(py);
-
-    // The xx decomposer args are the interaction strength (f64), basis_2q_fidelity (f64),
+    // The Python XXDecomposer args are the interaction strength (f64), basis_2q_fidelity (f64),
     // and embodiments (Bound<'_, PyAny>).
     let xx_decomposer_args = controlled_basis.iter().map(
-        |(name, op)| -> PyResult<(f64, f64, pyo3::Bound<'_, pyo3::PyAny>)> {
+        |(name, (op, props))| -> PyResult<(f64, f64, pyo3::Bound<'_, pyo3::PyAny>)> {
             let strength = 2.0
                 * TwoQubitWeylDecomposition::new_inner(
                     op.operation.matrix(&op.params).unwrap().view(),
@@ -834,8 +716,8 @@ fn get_2q_decomposers_from_target(
                 )
                 .unwrap()
                 .a();
-            let mut fidelity_value = match available_2q_props.get(name) {
-                Some(&(_, error)) => 1.0 - error.unwrap_or_default(), // default is 0.0
+            let mut fidelity_value = match props {
+                Some(error) => 1.0 - error,
                 None => 1.0,
             };
             if let Some(approx_degree) = approximation_degree {
@@ -854,15 +736,12 @@ fn get_2q_decomposers_from_target(
             Ok((strength, fidelity_value, embodiment))
         },
     );
-
     let basis_2q_fidelity_dict = PyDict::new(py);
     let embodiments_dict = PyDict::new(py);
     for (strength, fidelity, embodiment) in xx_decomposer_args.flatten() {
         basis_2q_fidelity_dict.set_item(strength, fidelity)?;
         embodiments_dict.set_item(strength, embodiment)?;
     }
-
-    // Iterate over 2q fidelities and select decomposers
     if basis_2q_fidelity_dict.len() > 0 {
         let xx_decomposer: &Bound<'_, PyAny> = imports::XX_DECOMPOSER.get_bound(py);
         for basis_1q in available_1q_basis {
@@ -901,49 +780,30 @@ fn get_2q_decomposers_from_target(
 
             decomposers.push(DecomposerElement {
                 decomposer: DecomposerType::XX(decomposer.into()),
-                gate: decomposer_gate,
+                packed_op: decomposer_gate.operation,
+                params: decomposer_gate.params.clone(),
             });
         }
     }
     Ok(Some(decomposers))
 }
 
+/// Function to evaluate hardware-native direction, this allows to correct
+/// the synthesis output to match the target constraints.
+/// Returns:
+///     * `true` if gate qubits are in the hardware-native direction
+///     * `false` if gate qubits must be flipped to match hardware-native direction
 fn preferred_direction(
-    decomposer: &DecomposerElement,
     ref_qubits: &[PhysicalQubit; 2],
     natural_direction: Option<bool>,
     coupling_edges: &HashSet<[PhysicalQubit; 2]>,
-    target: &Target,
+    target: Option<&Target>,
+    decomposer: &DecomposerElement,
 ) -> PyResult<Option<bool>> {
-    // Returns:
-    // * true if gate qubits are in the hardware-native direction
-    // * false if gate qubits must be flipped to match hardware-native direction
     let qubits: [PhysicalQubit; 2] = *ref_qubits;
     let mut reverse_qubits: [PhysicalQubit; 2] = qubits;
     reverse_qubits.reverse();
 
-    let compute_cost =
-        |lengths: bool, q_tuple: [PhysicalQubit; 2], in_cost: f64| -> PyResult<f64> {
-            let cost = match target.qargs_for_operation_name(decomposer.gate.operation.name()) {
-                Ok(_) => match target[decomposer.gate.operation.name()].get(Some(
-                    &q_tuple
-                        .into_iter()
-                        .collect::<SmallVec<[PhysicalQubit; 2]>>(),
-                )) {
-                    Some(Some(_props)) => {
-                        if lengths {
-                            _props.duration.unwrap_or(in_cost)
-                        } else {
-                            _props.error.unwrap_or(in_cost)
-                        }
-                    }
-                    _ => in_cost,
-                },
-                Err(_) => in_cost,
-            };
-            Ok(cost)
-        };
-
     let preferred_direction = match natural_direction {
         Some(false) => None,
         _ => {
@@ -955,31 +815,60 @@ fn preferred_direction(
                 (true, false) => Some(true),
                 (false, true) => Some(false),
                 _ => {
-                    let mut cost_0_1: f64 = f64::INFINITY;
-                    let mut cost_1_0: f64 = f64::INFINITY;
-
-                    // Try to find the cost in gate_lengths
-                    cost_0_1 = compute_cost(true, qubits, cost_0_1)?;
-                    cost_1_0 = compute_cost(true, reverse_qubits, cost_1_0)?;
-
-                    // If no valid cost was found in gate_lengths, check gate_errors
-                    if !(cost_0_1 < f64::INFINITY || cost_1_0 < f64::INFINITY) {
-                        cost_0_1 = compute_cost(false, qubits, cost_0_1)?;
-                        cost_1_0 = compute_cost(false, reverse_qubits, cost_1_0)?;
-                    }
+                    match target {
+                        Some(target) => {
+                            let mut cost_0_1: f64 = f64::INFINITY;
+                            let mut cost_1_0: f64 = f64::INFINITY;
+
+                            let compute_cost = |lengths: bool,
+                                                q_tuple: [PhysicalQubit; 2],
+                                                in_cost: f64|
+                             -> PyResult<f64> {
+                                let cost = match target
+                                    .qargs_for_operation_name(decomposer.packed_op.name())
+                                {
+                                    Ok(_) => match target[decomposer.packed_op.name()].get(Some(
+                                        &q_tuple
+                                            .into_iter()
+                                            .collect::<SmallVec<[PhysicalQubit; 2]>>(),
+                                    )) {
+                                        Some(Some(_props)) => {
+                                            if lengths {
+                                                _props.duration.unwrap_or(in_cost)
+                                            } else {
+                                                _props.error.unwrap_or(in_cost)
+                                            }
+                                        }
+                                        _ => in_cost,
+                                    },
+                                    Err(_) => in_cost,
+                                };
+                                Ok(cost)
+                            };
+                            // Try to find the cost in gate_lengths
+                            cost_0_1 = compute_cost(true, qubits, cost_0_1)?;
+                            cost_1_0 = compute_cost(true, reverse_qubits, cost_1_0)?;
+
+                            // If no valid cost was found in gate_lengths, check gate_errors
+                            if !(cost_0_1 < f64::INFINITY || cost_1_0 < f64::INFINITY) {
+                                cost_0_1 = compute_cost(false, qubits, cost_0_1)?;
+                                cost_1_0 = compute_cost(false, reverse_qubits, cost_1_0)?;
+                            }
 
-                    if cost_0_1 < cost_1_0 {
-                        Some(true)
-                    } else if cost_1_0 < cost_0_1 {
-                        Some(false)
-                    } else {
-                        None
+                            if cost_0_1 < cost_1_0 {
+                                Some(true)
+                            } else if cost_1_0 < cost_0_1 {
+                                Some(false)
+                            } else {
+                                None
+                            }
+                        }
+                        None => None,
                     }
                 }
             }
         }
     };
-
     if natural_direction == Some(true) && preferred_direction.is_none() {
         return Err(QiskitError::new_err(format!(
             concat!(
@@ -989,10 +878,10 @@ fn preferred_direction(
             qubits
         )));
     }
-
     Ok(preferred_direction)
 }
 
+/// Apply synthesis for decomposers that return a SEQUENCE (TwoQubitBasis and TwoQubitControlledU).
 fn synth_su4_sequence(
     su4_mat: &Array2<Complex64>,
     decomposer_2q: &DecomposerElement,
@@ -1009,9 +898,9 @@ fn synth_su4_sequence(
     };
     let sequence = TwoQubitUnitarySequence {
         gate_sequence: synth,
-        decomp_gate: decomposer_2q.gate.clone(),
+        decomp_op: decomposer_2q.packed_op.clone(),
+        decomp_params: decomposer_2q.params.clone(),
     };
-
     match preferred_direction {
         None => Ok(sequence),
         Some(preferred_dir) => {
@@ -1024,7 +913,6 @@ fn synth_su4_sequence(
                     synth_direction = Some(qubits.clone());
                 }
             }
-
             match synth_direction {
                 None => Ok(sequence),
                 Some(synth_direction) => {
@@ -1048,6 +936,9 @@ fn synth_su4_sequence(
     }
 }
 
+/// Apply reverse synthesis for decomposers that return a SEQUENCE (TwoQubitBasis and TwoQubitControlledU).
+/// This function is called by `synth_su4_sequence`` if the "direct" synthesis
+/// doesn't match the hardware restrictions.
 fn reversed_synth_su4_sequence(
     mut su4_mat: Array2<Complex64>,
     decomposer_2q: &DecomposerElement,
@@ -1071,7 +962,6 @@ fn reversed_synth_su4_sequence(
             "reversed_synth_su4_sequence should only be called for TwoQubitBasisDecomposer."
         )
     };
-
     let flip_bits: [u8; 2] = [1, 0];
     let mut reversed_gates = Vec::with_capacity(synth.gates().len());
     for (gate, params, qubit_ids) in synth.gates() {
@@ -1081,16 +971,17 @@ fn reversed_synth_su4_sequence(
             .collect::<SmallVec<[u8; 2]>>();
         reversed_gates.push((*gate, params.clone(), new_qubit_ids.clone()));
     }
-
     let mut reversed_synth: TwoQubitGateSequence = TwoQubitGateSequence::new();
     reversed_synth.set_state((reversed_gates, synth.global_phase()));
     let sequence = TwoQubitUnitarySequence {
         gate_sequence: reversed_synth,
-        decomp_gate: decomposer_2q.gate.clone(),
+        decomp_op: decomposer_2q.packed_op.clone(),
+        decomp_params: decomposer_2q.params.clone(),
     };
     Ok(sequence)
 }
 
+/// Apply synthesis for decomposers that return a DAG (XX).
 fn synth_su4_dag(
     py: Python,
     su4_mat: &Array2<Complex64>,
@@ -1113,7 +1004,6 @@ fn synth_su4_dag(
     } else {
         unreachable!("synth_su4_dag should only be called for XXDecomposer.")
     };
-
     match preferred_direction {
         None => Ok(synth_dag),
         Some(preferred_dir) => {
@@ -1149,6 +1039,9 @@ fn synth_su4_dag(
     }
 }
 
+/// Apply reverse synthesis for decomposers that return a DAG (XX).
+/// This function is called by `synth_su4_dag`` if the "direct" synthesis
+/// doesn't match the hardware restrictions.
 fn reversed_synth_su4_dag(
     py: Python<'_>,
     mut su4_mat: Array2<Complex64>,
@@ -1196,6 +1089,263 @@ fn reversed_synth_su4_dag(
     Ok(target_dag)
 }
 
+/// Score the synthesis output (DAG or sequence) based on the expected gate fidelity/error score.
+fn synth_error(
+    py: Python<'_>,
+    synth_circuit: impl Iterator<
+        Item = (
+            String,
+            Option<SmallVec<[Param; 3]>>,
+            SmallVec<[PhysicalQubit; 2]>,
+        ),
+    >,
+    target: &Target,
+) -> f64 {
+    let (lower_bound, upper_bound) = synth_circuit.size_hint();
+    let mut gate_fidelities = match upper_bound {
+        Some(bound) => Vec::with_capacity(bound),
+        None => Vec::with_capacity(lower_bound),
+    };
+    let mut score_instruction =
+        |inst_name: &str,
+         inst_params: &Option<SmallVec<[Param; 3]>>,
+         inst_qubits: &SmallVec<[PhysicalQubit; 2]>| {
+            if let Ok(names) = target.operation_names_for_qargs(Some(inst_qubits)) {
+                for name in names {
+                    if let Ok(target_op) = target.operation_from_name(name) {
+                        let are_params_close = if let Some(params) = inst_params {
+                            params.iter().zip(target_op.params.iter()).all(|(p1, p2)| {
+                                p1.is_close(py, p2, 1e-10)
+                                    .expect("Unexpected parameter expression error.")
+                            })
+                        } else {
+                            false
+                        };
+                        let is_parametrized = target_op
+                            .params
+                            .iter()
+                            .any(|param| matches!(param, Param::ParameterExpression(_)));
+                        if target_op.operation.name() == inst_name
+                            && (is_parametrized || are_params_close)
+                        {
+                            match target[name].get(Some(inst_qubits)) {
+                                Some(Some(props)) => {
+                                    gate_fidelities.push(1.0 - props.error.unwrap_or(0.0))
+                                }
+                                _ => gate_fidelities.push(1.0),
+                            }
+                            break;
+                        }
+                    }
+                }
+            }
+        };
+
+    for (inst_name, inst_params, inst_qubits) in synth_circuit {
+        score_instruction(&inst_name, &inst_params, &inst_qubits);
+    }
+    1.0 - gate_fidelities.into_iter().product::<f64>()
+}
+
+/// Perform 2q unitary synthesis for a given `unitary`. If some `target` is provided,
+/// the decomposition will be hardware-aware and take into the account the reported
+/// gate errors to select the best method among the options. If `target` is `None``,
+/// the decompostion will use the given `basis_gates` and the first valid decomposition
+/// will be returned (no selection).
+fn run_2q_unitary_synthesis(
+    py: Python,
+    unitary: Array2<Complex64>,
+    ref_qubits: &[PhysicalQubit; 2],
+    coupling_edges: &HashSet<[PhysicalQubit; 2]>,
+    target: Option<&Target>,
+    basis_gates: HashSet<String>,
+    approximation_degree: Option<f64>,
+    natural_direction: Option<bool>,
+    pulse_optimize: Option<bool>,
+    out_dag: &mut DAGCircuit,
+    out_qargs: &[Qubit],
+    mut apply_original_op: impl FnMut(&mut DAGCircuit) -> PyResult<()>,
+) -> PyResult<()> {
+    // Find decomposer candidates
+    let decomposers = match target {
+        Some(target) => {
+            let decomposers_2q = get_2q_decomposers_from_target(
+                py,
+                target,
+                ref_qubits,
+                approximation_degree,
+                pulse_optimize,
+            )?;
+            decomposers_2q.unwrap_or_default()
+        }
+        None => {
+            let basis_gates: IndexSet<&str> = basis_gates.iter().map(String::as_str).collect();
+            let decomposer_item: Option<DecomposerElement> =
+                get_2q_decomposer_from_basis(basis_gates, approximation_degree, pulse_optimize)?;
+            if decomposer_item.is_none() {
+                apply_original_op(out_dag)?;
+                return Ok(());
+            };
+            vec![decomposer_item.unwrap()]
+        }
+    };
+
+    // If there's a single decomposer candidate, avoid computing synthesis score.
+    // This will ALWAYS be the path if the `target` is `None` (`basis_gates` used).
+    if decomposers.len() == 1 {
+        let decomposer_item = decomposers.first().unwrap();
+        let preferred_dir = preferred_direction(
+            ref_qubits,
+            natural_direction,
+            coupling_edges,
+            target,
+            decomposer_item,
+        )?;
+
+        match decomposer_item.decomposer {
+            DecomposerType::TwoQubitBasis(_) => {
+                let synth = synth_su4_sequence(
+                    &unitary,
+                    decomposer_item,
+                    preferred_dir,
+                    approximation_degree,
+                )?;
+                apply_synth_sequence(py, out_dag, out_qargs, &synth)?;
+            }
+            DecomposerType::TwoQubitControlledU(_) => {
+                let synth = synth_su4_sequence(
+                    &unitary,
+                    decomposer_item,
+                    preferred_dir,
+                    approximation_degree,
+                )?;
+                apply_synth_sequence(py, out_dag, out_qargs, &synth)?;
+            }
+            DecomposerType::XX(_) => {
+                let synth = synth_su4_dag(
+                    py,
+                    &unitary,
+                    decomposer_item,
+                    preferred_dir,
+                    approximation_degree,
+                )?;
+                apply_synth_dag(py, out_dag, out_qargs, &synth)?;
+            }
+        }
+        return Ok(());
+    }
+
+    // If there is more than one available decomposer, select the one with the best synthesis score.
+    // This will only happen if `target` is not `None`, so we can assume that there is some target from
+    // this point onwards. The scored SEQUENCEs and DAGs are stored in independent vectors to avoid defining
+    // yet another custom type.
+    let mut synth_errors_sequence = Vec::new();
+    let mut synth_errors_dag = Vec::new();
+
+    // The sequence synthesis logic can be shared between TwoQubitBasis and TwoQubitControlledU,
+    // but the DAG logic needs to stay independent.
+    let synth_sequence = |decomposer, preferred_dir| -> PyResult<(TwoQubitUnitarySequence, f64)> {
+        let sequence =
+            synth_su4_sequence(&unitary, decomposer, preferred_dir, approximation_degree)?;
+        let scoring_info =
+            sequence
+                .gate_sequence
+                .gates()
+                .iter()
+                .map(|(gate, params, qubit_ids)| {
+                    let inst_qubits = qubit_ids.iter().map(|q| ref_qubits[*q as usize]).collect();
+                    match gate {
+                        Some(gate) => (
+                            gate.name().to_string(),
+                            Some(params.iter().map(|p| Param::Float(*p)).collect()),
+                            inst_qubits,
+                        ),
+                        None => (
+                            sequence.decomp_op.name().to_string(),
+                            Some(params.iter().map(|p| Param::Float(*p)).collect()),
+                            inst_qubits,
+                        ),
+                    }
+                });
+        let score = synth_error(py, scoring_info, target.unwrap());
+        Ok((sequence, score))
+    };
+
+    for decomposer in &decomposers {
+        let preferred_dir = preferred_direction(
+            ref_qubits,
+            natural_direction,
+            coupling_edges,
+            target,
+            decomposer,
+        )?;
+        match &decomposer.decomposer {
+            DecomposerType::TwoQubitBasis(_) => {
+                synth_errors_sequence.push(synth_sequence(decomposer, preferred_dir)?);
+            }
+            DecomposerType::TwoQubitControlledU(_) => {
+                synth_errors_sequence.push(synth_sequence(decomposer, preferred_dir)?);
+            }
+            DecomposerType::XX(_) => {
+                let synth_dag = synth_su4_dag(
+                    py,
+                    &unitary,
+                    decomposer,
+                    preferred_dir,
+                    approximation_degree,
+                )?;
+                let scoring_info = synth_dag
+                    .topological_op_nodes()
+                    .expect("Unexpected error in dag.topological_op_nodes()")
+                    .map(|node| {
+                        let NodeType::Operation(inst) = &synth_dag[node] else {
+                            unreachable!("DAG node must be an instruction")
+                        };
+                        let inst_qubits = synth_dag
+                            .get_qargs(inst.qubits)
+                            .iter()
+                            .map(|q| ref_qubits[q.0 as usize])
+                            .collect();
+                        (
+                            inst.op.name().to_string(),
+                            inst.params.clone().map(|boxed| *boxed),
+                            inst_qubits,
+                        )
+                    });
+                let score = synth_error(py, scoring_info, target.unwrap());
+                synth_errors_dag.push((synth_dag, score));
+            }
+        }
+    }
+
+    // Resolve synthesis scores between sequence and DAG.
+    let synth_sequence = synth_errors_sequence
+        .iter()
+        .enumerate()
+        .min_by(|error1, error2| error1.1 .1.partial_cmp(&error2.1 .1).unwrap())
+        .map(|(index, _)| &synth_errors_sequence[index]);
+
+    let synth_dag = synth_errors_dag
+        .iter()
+        .enumerate()
+        .min_by(|error1, error2| error1.1 .1.partial_cmp(&error2.1 .1).unwrap())
+        .map(|(index, _)| &synth_errors_dag[index]);
+
+    match (synth_sequence, synth_dag) {
+        (None, None) => apply_original_op(out_dag)?,
+        (Some((sequence, _)), None) => apply_synth_sequence(py, out_dag, out_qargs, sequence)?,
+        (None, Some((dag, _))) => apply_synth_dag(py, out_dag, out_qargs, dag)?,
+        (Some((sequence, sequence_error)), Some((dag, dag_error))) => {
+            if sequence_error > dag_error {
+                apply_synth_dag(py, out_dag, out_qargs, dag)?
+            } else {
+                apply_synth_sequence(py, out_dag, out_qargs, sequence)?
+            }
+        }
+    };
+    Ok(())
+}
+
 #[pymodule]
 pub fn unitary_synthesis(m: &Bound<PyModule>) -> PyResult<()> {
     m.add_wrapped(wrap_pyfunction!(py_run_main_loop))?;
diff --git a/pyproject.toml b/pyproject.toml
index 0ff81bf9add737e7670c3da8b1caef587ae0d626..61d84548473777cd06b11213ec66ed3d41b64f4c 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -70,7 +70,7 @@ Issues = "https://github.com/Qiskit/qiskit/issues"
 Changelog = "https://docs.quantum.ibm.com/api/qiskit/release-notes"
 
 [project.entry-points."qiskit.unitary_synthesis"]
-default = "qiskit.transpiler.passes.synthesis.unitary_synthesis:DefaultUnitarySynthesis"
+default = "qiskit.transpiler.passes.synthesis.default_unitary_synth_plugin:DefaultUnitarySynthesis"
 aqc = "qiskit.transpiler.passes.synthesis.aqc_plugin:AQCSynthesisPlugin"
 sk = "qiskit.transpiler.passes.synthesis.solovay_kitaev_synthesis:SolovayKitaevSynthesis"
 
diff --git a/qiskit/transpiler/passes/synthesis/default_unitary_synth_plugin.py b/qiskit/transpiler/passes/synthesis/default_unitary_synth_plugin.py
new file mode 100644
index 0000000000000000000000000000000000000000..4cf675cb15b82c180d7fba97d9c8c56a08cafc60
--- /dev/null
+++ b/qiskit/transpiler/passes/synthesis/default_unitary_synth_plugin.py
@@ -0,0 +1,653 @@
+# This code is part of Qiskit.
+#
+# (C) Copyright IBM 2017, 2020.
+#
+# This code is licensed under the Apache License, Version 2.0. You may
+# obtain a copy of this license in the LICENSE.txt file in the root directory
+# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
+#
+# Any modifications or derivative works of this code must retain this
+# copyright notice, and modified files need to carry a notice indicating
+# that they have been altered from the originals.
+
+"""
+=========================================================================================
+Unitary Synthesis Plugin (in :mod:`qiskit.transpiler.passes.synthesis.unitary_synthesis`)
+=========================================================================================
+
+.. autosummary::
+   :toctree: ../stubs/
+
+   DefaultUnitarySynthesis
+"""
+
+from __future__ import annotations
+from math import pi, inf, isclose
+from itertools import product
+from functools import partial
+import numpy as np
+
+from qiskit.circuit import Gate, Parameter
+from qiskit.circuit.library.standard_gates import (
+    iSwapGate,
+    CXGate,
+    CZGate,
+    RXXGate,
+    RZXGate,
+    RZZGate,
+    RYYGate,
+    ECRGate,
+    RXGate,
+    SXGate,
+    XGate,
+    RZGate,
+    UGate,
+    PhaseGate,
+    U1Gate,
+    U2Gate,
+    U3Gate,
+    RYGate,
+    RGate,
+    CRXGate,
+    CRYGate,
+    CRZGate,
+    CPhaseGate,
+)
+from qiskit.converters import circuit_to_dag
+from qiskit.dagcircuit.dagcircuit import DAGCircuit
+from qiskit.dagcircuit.dagnode import DAGOpNode
+from qiskit.exceptions import QiskitError
+from qiskit.quantum_info import Operator
+from qiskit.synthesis.two_qubit.xx_decompose import XXDecomposer, XXEmbodiments
+from qiskit.synthesis.two_qubit.two_qubit_decompose import (
+    TwoQubitBasisDecomposer,
+    TwoQubitWeylDecomposition,
+    TwoQubitControlledUDecomposer,
+)
+from qiskit.transpiler.exceptions import TranspilerError
+from qiskit.transpiler.passes.optimization.optimize_1q_decomposition import (
+    Optimize1qGatesDecomposition,
+    _possible_decomposers,
+)
+from qiskit.transpiler.passes.synthesis import plugin
+
+
+GATE_NAME_MAP = {
+    "cx": CXGate._standard_gate,
+    "rx": RXGate._standard_gate,
+    "sx": SXGate._standard_gate,
+    "x": XGate._standard_gate,
+    "rz": RZGate._standard_gate,
+    "u": UGate._standard_gate,
+    "p": PhaseGate._standard_gate,
+    "u1": U1Gate._standard_gate,
+    "u2": U2Gate._standard_gate,
+    "u3": U3Gate._standard_gate,
+    "ry": RYGate._standard_gate,
+    "r": RGate._standard_gate,
+    "rzz": RZZGate._standard_gate,
+    "ryy": RYYGate._standard_gate,
+    "rxx": RXXGate._standard_gate,
+    "rzx": RXXGate._standard_gate,
+    "cp": CPhaseGate._standard_gate,
+    "crx": RXXGate._standard_gate,
+    "cry": RXXGate._standard_gate,
+    "crz": RXXGate._standard_gate,
+}
+
+KAK_GATE_PARAM_NAMES = {
+    "rxx": RXXGate,
+    "rzz": RZZGate,
+    "ryy": RYYGate,
+    "rzx": RZXGate,
+    "cphase": CPhaseGate,
+    "crx": CRXGate,
+    "cry": CRYGate,
+    "crz": CRZGate,
+}
+
+KAK_GATE_NAMES = {
+    "cx": CXGate(),
+    "cz": CZGate(),
+    "iswap": iSwapGate(),
+    "ecr": ECRGate(),
+}
+
+
+def _choose_kak_gate(basis_gates):
+    """Choose the first available 2q gate to use in the KAK decomposition."""
+    kak_gate = None
+    kak_gates = sorted(set(basis_gates or []).intersection(KAK_GATE_NAMES.keys()))
+    kak_gates_params = sorted(set(basis_gates or []).intersection(KAK_GATE_PARAM_NAMES.keys()))
+
+    if kak_gates_params:
+        kak_gate = KAK_GATE_PARAM_NAMES[kak_gates_params[0]]
+
+    elif kak_gates:
+        kak_gate = KAK_GATE_NAMES[kak_gates[0]]
+
+    return kak_gate
+
+
+def _choose_euler_basis(basis_gates):
+    """Choose the first available 1q basis to use in the Euler decomposition."""
+    basis_set = set(basis_gates or [])
+    decomposers = _possible_decomposers(basis_set)
+    if decomposers:
+        return decomposers[0]
+    return "U"
+
+
+def _find_matching_euler_bases(target, qubit):
+    """Find matching available 1q basis to use in the Euler decomposition."""
+    basis_set = target.operation_names_for_qargs((qubit,))
+    return _possible_decomposers(basis_set)
+
+
+def _decomposer_2q_from_basis_gates(basis_gates, pulse_optimize=None, approximation_degree=None):
+    decomposer2q = None
+    kak_gate = _choose_kak_gate(basis_gates)
+    euler_basis = _choose_euler_basis(basis_gates)
+    basis_fidelity = approximation_degree or 1.0
+
+    if kak_gate in KAK_GATE_PARAM_NAMES.values():
+        decomposer2q = TwoQubitControlledUDecomposer(kak_gate, euler_basis)
+    elif kak_gate is not None:
+        decomposer2q = TwoQubitBasisDecomposer(
+            kak_gate,
+            basis_fidelity=basis_fidelity,
+            euler_basis=euler_basis,
+            pulse_optimize=pulse_optimize,
+        )
+    return decomposer2q
+
+
+def _error(circuit, target=None, qubits=None):
+    """
+    Calculate a rough error for a `circuit` that runs on specific
+    `qubits` of `target`.
+
+    Use basis errors from target if available, otherwise use length
+    of circuit as a weak proxy for error.
+    """
+    if target is None:
+        if isinstance(circuit, DAGCircuit):
+            return len(circuit.op_nodes())
+        else:
+            return len(circuit)
+    gate_fidelities = []
+    gate_durations = []
+
+    def score_instruction(inst, inst_qubits):
+        try:
+            keys = target.operation_names_for_qargs(inst_qubits)
+            for key in keys:
+                target_op = target.operation_from_name(key)
+                if isinstance(circuit, DAGCircuit):
+                    op = inst.op
+                else:
+                    op = inst.operation
+                if isinstance(target_op, op.base_class) and (
+                    target_op.is_parameterized()
+                    or all(
+                        isclose(float(p1), float(p2)) for p1, p2 in zip(target_op.params, op.params)
+                    )
+                ):
+                    inst_props = target[key].get(inst_qubits, None)
+                    if inst_props is not None:
+                        error = getattr(inst_props, "error", 0.0) or 0.0
+                        duration = getattr(inst_props, "duration", 0.0) or 0.0
+                        gate_fidelities.append(1 - error)
+                        gate_durations.append(duration)
+                    else:
+                        gate_fidelities.append(1.0)
+                        gate_durations.append(0.0)
+
+                    break
+            else:
+                raise KeyError
+        except KeyError as error:
+            if isinstance(circuit, DAGCircuit):
+                op = inst.op
+            else:
+                op = inst.operation
+            raise TranspilerError(
+                f"Encountered a bad synthesis. " f"Target has no {op} on qubits {qubits}."
+            ) from error
+
+    if isinstance(circuit, DAGCircuit):
+        for inst in circuit.topological_op_nodes():
+            inst_qubits = tuple(qubits[circuit.find_bit(q).index] for q in inst.qargs)
+            score_instruction(inst, inst_qubits)
+    else:
+        for inst in circuit:
+            inst_qubits = tuple(qubits[circuit.find_bit(q).index] for q in inst.qubits)
+            score_instruction(inst, inst_qubits)
+    # TODO:return np.sum(gate_durations)
+    return 1 - np.prod(gate_fidelities)
+
+
+def _preferred_direction(
+    decomposer2q, qubits, natural_direction, coupling_map=None, gate_lengths=None, gate_errors=None
+):
+    """
+    `decomposer2q` decomposes an SU(4) over `qubits`. A user sets `natural_direction`
+    to indicate whether they prefer synthesis in a hardware-native direction.
+    If yes, we return the `preferred_direction` here. If no hardware direction is
+    preferred, we raise an error (unless natural_direction is None).
+    We infer this from `coupling_map`, `gate_lengths`, `gate_errors`.
+
+    Returns [0, 1] if qubits are correct in the hardware-native direction.
+    Returns [1, 0] if qubits must be flipped to match hardware-native direction.
+    """
+    qubits_tuple = tuple(qubits)
+    reverse_tuple = qubits_tuple[::-1]
+
+    preferred_direction = None
+    if natural_direction in {None, True}:
+        # find native gate directions from a (non-bidirectional) coupling map
+        if coupling_map is not None:
+            neighbors0 = coupling_map.neighbors(qubits[0])
+            zero_one = qubits[1] in neighbors0
+            neighbors1 = coupling_map.neighbors(qubits[1])
+            one_zero = qubits[0] in neighbors1
+            if zero_one and not one_zero:
+                preferred_direction = [0, 1]
+            if one_zero and not zero_one:
+                preferred_direction = [1, 0]
+        # otherwise infer natural directions from gate durations or gate errors
+        if preferred_direction is None and (gate_lengths or gate_errors):
+            cost_0_1 = inf
+            cost_1_0 = inf
+            try:
+                cost_0_1 = next(
+                    duration
+                    for gate, duration in gate_lengths.get(qubits_tuple, [])
+                    if gate == decomposer2q.gate
+                )
+            except StopIteration:
+                pass
+            try:
+                cost_1_0 = next(
+                    duration
+                    for gate, duration in gate_lengths.get(reverse_tuple, [])
+                    if gate == decomposer2q.gate
+                )
+            except StopIteration:
+                pass
+            if not (cost_0_1 < inf or cost_1_0 < inf):
+                try:
+                    cost_0_1 = next(
+                        error
+                        for gate, error in gate_errors.get(qubits_tuple, [])
+                        if gate == decomposer2q.gate
+                    )
+                except StopIteration:
+                    pass
+                try:
+                    cost_1_0 = next(
+                        error
+                        for gate, error in gate_errors.get(reverse_tuple, [])
+                        if gate == decomposer2q.gate
+                    )
+                except StopIteration:
+                    pass
+            if cost_0_1 < cost_1_0:
+                preferred_direction = [0, 1]
+            elif cost_1_0 < cost_0_1:
+                preferred_direction = [1, 0]
+    if natural_direction is True and preferred_direction is None:
+        raise TranspilerError(
+            f"No preferred direction of gate on qubits {qubits} "
+            "could be determined from coupling map or "
+            "gate lengths / gate errors."
+        )
+    return preferred_direction
+
+
+class DefaultUnitarySynthesis(plugin.UnitarySynthesisPlugin):
+    """The default unitary synthesis plugin."""
+
+    @property
+    def supports_basis_gates(self):
+        return True
+
+    @property
+    def supports_coupling_map(self):
+        return True
+
+    @property
+    def supports_natural_direction(self):
+        return True
+
+    @property
+    def supports_pulse_optimize(self):
+        return True
+
+    @property
+    def supports_gate_lengths(self):
+        return False
+
+    @property
+    def supports_gate_errors(self):
+        return False
+
+    @property
+    def supports_gate_lengths_by_qubit(self):
+        return True
+
+    @property
+    def supports_gate_errors_by_qubit(self):
+        return True
+
+    @property
+    def max_qubits(self):
+        return None
+
+    @property
+    def min_qubits(self):
+        return None
+
+    @property
+    def supported_bases(self):
+        return None
+
+    @property
+    def supports_target(self):
+        return True
+
+    def __init__(self):
+        super().__init__()
+        self._decomposer_cache = {}
+
+    def _decomposer_2q_from_target(self, target, qubits, approximation_degree):
+        # we just need 2-qubit decomposers, in any direction.
+        # we'll fix the synthesis direction later.
+        qubits_tuple = tuple(sorted(qubits))
+        reverse_tuple = qubits_tuple[::-1]
+        if qubits_tuple in self._decomposer_cache:
+            return self._decomposer_cache[qubits_tuple]
+
+        # available instructions on this qubit pair, and their associated property.
+        available_2q_basis = {}
+        available_2q_props = {}
+
+        # 2q gates sent to 2q decomposers must not have any symbolic parameters.  The
+        # gates must be convertable to a numeric matrix. If a basis gate supports an arbitrary
+        # angle, we have to choose one angle (or more.)
+        def _replace_parameterized_gate(op):
+            if isinstance(op, RXXGate) and isinstance(op.params[0], Parameter):
+                op = RXXGate(pi / 2)
+            elif isinstance(op, RZXGate) and isinstance(op.params[0], Parameter):
+                op = RZXGate(pi / 4)
+            elif isinstance(op, RZZGate) and isinstance(op.params[0], Parameter):
+                op = RZZGate(pi / 2)
+            return op
+
+        try:
+            keys = target.operation_names_for_qargs(qubits_tuple)
+            for key in keys:
+                op = target.operation_from_name(key)
+                if not isinstance(op, Gate):
+                    continue
+                available_2q_basis[key] = _replace_parameterized_gate(op)
+                available_2q_props[key] = target[key][qubits_tuple]
+        except KeyError:
+            pass
+        try:
+            keys = target.operation_names_for_qargs(reverse_tuple)
+            for key in keys:
+                if key not in available_2q_basis:
+                    op = target.operation_from_name(key)
+                    if not isinstance(op, Gate):
+                        continue
+                    available_2q_basis[key] = _replace_parameterized_gate(op)
+                    available_2q_props[key] = target[key][reverse_tuple]
+        except KeyError:
+            pass
+        if not available_2q_basis:
+            raise TranspilerError(
+                f"Target has no gates available on qubits {qubits} to synthesize over."
+            )
+        # available decomposition basis on each of the qubits of the pair
+        # NOTE: assumes both qubits have the same single-qubit gates
+        available_1q_basis = _find_matching_euler_bases(target, qubits_tuple[0])
+
+        # find all decomposers
+        # TODO: reduce number of decomposers here somehow
+        decomposers = []
+
+        def is_supercontrolled(gate):
+            try:
+                operator = Operator(gate)
+            except QiskitError:
+                return False
+            kak = TwoQubitWeylDecomposition(operator.data)
+            return isclose(kak.a, pi / 4) and isclose(kak.c, 0.0)
+
+        def is_controlled(gate):
+            try:
+                operator = Operator(gate)
+            except QiskitError:
+                return False
+            kak = TwoQubitWeylDecomposition(operator.data)
+            return isclose(kak.b, 0.0) and isclose(kak.c, 0.0)
+
+        # possible supercontrolled decomposers (i.e. TwoQubitBasisDecomposer)
+        supercontrolled_basis = {
+            k: v for k, v in available_2q_basis.items() if is_supercontrolled(v)
+        }
+        for basis_1q, basis_2q in product(available_1q_basis, supercontrolled_basis.keys()):
+            props = available_2q_props.get(basis_2q)
+            if props is None:
+                basis_2q_fidelity = 1.0
+            else:
+                error = getattr(props, "error", 0.0)
+                if error is None:
+                    error = 0.0
+                basis_2q_fidelity = 1 - error
+            if approximation_degree is not None:
+                basis_2q_fidelity *= approximation_degree
+            decomposer = TwoQubitBasisDecomposer(
+                supercontrolled_basis[basis_2q],
+                euler_basis=basis_1q,
+                basis_fidelity=basis_2q_fidelity,
+            )
+            decomposers.append(decomposer)
+
+        # If our 2q basis gates are a subset of cx, ecr, or cz then we know TwoQubitBasisDecomposer
+        # is an ideal decomposition and there is no need to bother calculating the XX embodiments
+        # or try the XX decomposer
+        if {"cx", "cz", "ecr"}.issuperset(available_2q_basis):
+            self._decomposer_cache[qubits_tuple] = decomposers
+            return decomposers
+
+        # possible controlled decomposers (i.e. XXDecomposer)
+        controlled_basis = {k: v for k, v in available_2q_basis.items() if is_controlled(v)}
+        basis_2q_fidelity = {}
+        embodiments = {}
+        pi2_basis = None
+        for k, v in controlled_basis.items():
+            strength = 2 * TwoQubitWeylDecomposition(Operator(v).data).a  # pi/2: fully entangling
+            # each strength has its own fidelity
+            props = available_2q_props.get(k)
+            if props is None:
+                basis_2q_fidelity[strength] = 1.0
+            else:
+                error = getattr(props, "error", 0.0)
+                if error is None:
+                    error = 0.0
+                basis_2q_fidelity[strength] = 1 - error
+            # rewrite XX of the same strength in terms of it
+            embodiment = XXEmbodiments[v.base_class]
+            if len(embodiment.parameters) == 1:
+                embodiments[strength] = embodiment.assign_parameters([strength])
+            else:
+                embodiments[strength] = embodiment
+            # basis equivalent to CX are well optimized so use for the pi/2 angle if available
+            if isclose(strength, pi / 2) and k in supercontrolled_basis:
+                pi2_basis = v
+        # if we are using the approximation_degree knob, use it to scale already-given fidelities
+        if approximation_degree is not None:
+            basis_2q_fidelity = {k: v * approximation_degree for k, v in basis_2q_fidelity.items()}
+        if basis_2q_fidelity:
+            for basis_1q in available_1q_basis:
+                if isinstance(pi2_basis, CXGate) and basis_1q == "ZSX":
+                    # If we're going to use the pulse optimal decomposition
+                    # in TwoQubitBasisDecomposer we need to compute the basis
+                    # fidelity to use for the decomposition. Either use the
+                    # cx error rate if approximation degree is None, or
+                    # the approximation degree value if it's a float
+                    if approximation_degree is None:
+                        props = target["cx"].get(qubits_tuple)
+                        if props is not None:
+                            fidelity = 1.0 - getattr(props, "error", 0.0)
+                        else:
+                            fidelity = 1.0
+                    else:
+                        fidelity = approximation_degree
+                    pi2_decomposer = TwoQubitBasisDecomposer(
+                        pi2_basis,
+                        euler_basis=basis_1q,
+                        basis_fidelity=fidelity,
+                        pulse_optimize=True,
+                    )
+                    embodiments.update({pi / 2: XXEmbodiments[pi2_decomposer.gate.base_class]})
+                else:
+                    pi2_decomposer = None
+                decomposer = XXDecomposer(
+                    basis_fidelity=basis_2q_fidelity,
+                    euler_basis=basis_1q,
+                    embodiments=embodiments,
+                    backup_optimizer=pi2_decomposer,
+                )
+                decomposers.append(decomposer)
+
+        self._decomposer_cache[qubits_tuple] = decomposers
+        return decomposers
+
+    def run(self, unitary, **options):
+        # Approximation degree is set directly as an attribute on the
+        # instance by the UnitarySynthesis pass here as it's not part of
+        # plugin interface. However if for some reason it's not set assume
+        # it's 1.
+        approximation_degree = getattr(self, "_approximation_degree", 1.0)
+        basis_gates = options["basis_gates"]
+        coupling_map = options["coupling_map"][0]
+        natural_direction = options["natural_direction"]
+        pulse_optimize = options["pulse_optimize"]
+        gate_lengths = options["gate_lengths_by_qubit"]
+        gate_errors = options["gate_errors_by_qubit"]
+        qubits = options["coupling_map"][1]
+        target = options["target"]
+
+        if unitary.shape == (2, 2):
+            _decomposer1q = Optimize1qGatesDecomposition(basis_gates, target)
+            sequence = _decomposer1q._resynthesize_run(unitary, qubits[0])
+            if sequence is None:
+                return None
+            return _decomposer1q._gate_sequence_to_dag(sequence)
+        elif unitary.shape == (4, 4):
+            # select synthesizers that can lower to the target
+            if target is not None:
+                decomposers2q = self._decomposer_2q_from_target(
+                    target, qubits, approximation_degree
+                )
+            else:
+                decomposer2q = _decomposer_2q_from_basis_gates(
+                    basis_gates, pulse_optimize, approximation_degree
+                )
+                decomposers2q = [decomposer2q] if decomposer2q is not None else []
+            # choose the cheapest output among synthesized circuits
+            synth_circuits = []
+            # If we have a single TwoQubitBasisDecomposer skip dag creation as we don't need to
+            # store and can instead manually create the synthesized gates directly in the output dag
+            if len(decomposers2q) == 1 and isinstance(decomposers2q[0], TwoQubitBasisDecomposer):
+                preferred_direction = _preferred_direction(
+                    decomposers2q[0],
+                    qubits,
+                    natural_direction,
+                    coupling_map,
+                    gate_lengths,
+                    gate_errors,
+                )
+                return self._synth_su4_no_dag(
+                    unitary, decomposers2q[0], preferred_direction, approximation_degree
+                )
+            for decomposer2q in decomposers2q:
+                preferred_direction = _preferred_direction(
+                    decomposer2q, qubits, natural_direction, coupling_map, gate_lengths, gate_errors
+                )
+                synth_circuit = self._synth_su4(
+                    unitary, decomposer2q, preferred_direction, approximation_degree
+                )
+                synth_circuits.append(synth_circuit)
+            synth_circuit = min(
+                synth_circuits,
+                key=partial(_error, target=target, qubits=tuple(qubits)),
+                default=None,
+            )
+        else:
+            from qiskit.synthesis.unitary.qsd import (  # pylint: disable=cyclic-import
+                qs_decomposition,
+            )
+
+            # only decompose if needed. TODO: handle basis better
+            synth_circuit = qs_decomposition(unitary) if (basis_gates or target) else None
+        if synth_circuit is None:
+            return None
+        if isinstance(synth_circuit, DAGCircuit):
+            return synth_circuit
+        return circuit_to_dag(synth_circuit)
+
+    def _synth_su4_no_dag(self, unitary, decomposer2q, preferred_direction, approximation_degree):
+        approximate = not approximation_degree == 1.0
+        synth_circ = decomposer2q._inner_decomposer(unitary, approximate=approximate)
+        if not preferred_direction:
+            return (synth_circ, synth_circ.global_phase, decomposer2q.gate)
+
+        synth_direction = None
+        # if the gates in synthesis are in the opposite direction of the preferred direction
+        # resynthesize a new operator which is the original conjugated by swaps.
+        # this new operator is doubly mirrored from the original and is locally equivalent.
+        for gate, _params, qubits in synth_circ:
+            if gate is None or gate == CXGate._standard_gate:
+                synth_direction = qubits
+        if synth_direction is not None and synth_direction != preferred_direction:
+            # TODO: Avoid using a dag to correct the synthesis direction
+            return self._reversed_synth_su4(unitary, decomposer2q, approximation_degree)
+        return (synth_circ, synth_circ.global_phase, decomposer2q.gate)
+
+    def _synth_su4(self, su4_mat, decomposer2q, preferred_direction, approximation_degree):
+        approximate = not approximation_degree == 1.0
+        synth_circ = decomposer2q(su4_mat, approximate=approximate, use_dag=True)
+        if not preferred_direction:
+            return synth_circ
+        synth_direction = None
+        # if the gates in synthesis are in the opposite direction of the preferred direction
+        # resynthesize a new operator which is the original conjugated by swaps.
+        # this new operator is doubly mirrored from the original and is locally equivalent.
+        for inst in synth_circ.topological_op_nodes():
+            if inst.op.num_qubits == 2:
+                synth_direction = [synth_circ.find_bit(q).index for q in inst.qargs]
+        if synth_direction is not None and synth_direction != preferred_direction:
+            return self._reversed_synth_su4(su4_mat, decomposer2q, approximation_degree)
+        return synth_circ
+
+    def _reversed_synth_su4(self, su4_mat, decomposer2q, approximation_degree):
+        approximate = not approximation_degree == 1.0
+        su4_mat_mm = su4_mat.copy()
+        su4_mat_mm[[1, 2]] = su4_mat_mm[[2, 1]]
+        su4_mat_mm[:, [1, 2]] = su4_mat_mm[:, [2, 1]]
+        synth_circ = decomposer2q(su4_mat_mm, approximate=approximate, use_dag=True)
+        out_dag = DAGCircuit()
+        out_dag.global_phase = synth_circ.global_phase
+        out_dag.add_qubits(list(reversed(synth_circ.qubits)))
+        flip_bits = out_dag.qubits[::-1]
+        for node in synth_circ.topological_op_nodes():
+            qubits = tuple(flip_bits[synth_circ.find_bit(x).index] for x in node.qargs)
+            node = DAGOpNode.from_instruction(
+                node._to_circuit_instruction().replace(qubits=qubits, params=node.params)
+            )
+            out_dag._apply_op_node_back(node)
+        return out_dag
diff --git a/qiskit/transpiler/passes/synthesis/unitary_synthesis.py b/qiskit/transpiler/passes/synthesis/unitary_synthesis.py
index 3dfd6caff65cc0a947ae09acba3a317180f3760f..d0c98e9569273d6f021bc106bba27dcccc6d0900 100644
--- a/qiskit/transpiler/passes/synthesis/unitary_synthesis.py
+++ b/qiskit/transpiler/passes/synthesis/unitary_synthesis.py
@@ -11,147 +11,26 @@
 # that they have been altered from the originals.
 
 """
-=========================================================================================
-Unitary Synthesis Plugin (in :mod:`qiskit.transpiler.passes.synthesis.unitary_synthesis`)
-=========================================================================================
-
-.. autosummary::
-   :toctree: ../stubs/
-
-   DefaultUnitarySynthesis
+Unitary Synthesis Transpiler Pass
 """
 
 from __future__ import annotations
-from math import pi, inf, isclose
 from typing import Any
-from itertools import product
-from functools import partial
-import numpy as np
 
 from qiskit.circuit.controlflow import CONTROL_FLOW_OP_NAMES
-from qiskit.circuit import Gate, Parameter, CircuitInstruction
-from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
-from qiskit.circuit.library.standard_gates import (
-    iSwapGate,
-    CXGate,
-    CZGate,
-    RXXGate,
-    RZXGate,
-    RZZGate,
-    RYYGate,
-    ECRGate,
-    RXGate,
-    SXGate,
-    XGate,
-    RZGate,
-    UGate,
-    PhaseGate,
-    U1Gate,
-    U2Gate,
-    U3Gate,
-    RYGate,
-    RGate,
-    CRXGate,
-    CRYGate,
-    CRZGate,
-    CPhaseGate,
-)
+from qiskit.circuit import CircuitInstruction
 from qiskit.converters import circuit_to_dag, dag_to_circuit
 from qiskit.dagcircuit.dagcircuit import DAGCircuit
 from qiskit.dagcircuit.dagnode import DAGOpNode
-from qiskit.exceptions import QiskitError
-from qiskit.quantum_info import Operator
 from qiskit.synthesis.one_qubit import one_qubit_decompose
-from qiskit.synthesis.two_qubit.xx_decompose import XXDecomposer, XXEmbodiments
-from qiskit.synthesis.two_qubit.two_qubit_decompose import (
-    TwoQubitBasisDecomposer,
-    TwoQubitWeylDecomposition,
-    TwoQubitControlledUDecomposer,
-)
+
 from qiskit.transpiler.basepasses import TransformationPass
 from qiskit.transpiler.coupling import CouplingMap
 from qiskit.transpiler.exceptions import TranspilerError
-from qiskit.transpiler.passes.optimization.optimize_1q_decomposition import (
-    Optimize1qGatesDecomposition,
-    _possible_decomposers,
-)
 from qiskit.transpiler.passes.synthesis import plugin
 from qiskit.transpiler.target import Target
 
-from qiskit._accelerate.unitary_synthesis import run_default_main_loop
-
-GATE_NAME_MAP = {
-    "cx": CXGate._standard_gate,
-    "rx": RXGate._standard_gate,
-    "sx": SXGate._standard_gate,
-    "x": XGate._standard_gate,
-    "rz": RZGate._standard_gate,
-    "u": UGate._standard_gate,
-    "p": PhaseGate._standard_gate,
-    "u1": U1Gate._standard_gate,
-    "u2": U2Gate._standard_gate,
-    "u3": U3Gate._standard_gate,
-    "ry": RYGate._standard_gate,
-    "r": RGate._standard_gate,
-    "rzz": RZZGate._standard_gate,
-    "ryy": RYYGate._standard_gate,
-    "rxx": RXXGate._standard_gate,
-    "rzx": RXXGate._standard_gate,
-    "cp": CPhaseGate._standard_gate,
-    "crx": RXXGate._standard_gate,
-    "cry": RXXGate._standard_gate,
-    "crz": RXXGate._standard_gate,
-}
-
-KAK_GATE_PARAM_NAMES = {
-    "rxx": RXXGate,
-    "rzz": RZZGate,
-    "ryy": RYYGate,
-    "rzx": RZXGate,
-    "cphase": CPhaseGate,
-    "crx": CRXGate,
-    "cry": CRYGate,
-    "crz": CRZGate,
-}
-
-KAK_GATE_NAMES = {
-    "cx": CXGate(),
-    "cz": CZGate(),
-    "iswap": iSwapGate(),
-    "ecr": ECRGate(),
-}
-
-GateNameToGate = get_standard_gate_name_mapping()
-
-
-def _choose_kak_gate(basis_gates):
-    """Choose the first available 2q gate to use in the KAK decomposition."""
-    kak_gate = None
-    kak_gates = sorted(set(basis_gates or []).intersection(KAK_GATE_NAMES.keys()))
-    kak_gates_params = sorted(set(basis_gates or []).intersection(KAK_GATE_PARAM_NAMES.keys()))
-
-    if kak_gates_params:
-        kak_gate = KAK_GATE_PARAM_NAMES[kak_gates_params[0]]
-
-    elif kak_gates:
-        kak_gate = KAK_GATE_NAMES[kak_gates[0]]
-
-    return kak_gate
-
-
-def _choose_euler_basis(basis_gates):
-    """Choose the first available 1q basis to use in the Euler decomposition."""
-    basis_set = set(basis_gates or [])
-    decomposers = _possible_decomposers(basis_set)
-    if decomposers:
-        return decomposers[0]
-    return "U"
-
-
-def _find_matching_euler_bases(target, qubit):
-    """Find matching available 1q basis to use in the Euler decomposition."""
-    basis_set = target.operation_names_for_qargs((qubit,))
-    return _possible_decomposers(basis_set)
+from qiskit._accelerate.unitary_synthesis import run_main_loop
 
 
 def _choose_bases(basis_gates, basis_dict=None):
@@ -172,167 +51,6 @@ def _choose_bases(basis_gates, basis_dict=None):
     return out_basis
 
 
-def _decomposer_2q_from_basis_gates(basis_gates, pulse_optimize=None, approximation_degree=None):
-    decomposer2q = None
-    kak_gate = _choose_kak_gate(basis_gates)
-    euler_basis = _choose_euler_basis(basis_gates)
-    basis_fidelity = approximation_degree or 1.0
-
-    if kak_gate in KAK_GATE_PARAM_NAMES.values():
-        decomposer2q = TwoQubitControlledUDecomposer(kak_gate, euler_basis)
-    elif kak_gate is not None:
-        decomposer2q = TwoQubitBasisDecomposer(
-            kak_gate,
-            basis_fidelity=basis_fidelity,
-            euler_basis=euler_basis,
-            pulse_optimize=pulse_optimize,
-        )
-    return decomposer2q
-
-
-def _error(circuit, target=None, qubits=None):
-    """
-    Calculate a rough error for a `circuit` that runs on specific
-    `qubits` of `target`.
-
-    Use basis errors from target if available, otherwise use length
-    of circuit as a weak proxy for error.
-    """
-    if target is None:
-        if isinstance(circuit, DAGCircuit):
-            return len(circuit.op_nodes())
-        else:
-            return len(circuit)
-    gate_fidelities = []
-    gate_durations = []
-
-    def score_instruction(inst, inst_qubits):
-        try:
-            keys = target.operation_names_for_qargs(inst_qubits)
-            for key in keys:
-                target_op = target.operation_from_name(key)
-                if isinstance(circuit, DAGCircuit):
-                    op = inst.op
-                else:
-                    op = inst.operation
-                if isinstance(target_op, op.base_class) and (
-                    target_op.is_parameterized()
-                    or all(
-                        isclose(float(p1), float(p2)) for p1, p2 in zip(target_op.params, op.params)
-                    )
-                ):
-                    inst_props = target[key].get(inst_qubits, None)
-                    if inst_props is not None:
-                        error = getattr(inst_props, "error", 0.0) or 0.0
-                        duration = getattr(inst_props, "duration", 0.0) or 0.0
-                        gate_fidelities.append(1 - error)
-                        gate_durations.append(duration)
-                    else:
-                        gate_fidelities.append(1.0)
-                        gate_durations.append(0.0)
-
-                    break
-            else:
-                raise KeyError
-        except KeyError as error:
-            if isinstance(circuit, DAGCircuit):
-                op = inst.op
-            else:
-                op = inst.operation
-            raise TranspilerError(
-                f"Encountered a bad synthesis. " f"Target has no {op} on qubits {qubits}."
-            ) from error
-
-    if isinstance(circuit, DAGCircuit):
-        for inst in circuit.topological_op_nodes():
-            inst_qubits = tuple(qubits[circuit.find_bit(q).index] for q in inst.qargs)
-            score_instruction(inst, inst_qubits)
-    else:
-        for inst in circuit:
-            inst_qubits = tuple(qubits[circuit.find_bit(q).index] for q in inst.qubits)
-            score_instruction(inst, inst_qubits)
-    # TODO:return np.sum(gate_durations)
-    return 1 - np.prod(gate_fidelities)
-
-
-def _preferred_direction(
-    decomposer2q, qubits, natural_direction, coupling_map=None, gate_lengths=None, gate_errors=None
-):
-    """
-    `decomposer2q` decomposes an SU(4) over `qubits`. A user sets `natural_direction`
-    to indicate whether they prefer synthesis in a hardware-native direction.
-    If yes, we return the `preferred_direction` here. If no hardware direction is
-    preferred, we raise an error (unless natural_direction is None).
-    We infer this from `coupling_map`, `gate_lengths`, `gate_errors`.
-
-    Returns [0, 1] if qubits are correct in the hardware-native direction.
-    Returns [1, 0] if qubits must be flipped to match hardware-native direction.
-    """
-    qubits_tuple = tuple(qubits)
-    reverse_tuple = qubits_tuple[::-1]
-
-    preferred_direction = None
-    if natural_direction in {None, True}:
-        # find native gate directions from a (non-bidirectional) coupling map
-        if coupling_map is not None:
-            neighbors0 = coupling_map.neighbors(qubits[0])
-            zero_one = qubits[1] in neighbors0
-            neighbors1 = coupling_map.neighbors(qubits[1])
-            one_zero = qubits[0] in neighbors1
-            if zero_one and not one_zero:
-                preferred_direction = [0, 1]
-            if one_zero and not zero_one:
-                preferred_direction = [1, 0]
-        # otherwise infer natural directions from gate durations or gate errors
-        if preferred_direction is None and (gate_lengths or gate_errors):
-            cost_0_1 = inf
-            cost_1_0 = inf
-            try:
-                cost_0_1 = next(
-                    duration
-                    for gate, duration in gate_lengths.get(qubits_tuple, [])
-                    if gate == decomposer2q.gate
-                )
-            except StopIteration:
-                pass
-            try:
-                cost_1_0 = next(
-                    duration
-                    for gate, duration in gate_lengths.get(reverse_tuple, [])
-                    if gate == decomposer2q.gate
-                )
-            except StopIteration:
-                pass
-            if not (cost_0_1 < inf or cost_1_0 < inf):
-                try:
-                    cost_0_1 = next(
-                        error
-                        for gate, error in gate_errors.get(qubits_tuple, [])
-                        if gate == decomposer2q.gate
-                    )
-                except StopIteration:
-                    pass
-                try:
-                    cost_1_0 = next(
-                        error
-                        for gate, error in gate_errors.get(reverse_tuple, [])
-                        if gate == decomposer2q.gate
-                    )
-                except StopIteration:
-                    pass
-            if cost_0_1 < cost_1_0:
-                preferred_direction = [0, 1]
-            elif cost_1_0 < cost_0_1:
-                preferred_direction = [1, 0]
-    if natural_direction is True and preferred_direction is None:
-        raise TranspilerError(
-            f"No preferred direction of gate on qubits {qubits} "
-            "could be determined from coupling map or "
-            "gate lengths / gate errors."
-        )
-    return preferred_direction
-
-
 class UnitarySynthesis(TransformationPass):
     """Synthesize gates according to their basis gates."""
 
@@ -454,6 +172,10 @@ class UnitarySynthesis(TransformationPass):
         if self.plugins:
             plugin_method = self.plugins.ext_plugins[self.method].obj
         else:
+            from qiskit.transpiler.passes.synthesis.default_unitary_synth_plugin import (
+                DefaultUnitarySynthesis,
+            )
+
             plugin_method = DefaultUnitarySynthesis()
         plugin_kwargs: dict[str, Any] = {"config": self._plugin_config}
         _gate_lengths = _gate_errors = None
@@ -489,19 +211,20 @@ class UnitarySynthesis(TransformationPass):
             else {}
         )
 
-        if self.method == "default" and self._target is not None:
+        if self.method == "default":
             _coupling_edges = (
                 set(self._coupling_map.get_edges()) if self._coupling_map is not None else set()
             )
-
-            out = run_default_main_loop(
+            out = run_main_loop(
                 dag,
                 list(qubit_indices.values()),
                 self._min_qubits,
                 self._target,
+                self._basis_gates,
                 _coupling_edges,
                 self._approximation_degree,
                 self._natural_direction,
+                self._pulse_optimize,
             )
             return out
         else:
@@ -697,351 +420,3 @@ def _build_gate_errors_by_qubit(target=None):
             if operation_and_errors:
                 gate_errors[qubits] = operation_and_errors
     return gate_errors
-
-
-class DefaultUnitarySynthesis(plugin.UnitarySynthesisPlugin):
-    """The default unitary synthesis plugin."""
-
-    @property
-    def supports_basis_gates(self):
-        return True
-
-    @property
-    def supports_coupling_map(self):
-        return True
-
-    @property
-    def supports_natural_direction(self):
-        return True
-
-    @property
-    def supports_pulse_optimize(self):
-        return True
-
-    @property
-    def supports_gate_lengths(self):
-        return False
-
-    @property
-    def supports_gate_errors(self):
-        return False
-
-    @property
-    def supports_gate_lengths_by_qubit(self):
-        return True
-
-    @property
-    def supports_gate_errors_by_qubit(self):
-        return True
-
-    @property
-    def max_qubits(self):
-        return None
-
-    @property
-    def min_qubits(self):
-        return None
-
-    @property
-    def supported_bases(self):
-        return None
-
-    @property
-    def supports_target(self):
-        return True
-
-    def __init__(self):
-        super().__init__()
-        self._decomposer_cache = {}
-
-    def _decomposer_2q_from_target(self, target, qubits, approximation_degree):
-        # we just need 2-qubit decomposers, in any direction.
-        # we'll fix the synthesis direction later.
-        qubits_tuple = tuple(sorted(qubits))
-        reverse_tuple = qubits_tuple[::-1]
-        if qubits_tuple in self._decomposer_cache:
-            return self._decomposer_cache[qubits_tuple]
-
-        # available instructions on this qubit pair, and their associated property.
-        available_2q_basis = {}
-        available_2q_props = {}
-
-        # 2q gates sent to 2q decomposers must not have any symbolic parameters.  The
-        # gates must be convertable to a numeric matrix. If a basis gate supports an arbitrary
-        # angle, we have to choose one angle (or more.)
-        def _replace_parameterized_gate(op):
-            if isinstance(op, RXXGate) and isinstance(op.params[0], Parameter):
-                op = RXXGate(pi / 2)
-            elif isinstance(op, RZXGate) and isinstance(op.params[0], Parameter):
-                op = RZXGate(pi / 4)
-            elif isinstance(op, RZZGate) and isinstance(op.params[0], Parameter):
-                op = RZZGate(pi / 2)
-            return op
-
-        try:
-            keys = target.operation_names_for_qargs(qubits_tuple)
-            for key in keys:
-                op = target.operation_from_name(key)
-                if not isinstance(op, Gate):
-                    continue
-                available_2q_basis[key] = _replace_parameterized_gate(op)
-                available_2q_props[key] = target[key][qubits_tuple]
-        except KeyError:
-            pass
-        try:
-            keys = target.operation_names_for_qargs(reverse_tuple)
-            for key in keys:
-                if key not in available_2q_basis:
-                    op = target.operation_from_name(key)
-                    if not isinstance(op, Gate):
-                        continue
-                    available_2q_basis[key] = _replace_parameterized_gate(op)
-                    available_2q_props[key] = target[key][reverse_tuple]
-        except KeyError:
-            pass
-        if not available_2q_basis:
-            raise TranspilerError(
-                f"Target has no gates available on qubits {qubits} to synthesize over."
-            )
-        # available decomposition basis on each of the qubits of the pair
-        # NOTE: assumes both qubits have the same single-qubit gates
-        available_1q_basis = _find_matching_euler_bases(target, qubits_tuple[0])
-
-        # find all decomposers
-        # TODO: reduce number of decomposers here somehow
-        decomposers = []
-
-        def is_supercontrolled(gate):
-            try:
-                operator = Operator(gate)
-            except QiskitError:
-                return False
-            kak = TwoQubitWeylDecomposition(operator.data)
-            return isclose(kak.a, pi / 4) and isclose(kak.c, 0.0)
-
-        def is_controlled(gate):
-            try:
-                operator = Operator(gate)
-            except QiskitError:
-                return False
-            kak = TwoQubitWeylDecomposition(operator.data)
-            return isclose(kak.b, 0.0) and isclose(kak.c, 0.0)
-
-        # possible supercontrolled decomposers (i.e. TwoQubitBasisDecomposer)
-        supercontrolled_basis = {
-            k: v for k, v in available_2q_basis.items() if is_supercontrolled(v)
-        }
-        for basis_1q, basis_2q in product(available_1q_basis, supercontrolled_basis.keys()):
-            props = available_2q_props.get(basis_2q)
-            if props is None:
-                basis_2q_fidelity = 1.0
-            else:
-                error = getattr(props, "error", 0.0)
-                if error is None:
-                    error = 0.0
-                basis_2q_fidelity = 1 - error
-            if approximation_degree is not None:
-                basis_2q_fidelity *= approximation_degree
-            decomposer = TwoQubitBasisDecomposer(
-                supercontrolled_basis[basis_2q],
-                euler_basis=basis_1q,
-                basis_fidelity=basis_2q_fidelity,
-            )
-            decomposers.append(decomposer)
-
-        # If our 2q basis gates are a subset of cx, ecr, or cz then we know TwoQubitBasisDecomposer
-        # is an ideal decomposition and there is no need to bother calculating the XX embodiments
-        # or try the XX decomposer
-        if {"cx", "cz", "ecr"}.issuperset(available_2q_basis):
-            self._decomposer_cache[qubits_tuple] = decomposers
-            return decomposers
-
-        # possible controlled decomposers (i.e. XXDecomposer)
-        controlled_basis = {k: v for k, v in available_2q_basis.items() if is_controlled(v)}
-        basis_2q_fidelity = {}
-        embodiments = {}
-        pi2_basis = None
-        for k, v in controlled_basis.items():
-            strength = 2 * TwoQubitWeylDecomposition(Operator(v).data).a  # pi/2: fully entangling
-            # each strength has its own fidelity
-            props = available_2q_props.get(k)
-            if props is None:
-                basis_2q_fidelity[strength] = 1.0
-            else:
-                error = getattr(props, "error", 0.0)
-                if error is None:
-                    error = 0.0
-                basis_2q_fidelity[strength] = 1 - error
-            # rewrite XX of the same strength in terms of it
-            embodiment = XXEmbodiments[v.base_class]
-            if len(embodiment.parameters) == 1:
-                embodiments[strength] = embodiment.assign_parameters([strength])
-            else:
-                embodiments[strength] = embodiment
-            # basis equivalent to CX are well optimized so use for the pi/2 angle if available
-            if isclose(strength, pi / 2) and k in supercontrolled_basis:
-                pi2_basis = v
-        # if we are using the approximation_degree knob, use it to scale already-given fidelities
-        if approximation_degree is not None:
-            basis_2q_fidelity = {k: v * approximation_degree for k, v in basis_2q_fidelity.items()}
-        if basis_2q_fidelity:
-            for basis_1q in available_1q_basis:
-                if isinstance(pi2_basis, CXGate) and basis_1q == "ZSX":
-                    # If we're going to use the pulse optimal decomposition
-                    # in TwoQubitBasisDecomposer we need to compute the basis
-                    # fidelity to use for the decomposition. Either use the
-                    # cx error rate if approximation degree is None, or
-                    # the approximation degree value if it's a float
-                    if approximation_degree is None:
-                        props = target["cx"].get(qubits_tuple)
-                        if props is not None:
-                            fidelity = 1.0 - getattr(props, "error", 0.0)
-                        else:
-                            fidelity = 1.0
-                    else:
-                        fidelity = approximation_degree
-                    pi2_decomposer = TwoQubitBasisDecomposer(
-                        pi2_basis,
-                        euler_basis=basis_1q,
-                        basis_fidelity=fidelity,
-                        pulse_optimize=True,
-                    )
-                    embodiments.update({pi / 2: XXEmbodiments[pi2_decomposer.gate.base_class]})
-                else:
-                    pi2_decomposer = None
-                decomposer = XXDecomposer(
-                    basis_fidelity=basis_2q_fidelity,
-                    euler_basis=basis_1q,
-                    embodiments=embodiments,
-                    backup_optimizer=pi2_decomposer,
-                )
-                decomposers.append(decomposer)
-
-        self._decomposer_cache[qubits_tuple] = decomposers
-        return decomposers
-
-    def run(self, unitary, **options):
-        # Approximation degree is set directly as an attribute on the
-        # instance by the UnitarySynthesis pass here as it's not part of
-        # plugin interface. However if for some reason it's not set assume
-        # it's 1.
-        approximation_degree = getattr(self, "_approximation_degree", 1.0)
-        basis_gates = options["basis_gates"]
-        coupling_map = options["coupling_map"][0]
-        natural_direction = options["natural_direction"]
-        pulse_optimize = options["pulse_optimize"]
-        gate_lengths = options["gate_lengths_by_qubit"]
-        gate_errors = options["gate_errors_by_qubit"]
-        qubits = options["coupling_map"][1]
-        target = options["target"]
-
-        if unitary.shape == (2, 2):
-            _decomposer1q = Optimize1qGatesDecomposition(basis_gates, target)
-            sequence = _decomposer1q._resynthesize_run(unitary, qubits[0])
-            if sequence is None:
-                return None
-            return _decomposer1q._gate_sequence_to_dag(sequence)
-        elif unitary.shape == (4, 4):
-            # select synthesizers that can lower to the target
-            if target is not None:
-                decomposers2q = self._decomposer_2q_from_target(
-                    target, qubits, approximation_degree
-                )
-            else:
-                decomposer2q = _decomposer_2q_from_basis_gates(
-                    basis_gates, pulse_optimize, approximation_degree
-                )
-                decomposers2q = [decomposer2q] if decomposer2q is not None else []
-            # choose the cheapest output among synthesized circuits
-            synth_circuits = []
-            # If we have a single TwoQubitBasisDecomposer skip dag creation as we don't need to
-            # store and can instead manually create the synthesized gates directly in the output dag
-            if len(decomposers2q) == 1 and isinstance(decomposers2q[0], TwoQubitBasisDecomposer):
-                preferred_direction = _preferred_direction(
-                    decomposers2q[0],
-                    qubits,
-                    natural_direction,
-                    coupling_map,
-                    gate_lengths,
-                    gate_errors,
-                )
-                return self._synth_su4_no_dag(
-                    unitary, decomposers2q[0], preferred_direction, approximation_degree
-                )
-            for decomposer2q in decomposers2q:
-                preferred_direction = _preferred_direction(
-                    decomposer2q, qubits, natural_direction, coupling_map, gate_lengths, gate_errors
-                )
-                synth_circuit = self._synth_su4(
-                    unitary, decomposer2q, preferred_direction, approximation_degree
-                )
-                synth_circuits.append(synth_circuit)
-            synth_circuit = min(
-                synth_circuits,
-                key=partial(_error, target=target, qubits=tuple(qubits)),
-                default=None,
-            )
-        else:
-            from qiskit.synthesis.unitary.qsd import (  # pylint: disable=cyclic-import
-                qs_decomposition,
-            )
-
-            # only decompose if needed. TODO: handle basis better
-            synth_circuit = qs_decomposition(unitary) if (basis_gates or target) else None
-        if synth_circuit is None:
-            return None
-        if isinstance(synth_circuit, DAGCircuit):
-            return synth_circuit
-        return circuit_to_dag(synth_circuit)
-
-    def _synth_su4_no_dag(self, unitary, decomposer2q, preferred_direction, approximation_degree):
-        approximate = not approximation_degree == 1.0
-        synth_circ = decomposer2q._inner_decomposer(unitary, approximate=approximate)
-        if not preferred_direction:
-            return (synth_circ, synth_circ.global_phase, decomposer2q.gate)
-
-        synth_direction = None
-        # if the gates in synthesis are in the opposite direction of the preferred direction
-        # resynthesize a new operator which is the original conjugated by swaps.
-        # this new operator is doubly mirrored from the original and is locally equivalent.
-        for gate, _params, qubits in synth_circ:
-            if gate is None or gate == CXGate._standard_gate:
-                synth_direction = qubits
-        if synth_direction is not None and synth_direction != preferred_direction:
-            # TODO: Avoid using a dag to correct the synthesis direction
-            return self._reversed_synth_su4(unitary, decomposer2q, approximation_degree)
-        return (synth_circ, synth_circ.global_phase, decomposer2q.gate)
-
-    def _synth_su4(self, su4_mat, decomposer2q, preferred_direction, approximation_degree):
-        approximate = not approximation_degree == 1.0
-        synth_circ = decomposer2q(su4_mat, approximate=approximate, use_dag=True)
-        if not preferred_direction:
-            return synth_circ
-        synth_direction = None
-        # if the gates in synthesis are in the opposite direction of the preferred direction
-        # resynthesize a new operator which is the original conjugated by swaps.
-        # this new operator is doubly mirrored from the original and is locally equivalent.
-        for inst in synth_circ.topological_op_nodes():
-            if inst.op.num_qubits == 2:
-                synth_direction = [synth_circ.find_bit(q).index for q in inst.qargs]
-        if synth_direction is not None and synth_direction != preferred_direction:
-            return self._reversed_synth_su4(su4_mat, decomposer2q, approximation_degree)
-        return synth_circ
-
-    def _reversed_synth_su4(self, su4_mat, decomposer2q, approximation_degree):
-        approximate = not approximation_degree == 1.0
-        su4_mat_mm = su4_mat.copy()
-        su4_mat_mm[[1, 2]] = su4_mat_mm[[2, 1]]
-        su4_mat_mm[:, [1, 2]] = su4_mat_mm[:, [2, 1]]
-        synth_circ = decomposer2q(su4_mat_mm, approximate=approximate, use_dag=True)
-        out_dag = DAGCircuit()
-        out_dag.global_phase = synth_circ.global_phase
-        out_dag.add_qubits(list(reversed(synth_circ.qubits)))
-        flip_bits = out_dag.qubits[::-1]
-        for node in synth_circ.topological_op_nodes():
-            qubits = tuple(flip_bits[synth_circ.find_bit(x).index] for x in node.qargs)
-            node = DAGOpNode.from_instruction(
-                node._to_circuit_instruction().replace(qubits=qubits, params=node.params)
-            )
-            out_dag._apply_op_node_back(node)
-        return out_dag
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/transpiler/test_unitary_synthesis.py b/test/python/transpiler/test_unitary_synthesis.py
index d93d6800985ce702dee61611ea04661bd1e29b1b..311816ab447cd922902ee61aad922bd1b1f6fa58 100644
--- a/test/python/transpiler/test_unitary_synthesis.py
+++ b/test/python/transpiler/test_unitary_synthesis.py
@@ -32,7 +32,6 @@ from qiskit.transpiler.passes import UnitarySynthesis
 from qiskit.quantum_info.operators import Operator
 from qiskit.quantum_info.random import random_unitary
 from qiskit.transpiler import PassManager, CouplingMap, Target, InstructionProperties
-from qiskit.transpiler.exceptions import TranspilerError
 from qiskit.exceptions import QiskitError
 from qiskit.transpiler.passes import (
     Collect2qBlocks,
@@ -126,7 +125,6 @@ class TestUnitarySynthesisBasisGates(QiskitTestCase):
         qc.unitary(op_1q.data, [0])
         qc.unitary(op_2q.data, [0, 1])
         qc.unitary(op_3q.data, [0, 1, 2])
-
         out = UnitarySynthesis(basis_gates=None, min_qubits=2)(qc)
         self.assertEqual(out.count_ops(), {"unitary": 3})
 
@@ -250,7 +248,7 @@ class TestUnitarySynthesisBasisGates(QiskitTestCase):
             natural_direction=True,
         )
         pm = PassManager([triv_layout_pass, unisynth_pass])
-        with self.assertRaises(TranspilerError):
+        with self.assertRaises(QiskitError):
             pm.run(qc)
 
     def test_two_qubit_pulse_optimal_none_optimal(self):
diff --git a/test/python/transpiler/test_unitary_synthesis_plugin.py b/test/python/transpiler/test_unitary_synthesis_plugin.py
index f6790e8ed14d0f030496bb1ff9caa3d2dadbc351..f4012bcff0444f46b9f3a66250e72bf6169b4694 100644
--- a/test/python/transpiler/test_unitary_synthesis_plugin.py
+++ b/test/python/transpiler/test_unitary_synthesis_plugin.py
@@ -30,7 +30,7 @@ from qiskit.transpiler.passes.synthesis.plugin import (
     UnitarySynthesisPluginManager,
     unitary_synthesis_plugin_names,
 )
-from qiskit.transpiler.passes.synthesis.unitary_synthesis import DefaultUnitarySynthesis
+from qiskit.transpiler.passes.synthesis.default_unitary_synth_plugin import DefaultUnitarySynthesis
 from test import QiskitTestCase  # pylint: disable=wrong-import-order
```

## Validation

```json
{
 "image_head": "581dd3d84c9517df0011f0a5a2305102527d6c79",
 "patch_applies": true,
 "test_files": [
  "test/python/transpiler/test_unitary_synthesis.py",
  "test/python/transpiler/test_unitary_synthesis_plugin.py"
 ],
 "collected_before": 1,
 "collected_after": 2,
 "outcomes_before": {
  "ERROR": 1
 },
 "outcomes_after": {
  "ERROR": 2
 },
 "exit_before": 2,
 "exit_after": 2,
 "tail_before": "ugin.py'.\nHint: make sure your test modules/packages have valid Python names.\nTraceback:\n/usr/local/lib/python3.11/importlib/__init__.py:126: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\ntest/python/transpiler/test_unitary_synthesis_plugin.py:33: in <module>\n    from qiskit.transpiler.passes.synthesis.default_unitary_synth_plugin import DefaultUnitarySynthesis\nE   ModuleNotFoundError: No module named 'qiskit.transpiler.passes.synthesis.default_unitary_synth_plugin'\n=============================== warnings summary ===============================\nqiskit/providers/fake_provider/fake_backend.py:22\nqiskit/providers/fake_provider/fake_backend.py:22\n  /testbed/qiskit/providers/fake_provider/fake_backend.py:22: DeprecationWarning: qiskit.providers.models is deprecated since Qiskit 1.2 and will be removed in Qiskit 2.0. With the removal of Qobj, there is no need for these schema-conformant objects. If you still need to use them, it could be because you are using a BackendV1, which is also deprecated in favor of BackendV2.\n    from qiskit.providers.models import BackendProperties\n\n-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html\n=========================== short test summary info ============================\nERROR test/python/transpiler/test_unitary_synthesis_plugin.py\n!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!\n========================= 2 warnings, 1 error in 2.78s =========================",
 "tail_after": "iler/__init__.py:27: in <module>\n    from .transpiler import transpile\nqiskit/compiler/transpiler.py:28: in <module>\n    from qiskit.transpiler import Layout, CouplingMap, PropertySet\nqiskit/transpiler/__init__.py:1544: in <module>\n    from .preset_passmanagers import generate_preset_pass_manager\nqiskit/transpiler/preset_passmanagers/__init__.py:62: in <module>\n    from .common import (\nqiskit/transpiler/preset_passmanagers/common.py:24: in <module>\n    from qiskit.transpiler.passes import Error\nqiskit/transpiler/passes/__init__.py:209: in <module>\n    from .basis import Decompose\nqiskit/transpiler/passes/basis/__init__.py:15: in <module>\n    from .decompose import Decompose\nqiskit/transpiler/passes/basis/decompose.py:29: in <module>\n    from ..synthesis import HighLevelSynthesis\nqiskit/transpiler/passes/synthesis/__init__.py:15: in <module>\n    from .unitary_synthesis import UnitarySynthesis\nqiskit/transpiler/passes/synthesis/unitary_synthesis.py:33: in <module>\n    from qiskit._accelerate.unitary_synthesis import run_main_loop\nE   ImportError: cannot import name 'run_main_loop' from 'unitary_synthesis' (unknown location)\n=========================== short test summary info ============================\nERROR test/python/transpiler/test_unitary_synthesis.py\nERROR test/python/transpiler/test_unitary_synthesis_plugin.py\n!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!\n============================== 2 errors in 1.24s ===============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

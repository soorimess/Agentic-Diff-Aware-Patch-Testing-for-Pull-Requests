# Qiskit__qiskit-12495

[back to the list](README.md) -- **Implement `num_qubits` and `num_clbits` in Rust**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#12495](https://github.com/Qiskit/qiskit/pull/12495) (created 2024-06-03, merged 2024-06-04) |
| ChaCo lists | full, ablation |
| status | **no-developer-test** -- no developer test (FAIL_TO_PASS cannot be derived); image at the base commit, patch applies and reverts |
| base commit | [`797bb285632a`](https://github.com/Qiskit/qiskit/commit/797bb285632a4b58c35c9e4cf5be44502b5bd78a) (2024-06-03), first parent of the merge commit |
| merge commit | [`72ff2cf20e10`](https://github.com/Qiskit/qiskit/commit/72ff2cf20e1047236c15f27f08c384c40f4a82f8) |
| issues closed | none |
| version | 1.2 |
| image | `f2p-chaco/qiskit__qiskit-12495:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-12495.Dockerfile) |
| source files (`patch`) | `crates/circuit/src/circuit_data.rs`, `qiskit/circuit/quantumcircuit.py` |
| test files (`test_patch`) | none |
| compiled files changed | crates/circuit/src/circuit_data.rs |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #12495: Implement `num_qubits` and `num_clbits` in Rust

* `QuantumCircuit.num_qubits` and `num_clbits` are twice as fast after this PR.
* These are used in several places. For example `QuantumCircuit.width()` is three times faster.
* `num_qubits` and `num_clbits` are introduced in circuit_data.rs. These functions are called by the corresponding Python methods. They are also used in circuit_data.rs itself.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/crates/circuit/src/circuit_data.rs b/crates/circuit/src/circuit_data.rs
index 944565cf36d89571e540d4f2ecec0c08e11d8f73..d8eca9ef8546f108f04ebced83cd69f9e5586703 100644
--- a/crates/circuit/src/circuit_data.rs
+++ b/crates/circuit/src/circuit_data.rs
@@ -220,6 +220,16 @@ impl CircuitData {
         self.qubits.clone_ref(py)
     }
 
+    /// Return the number of qubits. This is equivalent to the length of the list returned by
+    /// :meth:`.CircuitData.qubits`
+    ///
+    /// Returns:
+    ///     int: The number of qubits.
+    #[getter]
+    pub fn num_qubits(&self) -> usize {
+        self.qubits_native.len()
+    }
+
     /// Returns the current sequence of registered :class:`.Clbit`
     /// instances as a list.
     ///
@@ -235,6 +245,25 @@ impl CircuitData {
         self.clbits.clone_ref(py)
     }
 
+    /// Return the number of clbits. This is equivalent to the length of the list returned by
+    /// :meth:`.CircuitData.clbits`.
+    ///
+    /// Returns:
+    ///     int: The number of clbits.
+    #[getter]
+    pub fn num_clbits(&self) -> usize {
+        self.clbits_native.len()
+    }
+
+    /// Return the width of the circuit. This is the number of qubits plus the
+    /// number of clbits.
+    ///
+    /// Returns:
+    ///     int: The width of the circuit.
+    pub fn width(&self) -> usize {
+        self.num_qubits() + self.num_clbits()
+    }
+
     /// Registers a :class:`.Qubit` instance.
     ///
     /// Args:
@@ -246,13 +275,13 @@ impl CircuitData {
     ///         was provided.
     #[pyo3(signature = (bit, *, strict=true))]
     pub fn add_qubit(&mut self, py: Python, bit: &Bound<PyAny>, strict: bool) -> PyResult<()> {
-        if self.qubits_native.len() != self.qubits.bind(bit.py()).len() {
+        if self.num_qubits() != self.qubits.bind(bit.py()).len() {
             return Err(PyRuntimeError::new_err(concat!(
                 "This circuit's 'qubits' list has become out of sync with the circuit data.",
                 " Did something modify it?"
             )));
         }
-        let idx: BitType = self.qubits_native.len().try_into().map_err(|_| {
+        let idx: BitType = self.num_qubits().try_into().map_err(|_| {
             PyRuntimeError::new_err(
                 "The number of qubits in the circuit has exceeded the maximum capacity",
             )
@@ -284,13 +313,13 @@ impl CircuitData {
     ///         was provided.
     #[pyo3(signature = (bit, *, strict=true))]
     pub fn add_clbit(&mut self, py: Python, bit: &Bound<PyAny>, strict: bool) -> PyResult<()> {
-        if self.clbits_native.len() != self.clbits.bind(bit.py()).len() {
+        if self.num_clbits() != self.clbits.bind(bit.py()).len() {
             return Err(PyRuntimeError::new_err(concat!(
                 "This circuit's 'clbits' list has become out of sync with the circuit data.",
                 " Did something modify it?"
             )));
         }
-        let idx: BitType = self.clbits_native.len().try_into().map_err(|_| {
+        let idx: BitType = self.num_clbits().try_into().map_err(|_| {
             PyRuntimeError::new_err(
                 "The number of clbits in the circuit has exceeded the maximum capacity",
             )
@@ -460,11 +489,11 @@ impl CircuitData {
     ) -> PyResult<()> {
         let mut temp = CircuitData::new(py, qubits, clbits, None, 0)?;
         if qubits.is_some() {
-            if temp.qubits_native.len() < self.qubits_native.len() {
+            if temp.num_qubits() < self.num_qubits() {
                 return Err(PyValueError::new_err(format!(
                     "Replacement 'qubits' of size {:?} must contain at least {:?} bits.",
-                    temp.qubits_native.len(),
-                    self.qubits_native.len(),
+                    temp.num_qubits(),
+                    self.num_qubits(),
                 )));
             }
             std::mem::swap(&mut temp.qubits, &mut self.qubits);
@@ -475,11 +504,11 @@ impl CircuitData {
             );
         }
         if clbits.is_some() {
-            if temp.clbits_native.len() < self.clbits_native.len() {
+            if temp.num_clbits() < self.num_clbits() {
                 return Err(PyValueError::new_err(format!(
                     "Replacement 'clbits' of size {:?} must contain at least {:?} bits.",
-                    temp.clbits_native.len(),
-                    self.clbits_native.len(),
+                    temp.num_clbits(),
+                    self.num_clbits(),
                 )));
             }
             std::mem::swap(&mut temp.clbits, &mut self.clbits);
diff --git a/qiskit/circuit/quantumcircuit.py b/qiskit/circuit/quantumcircuit.py
index a157f04375a387ad76a39d46d95bf739eb1d376a..73c5101bb4692d6d21e4e0417bc29ee49e08de6b 100644
--- a/qiskit/circuit/quantumcircuit.py
+++ b/qiskit/circuit/quantumcircuit.py
@@ -1919,10 +1919,10 @@ class QuantumCircuit:
             edge_map.update(zip(other.qubits, dest.qubits))
         else:
             mapped_qubits = dest.qbit_argument_conversion(qubits)
-            if len(mapped_qubits) != len(other.qubits):
+            if len(mapped_qubits) != other.num_qubits:
                 raise CircuitError(
                     f"Number of items in qubits parameter ({len(mapped_qubits)}) does not"
-                    f" match number of qubits in the circuit ({len(other.qubits)})."
+                    f" match number of qubits in the circuit ({other.num_qubits})."
                 )
             if len(set(mapped_qubits)) != len(mapped_qubits):
                 raise CircuitError(
@@ -1935,10 +1935,10 @@ class QuantumCircuit:
             edge_map.update(zip(other.clbits, dest.clbits))
         else:
             mapped_clbits = dest.cbit_argument_conversion(clbits)
-            if len(mapped_clbits) != len(other.clbits):
+            if len(mapped_clbits) != other.num_clbits:
                 raise CircuitError(
                     f"Number of items in clbits parameter ({len(mapped_clbits)}) does not"
-                    f" match number of clbits in the circuit ({len(other.clbits)})."
+                    f" match number of clbits in the circuit ({other.num_clbits})."
                 )
             if len(set(mapped_clbits)) != len(mapped_clbits):
                 raise CircuitError(
@@ -2917,7 +2917,7 @@ class QuantumCircuit:
                     else:
                         self._data.add_qubit(bit)
                         self._qubit_indices[bit] = BitLocations(
-                            len(self._data.qubits) - 1, [(register, idx)]
+                            self._data.num_qubits - 1, [(register, idx)]
                         )
 
             elif isinstance(register, ClassicalRegister):
@@ -2929,7 +2929,7 @@ class QuantumCircuit:
                     else:
                         self._data.add_clbit(bit)
                         self._clbit_indices[bit] = BitLocations(
-                            len(self._data.clbits) - 1, [(register, idx)]
+                            self._data.num_clbits - 1, [(register, idx)]
                         )
 
             elif isinstance(register, list):
@@ -2950,10 +2950,10 @@ class QuantumCircuit:
                 self._ancillas.append(bit)
             if isinstance(bit, Qubit):
                 self._data.add_qubit(bit)
-                self._qubit_indices[bit] = BitLocations(len(self._data.qubits) - 1, [])
+                self._qubit_indices[bit] = BitLocations(self._data.num_qubits - 1, [])
             elif isinstance(bit, Clbit):
                 self._data.add_clbit(bit)
-                self._clbit_indices[bit] = BitLocations(len(self._data.clbits) - 1, [])
+                self._clbit_indices[bit] = BitLocations(self._data.num_clbits - 1, [])
             else:
                 raise CircuitError(
                     "Expected an instance of Qubit, Clbit, or "
@@ -3393,12 +3393,12 @@ class QuantumCircuit:
             int: Width of circuit.
 
         """
-        return len(self.qubits) + len(self.clbits)
+        return self._data.width()
 
     @property
     def num_qubits(self) -> int:
         """Return number of qubits."""
-        return len(self.qubits)
+        return self._data.num_qubits
 
     @property
     def num_ancillas(self) -> int:
@@ -3408,7 +3408,7 @@ class QuantumCircuit:
     @property
     def num_clbits(self) -> int:
         """Return number of classical bits."""
-        return len(self.clbits)
+        return self._data.num_clbits
 
     # The stringified return type is because OrderedDict can't be subscripted before Python 3.9, and
     # typing.OrderedDict wasn't added until 3.7.2.  It can be turned into a proper type once 3.6
@@ -3879,18 +3879,18 @@ class QuantumCircuit:
         else:
             circ = self.copy()
         if add_bits:
-            new_creg = circ._create_creg(len(circ.qubits), "meas")
+            new_creg = circ._create_creg(circ.num_qubits, "meas")
             circ.add_register(new_creg)
             circ.barrier()
             circ.measure(circ.qubits, new_creg)
         else:
-            if len(circ.clbits) < len(circ.qubits):
+            if circ.num_clbits < circ.num_qubits:
                 raise CircuitError(
                     "The number of classical bits must be equal or greater than "
                     "the number of qubits."
                 )
             circ.barrier()
-            circ.measure(circ.qubits, circ.clbits[0 : len(circ.qubits)])
+            circ.measure(circ.qubits, circ.clbits[0 : circ.num_qubits])
 
         if not inplace:
             return circ
```

## `test_patch` -- the developer's tests (held out)

```diff

```

## Validation

```json
{
 "image_head": "797bb285632a4b58c35c9e4cf5be44502b5bd78a",
 "patch_applies": true
}
```

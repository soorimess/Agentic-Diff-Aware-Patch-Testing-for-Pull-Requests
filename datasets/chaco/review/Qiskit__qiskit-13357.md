# Qiskit__qiskit-13357

[back to the list](README.md) -- **Add run_options option and support for processing level 1 data to BackendSamplerV2**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#13357](https://github.com/Qiskit/qiskit/pull/13357) (created 2024-10-22, merged 2024-11-05) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 1 developer test(s) flip; oracle reproduces it |
| base commit | [`db0433920c86`](https://github.com/Qiskit/qiskit/commit/db0433920c86e55f4ec06b3837d10d94b040e117) (2024-11-04), first parent of the merge commit |
| merge commit | [`2efb59ce4cd3`](https://github.com/Qiskit/qiskit/commit/2efb59ce4cd3c2d8721390648cdca6d2fd41f792) |
| issues closed | none |
| version | 1.3 |
| image | `f2p-chaco/qiskit__qiskit-13357:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-13357.Dockerfile) |
| source files (`patch`) | `qiskit/primitives/backend_estimator.py`, `qiskit/primitives/backend_sampler_v2.py`, `releasenotes/notes/backend-sampler-v2-level1-dc13af460cd38454.yaml` |
| test files (`test_patch`) | `test/python/primitives/test_backend_sampler_v2.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (1)

- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_level1`

## PASS_TO_PASS (81)

<details><summary>show</summary>

- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_aliased_cregs_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_aliased_cregs_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_aliased_cregs_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_aliased_cregs_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_multiple_cregs_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_multiple_cregs_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_multiple_cregs_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_multiple_cregs_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_unitary_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_unitary_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_unitary_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_circuit_with_unitary_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_diff_shots_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_diff_shots_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_diff_shots_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_diff_shots_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_empty_creg_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_empty_creg_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_empty_creg_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_empty_creg_4`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_iter_pub`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_job_size_limit_backend_v1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_job_size_limit_backend_v2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_metadata`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_no_cregs_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_no_cregs_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_no_cregs_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_no_cregs_4`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_primitive_job_status_done_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_primitive_job_status_done_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_primitive_job_status_done_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_primitive_job_status_done_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_1qubit_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_1qubit_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_1qubit_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_1qubit_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_2qubit_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_2qubit_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_2qubit_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_2qubit_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_empty_parameter_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_empty_parameter_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_empty_parameter_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_empty_parameter_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_errors_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_errors_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_errors_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_errors_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_numpy_params_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_numpy_params_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_numpy_params_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_numpy_params_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_reverse_meas_order_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_reverse_meas_order_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_reverse_meas_order_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_reverse_meas_order_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_shots_result_size_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_shots_result_size_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_shots_result_size_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_shots_result_size_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_single_circuit_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_single_circuit_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_single_circuit_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_single_circuit_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_with_shots_option_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_with_shots_option_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_with_shots_option_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_with_shots_option_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_2`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_3`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_v1_1`
- `test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_with_parameterized_circuits_v1_1`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #13357: Add run_options option and support for processing level 1 data to BackendSamplerV2

This change adds support to the `BackendSamplerV2` class so that it will accept a `run_options` dict option and pass its content through to the underlying `BackendV2`'s `run()` method.

Additionally, to support `meas_level=1`, the results processing code checks for a `meas_level` option inside of `run_options` and handles `meas_level=1` data appropriately when it is set, rather than always assuming the returned data is level 2.

Finally, the behavior of `BackendSamplerV2` was changed so that it does clear the `QuantumCircuit.metadata` of its input circuits before passing them on to `backend.run` like it did previously.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/primitives/backend_estimator.py b/qiskit/primitives/backend_estimator.py
index 722ee900ceeaeab1c767193db4eed4585d3fd6ed..5f9f8d20c75e39b9ce311d52a45cafd56936ff50 100644
--- a/qiskit/primitives/backend_estimator.py
+++ b/qiskit/primitives/backend_estimator.py
@@ -44,13 +44,15 @@ from .utils import _circuit_key, _observable_key, init_observable
 def _run_circuits(
     circuits: QuantumCircuit | list[QuantumCircuit],
     backend: BackendV1 | BackendV2,
+    clear_metadata: bool = True,
     **run_options,
 ) -> tuple[list[Result], list[dict]]:
     """Remove metadata of circuits and run the circuits on a backend.
     Args:
         circuits: The circuits
         backend: The backend
-        monitor: Enable job minotor if True
+        clear_metadata: Clear circuit metadata before passing to backend.run if
+            True.
         **run_options: run_options
     Returns:
         The result and the metadata of the circuits
@@ -60,7 +62,8 @@ def _run_circuits(
     metadata = []
     for circ in circuits:
         metadata.append(circ.metadata)
-        circ.metadata = {}
+        if clear_metadata:
+            circ.metadata = {}
     if isinstance(backend, BackendV1):
         max_circuits = getattr(backend.configuration(), "max_experiments", None)
     elif isinstance(backend, BackendV2):
diff --git a/qiskit/primitives/backend_sampler_v2.py b/qiskit/primitives/backend_sampler_v2.py
index bac0bec5eaedada508219bf4ec1345dd013a0c9d..40a6d8560e07b04ae93ce0387f39955371ab808f 100644
--- a/qiskit/primitives/backend_sampler_v2.py
+++ b/qiskit/primitives/backend_sampler_v2.py
@@ -17,12 +17,13 @@ from __future__ import annotations
 import warnings
 from collections import defaultdict
 from dataclasses import dataclass
-from typing import Iterable
+from typing import Any, Iterable, Union
 
 import numpy as np
 from numpy.typing import NDArray
 
 from qiskit.circuit import QuantumCircuit
+from qiskit.exceptions import QiskitError
 from qiskit.primitives.backend_estimator import _run_circuits
 from qiskit.primitives.base import BaseSamplerV2
 from qiskit.primitives.containers import (
@@ -53,6 +54,11 @@ class Options:
     Default: None.
     """
 
+    run_options: dict[str, Any] | None = None
+    """A dictionary of options to pass to the backend's ``run()`` method.
+    Default: None (no option passed to backend's ``run`` method)
+    """
+
 
 @dataclass
 class _MeasureInfo:
@@ -62,6 +68,16 @@ class _MeasureInfo:
     start: int
 
 
+ResultMemory = Union[list[str], list[list[float]], list[list[list[float]]]]
+"""Type alias for possible level 2 and level 1 result memory formats. For level
+2, the format is a list of bit strings. For level 1, format can be either a
+list of I/Q pairs (list with two floats) for each memory slot if using
+``meas_return=avg`` or a list of of lists of I/Q pairs if using
+``meas_return=single`` with the outer list indexing shot number and the inner
+list indexing memory slot.
+"""
+
+
 class BackendSamplerV2(BaseSamplerV2):
     """Evaluates bitstrings for provided quantum circuits
 
@@ -91,6 +107,9 @@ class BackendSamplerV2(BaseSamplerV2):
     * ``seed_simulator``: The seed to use in the simulator. If None, a random seed will be used.
       Default: None.
 
+    * ``run_options``: A dictionary of options to pass through to the ``run()``
+      method of the wrapped :class:`~.BackendV2` instance.
+
     .. note::
 
         This class requires a backend that supports ``memory`` option.
@@ -165,19 +184,27 @@ class BackendSamplerV2(BaseSamplerV2):
         for circuits in bound_circuits:
             flatten_circuits.extend(np.ravel(circuits).tolist())
 
+        run_opts = self._options.run_options or {}
         # run circuits
         results, _ = _run_circuits(
             flatten_circuits,
             self._backend,
+            clear_metadata=False,
             memory=True,
             shots=shots,
             seed_simulator=self._options.seed_simulator,
+            **run_opts,
         )
         result_memory = _prepare_memory(results)
 
         # pack memory to an ndarray of uint8
         results = []
         start = 0
+        meas_level = (
+            None
+            if self._options.run_options is None
+            else self._options.run_options.get("meas_level")
+        )
         for pub, bound in zip(pubs, bound_circuits):
             meas_info, max_num_bytes = _analyze_circuit(pub.circuit)
             end = start + bound.size
@@ -189,6 +216,7 @@ class BackendSamplerV2(BaseSamplerV2):
                     meas_info,
                     max_num_bytes,
                     pub.circuit.metadata,
+                    meas_level,
                 )
             )
             start = end
@@ -197,28 +225,43 @@ class BackendSamplerV2(BaseSamplerV2):
 
     def _postprocess_pub(
         self,
-        result_memory: list[list[str]],
+        result_memory: list[ResultMemory],
         shots: int,
         shape: tuple[int, ...],
         meas_info: list[_MeasureInfo],
         max_num_bytes: int,
         circuit_metadata: dict,
+        meas_level: int | None,
     ) -> SamplerPubResult:
-        """Converts the memory data into an array of bit arrays with the shape of the pub."""
-        arrays = {
-            item.creg_name: np.zeros(shape + (shots, item.num_bytes), dtype=np.uint8)
-            for item in meas_info
-        }
-        memory_array = _memory_array(result_memory, max_num_bytes)
-
-        for samples, index in zip(memory_array, np.ndindex(*shape)):
-            for item in meas_info:
-                ary = _samples_to_packed_array(samples, item.num_bits, item.start)
-                arrays[item.creg_name][index] = ary
-
-        meas = {
-            item.creg_name: BitArray(arrays[item.creg_name], item.num_bits) for item in meas_info
-        }
+        """Converts the memory data into a sampler pub result
+
+        For level 2 data, the memory data are stored in an array of bit arrays
+        with the shape of the pub. For level 1 data, the data are stored in a
+        complex numpy array.
+        """
+        if meas_level == 2 or meas_level is None:
+            arrays = {
+                item.creg_name: np.zeros(shape + (shots, item.num_bytes), dtype=np.uint8)
+                for item in meas_info
+            }
+            memory_array = _memory_array(result_memory, max_num_bytes)
+
+            for samples, index in zip(memory_array, np.ndindex(*shape)):
+                for item in meas_info:
+                    ary = _samples_to_packed_array(samples, item.num_bits, item.start)
+                    arrays[item.creg_name][index] = ary
+
+            meas = {
+                item.creg_name: BitArray(arrays[item.creg_name], item.num_bits)
+                for item in meas_info
+            }
+        elif meas_level == 1:
+            raw = np.array(result_memory)
+            cplx = raw[..., 0] + 1j * raw[..., 1]
+            cplx = np.reshape(cplx, (*shape, *cplx.shape[1:]))
+            meas = {item.creg_name: cplx for item in meas_info}
+        else:
+            raise QiskitError(f"Unsupported meas_level: {meas_level}")
         return SamplerPubResult(
             DataBin(**meas, shape=shape),
             metadata={"shots": shots, "circuit_metadata": circuit_metadata},
@@ -248,7 +291,7 @@ def _analyze_circuit(circuit: QuantumCircuit) -> tuple[list[_MeasureInfo], int]:
     return meas_info, _min_num_bytes(max_num_bits)
 
 
-def _prepare_memory(results: list[Result]) -> list[list[str]]:
+def _prepare_memory(results: list[Result]) -> list[ResultMemory]:
     """Joins splitted results if exceeding max_experiments"""
     lst = []
     for res in results:
diff --git a/releasenotes/notes/backend-sampler-v2-level1-dc13af460cd38454.yaml b/releasenotes/notes/backend-sampler-v2-level1-dc13af460cd38454.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..594e610939cf387142829f94ce477508d7529022
--- /dev/null
+++ b/releasenotes/notes/backend-sampler-v2-level1-dc13af460cd38454.yaml
@@ -0,0 +1,17 @@
+---
+features:
+  - |
+    Support for level 1 data was added to :class:`~.BackendSamplerV2` as was
+    support for passing options through to the ``run()`` method of the wrapped
+    :class:`~.BackendV2`. The run options can be specified using a
+    ``"run_options"`` entry inside of the ``options`` dicitonary passed to
+    :class:`~.BackendSamplerV2`. The ``"run_options"`` entry should be a
+    dictionary mapping argument names to values for passing to the backend's
+    ``run()`` method. When a ``"meas_level"`` option with a value of 1 is set
+    in the run options, the results from the backend will be treated as level 1
+    results rather as bit arrays (the level 2 format).
+upgrade:
+  - |
+    When using :class:`~.BackendSamplerV2`, circuit metadata is no longer
+    cleared before passing circuits to the ``run()`` method of the wrapped
+    :class:`~.BackendV2` instance.
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/test/python/primitives/test_backend_sampler_v2.py b/test/python/primitives/test_backend_sampler_v2.py
index b5077cec50168aea8b05d5f20dee29460eef4860..77830d5c922428c0387ab545f4c843f54bd17089 100644
--- a/test/python/primitives/test_backend_sampler_v2.py
+++ b/test/python/primitives/test_backend_sampler_v2.py
@@ -31,8 +31,10 @@ from qiskit.primitives.containers.data_bin import DataBin
 from qiskit.primitives.containers.sampler_pub import SamplerPub
 from qiskit.providers import JobStatus
 from qiskit.providers.backend_compat import BackendV2Converter
-from qiskit.providers.basic_provider import BasicSimulator
+from qiskit.providers.basic_provider import BasicProviderJob, BasicSimulator
 from qiskit.providers.fake_provider import Fake7QPulseV1, GenericBackendV2
+from qiskit.result import Result
+from qiskit.qobj.utils import MeasReturnType, MeasLevel
 from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
 from ..legacy_cmaps import LAGOS_CMAP
 
@@ -50,6 +52,64 @@ BACKENDS_V2 = [
 BACKENDS = BACKENDS_V1 + BACKENDS_V2
 
 
+class Level1BackendV2(GenericBackendV2):
+    """Wrapper around GenericBackendV2 adding level 1 data support for testing
+
+    GenericBackendV2 is used to run the simulation. Then level 1 data (a
+    complex number per classical register per shot) is generated by mapping 0
+    to -1 and 1 to 1 with a random number added to each shot drawn from a
+    normal distribution with a standard deviation of ``level1_sigma``. Each
+    data point has ``1j * idx`` added to it where ``idx`` is the index of the
+    classical register. For ``meas_return="avg"``, the individual shot results
+    are still calculated and then averaged.
+    """
+
+    level1_sigma = 0.1
+
+    def run(self, run_input, **options):
+        # Validate level 1 options
+        if "meas_level" not in options or "meas_return" not in options:
+            raise ValueError(f"{type(self)} requires 'meas_level' and 'meas_return' run options!")
+        meas_level = options.pop("meas_level")
+        if meas_level != 1:
+            raise ValueError(f"'meas_level' must be 1, not {meas_level}")
+        meas_return = options.pop("meas_return")
+        if meas_return not in ("single", "avg"):
+            raise ValueError(f"Unexpected value for 'meas_return': {meas_return}")
+
+        options["memory"] = True
+
+        rng = np.random.default_rng(seed=options.get("seed_simulator"))
+
+        inner_job = super().run(run_input, **options)
+        result_dict = inner_job.result().to_dict()
+        for circ, exp_result in zip(run_input, result_dict["results"]):
+            num_clbits = sum(cr.size for cr in circ.cregs)
+            bitstrings = [
+                format(int(x, 16), f"0{num_clbits}b") for x in exp_result["data"]["memory"]
+            ]
+            new_data = [
+                [
+                    [2 * int(d) - 1 + rng.normal(scale=self.level1_sigma), i]
+                    for i, d in enumerate(reversed(bs))
+                ]
+                for bs in bitstrings
+            ]
+            if meas_return == "avg":
+                new_data = [
+                    [sum(shot[idx][0] for shot in new_data) / len(new_data), idx]
+                    for idx in range(num_clbits)
+                ]
+                exp_result["meas_return"] = MeasReturnType.AVERAGE
+            else:
+                exp_result["meas_return"] = MeasReturnType.SINGLE
+            exp_result["data"] = {"memory": new_data}
+            exp_result["meas_level"] = MeasLevel.KERNELED
+
+        result = Result.from_dict(result_dict)
+        return BasicProviderJob(self, inner_job.job_id(), result)
+
+
 @ddt
 class TestBackendSamplerV2(QiskitTestCase):
     """Test for BackendSamplerV2"""
@@ -942,6 +1002,55 @@ class TestBackendSamplerV2(QiskitTestCase):
         self.assertLessEqual(result[0].data.meas.num_shots, self._shots)
         self.assertEqual(sum(result[0].data.meas.get_counts().values()), self._shots)
 
+    def test_run_level1(self):
+        """Test running with meas_level=1"""
+        nq = 2
+        shots = 100
+
+        backend = Level1BackendV2(nq)
+        qc = QuantumCircuit(nq)
+        qc.x(1)
+        qc.measure_all()
+        pm = generate_preset_pass_manager(optimization_level=0, backend=backend)
+        qc = pm.run(qc)
+        options = {
+            "default_shots": shots,
+            "seed_simulator": self._seed,
+            "run_options": {
+                "meas_level": 1,
+                "meas_return": "single",
+            },
+        }
+        sampler = BackendSamplerV2(backend=backend, options=options)
+        result_single = sampler.run([qc]).result()
+
+        options = {
+            "default_shots": shots,
+            "seed_simulator": self._seed,
+            "run_options": {
+                "meas_level": 1,
+                "meas_return": "avg",
+            },
+        }
+        sampler = BackendSamplerV2(backend=backend, options=options)
+        result_avg = sampler.run([qc]).result()
+
+        # Check that averaging the meas_return="single" data matches the
+        # meas_return="avg" data.
+        averaged_singles = np.average(result_single[0].join_data(), axis=0)
+        average_data = result_avg[0].join_data()
+        self.assertLessEqual(
+            max(abs(averaged_singles - average_data)),
+            backend.level1_sigma / np.sqrt(shots) * 6,
+        )
+
+        # Check that average data matches expected form for the circuit
+        expected_average = np.array([-1, 1 + 1j])
+        self.assertLessEqual(
+            max(abs(expected_average - average_data)),
+            backend.level1_sigma / np.sqrt(shots) * 6,
+        )
+
     @combine(backend=BACKENDS_V2)
     def test_primitive_job_status_done(self, backend):
         """test primitive job's status"""
```

## Validation

```json
{
 "test_files": [
  "test/python/primitives/test_backend_sampler_v2.py"
 ],
 "collected_before": 82,
 "collected_after": 82,
 "outcomes_before": {
  "PASSED": 81,
  "FAILED": 1
 },
 "outcomes_after": {
  "PASSED": 82
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "hon/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_2\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_3\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_v1_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_2\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_3\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_2\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_3\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_v1_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_v1_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_with_parameterized_circuits_v1_1\nFAILED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_run_level1\n================= 1 failed, 81 passed, 583 warnings in 58.54s ==================",
 "tail_after": "backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_2\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_3\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sample_run_multiple_circuits_v1_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_2\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_3\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_2\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_3\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_multiple_times_v1_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_v1_1\nPASSED test/python/primitives/test_backend_sampler_v2.py::TestBackendSamplerV2::test_sampler_run_with_parameterized_circuits_v1_1\n====================== 82 passed, 585 warnings in 51.25s =======================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

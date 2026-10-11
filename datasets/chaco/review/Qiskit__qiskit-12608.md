# Qiskit__qiskit-12608

[back to the list](README.md) -- **Fix v2 pulse drawer **

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#12608](https://github.com/Qiskit/qiskit/pull/12608) (created 2024-06-20, merged 2024-06-20) |
| ChaCo lists | full, ablation |
| status | **no-developer-test** -- no developer test (FAIL_TO_PASS cannot be derived); image at the base commit, patch applies and reverts |
| base commit | [`591260f0694f`](https://github.com/Qiskit/qiskit/commit/591260f0694fb1944507283ce10cf8f068bd3935) (2024-06-20), first parent of the merge commit |
| merge commit | [`7d1731b60d8d`](https://github.com/Qiskit/qiskit/commit/7d1731b60d8dd6219a292dc62f24d1a8d780e43a) |
| issues closed | none |
| version | 1.2 |
| image | `f2p-chaco/qiskit__qiskit-12608:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-12608.Dockerfile) |
| source files (`patch`) | `qiskit/visualization/pulse_v2/device_info.py`, `releasenotes/notes/fix-v2-pulse-drawer-d05e4e392766909f.yaml` |
| test files (`test_patch`) | none |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (0)

<details><summary>show</summary>

(none)

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #12608: Fix v2 pulse drawer

### Summary

v2 pulse drawer crashes when the draw function is called with a V2 backend that doesn't have configuration and defaults attributes. Since qiskit-ibm-runtime 0.24 was released and fake V1 backends were deprecated, we should to support visualization with fake V2 backends that doen't have configuration and defaults attributes.

### Details and comments
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/visualization/pulse_v2/device_info.py b/qiskit/visualization/pulse_v2/device_info.py
index 1e809c43abd2d80527d5bb0acff9f15e189aa529..7898f978772ca3b637184c01691d80652c8c88db 100644
--- a/qiskit/visualization/pulse_v2/device_info.py
+++ b/qiskit/visualization/pulse_v2/device_info.py
@@ -40,7 +40,7 @@ from typing import Dict, List, Union, Optional
 
 from qiskit import pulse
 from qiskit.providers import BackendConfigurationError
-from qiskit.providers.backend import Backend
+from qiskit.providers.backend import Backend, BackendV2
 
 
 class DrawerBackendInfo(ABC):
@@ -106,40 +106,67 @@ class OpenPulseBackendInfo(DrawerBackendInfo):
         Returns:
             OpenPulseBackendInfo: New configured instance.
         """
-        configuration = backend.configuration()
-        defaults = backend.defaults()
-
-        # load name
-        name = backend.name()
-
-        # load cycle time
-        dt = configuration.dt
-
-        # load frequencies
         chan_freqs = {}
-
-        chan_freqs.update(
-            {pulse.DriveChannel(qind): freq for qind, freq in enumerate(defaults.qubit_freq_est)}
-        )
-        chan_freqs.update(
-            {pulse.MeasureChannel(qind): freq for qind, freq in enumerate(defaults.meas_freq_est)}
-        )
-        for qind, u_lo_mappers in enumerate(configuration.u_channel_lo):
-            temp_val = 0.0 + 0.0j
-            for u_lo_mapper in u_lo_mappers:
-                temp_val += defaults.qubit_freq_est[u_lo_mapper.q] * u_lo_mapper.scale
-            chan_freqs[pulse.ControlChannel(qind)] = temp_val.real
-
-        # load qubit channel mapping
         qubit_channel_map = defaultdict(list)
-        for qind in range(configuration.n_qubits):
-            qubit_channel_map[qind].append(configuration.drive(qubit=qind))
-            qubit_channel_map[qind].append(configuration.measure(qubit=qind))
-            for tind in range(configuration.n_qubits):
+
+        if hasattr(backend, "configuration") and hasattr(backend, "defaults"):
+            configuration = backend.configuration()
+            defaults = backend.defaults()
+
+            name = configuration.backend_name
+            dt = configuration.dt
+
+            # load frequencies
+            chan_freqs.update(
+                {
+                    pulse.DriveChannel(qind): freq
+                    for qind, freq in enumerate(defaults.qubit_freq_est)
+                }
+            )
+            chan_freqs.update(
+                {
+                    pulse.MeasureChannel(qind): freq
+                    for qind, freq in enumerate(defaults.meas_freq_est)
+                }
+            )
+            for qind, u_lo_mappers in enumerate(configuration.u_channel_lo):
+                temp_val = 0.0 + 0.0j
+                for u_lo_mapper in u_lo_mappers:
+                    temp_val += defaults.qubit_freq_est[u_lo_mapper.q] * u_lo_mapper.scale
+                chan_freqs[pulse.ControlChannel(qind)] = temp_val.real
+
+            # load qubit channel mapping
+            for qind in range(configuration.n_qubits):
+                qubit_channel_map[qind].append(configuration.drive(qubit=qind))
+                qubit_channel_map[qind].append(configuration.measure(qubit=qind))
+                for tind in range(configuration.n_qubits):
+                    try:
+                        qubit_channel_map[qind].extend(configuration.control(qubits=(qind, tind)))
+                    except BackendConfigurationError:
+                        pass
+        elif isinstance(backend, BackendV2):
+            # Pure V2 model doesn't contain channel frequency information.
+            name = backend.name
+            dt = backend.dt
+
+            # load qubit channel mapping
+            for qind in range(backend.num_qubits):
+                # channels are NotImplemented by default so we must catch arbitrary error.
+                try:
+                    qubit_channel_map[qind].append(backend.drive_channel(qind))
+                except Exception:  # pylint: disable=broad-except
+                    pass
                 try:
-                    qubit_channel_map[qind].extend(configuration.control(qubits=(qind, tind)))
-                except BackendConfigurationError:
+                    qubit_channel_map[qind].append(backend.measure_channel(qind))
+                except Exception:  # pylint: disable=broad-except
                     pass
+                for tind in range(backend.num_qubits):
+                    try:
+                        qubit_channel_map[qind].extend(backend.control_channel(qubits=(qind, tind)))
+                    except Exception:  # pylint: disable=broad-except
+                        pass
+        else:
+            raise RuntimeError("Backend object not yet supported")
 
         return OpenPulseBackendInfo(
             name=name, dt=dt, channel_frequency_map=chan_freqs, qubit_channel_map=qubit_channel_map
diff --git a/releasenotes/notes/fix-v2-pulse-drawer-d05e4e392766909f.yaml b/releasenotes/notes/fix-v2-pulse-drawer-d05e4e392766909f.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..b158703c6b89fca120c0456741b11dc7521d9437
--- /dev/null
+++ b/releasenotes/notes/fix-v2-pulse-drawer-d05e4e392766909f.yaml
@@ -0,0 +1,7 @@
+---
+fixes:
+  - |
+    Fixed a bug in :func:`qiskit.visualization.pulse_v2.interface.draw` that didn't 
+    draw pulse schedules when the draw function was called with a :class:`.BackendV2` argument.
+    Because the V2 backend doesn't report hardware channel frequencies,
+    the generated drawing will show 'no freq.' below each channel label.
```

## `test_patch` -- the developer's tests (held out)

```diff

```

## Validation

```json
{
 "image_head": "591260f0694fb1944507283ce10cf8f068bd3935",
 "patch_applies": true
}
```

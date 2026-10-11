# Qiskit__qiskit-14353

[back to the list](README.md) -- **Do not construct layout passes with no coupling map**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#14353](https://github.com/Qiskit/qiskit/pull/14353) (created 2025-05-13, merged 2025-05-18) |
| ChaCo lists | full, ablation |
| status | **no-developer-test** -- no developer test (FAIL_TO_PASS cannot be derived); image at the base commit, patch applies and reverts |
| base commit | [`d4df68bceee9`](https://github.com/Qiskit/qiskit/commit/d4df68bceee9a96f73e928076f466c7ea858fdee) (2025-05-16), first parent of the merge commit |
| merge commit | [`a18e15163d8a`](https://github.com/Qiskit/qiskit/commit/a18e15163d8a93c0e072d4d3c50151a2cd9f036a) |
| issues closed | none |
| version | 2.1 |
| image | `f2p-chaco/qiskit__qiskit-14353:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-14353.Dockerfile) |
| source files (`patch`) | `qiskit/transpiler/preset_passmanagers/builtin_plugins.py`, `releasenotes/notes/no-layout-presets-87e0bcde698f002e.yaml` |
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
Pull request #14353: Do not construct layout passes with no coupling map

### Summary

The builtin plugins fairly frequently construct instances of the layout passes with `coupling_map=None` (or similar), even when this is against the documentation of the passes.  A couple of passes, but not all, have defensive code in their `run` methods to raise a better error in this case, but even so, there is an assumption that passes will not be _run_ with `coupling_map=None`.

The preset pass managers do follow this assumption; conditional code prevents those passes from ever being called.  However, we know that there's no coupling map ahead of time, so we can simply not even construct the layout passes, let alone add them to the `PassManager`.




### Details and comments

Input normalisation typically wants to be done in pass initialisation, not deferred to runtime (though expensive properties can still be computed only on first run and cached).  The current strategy of silently ignoring invalid inputs until runtime makes it harder to do this; it's clearer to have the pass-manager construction logic never produce objects in invalid states in the first place.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/transpiler/preset_passmanagers/builtin_plugins.py b/qiskit/transpiler/preset_passmanagers/builtin_plugins.py
index f13d89b63cc0310ed659cec9866af8ab04942f9e..8543ffd9708616ad46c8ed3fbf143ada44b74db0 100644
--- a/qiskit/transpiler/preset_passmanagers/builtin_plugins.py
+++ b/qiskit/transpiler/preset_passmanagers/builtin_plugins.py
@@ -736,13 +736,18 @@ class DefaultLayoutPassManager(PassManagerStagePlugin):
         layout = PassManager()
         layout.append(_given_layout)
         if optimization_level == 0:
-            layout.append(
-                ConditionalController(
-                    TrivialLayout(coupling_map), condition=_choose_layout_condition
+            if coupling_map is not None:
+                layout.append(
+                    ConditionalController(
+                        TrivialLayout(coupling_map), condition=_choose_layout_condition
+                    )
                 )
-            )
             layout += common.generate_embed_passmanager(coupling_map)
             return layout
+
+        if coupling_map is None:
+            # There's nothing to lay out onto.  We only need to embed the initial layout, if given.
+            pass
         elif optimization_level == 1:
             layout.append(
                 ConditionalController(
@@ -870,9 +875,12 @@ class TrivialLayoutPassManager(PassManagerStagePlugin):
 
         layout = PassManager()
         layout.append(_given_layout)
-        layout.append(
-            ConditionalController(TrivialLayout(coupling_map), condition=_choose_layout_condition)
-        )
+        if coupling_map is not None:
+            layout.append(
+                ConditionalController(
+                    TrivialLayout(coupling_map), condition=_choose_layout_condition
+                )
+            )
         layout += common.generate_embed_passmanager(coupling_map)
         return layout
 
@@ -893,15 +901,16 @@ class DenseLayoutPassManager(PassManagerStagePlugin):
 
         layout = PassManager()
         layout.append(_given_layout)
-        layout.append(
-            ConditionalController(
-                DenseLayout(
-                    coupling_map=pass_manager_config.coupling_map,
-                    target=pass_manager_config.target,
-                ),
-                condition=_choose_layout_condition,
+        if coupling_map is not None:
+            layout.append(
+                ConditionalController(
+                    DenseLayout(
+                        coupling_map=pass_manager_config.coupling_map,
+                        target=pass_manager_config.target,
+                    ),
+                    condition=_choose_layout_condition,
+                )
             )
-        )
         layout += common.generate_embed_passmanager(coupling_map)
         return layout
 
@@ -925,7 +934,9 @@ class SabreLayoutPassManager(PassManagerStagePlugin):
 
         layout = PassManager()
         layout.append(_given_layout)
-        if optimization_level == 0:
+        if coupling_map is None:
+            layout_pass = None
+        elif optimization_level == 0:
             trial_count = _get_trial_count(5)
 
             layout_pass = SabreLayout(
@@ -971,17 +982,18 @@ class SabreLayoutPassManager(PassManagerStagePlugin):
             )
         else:
             raise TranspilerError(f"Invalid optimization level: {optimization_level}")
-        layout.append(
-            ConditionalController(
-                [
-                    BarrierBeforeFinalMeasurements(
-                        "qiskit.transpiler.internal.routing.protection.barrier"
-                    ),
-                    layout_pass,
-                ],
-                condition=_choose_layout_condition,
+        if layout_pass is not None:
+            layout.append(
+                ConditionalController(
+                    [
+                        BarrierBeforeFinalMeasurements(
+                            "qiskit.transpiler.internal.routing.protection.barrier"
+                        ),
+                        layout_pass,
+                    ],
+                    condition=_choose_layout_condition,
+                )
             )
-        )
         embed = common.generate_embed_passmanager(coupling_map)
         layout.append(ConditionalController(embed.to_flow_controller(), condition=_swap_mapped))
         return layout
diff --git a/releasenotes/notes/no-layout-presets-87e0bcde698f002e.yaml b/releasenotes/notes/no-layout-presets-87e0bcde698f002e.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..becc15f5bafc0ce1413a4f81ac61078c38fcbd32
--- /dev/null
+++ b/releasenotes/notes/no-layout-presets-87e0bcde698f002e.yaml
@@ -0,0 +1,12 @@
+---
+upgrade_transpiler:
+  - |
+    :ref:`The built-in layout plugins <transpiler-preset-stage-layout>` for the present pass
+    managers will no longer contain their principal component (e.g. a :class:`.SabreLayout` instance
+    for :ref:`the "sabre" stage <transpiler-preset-stage-layout-sabre>`) if no coupling constraints
+    are provided.  Previously, the plugins would construct invalid instances of their layout passes,
+    under an assumption that separate logic would prevent the passes from executing and raising
+    exceptions.
+
+    This should have no meaningful effect on the use of the preset pass managers or the plugins,
+    since it was already never valid to call the passes in an invalid state .
```

## `test_patch` -- the developer's tests (held out)

```diff

```

## Validation

```json
{
 "image_head": "d4df68bceee9a96f73e928076f466c7ea858fdee",
 "patch_applies": true
}
```

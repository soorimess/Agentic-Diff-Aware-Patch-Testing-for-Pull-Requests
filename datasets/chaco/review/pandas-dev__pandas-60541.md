# pandas-dev__pandas-60541

[back to the list](README.md) -- **FIX: ruff checks in expressions/pytables**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#60541](https://github.com/pandas-dev/pandas/pull/60541) (created 2024-12-11, merged 2024-12-11) |
| ChaCo lists | full, ablation |
| status | **no-developer-test** -- the PR adds or changes no test: FAIL_TO_PASS cannot be derived |
| base commit | [`ca91dd4c39a0`](https://github.com/pandas-dev/pandas/commit/ca91dd4c39a02c0026b98c16c56996f81506e004) (2024-12-09), first parent of the merge commit |
| merge commit | [`719fc0fcbcda`](https://github.com/pandas-dev/pandas/commit/719fc0fcbcda23a79156ccfc990228df0851452f) |
| issues closed | none |
| version | (set by validate) |
| image | `f2p-chaco/pandas-dev__pandas-60541:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-60541.Dockerfile) |
| source files (`patch`) | `pandas/core/computation/expressions.py`, `pandas/core/computation/pytables.py` |
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
Pull request #60541: FIX: ruff checks in expressions/pytables

Fixes style checks on main
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/pandas/core/computation/expressions.py b/pandas/core/computation/expressions.py
index a2c3a706ae29c2f12983c34b8191e3e0716dab11..5a5fad0d83d7a5a7939d4384498a6a5288bb3543 100644
--- a/pandas/core/computation/expressions.py
+++ b/pandas/core/computation/expressions.py
@@ -108,7 +108,7 @@ def _evaluate_numexpr(op, op_str, left_op, right_op):
         try:
             result = ne.evaluate(
                 f"left_value {op_str} right_value",
-                local_dict={"left_value": left_value, "right_value": right_op},
+                local_dict={"left_value": left_value, "right_value": right_value},
                 casting="safe",
             )
         except TypeError:
@@ -257,7 +257,10 @@ def where(cond, left_op, right_op, use_numexpr: bool = True):
         Whether to try to use numexpr.
     """
     assert _where is not None
-    return _where(cond, left_op, right_op) if use_numexpr else _where_standard(cond, left_op, right_op)
+    if use_numexpr:
+        return _where(cond, left_op, right_op)
+    else:
+        return _where_standard(cond, left_op, right_op)
 
 
 def set_test_mode(v: bool = True) -> None:
diff --git a/pandas/core/computation/pytables.py b/pandas/core/computation/pytables.py
index 4a75acce4663278e78a028b0096d074a862990e4..166c9d47294cd7b3cf384aaa63046edea849d340 100644
--- a/pandas/core/computation/pytables.py
+++ b/pandas/core/computation/pytables.py
@@ -274,7 +274,9 @@ class BinOp(ops.BinOp):
             # string quoting
             return TermValue(conv_val, stringify(conv_val), "string")
         else:
-            raise TypeError(f"Cannot compare {conv_val} of type {type(conv_val)} to {kind} column")
+            raise TypeError(
+                f"Cannot compare {conv_val} of type {type(conv_val)} to {kind} column"
+            )
 
     def convert_values(self) -> None:
         pass
```

## `test_patch` -- the developer's tests (held out)

```diff

```


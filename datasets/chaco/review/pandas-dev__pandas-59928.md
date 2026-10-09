# pandas-dev__pandas-59928

[back to the list](README.md) -- **CLN: indexes/base.py**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#59928](https://github.com/pandas-dev/pandas/pull/59928) (created 2024-09-30, merged 2024-10-03) |
| ChaCo lists | full, ablation |
| status | **no-developer-test** -- the PR adds or changes no test: FAIL_TO_PASS cannot be derived |
| base commit | [`198ed865420c`](https://github.com/pandas-dev/pandas/commit/198ed865420c2a206dc062a32be47c7cc5e76bc0) (2024-10-03), first parent of the merge commit |
| merge commit | [`c47296ad3b99`](https://github.com/pandas-dev/pandas/commit/c47296ad3b9908f77fba5830ec9dbb7f546cb720) |
| issues closed | none |
| version | (set by validate) |
| image | `f2p-chaco/pandas-dev__pandas-59928:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-59928.Dockerfile) |
| source files (`patch`) | `pandas/core/indexes/base.py` |
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
Pull request #59928: CLN: indexes/base.py

* Use `is_iterator` instead of one off `ensure_has_len`
* Just process data twice instead of n times in `trim_front`
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/pandas/core/indexes/base.py b/pandas/core/indexes/base.py
index 852049804a4f566ebce5c2ac1d2b07ed3660370f..749a5fea4d5137cd8d0ba863cff109fa951925a1 100644
--- a/pandas/core/indexes/base.py
+++ b/pandas/core/indexes/base.py
@@ -4153,7 +4153,8 @@ class Index(IndexOpsMixin, PandasObject):
         preserve_names = not hasattr(target, "name")
 
         # GH7774: preserve dtype/tz if target is empty and not an Index.
-        target = ensure_has_len(target)  # target may be an iterator
+        if is_iterator(target):
+            target = list(target)
 
         if not isinstance(target, Index) and len(target) == 0:
             if level is not None and self._is_multi:
@@ -7568,21 +7569,9 @@ def ensure_index(index_like: Axes, copy: bool = False) -> Index:
         return Index(index_like, copy=copy)
 
 
-def ensure_has_len(seq):
-    """
-    If seq is an iterator, put its values into a list.
-    """
-    try:
-        len(seq)
-    except TypeError:
-        return list(seq)
-    else:
-        return seq
-
-
 def trim_front(strings: list[str]) -> list[str]:
     """
-    Trims zeros and decimal points.
+    Trims leading spaces evenly among all strings.
 
     Examples
     --------
@@ -7594,8 +7583,9 @@ def trim_front(strings: list[str]) -> list[str]:
     """
     if not strings:
         return strings
-    while all(strings) and all(x[0] == " " for x in strings):
-        strings = [x[1:] for x in strings]
+    smallest_leading_space = min(len(x) - len(x.lstrip()) for x in strings)
+    if smallest_leading_space > 0:
+        strings = [x[smallest_leading_space:] for x in strings]
     return strings
```

## `test_patch` -- the developer's tests (held out)

```diff

```


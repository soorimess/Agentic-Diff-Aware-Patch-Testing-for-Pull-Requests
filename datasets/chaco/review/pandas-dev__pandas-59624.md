# pandas-dev__pandas-59624

[back to the list](README.md) -- **API (string): str.center with pyarrow-backed string dtype**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#59624](https://github.com/pandas-dev/pandas/pull/59624) (created 2024-08-27, merged 2024-09-02) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 1 developer test(s) flip; oracle reproduces it |
| base commit | [`2c7674047e28`](https://github.com/pandas-dev/pandas/commit/2c7674047e28f3a6eefedeeff20aaff03dca7300) (2024-09-02), first parent of the merge commit |
| merge commit | [`db1b8ab2fc1a`](https://github.com/pandas-dev/pandas/commit/db1b8ab2fc1a65c2e520dc9ffb6390743a00d63b) |
| issues closed | [#54807](https://github.com/pandas-dev/pandas/issues/54807) |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-59624:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-59624.Dockerfile) |
| source files (`patch`) | `doc/source/whatsnew/v2.3.0.rst`, `pandas/core/arrays/_arrow_string_mixins.py`, `pandas/core/arrays/string_arrow.py` |
| test files (`test_patch`) | `pandas/tests/strings/test_case_justify.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (1)

- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar[string=str[pyarrow]]`

## PASS_TO_PASS (111)

<details><summary>show</summary>

- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=object-data0-expected0]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=object-data1-expected1]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=object-data2-expected2]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=str[pyarrow]-data0-expected0]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=str[pyarrow]-data1-expected1]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=str[pyarrow]-data2-expected2]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=str[python]-data0-expected0]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=str[python]-data1-expected1]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=str[python]-data2-expected2]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=string[pyarrow]-data0-expected0]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=string[pyarrow]-data1-expected1]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=string[pyarrow]-data2-expected2]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=string[python]-data0-expected0]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=string[python]-data1-expected1]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize[string=string[python]-data2-expected2]`
- `pandas/tests/strings/test_case_justify.py::test_capitalize_mixed_object`
- `pandas/tests/strings/test_case_justify.py::test_casefold`
- `pandas/tests/strings/test_case_justify.py::test_casemethods[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_casemethods[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_casemethods[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_casemethods[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_casemethods[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar_bad_arg_raises[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar_bad_arg_raises[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar_bad_arg_raises[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar_bad_arg_raises[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar_bad_arg_raises[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_mixed_object`
- `pandas/tests/strings/test_case_justify.py::test_lower_upper[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_lower_upper[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_lower_upper[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_lower_upper[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_lower_upper[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_lower_upper_mixed_object`
- `pandas/tests/strings/test_case_justify.py::test_pad[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_pad[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_pad[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_pad[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_pad[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar_bad_arg_raises[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar_bad_arg_raises[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar_bad_arg_raises[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar_bad_arg_raises[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_fillchar_bad_arg_raises[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_pad_mixed_object`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=object-center]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=object-ljust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=object-pad]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=object-rjust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=object-zfill]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[pyarrow]-center]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[pyarrow]-ljust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[pyarrow]-pad]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[pyarrow]-rjust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[pyarrow]-zfill]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[python]-center]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[python]-ljust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[python]-pad]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[python]-rjust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=str[python]-zfill]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[pyarrow]-center]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[pyarrow]-ljust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[pyarrow]-pad]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[pyarrow]-rjust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[pyarrow]-zfill]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[python]-center]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[python]-ljust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[python]-pad]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[python]-rjust]`
- `pandas/tests/strings/test_case_justify.py::test_pad_width_bad_arg_raises[string=string[python]-zfill]`
- `pandas/tests/strings/test_case_justify.py::test_swapcase[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_swapcase[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_swapcase[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_swapcase[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_swapcase[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_swapcase_mixed_object`
- `pandas/tests/strings/test_case_justify.py::test_title[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_title[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_title[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_title[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_title[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_title_mixed_object`
- `pandas/tests/strings/test_case_justify.py::test_wrap[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_wrap[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_wrap[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_wrap[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_wrap[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=string[python]]`
- `pandas/tests/strings/test_case_justify.py::test_zfill[string=object]`
- `pandas/tests/strings/test_case_justify.py::test_zfill[string=str[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_zfill[string=str[python]]`
- `pandas/tests/strings/test_case_justify.py::test_zfill[string=string[pyarrow]]`
- `pandas/tests/strings/test_case_justify.py::test_zfill[string=string[python]]`

</details>

## Problem statement (what the agent may be shown)

````text
Issue #54807: API: behaviour for the "str.center()" string method for the pyarrow-backed string dtype

From https://github.com/pandas-dev/pandas/pull/54533#discussion_r1299808126 (and relevant for new String dtype https://github.com/pandas-dev/pandas/issues/54792)

In general the pyarrow backed string dtype is meant to behave the same as the existing object-dtype or non-pyarrow backed StringDtype, so users in generally should have a smooth way of upgrading. In general most string compute functions in pyarrow have similar behaviour, or we still have a few places where we fall back to the original object-based methods.

One specific method that currently has a different behaviour is `str.center`:

```python
>>> pd.Series(["a", "bb", "cccc"], dtype="object").str.center(5, fillchar="X")
0    XXaXX
1    XXbbX
2    Xcccc
dtype: object

>>> pd.Series(["a", "bb", "cccc"], dtype="string[python]").str.center(5, fillchar="X")
0    XXaXX
1    XXbbX
2    Xcccc
dtype: string

>>> pd.Series(["a", "bb", "cccc"], dtype="string[pyarrow]").str.center(5, fillchar="X")
0    XXaXX
1    XXbbX
2    Xcccc
dtype: string

>>> pd.Series(["a", "bb", "cccc"], dtype="string[pyarrow_numpy]").str.center(5, fillchar="X")
0    XXaXX
1    XbbXX    # <-- aligned left instead of right
2    ccccX    # <-- aligned left instead of right
dtype: string
```

The first three dtypes all give the same result, but for the last one using `StringDtype(storage="pyarrow_numpy")`, the strings are "aligned" to the left instead of right in case an uneven fill chars have to be used. 

This is a behaviour we inherited from the Python `str` center method, but the pyarrow `pyarrow.compute.ascii_center` function apparently made the opposite choice (I don't think was necessarily an intentional choice to deviate from this; there was no discussion about this on the PR (https://github.com/apache/arrow/pull/10586), which did add the comment *"If odd number of spaces, put the extra space on the left"* to the relevant place in the code that handles this).

This is a potentially breaking change for users, so to start with should decide if we want to keep the current behaviour or not for the future string dtype. On the short term, we can fall back to the python string objects method (like we do for the other string dtypes). But we can also ask pyarrow to add a keyword to control this aspect of the compute function (that should be an easy change), so that in the future we can again use the faster pyarrow function.

---

Pull request #59624: API (string): str.center with pyarrow-backed string dtype

Two bad options for older-pyarrow: different behavior or object fallback.  I guessed that @mroeschke would prefer different behavior here, would be happy to be proved wrong.
````

## Hints (issue comments before the PR; not shown to the agent)

```text
xref https://github.com/apache/arrow/issues/15053
I added a `lean_left_on_odd_padding` keyword upstream in pyarrow to control this behaviour, and this is released with pyarrow 17.0. So I would propose that we fallback to the object dtype based implementation for older versions, and only use pyarrow for 17.0+ with this new keyword, to ensure we can give consistent (and not breaking) behaviour.

(at least for the new NaN variant of the String dtype under PDEP 14)
i just came across this in trying to see if ArrowStringArray._str_pad could re-use ArrowEA._str_pad.  The `pd.ArrowDtype(pa.string())` behavior matches the pyarrow_numpy behavior from the OP.  Does the proposal to fall back to the object behavior for older pyarrow and use the new keyword for newer pyarrow apply to the ArrowEA._str_pad method too?  If so I'm +1.  (i guess im +1 either way, but more enthusiastic if we can get across-the-board consistency and de-duplication)
I am fine with doing that across the board, but up to @mroeschke to decide for ArrowExtensionArray
I'm not super keen on having ArrowEA falling back in general, but if this would just be temporary until pyarrow 17 is our minimum version (where it sounds like we no longer need the fallback) then I would be OK with the logic sharing for code-deduplication.
I guess this makes sense to do as a breaking change in 3.0

On Mon, Aug 26, 2024 at 11:17 AM Matthew Roeschke ***@***.***>
wrote:

> I'm not super keen on having ArrowEA falling back in general, but if this
> would just be temporary until pyarrow 17 is our minimum version (where it
> sounds like we no longer need the fallback) then I would be OK with the
> logic sharing for code-deduplication.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/pandas-dev/pandas/issues/54807#issuecomment-2310792542>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AB5UM6FGACDS4FYINHOCDJTZTNWJZAVCNFSM6AAAAABLULQKYWVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGMJQG44TENJUGI>
> .
> You are receiving this because you commented.Message ID:
> ***@***.***>
>
```

## `patch` -- the change under test

```diff
diff --git a/doc/source/whatsnew/v2.3.0.rst b/doc/source/whatsnew/v2.3.0.rst
index 8a64aa7c609d60821acb6173a1ccff5fb7a6f2fe..03355f655eb28ce29c0e8819095dee4ae2cedafb 100644
--- a/doc/source/whatsnew/v2.3.0.rst
+++ b/doc/source/whatsnew/v2.3.0.rst
@@ -103,7 +103,8 @@ Conversion
 Strings
 ^^^^^^^
 - Bug in :meth:`Series.str.replace` when ``n < 0`` for :class:`StringDtype` with ``storage="pyarrow"`` (:issue:`59628`)
--
+- Bug in the ``center`` method on :class:`Series` and :class:`Index` object ``str`` accessors with pyarrow-backed dtype not matching the python behavior in corner cases with an odd number of fill characters (:issue:`54792`)
+
 
 Interval
 ^^^^^^^^
diff --git a/pandas/core/arrays/_arrow_string_mixins.py b/pandas/core/arrays/_arrow_string_mixins.py
index c810af32f748095a0d553c6d897ae418569df5f1..b5cf0573e70bafc122b71b5077d9cd24e89d38f2 100644
--- a/pandas/core/arrays/_arrow_string_mixins.py
+++ b/pandas/core/arrays/_arrow_string_mixins.py
@@ -1,5 +1,6 @@
 from __future__ import annotations
 
+from functools import partial
 from typing import (
     TYPE_CHECKING,
     Literal,
@@ -7,7 +8,10 @@ from typing import (
 
 import numpy as np
 
-from pandas.compat import pa_version_under10p1
+from pandas.compat import (
+    pa_version_under10p1,
+    pa_version_under17p0,
+)
 
 from pandas.core.dtypes.missing import isna
 
@@ -49,7 +53,19 @@ class ArrowStringArrayMixin:
         elif side == "right":
             pa_pad = pc.utf8_rpad
         elif side == "both":
-            pa_pad = pc.utf8_center
+            if pa_version_under17p0:
+                # GH#59624 fall back to object dtype
+                from pandas import array
+
+                obj_arr = self.astype(object, copy=False)  # type: ignore[attr-defined]
+                obj = array(obj_arr, dtype=object)
+                result = obj._str_pad(width, side, fillchar)  # type: ignore[attr-defined]
+                return type(self)._from_sequence(result, dtype=self.dtype)  # type: ignore[attr-defined]
+            else:
+                # GH#54792
+                # https://github.com/apache/arrow/issues/15053#issuecomment-2317032347
+                lean_left = (width % 2) == 0
+                pa_pad = partial(pc.utf8_center, lean_left_on_odd_padding=lean_left)
         else:
             raise ValueError(
                 f"Invalid side: {side}. Side must be one of 'left', 'right', 'both'"
diff --git a/pandas/core/arrays/string_arrow.py b/pandas/core/arrays/string_arrow.py
index e8e74b0ba12154991d266fe10b60bce9ee078ccf..a3169985828e8c79b935be6cdc58cc8a52141c93 100644
--- a/pandas/core/arrays/string_arrow.py
+++ b/pandas/core/arrays/string_arrow.py
@@ -284,6 +284,7 @@ class ArrowStringArray(ObjectStringArrayMixin, ArrowExtensionArray, BaseStringAr
     _str_map = BaseStringArray._str_map
     _str_startswith = ArrowStringArrayMixin._str_startswith
     _str_endswith = ArrowStringArrayMixin._str_endswith
+    _str_pad = ArrowStringArrayMixin._str_pad
 
     def _str_contains(
         self, pat, case: bool = True, flags: int = 0, na=np.nan, regex: bool = True
@@ -546,7 +547,6 @@ class ArrowStringArrayNumpySemantics(ArrowStringArray):
     _str_get = ArrowStringArrayMixin._str_get
     _str_removesuffix = ArrowStringArrayMixin._str_removesuffix
     _str_capitalize = ArrowStringArrayMixin._str_capitalize
-    _str_pad = ArrowStringArrayMixin._str_pad
     _str_title = ArrowStringArrayMixin._str_title
     _str_swapcase = ArrowStringArrayMixin._str_swapcase
     _str_slice_replace = ArrowStringArrayMixin._str_slice_replace
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/strings/test_case_justify.py b/pandas/tests/strings/test_case_justify.py
index 41aedae90ca7656a3df7c4f09beee79b2f533741..819556f961fa39fa2e93388fd12d37b0f9aefa4d 100644
--- a/pandas/tests/strings/test_case_justify.py
+++ b/pandas/tests/strings/test_case_justify.py
@@ -291,11 +291,7 @@ def test_center_ljust_rjust_mixed_object():
 
 
 def test_center_ljust_rjust_fillchar(any_string_dtype):
-    if any_string_dtype == "string[pyarrow_numpy]":
-        pytest.skip(
-            "Arrow logic is different, "
-            "see https://github.com/pandas-dev/pandas/pull/54533/files#r1299808126",
-        )
+    # GH#54533, GH#54792
     s = Series(["a", "bb", "cccc", "ddddd", "eeeeee"], dtype=any_string_dtype)
 
     result = s.str.center(5, fillchar="X")
```

## Validation

```json
{
 "test_files": [
  "pandas/tests/strings/test_case_justify.py"
 ],
 "collected_before": 112,
 "collected_after": 112,
 "outcomes_before": {
  "PASSED": 111,
  "FAILED": 1
 },
 "outcomes_after": {
  "PASSED": 112
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "enter_ljust_rjust_fillchar_bad_arg_raises[string=str[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=object]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=string[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=string[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=str[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=str[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=object]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=string[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=string[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=str[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=str[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=object]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=string[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=string[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=str[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=str[python]]\nFAILED pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar[string=str[pyarrow]]\n======================== 1 failed, 111 passed in 0.31s =========================",
 "tail_after": "st_fillchar_bad_arg_raises[string=str[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_center_ljust_rjust_fillchar_bad_arg_raises[string=str[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=object]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=string[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=string[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=str[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_zfill[string=str[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=object]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=string[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=string[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=str[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap[string=str[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=object]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=string[python]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=string[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=str[pyarrow]]\nPASSED pandas/tests/strings/test_case_justify.py::test_wrap_unicode[string=str[python]]\n============================= 112 passed in 0.25s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```

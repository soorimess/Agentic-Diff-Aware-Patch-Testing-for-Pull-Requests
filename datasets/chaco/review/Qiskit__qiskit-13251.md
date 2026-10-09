# Qiskit__qiskit-13251

[back to the list](README.md) -- **Workaround symengine serialization payload incompatibility**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#13251](https://github.com/Qiskit/qiskit/pull/13251) (created 2024-10-01, merged 2024-10-02) |
| ChaCo lists | full, ablation |
| status | **no-developer-test** -- the PR adds or changes no test: FAIL_TO_PASS cannot be derived |
| base commit | [`f1b25806e976`](https://github.com/Qiskit/qiskit/commit/f1b25806e97674428b8d687bd5886f23fd6cbe80) (2024-10-02), first parent of the merge commit |
| merge commit | [`fee9f771c2c2`](https://github.com/Qiskit/qiskit/commit/fee9f771c2c28bd3bc67b364fbed2e71e3b1b805) |
| issues closed | none |
| version | (set by validate) |
| image | `f2p-chaco/qiskit__qiskit-13251:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-13251.Dockerfile) |
| source files (`patch`) | `qiskit/qpy/__init__.py`, `qiskit/qpy/binary_io/schedules.py`, `qiskit/qpy/binary_io/value.py`, `qiskit/qpy/common.py`, `qiskit/qpy/interface.py`, `releasenotes/notes/fix-qpy-symengine-compat-858970a9a1d6bc14.yaml`, `requirements.txt` |
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
Pull request #13251: Workaround symengine serialization payload incompatibility

### Summary

In QPY we rely on symengine's internal serialization to represent the internal symbolic expression stored inside a ParameterExpression object. However, this format is nominally symengine version specific and will raise an error if there is a mismatch between the version used to generate the payload and what is trying to read it. This became an issue in the recent symengine 0.13 release which started to raise an error when people installed it and tried to load QPY payloads across the versions. This makes the symengine serialization unsuitable for use in QPY because it's supposed to be independent of these kind of concerns, especially when QPY is used in a server-client model where you don't necessarily control the installed environment of symengine.

To correctly address this issue we'll need a new version of the QPY format that owns the serialization format of ParameterExpressions directly instead of relying on symengine which doesn't offer a compatibility guarantee on the format. However this won't be quick solution and users are encountering issues since the release of 0.13. This commit introduces a workaround for this specific instance of the mismatch. It turns out the payload format between 0.11 and 0.13 is completely unchanged except for the version number. So before passing the parameter expression payload to symengine for deserialization this commit checks the versions numbers are the same, if they're not it checks that we're dealing with 0.11 or 0.13, and if so it changes the version number in the payloads header appropriately. If the version number is outside those bounds it raises an exception because while this hack is known to be safe for translating between symengine 0.11 and 0.13, it's not possible to know for a future version whether the payload format changed or not.

Longer term we will need a proper fix in qpy version 13 that introduces a qiskit native serialization format for parameter expression instead of relying on symengine or sympy to do it for us.

### Details and comments
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/qpy/__init__.py b/qiskit/qpy/__init__.py
index eccb09ce73d6a8d1df785062ff20c253c5df8e3a..d6928a134a83000139cc5248be72c952a429f27d 100644
--- a/qiskit/qpy/__init__.py
+++ b/qiskit/qpy/__init__.py
@@ -116,6 +116,30 @@ and how the feature will be internally handled.
 
 .. autoexception:: QPYLoadingDeprecatedFeatureWarning
 
+.. note::
+
+    With versions of Qiskit before 1.2.3, the ``use_symengine=True`` argument to :func:`.qpy.dump`
+    could cause problems with backwards compatibility if there were :class:`.ParameterExpression`
+    objects to serialize.  In particular:
+
+    * When the loading version of Qiskit is 1.2.3 or greater, QPY files generated with any version
+      of Qiskit >= 0.46.0 can be loaded.  If a version of Qiskit between 0.45.0 and 0.45.3 was used
+      to generate the files, and the non-default argument ``use_symengine=True`` was given to
+      :func:`.qpy.dump`, the file can only be read if the version of ``symengine`` used in the
+      generating environment was in the 0.11 or 0.13 series, but if the environment was created
+      during the support window of Qiskit 0.45, it is likely that ``symengine==0.9.2`` was used.
+
+    * When the loading version of Qiskit is between 0.46.0 and 1.2.2 inclusive, the file can only be
+      read if the installed version of ``symengine`` in the loading environment matches the version
+      used in the generating environment.
+
+    To recover a QPY file that fails with ``symengine`` version-related errors during a call to
+    :func:`.qpy.load`, first attempt to use Qiskit >= 1.2.3 to load the file.  If this still fails,
+    it is likely because Qiskit 0.45.x was used to generate the file with ``use_symengine=True``.
+    In this case, use Qiskit 0.45.3 with ``symengine==0.9.2`` to load the file, and then re-export
+    it to QPY setting ``use_symengine=False``.  The resulting file can then be loaded by any later
+    version of Qiskit.
+
 QPY format version history
 --------------------------
 
diff --git a/qiskit/qpy/binary_io/schedules.py b/qiskit/qpy/binary_io/schedules.py
index eae5e6f57ad903f7abe48e32678e10f0de26af2f..1bf86d254186b70b9acfddf0b4f36bdb5a357b2e 100644
--- a/qiskit/qpy/binary_io/schedules.py
+++ b/qiskit/qpy/binary_io/schedules.py
@@ -20,9 +20,6 @@ from io import BytesIO
 
 import numpy as np
 import symengine as sym
-from symengine.lib.symengine_wrapper import (  # pylint: disable = no-name-in-module
-    load_basic,
-)
 
 from qiskit.exceptions import QiskitError
 from qiskit.pulse import library, channels, instructions
@@ -106,7 +103,7 @@ def _loads_symbolic_expr(expr_bytes, use_symengine=False):
         return None
     expr_bytes = zlib.decompress(expr_bytes)
     if use_symengine:
-        return load_basic(expr_bytes)
+        return common.load_symengine_payload(expr_bytes)
     else:
         from sympy import parse_expr
 
diff --git a/qiskit/qpy/binary_io/value.py b/qiskit/qpy/binary_io/value.py
index 105d4364c07ef534758cbae09d6caa3dea974cad..5b82e14d15cd1b324e2bd1d6194ebc98ae6e5927 100644
--- a/qiskit/qpy/binary_io/value.py
+++ b/qiskit/qpy/binary_io/value.py
@@ -20,9 +20,6 @@ import uuid
 
 import numpy as np
 import symengine
-from symengine.lib.symengine_wrapper import (  # pylint: disable = no-name-in-module
-    load_basic,
-)
 
 
 from qiskit.circuit import CASE_DEFAULT, Clbit, ClassicalRegister
@@ -290,7 +287,7 @@ def _read_parameter_expression_v3(file_obj, vectors, use_symengine):
 
     payload = file_obj.read(data.expr_size)
     if use_symengine:
-        expr_ = load_basic(payload)
+        expr_ = common.load_symengine_payload(payload)
     else:
         from sympy.parsing.sympy_parser import parse_expr
 
diff --git a/qiskit/qpy/common.py b/qiskit/qpy/common.py
index 048320d5cad6f61a1b94f4b702adccde9c934429..6084f53a1701561b98f1cbc1c31ef8336ced5ae6 100644
--- a/qiskit/qpy/common.py
+++ b/qiskit/qpy/common.py
@@ -18,7 +18,12 @@ Common functions across several serialization and deserialization modules.
 import io
 import struct
 
-from qiskit.qpy import formats
+import symengine
+from symengine.lib.symengine_wrapper import (  # pylint: disable = no-name-in-module
+    load_basic,
+)
+
+from qiskit.qpy import formats, exceptions
 
 QPY_VERSION = 12
 QPY_COMPATIBILITY_VERSION = 10
@@ -304,3 +309,42 @@ def mapping_from_binary(binary_data, deserializer, **kwargs):
         mapping = read_mapping(container, deserializer, **kwargs)
 
     return mapping
+
+
+def load_symengine_payload(payload: bytes) -> symengine.Expr:
+    """Load a symengine expression from it's serialized cereal payload."""
+    # This is a horrible hack to workaround the symengine version checking
+    # it's deserialization does. There were no changes to the serialization
+    # format between 0.11 and 0.13 but the deserializer checks that it can't
+    # load across a major or minor version boundary. This works around it
+    # by just lying about the generating version.
+    symengine_version = symengine.__version__.split(".")
+    major = payload[2]
+    minor = payload[3]
+    if int(symengine_version[1]) != minor:
+        if major != "0":
+            raise exceptions.QpyError(
+                "Qiskit doesn't support loading a symengine payload generated with symengine >= 1.0"
+            )
+        if minor == 9:
+            raise exceptions.QpyError(
+                "Qiskit doesn't support loading a historical QPY file with `use_symengine=True` "
+                "generated in an environment using symengine 0.9.0. If you need to load this file "
+                "you can do so with Qiskit 0.45.x or 0.46.x and re-export the QPY file using "
+                "`use_symengine=False`."
+            )
+        if minor not in (11, 13):
+            raise exceptions.QpyError(
+                f"Incompatible symengine version {major}.{minor} used to generate the QPY "
+                "payload"
+            )
+        minor_version = int(symengine_version[1])
+        if minor_version not in (11, 13):
+            raise exceptions.QpyError(
+                f"Incompatible installed symengine version {symengine.__version__} to load "
+                "this QPY payload"
+            )
+        payload = bytearray(payload)
+        payload[3] = minor_version
+        payload = bytes(payload)
+    return load_basic(payload)
diff --git a/qiskit/qpy/interface.py b/qiskit/qpy/interface.py
index d89117bc6a1cd5d3913ff3f3a4d556165cd24f1b..827857ab2b0564a60b2127490af2f348aa3d39be 100644
--- a/qiskit/qpy/interface.py
+++ b/qiskit/qpy/interface.py
@@ -144,6 +144,17 @@ def dump(
                 from the QPY format at that version will persist. This should only be used if
                 compatibility with loading the payload with an older version of Qiskit is necessary.
 
+            .. note::
+
+                If serializing a :class:`.QuantumCircuit` or :class:`.ScheduleBlock` that contain
+                :class:`.ParameterExpression` objects with ``version`` set low with the intent to
+                load the payload using a historical release of Qiskit, it is safest to set the
+                ``use_symengine`` flag to ``False``.  Versions of Qiskit prior to 1.2.3 cannot load
+                QPY files containing ``symengine``-serialized :class:`.ParameterExpression` objects
+                unless the version of ``symengine`` used between the loading and generating
+                environments matches.
+
+
     Raises:
         QpyError: When multiple data format is mixed in the output.
         TypeError: When invalid data type is input.
diff --git a/releasenotes/notes/fix-qpy-symengine-compat-858970a9a1d6bc14.yaml b/releasenotes/notes/fix-qpy-symengine-compat-858970a9a1d6bc14.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..359106de496f815e9a23c72796f7220d086e0a5a
--- /dev/null
+++ b/releasenotes/notes/fix-qpy-symengine-compat-858970a9a1d6bc14.yaml
@@ -0,0 +1,62 @@
+---
+fixes:
+  - |
+    Fixed an issue with :func:`.qpy.load` when loading a QPY file containing
+    a :class:`.ParameterExpression`, if the versions of ``symengine`` installed
+    in the generating and loading environments were not the same.  For example,
+    if a QPY file containing :class:`.ParameterExpression`\ s was generated
+    using Qiskit 1.2.2 with ``symengine==0.11.0`` installed, Qiskit 1.2.2 with
+    ``syengine==0.13.0`` installed would be unable to load it.
+
+    Previously, an error would have been raised by ``symengine`` around this
+    version mismatch. This has been worked around for ``symengine`` 0.11 and
+    0.13 (there was no 0.12), but if you're trying to use different versions of
+    ``symengine`` and there is a mismatch, this version of Qiskit still might not
+    work.
+issues:
+  - |
+    Versions of Qiskit before 1.2.3 will not be able to load QPY files dumped
+    using :func:`.qpy.dump`, even with ``version`` set appropriately, if:
+
+    * there are unbound :class:`.ParameterExpression`\ s in the QPY file,
+    * the ``use_symengine=True`` flag was set (which is the default in Qiskit >=
+      1.0.0) in :func:`.qpy.dump`,
+    * the version of ``symengine`` installed in the generating and loading
+      environments are not within the same minor version.
+
+    This applies regardless of the version of Qiskit used in the generation (at
+    least up to Qiskit 1.2.3 inclusive).
+
+    If you want to maximize compatibility with older versions of Qiskit, you
+    should set ``use_symengine=False``.  Newer versions of Qiskit should not
+    require this.
+  - |
+    QPY files from the Qiskit 0.45 series can, under a very specific and unlikely
+    set of circumstances, fail to load with any newer version of Qiskit,
+    including Qiskit 1.2.3.  The criteria are:
+
+    * the :class:`.QuantumCircuit` or :class:`.ScheduleBlock` to be dumped
+      contained unbound :class:`.ParameterExpression` objects,
+    * the installed version of ``symengine`` was in the 0.9 series (which was the
+      most recent release during the support window of Qiskit 0.45),
+    * the ``use_symengine=True`` flag was set (which was *not* the default).
+
+    Later versions of Qiskit used during generation are not affected, because
+    they required newer versions than ``symengine`` 0.9.
+
+    In this case, you can recover the QPY file by reloading it with an environment
+    with Qiskit 0.45.3 and ``symengine`` 0.9.2 installed.  Then, use
+    :func:`.qpy.dump` with ``use_symengine=False`` to re-export the file. This
+    will then be readable by any newer version of Qiskit.
+upgrade:
+  - |
+    The supported versions of `symengine <https://pypi.org/project/symengine/>`__
+    have been pre-emptively capped at < 0.14.0 (which is expected to be the next
+    minor version, as of this release of Qiskit).  This has been done to protect
+    against a potential incompatibility in :mod:`.qpy` when serializing
+    :class:`.ParameterExpression` objects. The serialization used in
+    :ref:`qpy_format` versions 10, 11, and 12 for :class:`.ParameterExpression`
+    objects is tied to the symengine version used to generate it, and there is the potential
+    for a future symengine release to not be compatible. This upper version cap is to prevent
+    a future release of symengine causing incompatibilities when trying to load QPY files
+    using :class:`.qpy.load`.
diff --git a/requirements.txt b/requirements.txt
index 2dd5e49e2b3d207735b7fa1ddb0c768619cf533b..4c13eb6dc60af405385c3c7fbfd4126b36d12215 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -6,4 +6,4 @@ dill>=0.3
 python-dateutil>=2.8.0
 stevedore>=3.0.0
 typing-extensions
-symengine>=0.11
+symengine>=0.11,<0.14
```

## `test_patch` -- the developer's tests (held out)

```diff

```


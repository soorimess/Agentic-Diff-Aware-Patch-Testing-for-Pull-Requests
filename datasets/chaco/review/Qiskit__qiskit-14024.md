# Qiskit__qiskit-14024

[back to the list](README.md) -- **Introduce custom sympy srepr parser**

| field | value |
|---|---|
| pull request | [Qiskit/qiskit#14024](https://github.com/Qiskit/qiskit/pull/14024) (created 2025-03-14, merged 2025-03-17) |
| ChaCo lists | full, ablation |
| status | **no-developer-test** -- no developer test (FAIL_TO_PASS cannot be derived); image at the base commit, patch applies and reverts |
| base commit | [`a5c33a8aa3fa`](https://github.com/Qiskit/qiskit/commit/a5c33a8aa3face520c3819520441f0f4f2c996ee) (2025-03-17), first parent of the merge commit |
| merge commit | [`8bcc9f1f73d5`](https://github.com/Qiskit/qiskit/commit/8bcc9f1f73d53bb6c19f33949d3decb3133c7f4c) |
| issues closed | none |
| version | 2.1 |
| image | `f2p-chaco/qiskit__qiskit-14024:latest` -- [Dockerfile](../dockerfiles/Qiskit__qiskit-14024.Dockerfile) |
| source files (`patch`) | `qiskit/circuit/parameterexpression.py`, `qiskit/circuit/tools/pi_check.py`, `qiskit/qpy/binary_io/parse_sympy_repr.py`, `qiskit/qpy/binary_io/value.py`, `qiskit/transpiler/passes/optimization/template_matching/template_substitution.py`, `releasenotes/notes/fix-ace-qpyv1-609551d84531e016.yaml` |
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
Pull request #14024: Introduce custom sympy srepr parser

### Summary

This commit introduces a custom parser to QPY for parameter expression payloads that were generated using sympy. Prior to QPY version 10 this was the only way we supported serializing parameter expressions in QPY. For QPY version 10, 11, and 12 sympy could optionally be used if the payload was generated explicitly to not use symengine (in qiskit 1.0 it defaulted to use symengine).

This serialization format relied on sympy to generate a string representation of the expression which we then put in the payload. On deserialization we called sympy's parse_expr() function which internally is calling sympy's sympify() internally. Sympy documents that sympify() relies on Python's eval() for string input and should not be used with untrusted input. But parse_expr() didn't have such a warning (at the time, I plan to contribute adding one), so using this function provides an avenue for arbitrary code execution during QPY deserialization.

This commit fixes this issue by writing a custom parser for the string representation in a QPY payload based on python's ast module. This parser walks the abstract syntax tree and builds the sympy expression object as it it goes. It is restricted to the operations that ParameterExpression supports and if any part of the string tries to use functionality outside that set it will error.

### Details and comments
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/qiskit/circuit/parameterexpression.py b/qiskit/circuit/parameterexpression.py
index c2400a1f96aff49ac6c4c3569f43b929d92d4652..2683cb5c015b0045796a6eae0365157634c854c2 100644
--- a/qiskit/circuit/parameterexpression.py
+++ b/qiskit/circuit/parameterexpression.py
@@ -26,6 +26,7 @@ import numpy
 import symengine
 
 from qiskit.circuit.exceptions import CircuitError
+from qiskit.exceptions import QiskitError
 from qiskit.utils.optionals import HAS_SYMPY
 
 # This type is redefined at the bottom to insert the full reference to "ParameterExpression", so it
@@ -531,6 +532,9 @@ class ParameterExpression:
     def __str__(self):
         from sympy import sympify, sstr
 
+        if not isinstance(self._symbol_expr, symengine.Basic):
+            raise QiskitError("Invalid ParameterExpression")
+
         return sstr(sympify(self._symbol_expr), full_prec=False)
 
     def __complex__(self):
@@ -611,6 +615,9 @@ class ParameterExpression:
                 return False
             from sympy import sympify
 
+            if not isinstance(self._symbol_expr, symengine.Basic):
+                raise QiskitError("Invalid ParameterExpression")
+
             return sympify(self._symbol_expr).equals(sympify(other._symbol_expr))
         elif isinstance(other, numbers.Number):
             return len(self.parameters) == 0 and complex(self._symbol_expr) == other
diff --git a/qiskit/circuit/tools/pi_check.py b/qiskit/circuit/tools/pi_check.py
index 334b9683ae9b4c58bf75dad9f161a1936a76457d..e3bee8f326c98e9280a8729ad1047419d302ad36 100644
--- a/qiskit/circuit/tools/pi_check.py
+++ b/qiskit/circuit/tools/pi_check.py
@@ -49,7 +49,10 @@ def pi_check(inpt, eps=1e-9, output="text", ndigits=None):
     if isinstance(inpt, ParameterExpression):
         param_str = str(inpt)
         from sympy import sympify
+        import symengine
 
+        if not isinstance(inpt._symbol_expr, symengine.Basic):
+            raise QiskitError("Invalid ParameterExpression provided")
         expr = sympify(inpt._symbol_expr)
         syms = expr.atoms()
         for sym in syms:
diff --git a/qiskit/qpy/binary_io/parse_sympy_repr.py b/qiskit/qpy/binary_io/parse_sympy_repr.py
new file mode 100644
index 0000000000000000000000000000000000000000..af9d6f8b5d205c08959da2fced615fceaeaec631
--- /dev/null
+++ b/qiskit/qpy/binary_io/parse_sympy_repr.py
@@ -0,0 +1,121 @@
+# This code is part of Qiskit.
+#
+# (C) Copyright IBM 2025.
+#
+# This code is licensed under the Apache License, Version 2.0. You may
+# obtain a copy of this license in the LICENSE.txt file in the root directory
+# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
+#
+# Any modifications or derivative works of this code must retain this
+# copyright notice, and modified files need to carry a notice indicating
+# that they have been altered from the originals.
+
+"""Parser for sympy expressions srepr from ParameterExpression internals."""
+
+import ast
+
+from qiskit.qpy.exceptions import QpyError
+
+
+ALLOWED_CALLERS = {
+    "Abs",
+    "Add",
+    "Sub",
+    "Mul",
+    "Div",
+    "Pow",
+    "Symbol",
+    "Integer",
+    "Rational",
+    "Complex",
+    "Float",
+    "log",
+    "sin",
+    "cos",
+    "tan",
+    "atan",
+    "acos",
+    "asin",
+    "exp",
+    "conjugate",
+}
+
+UNARY = {
+    "sin",
+    "cos",
+    "tan",
+    "atan",
+    "acos",
+    "asin",
+    "conjugate",
+    "Symbol",
+    "Integer",
+    "Complex",
+    "Abs",
+    "Float",
+}
+
+
+class ParseSympyWalker(ast.NodeVisitor):
+    """A custom ast walker that is passed the sympy srepr from QPY < 13 and creates a custom
+    expression."""
+
+    def __init__(self):
+        self.stack = []
+
+    def visit_UnaryOp(self, node: ast.UnaryOp):  # pylint: disable=invalid-name
+        """Visit a python unary op node"""
+        self.visit(node.operand)
+        arg = self.stack.pop()
+        if isinstance(node.op, ast.UAdd):
+            self.stack.append(+arg)
+        elif isinstance(node.op, ast.USub):
+            self.stack.append(-arg)
+        elif isinstance(node.op, ast.Not):
+            self.stack.append(not arg)
+        elif isinstance(node.op, ast.Invert):
+            self.stack.append(~arg)
+        else:
+            raise QpyError(f"Invalid unary op as part of sympy srepr: {node.op}")
+
+    def visit_Constant(self, node: ast.Constant):  # pylint: disable=invalid-name
+        """Visit a constant node."""
+        self.stack.append(node.value)
+
+    def visit_Call(self, node: ast.Call):  # pylint: disable=invalid-name
+        """Visit a call node
+
+        This can only be parameter expression allowed sympy call types.
+        """
+        import sympy
+
+        if isinstance(node.func, ast.Name):
+            name = node.func.id
+        else:
+            raise QpyError("Unknown node type")
+
+        if name not in ALLOWED_CALLERS:
+            raise QpyError(f"{name} is not part of a valid sympy expression srepr")
+
+        args = node.args
+        if name in UNARY:
+            if len(args) != 1:
+                raise QpyError(f"{name} has an invalid number of args in sympy srepr")
+            self.visit(args[0])
+            obj = getattr(sympy, name)(self.stack.pop())
+            self.stack.append(obj)
+        else:
+            for arg in args:
+                self.visit(arg)
+            out_args = [self.stack.pop() for _ in range(len(args))]
+            out_args.reverse()
+            obj = getattr(sympy, name)(*out_args)
+            self.stack.append(obj)
+
+
+def parse_sympy_repr(sympy_repr: str):
+    """Parse a given sympy srepr into a symbolic expression object."""
+    tree = ast.parse(sympy_repr, mode="eval")
+    visitor = ParseSympyWalker()
+    visitor.visit(tree)
+    return visitor.stack.pop()
diff --git a/qiskit/qpy/binary_io/value.py b/qiskit/qpy/binary_io/value.py
index f7ef0a9514ed95400c2fc023b6bf5dd026fa6b48..61c092962d9dcaeccaee581e46c458debf16de8d 100644
--- a/qiskit/qpy/binary_io/value.py
+++ b/qiskit/qpy/binary_io/value.py
@@ -34,6 +34,7 @@ from qiskit.circuit.parameterexpression import (
 )
 from qiskit.circuit.parametervector import ParameterVector, ParameterVectorElement
 from qiskit.qpy import common, formats, exceptions, type_keys
+from qiskit.qpy.binary_io.parse_sympy_repr import parse_sympy_repr
 
 
 def _write_parameter(file_obj, obj):
@@ -473,9 +474,9 @@ def _read_parameter_expression(file_obj):
     data = formats.PARAMETER_EXPR(
         *struct.unpack(formats.PARAMETER_EXPR_PACK, file_obj.read(formats.PARAMETER_EXPR_SIZE))
     )
-    from sympy.parsing.sympy_parser import parse_expr
 
-    expr_ = symengine.sympify(parse_expr(file_obj.read(data.expr_size).decode(common.ENCODE)))
+    sympy_str = file_obj.read(data.expr_size).decode(common.ENCODE)
+    expr_ = symengine.sympify(parse_sympy_repr(sympy_str))
     symbol_map = {}
     for _ in range(data.map_elements):
         elem_data = formats.PARAM_EXPR_MAP_ELEM(
@@ -514,9 +515,8 @@ def _read_parameter_expression_v3(file_obj, vectors, use_symengine):
     if use_symengine:
         expr_ = common.load_symengine_payload(payload)
     else:
-        from sympy.parsing.sympy_parser import parse_expr
-
-        expr_ = symengine.sympify(parse_expr(payload.decode(common.ENCODE)))
+        sympy_str = payload.decode(common.ENCODE)
+        expr_ = symengine.sympify(parse_sympy_repr(sympy_str))
 
     symbol_map = {}
     for _ in range(data.map_elements):
diff --git a/qiskit/transpiler/passes/optimization/template_matching/template_substitution.py b/qiskit/transpiler/passes/optimization/template_matching/template_substitution.py
index 22bb0d200086a8c23cf2a155f9610299fa4e9856..191f43f326c7c83697d89d4684b6c03ee470a5b0 100644
--- a/qiskit/transpiler/passes/optimization/template_matching/template_substitution.py
+++ b/qiskit/transpiler/passes/optimization/template_matching/template_substitution.py
@@ -496,7 +496,6 @@ class TemplateSubstitution:
                 parameter constraints, returns None.
         """
         import sympy as sym
-        from sympy.parsing.sympy_parser import parse_expr
 
         if _optionals.HAS_SYMENGINE:
             import symengine
@@ -572,7 +571,8 @@ class TemplateSubstitution:
                 if isinstance(circuit_param, ParameterExpression):
                     circ_param_sym = circuit_param.sympify()
                 else:
-                    circ_param_sym = parse_expr(str(circuit_param))
+                    # if it's not a ParameterExpression we're a float
+                    circ_param_sym = sym.Float(circuit_param)
                 equations.append(sym.Eq(template_param.sympify(), circ_param_sym))
 
                 for param in template_param.parameters:
diff --git a/releasenotes/notes/fix-ace-qpyv1-609551d84531e016.yaml b/releasenotes/notes/fix-ace-qpyv1-609551d84531e016.yaml
new file mode 100644
index 0000000000000000000000000000000000000000..eea32ab5f4f244590b5024b5f2b7a8e993a173b0
--- /dev/null
+++ b/releasenotes/notes/fix-ace-qpyv1-609551d84531e016.yaml
@@ -0,0 +1,9 @@
+---
+security:
+  - |
+    Fixed a security vulnerability in :func:`.qpy.load` when loading
+    payloads that use ``sympy`` to serialize
+    :class:`.ParameterExpression` objects and other symbolic expressions.
+    This potentially includes any QPY payload using QPY version < 10, and
+    optionally 10, 11, and 12 depending on the symbolic encoding used in the
+    serialization step (:func:`.qpy.dump`).
```

## `test_patch` -- the developer's tests (held out)

```diff

```

## Validation

```json
{
 "image_head": "a5c33a8aa3face520c3819520441f0f4f2c996ee",
 "patch_applies": true
}
```

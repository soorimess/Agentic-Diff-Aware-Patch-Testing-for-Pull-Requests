"""Which statement a line belongs to.

A changed line is not always a line either coverage or `mutmut` can say anything about.
Both of them work in *statements*, and a statement can span several lines:

    if (len(item.args[0].args) != 1 and
            isinstance(item.base, (Mul, Pow))):

`sympy-21612` changes only the second of those two lines. coverage.py reports
`executed_lines` and `missing_lines`, and a continuation line is in neither unless it
ran -- so it can be scored *hit* and never *missed*. When the test does not reach it, every
changed line disappears and the harness reports "the changed lines are all comments or
blanks", which is false: it is executable code the test missed, and the honest reading is
0%, not unmeasurable. The error flatters us, because it removes a zero from the average
instead of recording one. `mutmut`, given the same line number, offers no mutation at all,
for the same reason.

Mapping each line to the statement that contains it fixes both. The rule is the *innermost*
statement whose span covers the line, which for the example above is the `if` -- its body
statements start on later lines and do not contain line two, so the condition's own header
wins.
"""
from __future__ import annotations

import ast


def statement_start(source: str, lines: set[int] | None = None) -> dict[int, int]:
    """Map each line to the first line of the innermost statement containing it.

    `lines` narrows the result to the lines worth asking about; the walk is over every
    statement either way, and these files run to thousands of lines. A line inside no
    statement -- a comment, a blank, the space between two functions -- is absent from the
    mapping rather than mapped to itself, so a caller can tell "no statement here" from
    "this line is its own statement".

    Unparsable source returns `{}`. A file that does not parse is a file neither coverage
    nor mutmut had an opinion about either, so there is nothing to recover.
    """
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return {}

    # A line that is blank or a bare comment belongs to no statement, whatever the spans
    # say. Without this a comment sitting between a `def` and its first body line falls
    # inside the header range and maps onto the `def` -- which would turn a patch that
    # touches nothing executable, like `scikit-learn-25747`, into one that appears to.
    text = source.splitlines()
    def _is_code(ln: int) -> bool:
        if not 1 <= ln <= len(text):
            return False
        stripped = text[ln - 1].strip()
        return bool(stripped) and not stripped.startswith("#")

    best: dict[int, tuple[int, int]] = {}          # line -> (span, first line)
    for node in ast.walk(tree):
        if not isinstance(node, ast.stmt):
            continue
        start = node.lineno
        end = getattr(node, "end_lineno", None) or start
        # A compound statement claims only its header. Its body is made of statements
        # that speak for themselves, and letting the `def` span its whole function would
        # map a comment in the middle of the body onto the `def` line -- turning a
        # patch that touches nothing executable into one that appears to.
        children = [c.lineno for key in ("body", "orelse", "handlers", "finalbody")
                    for c in getattr(node, key, []) or [] if hasattr(c, "lineno")]
        if children:
            end = min(end, min(children) - 1)
        for ln in range(start, end + 1):
            if lines is not None and ln not in lines:
                continue
            if not _is_code(ln):
                continue
            span = end - start
            current = best.get(ln)
            if current is None or span < current[0]:
                best[ln] = (span, start)
    return {ln: first for ln, (_, first) in best.items()}


def widen(source: str, lines: set[int]) -> set[int]:
    """`lines`, plus the first line of every statement any of them falls inside.

    What to hand a tool that only speaks in statements. The originals are kept: a line
    that is already a statement start maps to itself, and one that is genuinely a comment
    contributes nothing.
    """
    return lines | set(statement_start(source, lines).values())

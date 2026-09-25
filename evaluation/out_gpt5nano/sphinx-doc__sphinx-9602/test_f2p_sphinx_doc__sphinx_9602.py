"""Regression tests for sphinx-9602 Literal annotations.

This test asserts the observed behaviour prior to a fix that wraps literal
values inside typing.Literal[...] with a literal node. The pre-fix behaviour
emits a cross-reference for the inner value (e.g. "True"), which nitpicky would
flag as a missing py:class target. The test is written to capture this observable
so that the regression can be confirmed when the patch is applied.
"""

from sphinx.domains.python import _parse_annotation
from sphinx.addnodes import pending_xref, desc_sig_punctuation
from sphinx.testing.util import assert_node


def test_literal_annotation_crossref_in_literal(app):
    doctree = _parse_annotation("typing.Literal[True]", app.env)
    assert_node(doctree, ([pending_xref, "Literal"],
                          [desc_sig_punctuation, "."],
                          [desc_sig_punctuation, "["],
                          [pending_xref, "True"],
                          [desc_sig_punctuation, "]"]))

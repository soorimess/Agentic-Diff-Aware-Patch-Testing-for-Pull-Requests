"""
    test_f2p_sphinx_doc__sphinx_9602
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression tests for Sphinx issue 9602.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from sphinx.addnodes import desc_sig_punctuation, pending_xref
from sphinx.domains.python import _parse_annotation
from sphinx.testing.util import assert_node


def test_literal_annotation_values_are_not_cross_references(app):
    doctree = _parse_annotation("Literal[True, 1, 'debug']", app.env)
    assert_node(doctree, ([pending_xref, "Literal"],
                          [desc_sig_punctuation, "["],
                          "True",
                          [desc_sig_punctuation, ", "],
                          "1",
                          [desc_sig_punctuation, ", "],
                          "'debug'",
                          [desc_sig_punctuation, "]"]))
    assert_node(doctree[0], pending_xref, refdomain="py", reftype="class",
                reftarget="Literal")

    doctree = _parse_annotation("typing.Literal[False]", app.env)
    assert_node(doctree, ([pending_xref, "typing.Literal"],
                          [desc_sig_punctuation, "["],
                          "False",
                          [desc_sig_punctuation, "]"]))
    assert_node(doctree[0], pending_xref, refdomain="py", reftype="class",
                reftarget="typing.Literal")

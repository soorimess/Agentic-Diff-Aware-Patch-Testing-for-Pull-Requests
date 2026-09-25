"""Regression test for Sphinx issue #10614

This verifies that when rendering an inheritance diagram as SVG the
links generated for references with a refid do not get an extra "../"
prefix.  The bug used to prepend "../" for SVG output which caused
links to resolve incorrectly when the embedding page was in a nested
directory.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from docutils import nodes

from sphinx.ext.inheritance_diagram import (
    inheritance_diagram,
    html_visit_inheritance_diagram,
)
from sphinx import addnodes


def _run_html_visit_and_capture(node, translator):
    """Helper: monkeypatch render_dot_html and run visitor, returning captured urls."""
    import sphinx.ext.inheritance_diagram as idmod

    captured = {}

    class FakeGraph:
        def generate_dot(self, name, urls=None, env=None, *args, **kwargs):
            captured['urls'] = dict(urls or {})
            return 'DOTCODE'

    node['graph'] = FakeGraph()

    original_render = idmod.render_dot_html

    def fake_render_dot_html(*args, **kwargs):
        return None

    idmod.render_dot_html = fake_render_dot_html

    try:
        with pytest.raises(nodes.SkipNode):
            html_visit_inheritance_diagram(translator, node)
    finally:
        idmod.render_dot_html = original_render

    return captured


def _make_translator_with_svg():
    fake_config = SimpleNamespace(graphviz_output_format='svg')
    fake_env = SimpleNamespace(config=fake_config)
    fake_builder = SimpleNamespace(env=fake_env,
                                   current_docname='my_package/index',
                                   out_suffix='.html')
    return SimpleNamespace(builder=fake_builder)


def test_svg_refid_links_have_no_extra_parent_prefix():
    node = inheritance_diagram()
    node['content'] = 'dummy'
    node['parts'] = 0

    child = addnodes.pending_xref('')
    child['refid'] = 'the-id'
    child['reftitle'] = 'my.module.MyClass'
    node.extend([child])

    translator = _make_translator_with_svg()

    captured = _run_html_visit_and_capture(node, translator)

    assert 'urls' in captured
    key = child['reftitle']
    assert key in captured['urls']
    expected = f"{translator.builder.current_docname}{translator.builder.out_suffix}#{child['refid']}"
    assert captured['urls'][key] == expected, (
        "SVG refid links must be relative to the current filename without an "
        "extra '../' prefix"
    )


def test_svg_refuri_internal_false_uses_fragment_and_no_prefix():
    node = inheritance_diagram()
    node['content'] = 'dummy'
    node['parts'] = 0

    child = addnodes.pending_xref('')
    child['refuri'] = 'my_package/my_class_1.html#my_package.MyClass1'
    child['reftitle'] = 'display_text'
    child['internal'] = False
    node.extend([child])

    translator = _make_translator_with_svg()

    captured = _run_html_visit_and_capture(node, translator)

    assert 'urls' in captured
    key = child['refuri'].rsplit('#', 1)[-1]
    assert key in captured['urls']
    assert captured['urls'][key] == child['refuri']


def test_svg_refuri_internal_true_uses_reftitle_and_no_prefix():
    node = inheritance_diagram()
    node['content'] = 'dummy'
    node['parts'] = 0

    child = addnodes.pending_xref('')
    child['refuri'] = 'path/to/target.html#target.Anchor'
    child['reftitle'] = 'shown.Title'
    # internal unspecified -> treated as True
    node.extend([child])

    translator = _make_translator_with_svg()

    captured = _run_html_visit_and_capture(node, translator)

    assert 'urls' in captured
    key = child['reftitle']
    assert key in captured['urls']
    assert captured['urls'][key] == child['refuri']

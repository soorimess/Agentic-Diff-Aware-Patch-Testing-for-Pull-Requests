"""Regression test for https://github.com/sphinx-doc/sphinx/issues/10614

This reproduces the problem where SVG inheritance-diagram links were built
relative to the SVG file (so nested pages got "../" prefixed URLs).

The test constructs an inheritance_diagram node with a single pending_xref
(child) and a fake graph that emits the DOT using the urls mapping produced
by html_visit_inheritance_diagram.  For a nested document (current_docname
"my_package/index"), and when graphviz_output_format is "svg", the URL for
an internal refid should be "my_package/index.html#..." (no "../" prefix).

It also checks the behavior for pending_xref nodes that have an external
refuri: the produced url should not have the extra "../" prefix when SVG is
used (and the mapping key should match the class fullname).
"""

from __future__ import annotations

import pytest
from docutils import nodes

import sphinx.ext.inheritance_diagram as inh
from sphinx import addnodes


def _make_fake_translator(nested_docname: str = 'my_package/index'):
    class DummyConfig:
        pass

    conf = DummyConfig()
    conf.graphviz_output_format = 'svg'

    class DummyEnv:
        def __init__(self, config):
            self.config = config

    class DummyBuilder:
        def __init__(self):
            self.env = DummyEnv(conf)
            self.current_docname = nested_docname
            self.out_suffix = '.html'

    translator = type('T', (), {})()
    translator.builder = DummyBuilder()
    return translator


def test_inheritance_diagram_svg_links_for_nested_page(monkeypatch):
    captured: dict[str, str] = {}

    # replace render_dot_html to capture the generated DOT code instead of
    # invoking graphviz/dot on the system.
    def fake_render_dot_html(self, node, code, options, *args, **kwargs):
        captured['code'] = code

    monkeypatch.setattr(inh, 'render_dot_html', fake_render_dot_html)

    # A minimal fake graph whose generate_dot emits a fragment containing
    # the URL value taken from the urls mapping for the fullname.
    class FakeGraph:
        def __init__(self):
            # (node_name, fullname, bases, tooltip)
            self.class_info = [('MyClass', 'my_package.MyClass', [], None)]

        def generate_dot(self, name, urls, env=None, graph_attrs=None,
                         node_attrs=None, edge_attrs=None):
            fullname = self.class_info[0][1]
            url = urls.get(fullname)
            return f'NODE {fullname} URL={url}'

    # build a fake inheritance_diagram node with one pending_xref child
    node = inh.inheritance_diagram()
    node['content'] = 'my_package.MyClass'
    node['parts'] = 0
    node['graph'] = FakeGraph()

    child = addnodes.pending_xref()
    # simulate a resolved internal reference (refid present)
    child['refid'] = 'my_package.MyClass'
    # reftitle should match the fullname used by the graph
    child['reftitle'] = 'my_package.MyClass'
    node.append(child)

    translator = _make_fake_translator()

    # the visitor raises SkipNode; that's expected so we assert it
    with pytest.raises(nodes.SkipNode):
        inh.html_visit_inheritance_diagram(translator, node)

    assert 'my_package/index.html#my_package.MyClass' in captured['code']
    assert '../my_package/index.html#my_package.MyClass' not in captured['code']


def test_inheritance_diagram_svg_links_for_refuri(monkeypatch):
    """Pending xref that has refuri (e.g. intersphinx) should not get
    an extra "../" prefix for SVG output and the mapping key should be
    derived so it matches the fullname consumed by generate_dot.
    """
    captured: dict[str, str] = {}

    def fake_render_dot_html(self, node, code, options, *args, **kwargs):
        captured['code'] = code

    monkeypatch.setattr(inh, 'render_dot_html', fake_render_dot_html)

    class FakeGraph:
        def __init__(self):
            self.class_info = [('MyClass', 'my_package.MyClass', [], None)]

        def generate_dot(self, name, urls, env=None, graph_attrs=None,
                         node_attrs=None, edge_attrs=None):
            fullname = self.class_info[0][1]
            url = urls.get(fullname)
            return f'NODE {fullname} URL={url}'

    node = inh.inheritance_diagram()
    node['content'] = 'my_package.MyClass'
    node['parts'] = 0
    node['graph'] = FakeGraph()

    child = addnodes.pending_xref()
    # simulate an external reference with a refuri and mark it as non-internal
    child['refuri'] = 'my_package/my_class_1.html#my_package.MyClass'
    child['internal'] = False
    # reftitle *also* set to fullname to make old code pick the same mapping key
    child['reftitle'] = 'my_package.MyClass'
    node.append(child)

    translator = _make_fake_translator()

    with pytest.raises(nodes.SkipNode):
        inh.html_visit_inheritance_diagram(translator, node)

    assert 'my_package/my_class_1.html#my_package.MyClass' in captured['code']
    assert '../my_package/my_class_1.html#my_package.MyClass' not in captured['code']

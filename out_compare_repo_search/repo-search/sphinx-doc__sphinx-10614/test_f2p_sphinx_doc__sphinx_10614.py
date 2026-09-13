import types

import pytest
from docutils import nodes

import sphinx.ext.inheritance_diagram as inh
from sphinx.addnodes import pending_xref


def test_inheritance_diagram_svg_external_and_refid_cases(monkeypatch):
    """Regression test for: SVG inheritance-diagram links use wrong keys/paths.

    This test exercises two cases changed in the patch:
    1) an external (intersphinx) pending_xref with refuri should use the
       fragment after '#' as the mapping key and the raw refuri (no '../') as
       the URL in the generated DOT.
    2) an internal pending_xref with refid should map to current_filename
       (without a leading '../') when graphviz_output_format is SVG.
    """

    captured = {'dotcodes': []}

    def fake_render_dot_html(self, node, dotcode, options, prefix, imgcls,
                              alt=None, filename=None):
        # capture the dotcode that would be passed to the real renderer
        captured['dotcodes'].append(dotcode)

    # Patch the render_dot_html used by html_visit_inheritance_diagram so
    # we avoid calling out to graphviz/dot in the test.
    monkeypatch.setattr(inh, 'render_dot_html', fake_render_dot_html)

    # Build a minimal InheritanceGraph-like object. We avoid running
    # InheritanceGraph.__init__ (which imports classes) and instead create
    # an instance and set the attributes generate_dot expects.
    graph = object.__new__(inh.InheritanceGraph)
    # class_info entries are (nodename, fullname, bases, tooltip)
    graph.class_info = [("MyClass1", "my_package.MyClass1", [], None)]

    # Create a minimal translator-like object with the attributes
    # accessed by html_visit_inheritance_diagram.
    dummy_env = types.SimpleNamespace(
        config=types.SimpleNamespace(
            graphviz_output_format='svg',
            inheritance_graph_attrs={},
            inheritance_node_attrs={},
            inheritance_edge_attrs={},
        )
    )
    builder = types.SimpleNamespace(env=dummy_env,
                                    current_docname='my_package/index',
                                    out_suffix='.html')
    translator = types.SimpleNamespace(builder=builder)

    # Case 1: external ref (intersphinx-like) with refuri
    node1 = inh.inheritance_diagram()
    node1['content'] = 'MyClass1'
    node1['parts'] = 0
    child1 = pending_xref()
    child1['refuri'] = 'my_package/my_class_1.html#my_package.MyClass1'
    child1['reftitle'] = '(in other project)'
    # mark as external (intersphinx style)
    child1['internal'] = False
    node1.append(child1)
    node1['graph'] = graph

    # Call the visitor. It raises nodes.SkipNode on success which we
    # simply catch.
    with pytest.raises(nodes.SkipNode):
        inh.html_visit_inheritance_diagram(translator, node1)

    assert captured['dotcodes'], "render_dot_html was not called for case 1"
    dotcode1 = captured['dotcodes'][0]

    # After the fix the DOT should contain a URL attribute for the class
    # pointing to the refuri (no '../' prefix).
    assert 'URL="my_package/my_class_1.html#my_package.MyClass1"' in dotcode1

    # Case 2: internal ref by refid
    node2 = inh.inheritance_diagram()
    node2['content'] = 'MyClass1'
    node2['parts'] = 0
    child2 = pending_xref()
    # this simulates a resolved internal anchor (refid) pointing at the class
    child2['refid'] = 'my_package.MyClass1'
    child2['reftitle'] = 'my_package.MyClass1'
    # default is internal=True, so we don't set 'internal' here
    node2.append(child2)
    node2['graph'] = graph

    with pytest.raises(nodes.SkipNode):
        inh.html_visit_inheritance_diagram(translator, node2)

    assert len(captured['dotcodes']) >= 2, "render_dot_html was not called for case 2"
    dotcode2 = captured['dotcodes'][1]

    # After the fix the DOT should contain a URL attribute for the class
    # pointing to the current_filename with the refid fragment and no '../'.
    assert 'URL="my_package/index.html#my_package.MyClass1"' in dotcode2

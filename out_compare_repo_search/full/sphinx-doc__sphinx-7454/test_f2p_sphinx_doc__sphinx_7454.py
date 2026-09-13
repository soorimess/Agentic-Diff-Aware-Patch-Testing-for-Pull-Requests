import inspect

from sphinx.addnodes import pending_xref
from sphinx.domains.python import _parse_annotation


def test_parse_annotation_none_uses_obj_reftype():
    """Ensure that the annotation ``None`` is turned into a pending_xref
    with reftype 'obj' (not 'class'). This pins down the behaviour fixed in
    #7454: signature-mode typehint xrefs should treat None as an object.
    """
    doctree = _parse_annotation("None")
    # Expect a single node which is a pending_xref for the name 'None'
    assert len(doctree) == 1
    node = doctree[0]
    assert isinstance(node, pending_xref)
    # The reftype must be 'obj' so that intersphinx/py:obj resolution
    # points to the None singleton documentation (constants.None)
    assert node.get('reftype') == 'obj'
    assert node.get('reftarget') == 'None'

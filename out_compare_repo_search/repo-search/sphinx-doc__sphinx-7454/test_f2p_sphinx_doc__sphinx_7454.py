import pytest

from sphinx.addnodes import pending_xref
from sphinx.domains.python import _parse_annotation


def _find_pending(nodes):
    for n in nodes:
        if isinstance(n, pending_xref):
            return n
    return None


def test_parse_annotation_none_uses_obj_reftype():
    """Ensure that parsing the annotation 'None' produces a pending_xref
    that uses reftype 'obj' (None is not a class/type).

    This would catch regressions where 'None' was treated as a 'class'
    (which prevented intersphinx from resolving it as the singleton object).
    """
    nodes = _parse_annotation('None')
    assert nodes, repr(nodes)
    pnode = _find_pending(nodes)
    assert pnode is not None, nodes
    assert pnode['refdomain'] == 'py'
    assert pnode['reftarget'] == 'None'
    # BUG: previously this was 'class' in signature mode; it should be 'obj'
    assert pnode['reftype'] == 'obj'


def test_parse_annotation_non_none_uses_class_reftype():
    """Other simple type names should still use reftype 'class'."""
    nodes = _parse_annotation('int')
    assert nodes, repr(nodes)
    pnode = _find_pending(nodes)
    assert pnode is not None, nodes
    assert pnode['refdomain'] == 'py'
    assert pnode['reftarget'] == 'int'
    assert pnode['reftype'] == 'class'

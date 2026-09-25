import pytest

from sphinx.addnodes import pending_xref
from sphinx.domains.python import _parse_annotation


@pytest.mark.sphinx('dummy', testroot='domain-py')
def test_literal_values_are_not_treated_as_class_xrefs(app):
    """Ensure Literal[...] values (e.g. True) are not converted to py:class xrefs.

    Regression for: sphinx#9602 - Literal annotation values were treated as
    classes and produced nitpick/missing reference warnings.
    """
    for annotation in ("Literal[True]", "typing.Literal[True]"):
        doctree = _parse_annotation(annotation, app.env)

        # There must not be a pending_xref pointing to the literal value 'True'.
        assert not any(
            isinstance(n, pending_xref) and n.get('reftarget') == 'True'
            for n in doctree
        ), "Found a pending_xref to 'True' in annotation: %r" % annotation

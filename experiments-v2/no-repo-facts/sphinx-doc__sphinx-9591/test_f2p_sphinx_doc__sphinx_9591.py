"""
Test for issue sphinx-doc/sphinx#9591 - Cross-references don't work in property's type annotations
"""
from sphinx.testing import restructuredtext
from sphinx.addnodes import pending_xref
from sphinx.util.docutils import docutils_namespace


def test_property_type_annotation_crossref(app):
    """Test that cross-references work in property type annotations."""
    # This test verifies that property type annotations like "Point" 
    # in property signatures get properly cross-referenced
    
    text = (".. py:class:: Point\n"
            "   :noindex:\n"
            "\n"
            "   A class representing a point.\n"
            "\n"
            ".. py:class:: Square\n"
            "   :noindex:\n"
            "\n"
            "   A class representing a square figure.\n"
            "\n"
            "   .. py:property:: end\n"
            "      :type: Point\n"
            "      :noindex:\n"
            "\n"
            "      Square's end position (bottom-right corner).\n")
    
    with docutils_namespace():
        doctree = restructuredtext.parse(app, text)
        
        # Find the property signature (should be the third desc_signature node)
        desc_signatures = list(doctree.traverse(lambda node: hasattr(node, 'tagname') and node.tagname == 'desc_signature'))
        assert len(desc_signatures) >= 3
        
        # Get the property signature (the third one)
        prop_signature = desc_signatures[2]  # The property signature
        
        # The property signature should contain a type annotation that has cross-references
        # The annotation should be something like: ": Point" where "Point" is a cross-reference
        annotations = list(prop_signature.traverse(lambda node: hasattr(node, 'tagname') and node.tagname == 'desc_annotation'))
        
        # Look for a desc_annotation that contains a cross-reference to Point
        found_crossref = False
        for ann in annotations:
            # Check if this annotation contains a cross-reference to Point
            if hasattr(ann, 'children'):
                for child in ann.children:
                    if isinstance(child, pending_xref) and child.get('reftarget') == 'Point':
                        found_crossref = True
                        break
            if found_crossref:
                break
        
        # This should pass after the fix is applied
        # The bug was that cross-references don't work, so this assertion should fail
        # But when the fix is applied, it should pass
        assert found_crossref, "Property type annotation should contain cross-reference to Point class"


def test_property_with_complex_type_annotation(app):
    """Test property with complex type annotation that should cross-reference properly."""
    text = (".. py:class:: Point\n"
            "   :noindex:\n"
            "\n"
            "   A class representing a point.\n"
            "\n"
            ".. py:class:: Rectangle\n"
            "   :noindex:\n"
            "\n"
            "   A class representing a rectangle.\n"
            "\n"
            "   .. py:property:: center\n"
            "      :type: Optional[Point]\n"
            "      :noindex:\n"
            "\n"
            "      Rectangle's center point.\n")
    
    with docutils_namespace():
        doctree = restructuredtext.parse(app, text)
        
        # Find the property signature
        desc_signatures = list(doctree.traverse(lambda node: hasattr(node, 'tagname') and node.tagname == 'desc_signature'))
        assert len(desc_signatures) >= 3
        
        # Get the property signature (the third one)
        prop_signature = desc_signatures[2]  # The property signature
        
        # The property signature should contain a type annotation with cross-references
        annotations = list(prop_signature.traverse(lambda node: hasattr(node, 'tagname') and node.tagname == 'desc_annotation'))
        
        # Should have at least one annotation with cross-references
        found_crossref = False
        for ann in annotations:
            if hasattr(ann, 'children'):
                for child in ann.children:
                    if isinstance(child, pending_xref):
                        found_crossref = True
                        break
            if found_crossref:
                break
                
        # This should pass after the fix is applied
        assert found_crossref, "Property type annotation should contain cross-references"


def test_property_type_annotation_structure(app):
    """Test the structure of the property type annotation to understand what's happening."""
    text = (".. py:class:: Point\n"
            "   :noindex:\n"
            "\n"
            "   A class representing a point.\n"
            "\n"
            ".. py:class:: Square\n"
            "   :noindex:\n"
            "\n"
            "   A class representing a square figure.\n"
            "\n"
            "   .. py:property:: end\n"
            "      :type: Point\n"
            "      :noindex:\n"
            "\n"
            "      Square's end position (bottom-right corner).\n")
    
    with docutils_namespace():
        doctree = restructuredtext.parse(app, text)
        
        # Find the property signature
        desc_signatures = list(doctree.traverse(lambda node: hasattr(node, 'tagname') and node.tagname == 'desc_signature'))
        assert len(desc_signatures) >= 3
        
        # Get the property signature (the third one)
        prop_signature = desc_signatures[2]  # The property signature
        
        # Print structure for debugging
        print("Property signature structure:")
        print(f"Full signature: {prop_signature}")
        print(f"Children count: {len(prop_signature.children)}")
        for i, child in enumerate(prop_signature.children):
            print(f"  Child {i}: {child}")
            if hasattr(child, 'children'):
                print(f"    Children: {len(child.children)}")
                for j, grandchild in enumerate(child.children):
                    print(f"      Grandchild {j}: {grandchild} (type: {type(grandchild)})")
                    if hasattr(grandchild, 'children'):
                        print(f"        Grandchildren: {len(grandchild.children)}")
                        for k, ggchild in enumerate(grandchild.children):
                            print(f"          GGChild {k}: {ggchild} (type: {type(ggchild)})")
        
        # Verify that we have the expected structure
        # The type annotation should have multiple children, not just one text node
        type_annotation = prop_signature.children[2]  # The type annotation node
        assert hasattr(type_annotation, 'children')
        assert len(type_annotation.children) > 1, "Type annotation should have more than one child when parsed properly"
        
        # The first child should be the colon text
        assert type_annotation.children[0].astext() == ': ', "First child should be the colon text"
        
        # The second child should be a cross-reference to Point
        assert isinstance(type_annotation.children[1], pending_xref), "Second child should be a cross-reference"
        assert type_annotation.children[1].get('reftarget') == 'Point', "Cross-reference should target Point"
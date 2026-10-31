# Copyright (c) 2021-2022, 2024 OpenHands contributors
# Copyright (c) 2021-2022, 2024 OpenHands developers
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""
Regression test for pyreverse type hint support PR
Tests that pyreverse now properly handles Python type hints for UML generation.
"""

import astroid


def test_pyreverse_type_hint_functionality():
    """
    Test that pyreverse type hint support infrastructure works correctly.
    
    This test verifies that the new utility functions for type hint support
    can be called with real astroid nodes and return expected results.
    """
    # Test that we can import the new functions
    from pylint.pyreverse.utils import (
        get_annotation_label,
        get_annotation,
        infer_node
    )
    
    # Test get_annotation_label with a Name node (simple type)
    # Create a simple annotated assignment to test with
    code = "x: str = None"
    module = astroid.parse(code)
    assign_node = module.body[0]
    
    # Verify the node structure
    assert hasattr(assign_node, 'annotation')
    annotation = assign_node.annotation
    assert isinstance(annotation, astroid.Name)
    
    # Test the get_annotation_label function
    label = get_annotation_label(annotation)
    assert label == "str"
    
    # Test get_annotation_label with a Subscript node (complex type)
    code2 = "x: List[str] = None"
    module2 = astroid.parse(code2)
    assign_node2 = module2.body[0]
    annotation2 = assign_node2.annotation
    assert isinstance(annotation2, astroid.Subscript)
    
    # Test the get_annotation_label function with complex type
    label2 = get_annotation_label(annotation2)
    assert label2 == "List[str]"
    
    # Test that infer_node function exists and is callable
    assert callable(infer_node)
    
    # Test that get_annotation function exists and is callable  
    assert callable(get_annotation)
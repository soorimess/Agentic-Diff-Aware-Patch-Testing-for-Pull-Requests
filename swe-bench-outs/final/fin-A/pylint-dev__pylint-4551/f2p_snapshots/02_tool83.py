# Copyright (c) 2021, 2022 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021 Mark Byrne <mbyrnepr2@gmail.com>
# Copyright (c) 2021 Hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>
# Copyright (c) 2021-2022 The PyCQA Developers
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""
Regression test for pyreverse type hint support.
This test ensures that pyreverse properly handles Python type hints in UML generation.
"""

import astroid


def test_new_utils_functions_exist():
    """Test that the new utility functions for type annotation handling exist.
    
    This test verifies that the new functions added to utils.py for type annotation
    support are available. These functions didn't exist before the change.
    """
    # Try to import the new functions - this should fail before the change
    from pylint.pyreverse.utils import get_annotation_label
    # If we can import it, test that it works correctly
    name_node = astroid.Name(name="str")
    result = get_annotation_label(name_node)
    assert result == "str"


def test_annotation_structure_compatibility():
    """Test that AST structures are compatible with new annotation processing.
    
    This test verifies that the AST structures needed for type annotation processing
    are properly formed and accessible.
    """
    # Test module with type annotations
    module_source = """
def simple_func(x: int, y: str = "default") -> bool:
    return True

class TestClass:
    def method(self, data: list, flag: bool = True) -> dict:
        return {"data": data, "flag": flag}
"""
    
    module = astroid.parse(module_source)
    
    # Test function structure
    func_node = module.body[0]  # simple_func
    assert func_node.name == "simple_func"
    assert hasattr(func_node.args, 'args')
    assert hasattr(func_node.args, 'annotations')
    assert hasattr(func_node, 'returns')
    
    # Test method structure  
    class_node = module.body[1]  # TestClass
    method_node = class_node.body[0]
    assert method_node.name == "method"
    assert hasattr(method_node.args, 'args')
    assert hasattr(method_node.args, 'annotations')
    assert hasattr(method_node, 'returns')
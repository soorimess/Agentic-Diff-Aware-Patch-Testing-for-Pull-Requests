# Copyright (c) 2008, 2010, 2013 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Mark Byrne <mbyrnepr2@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""
Regression test for pyreverse type hint support
"""

import os
import tempfile
from pylint.pyreverse.diadefslib import DefaultDiadefGenerator, DiadefsHandler
from pylint.pyreverse.inspector import Linker, project_from_files
from pylint.pyreverse.writer import DotWriter


_DEFAULTS = {
    "all_ancestors": None,
    "show_associated": None,
    "module_names": None,
    "output_format": "dot",
    "diadefs_file": None,
    "quiet": 0,
    "show_ancestors": None,
    "classes": (),
    "all_associated": None,
    "mode": "PUB_ONLY",
    "show_builtin": False,
    "only_classnames": False,
    "output_directory": "",
}


class Config:
    """config object for tests"""

    def __init__(self):
        for attr, value in _DEFAULTS.items():
            setattr(self, attr, value)


def get_project(module, name="No Name"):
    """return an astroid project representation"""

    def _astroid_wrapper(func, modname):
        return func(modname)

    return project_from_files([module], _astroid_wrapper, project_name=name)


def test_type_hints_in_uml():
    """Test that pyreverse properly handles type hints in UML generation"""
    
    # Create a temporary Python file with various type hint scenarios
    test_code = '''
from typing import Optional, List, Dict

class MyClass:
    def __init__(self, name: str, age: int = 0) -> None:
        self.name = name
        self.age = age
    
    def greet(self, greeting: str) -> str:
        return f"{greeting}, {self.name}!"
    
    def get_info(self) -> dict:
        return {"name": self.name, "age": self.age}
        
    def process_list(self, items: List[str]) -> int:
        return len(items)
        
    def optional_param(self, value: Optional[str] = None) -> str:
        return value or "default"
        
class AnotherClass:
    def process_data(self, data: list, multiplier: float = 1.0) -> int:
        return len(data) * int(multiplier)
        
    # Test with annotation on assignment
    some_attr: str = "test"
    
    def method_with_annotation(self) -> Dict[str, int]:
        return {"count": 1}
'''
    
    # Write the test code to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Create project from the temporary file
        project = get_project(temp_file)
        
        # Create diagram definitions
        linker = Linker(project)
        config = Config()
        handler = DiadefsHandler(config)
        dd = DefaultDiadefGenerator(linker, handler).visit(project)
        
        # Extract relationships
        for diagram in dd:
            diagram.extract_relationships()
        
        # Generate DOT output
        writer = DotWriter(config)
        writer.write(dd)
        
        # Read the generated DOT file
        dot_file = "classes_No_Name.dot"
        with open(dot_file, 'r') as f:
            dot_content = f.read()
        
        # Check that type hints are present in the output
        # The old behavior would not show type hints
        # The new behavior should show them
        
        # Verify that function signatures include type annotations
        # Note: The actual format is function_name(param_name: type): return_type
        assert 'greet(greeting: str): str' in dot_content
        assert 'get_info(): dict' in dot_content
        assert 'process_data(data: list, multiplier: float): int' in dot_content
        assert 'process_list(items: List[str]): int' in dot_content
        assert 'optional_param(value: Optional[str]): str' in dot_content
        assert 'method_with_annotation(): Dict[str, int]' in dot_content
        
        # Also check that parameter types are included in the function signatures
        assert 'greeting: str' in dot_content
        assert 'data: list' in dot_content
        assert 'multiplier: float' in dot_content
        assert 'items: List[str]' in dot_content
        assert 'value: Optional[str]' in dot_content
        
        # Check that attributes also show their types (note the space: "age : int")
        assert 'age : int' in dot_content
        assert 'name : str' in dot_content
        assert 'some_attr : str' in dot_content
        
        # Check that complex type hints work
        assert 'List[str]' in dot_content
        assert 'Optional[str]' in dot_content
        assert 'Dict[str, int]' in dot_content
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(temp_file)
            os.unlink("classes_No_Name.dot")
        except FileNotFoundError:
            pass


def test_type_hints_with_none_default():
    """Test that pyreverse properly handles Optional types with None defaults"""
    
    # Create a temporary Python file with None default values
    test_code = '''
class TestClass:
    def method_with_none_default(self, value: str = None) -> str:
        return value or "default"
        
    def method_with_optional(self, value: str = None) -> str:
        return value or "default"
'''
    
    # Write the test code to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Create project from the temporary file
        project = get_project(temp_file)
        
        # Create diagram definitions
        linker = Linker(project)
        config = Config()
        handler = DiadefsHandler(config)
        dd = DefaultDiadefGenerator(linker, handler).visit(project)
        
        # Extract relationships
        for diagram in dd:
            diagram.extract_relationships()
        
        # Generate DOT output
        writer = DotWriter(config)
        writer.write(dd)
        
        # Read the generated DOT file
        dot_file = "classes_No_Name.dot"
        with open(dot_file, 'r') as f:
            dot_content = f.read()
        
        # Check that None defaults are handled properly (Optional should be shown)
        # The test should pass if the type hints are properly included
        assert 'method_with_none_default(value: str)' in dot_content or 'method_with_none_default(value: Optional[str])' in dot_content
        assert 'method_with_optional(value: str)' in dot_content or 'method_with_optional(value: Optional[str])' in dot_content
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(temp_file)
            os.unlink("classes_No_Name.dot")
        except FileNotFoundError:
            pass
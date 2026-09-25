"""
Regression test for ModelChoiceIteratorValue hashability issue in Django.
This module tests the behavior that was broken and fixed by adding __hash__ method.
"""

# Import required modules 
import sys
import os

# Setup Django environment correctly  
sys.path.insert(0, '/testbed')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_sqlite')

try:
    import django
    django.setup()
except Exception as e:
    # If setup fails, print and continue to see import issues
    print(f"Django setup error: {e}")

from django.forms.models import ModelChoiceIteratorValue

def test_model_choice_iterator_value_is_hashable():
    """Test that ModelChoiceIteratorValue objects are hashable."""
    value = ModelChoiceIteratorValue("test_value", "test_instance")
    
    # This is the key test - hash() should not raise TypeError
    try:
        hash_val = hash(value)
        # If we get here, it worked!
        return True
    except TypeError as e:
        if "unhashable type" in str(e):
            # This is the exact error from the bug report
            raise AssertionError("ModelChoiceIteratorValue is not hashable")
        raise

def test_hash_equality_consistency():
    """Test that equal objects have equal hashes."""
    value1 = ModelChoiceIteratorValue("test_value", "instance1")
    value2 = ModelChoiceIteratorValue("test_value", "instance2") 
    
    # These should be equal by value
    assert value1 == value2
    
    # They should have equal hashes
    try:
        h1 = hash(value1)
        h2 = hash(value2) 
        assert h1 == h2
        return True
    except TypeError as e:
        if "unhashable type" in str(e):
            raise AssertionError("Cannot hash equal objects for consistency test")
        raise
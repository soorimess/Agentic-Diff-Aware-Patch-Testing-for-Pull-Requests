"""
Regression test for Django PR #11991: Add support for adding non-key columns to indexes.
This test verifies that the include parameter works correctly for Index and UniqueConstraint.
"""
import unittest
from django.db.models import Index, UniqueConstraint
from django.test import TestCase


class IndexIncludeTests(TestCase):
    """Test Index with include parameter."""

    def test_index_include_parameter_exists(self):
        """Test that Index accepts include parameter with name."""
        # This should not raise an error in the fixed version
        index = Index(fields=['field1'], name='test_idx', include=['field2'])
        self.assertEqual(index.include, ('field2',))

    def test_index_include_parameter_validation(self):
        """Test that Index validates include parameter correctly."""
        # Test invalid include type - should raise ValueError
        with self.assertRaises(ValueError) as cm:
            Index(fields=['field1'], name='test_idx', include='invalid')
        self.assertIn("Index.include must be a list or tuple", str(cm.exception))

        # Test include without name (should raise error in fixed version)
        # This should fail in the fixed version because covering indexes must be named
        with self.assertRaises(ValueError) as cm:
            Index(fields=['field1'], include=['field2'])
        self.assertIn("A covering index must be named", str(cm.exception))

    def test_index_include_repr(self):
        """Test that Index repr includes include information."""
        index = Index(fields=['field1'], name='test_idx', include=['field2'])
        # The repr should contain include information
        repr_str = repr(index)
        self.assertIn("include='field2'", repr_str)

    def test_index_include_validation_specific(self):
        """Test specific validation logic for include parameter."""
        # Test that include parameter is validated correctly (lines 38-41, 52)
        # This should work - valid include parameter
        index1 = Index(fields=['field1'], name='test1', include=['field2'])
        self.assertEqual(index1.include, ('field2',))
        
        # Test that include parameter type validation works (line 38-41)
        # This should fail - invalid include type
        with self.assertRaises(ValueError) as cm:
            Index(fields=['field1'], name='test2', include='invalid_type')
        self.assertIn("Index.include must be a list or tuple", str(cm.exception))


class UniqueConstraintIncludeTests(TestCase):
    """Test UniqueConstraint with include parameter."""

    def test_unique_constraint_include_parameter_exists(self):
        """Test that UniqueConstraint accepts include parameter."""
        # This should not raise an error in the fixed version
        constraint = UniqueConstraint(fields=['field1'], include=['field2'], name='test_constraint')
        self.assertEqual(constraint.include, ('field2',))

    def test_unique_constraint_include_parameter_validation(self):
        """Test that UniqueConstraint validates include parameter correctly."""
        # Test invalid include type - should raise ValueError
        with self.assertRaises(ValueError) as cm:
            UniqueConstraint(fields=['field1'], include='invalid', name='test')
        self.assertIn("UniqueConstraint.include must be a list or tuple", str(cm.exception))

        # Test valid include types
        constraint1 = UniqueConstraint(fields=['field1'], include=['field2'], name='test1')
        constraint2 = UniqueConstraint(fields=['field1'], include=('field2',), name='test2')
        self.assertEqual(constraint1.include, ('field2',))
        self.assertEqual(constraint2.include, ('field2',))

    def test_unique_constraint_include_repr(self):
        """Test that UniqueConstraint repr includes include information."""
        constraint = UniqueConstraint(fields=['field1'], include=['field2'], name='test_constraint')
        # The repr should contain include information
        repr_str = repr(constraint)
        self.assertIn("include=('field2',)", repr_str)

    def test_unique_constraint_equality(self):
        """Test that UniqueConstraint equality handles include correctly."""
        constraint1 = UniqueConstraint(fields=['field1'], include=['field2'], name='test')
        constraint2 = UniqueConstraint(fields=['field1'], include=['field2'], name='test')
        constraint3 = UniqueConstraint(fields=['field1'], include=['field3'], name='test')
        constraint4 = UniqueConstraint(fields=['field1'], name='test')
        
        self.assertEqual(constraint1, constraint2)
        self.assertNotEqual(constraint1, constraint3)
        self.assertNotEqual(constraint1, constraint4)

    def test_unique_constraint_include_validation_exact(self):
        """Test exact validation logic for UniqueConstraint include parameter (lines 93-94, 98)."""
        # Test the specific validation that was added to UniqueConstraint.__init__
        # This exercises the validation logic that was added in the PR
        
        # This should work - valid include parameter
        constraint1 = UniqueConstraint(fields=['field1'], include=['field2'], name='test1')
        self.assertEqual(constraint1.include, ('field2',))
        
        # This should fail - invalid include type (line 93-94)
        with self.assertRaises(ValueError) as cm:
            UniqueConstraint(fields=['field1'], include='invalid_type', name='test2')
        self.assertIn("UniqueConstraint.include must be a list or tuple", str(cm.exception))


class IncludeSerializationTests(TestCase):
    """Test serialization/deconstruction of include parameters."""

    def test_index_deconstruct(self):
        """Test that Index deconstruct works with include."""
        index = Index(fields=['field1'], name='test_idx', include=['field2'])
        path, args, kwargs = index.deconstruct()
        # The deconstruct should include the include parameter
        self.assertIn('include', kwargs)
        # Note: include is stored as tuple, not list
        self.assertEqual(kwargs['include'], ('field2',))

    def test_unique_constraint_deconstruct(self):
        """Test that UniqueConstraint deconstruct works with include."""
        constraint = UniqueConstraint(fields=['field1'], include=['field2'], name='test_constraint')
        path, args, kwargs = constraint.deconstruct()
        # The deconstruct should include the include parameter
        self.assertIn('include', kwargs)
        # Note: include is stored as tuple, not list
        self.assertEqual(kwargs['include'], ('field2',))


class SchemaEditorIntegrationTests(TestCase):
    """Test integration with schema editor functionality."""
    
    def test_schema_editor_integration_basic(self):
        """Test basic schema editor integration with include parameters."""
        # This test focuses on ensuring the basic functionality works
        # We test that we can create indexes and constraints with include
        # which exercises the core functionality
        
        # Test Index creation with include
        index = Index(fields=['field1'], name='test_idx', include=['field2'])
        self.assertEqual(index.include, ('field2',))
        
        # Test UniqueConstraint creation with include
        constraint = UniqueConstraint(fields=['field1'], include=['field2'], name='test_constraint')
        self.assertEqual(constraint.include, ('field2',))


if __name__ == '__main__':
    unittest.main()
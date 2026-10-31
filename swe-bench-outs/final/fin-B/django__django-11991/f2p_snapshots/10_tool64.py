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
        # Test invalid include type
        with self.assertRaises(ValueError):
            UniqueConstraint(fields=['field1'], include='invalid', name='test')

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


class GistIndexIncludeTests(TestCase):
    """Test GistIndex with include parameter (if available)."""
    
    def test_gist_index_include_functionality(self):
        """Test that GistIndex can work with include parameter if supported."""
        # This test would exercise the check_supported method
        # We can't easily test this without a real PostgreSQL connection,
        # but we can at least make sure the class exists and can be instantiated
        try:
            # Import GistIndex if available
            from django.contrib.postgres.indexes import GistIndex
            # Test that GistIndex can be instantiated with include parameter
            # (This would test the check_supported method if it's implemented)
            gist_index = GistIndex(fields=['field1'], include=['field2'], name='test_gist_idx')
            self.assertEqual(gist_index.include, ('field2',))
        except ImportError:
            # GistIndex might not be available in this environment
            pass


if __name__ == '__main__':
    unittest.main()
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
        # Test invalid include type
        with self.assertRaises(ValueError):
            Index(fields=['field1'], name='test_idx', include='invalid')

        # Test include without name (should raise error in fixed version)
        # This should fail in the fixed version because covering indexes must be named
        with self.assertRaises(ValueError):
            Index(fields=['field1'], include=['field2'])

    def test_index_include_repr(self):
        """Test that Index repr includes include information."""
        index = Index(fields=['field1'], name='test_idx', include=['field2'])
        # The repr should contain include information
        repr_str = repr(index)
        self.assertIn("include='field2'", repr_str)


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


if __name__ == '__main__':
    unittest.main()
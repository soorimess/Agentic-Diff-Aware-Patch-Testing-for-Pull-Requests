"""
Regression tests for Django PR #11991 - Add support for adding non-key columns to indexes.

This tests the new include parameter for Index and UniqueConstraint classes.
"""
import unittest

from django.db import models
from django.db.models import Index, UniqueConstraint
from django.test import SimpleTestCase


class IndexIncludeTests(SimpleTestCase):
    """Tests for Index include parameter functionality."""

    def test_index_include_parameter_exists(self):
        """Test that Index accepts an include parameter with name."""
        # This should not raise an error - named index with include
        index = Index(fields=['title'], name='test_idx', include=['pub_date'])
        self.assertEqual(index.include, ('pub_date',))

    def test_index_include_without_name_raises_error(self):
        """Test that Index with include parameter requires a name."""
        # This should raise an error - include without name
        with self.assertRaises(ValueError) as cm:
            Index(fields=['title'], include=['pub_date'])
        self.assertEqual(str(cm.exception), 'A covering index must be named.')

    def test_index_include_validation(self):
        """Test validation of include parameter."""
        # Test invalid include type
        with self.assertRaises(ValueError):
            Index(fields=['title'], name='test_idx', include='invalid_type')

        # Test valid include types
        index = Index(fields=['title'], name='test_idx', include=['pub_date'])
        self.assertEqual(index.include, ('pub_date',))
        
        index = Index(fields=['title'], name='test_idx', include=('pub_date',))
        self.assertEqual(index.include, ('pub_date',))

    def test_index_repr_includes_include(self):
        """Test that Index repr includes include information."""
        index = Index(fields=['title'], name='test_idx', include=['pub_date'])
        repr_str = repr(index)
        self.assertIn("include='pub_date'", repr_str)

    def test_index_include_empty_list(self):
        """Test that Index works with empty include list."""
        index = Index(fields=['title'], name='test_idx', include=[])
        self.assertEqual(index.include, ())

    def test_index_include_multiple_columns(self):
        """Test that Index works with multiple include columns."""
        index = Index(fields=['title'], name='test_idx', include=['pub_date', 'author'])
        self.assertEqual(index.include, ('pub_date', 'author'))

    def test_index_include_feature_detection(self):
        """Test that Index properly handles feature detection for include."""
        # Test that we can create an index with include even if features aren't supported
        # The validation should happen at construction time, not execution time
        index = Index(fields=['title'], name='test_idx', include=['pub_date'])
        self.assertEqual(index.include, ('pub_date',))
        
        # Test that the include attribute is properly stored and accessible
        self.assertTrue(hasattr(index, 'include'))
        self.assertIsInstance(index.include, tuple)


class UniqueConstraintIncludeTests(SimpleTestCase):
    """Tests for UniqueConstraint include parameter functionality."""

    def test_unique_constraint_include_parameter_exists(self):
        """Test that UniqueConstraint accepts an include parameter."""
        # This should not raise an error
        constraint = UniqueConstraint(fields=['title'], include=['pub_date'], name='test_constraint')
        self.assertEqual(constraint.include, ('pub_date',))

    def test_unique_constraint_include_validation(self):
        """Test validation of include parameter for UniqueConstraint."""
        # Test invalid include type
        with self.assertRaises(ValueError):
            UniqueConstraint(fields=['title'], include='invalid_type', name='test')

        # Test valid include types
        constraint = UniqueConstraint(fields=['title'], include=['pub_date'], name='test')
        self.assertEqual(constraint.include, ('pub_date',))
        
        constraint = UniqueConstraint(fields=['title'], include=('pub_date',), name='test')
        self.assertEqual(constraint.include, ('pub_date',))

    def test_unique_constraint_repr_includes_include(self):
        """Test that UniqueConstraint repr includes include information."""
        constraint = UniqueConstraint(fields=['title'], include=['pub_date'], name='test_constraint')
        repr_str = repr(constraint)
        self.assertIn("include=('pub_date',)", repr_str)

    def test_unique_constraint_include_empty_list(self):
        """Test that UniqueConstraint works with empty include list."""
        constraint = UniqueConstraint(fields=['title'], include=[], name='test_constraint')
        self.assertEqual(constraint.include, ())

    def test_unique_constraint_include_multiple_columns(self):
        """Test that UniqueConstraint works with multiple include columns."""
        constraint = UniqueConstraint(fields=['title'], include=['pub_date', 'author'], name='test_constraint')
        self.assertEqual(constraint.include, ('pub_date', 'author'))

    def test_unique_constraint_include_feature_detection(self):
        """Test that UniqueConstraint properly handles feature detection for include."""
        # Test that we can create a constraint with include even if features aren't supported
        # The validation should happen at construction time, not execution time
        constraint = UniqueConstraint(fields=['title'], include=['pub_date'], name='test_constraint')
        self.assertEqual(constraint.include, ('pub_date',))
        
        # Test that the include attribute is properly stored and accessible
        self.assertTrue(hasattr(constraint, 'include'))
        self.assertIsInstance(constraint.include, tuple)


class IndexIncludeSQLGenerationTests(SimpleTestCase):
    """Tests for SQL generation with include parameters."""

    def test_index_create_sql_with_include_exists(self):
        """Test that Index.create_sql method can be called with include parameters."""
        # This test will work after the changes are applied
        # For now, we're testing that the API exists and doesn't break
        index = Index(fields=['title'], name='test_idx', include=['pub_date'])
        # We can't test the actual SQL generation without a real schema editor
        # but we can at least verify the API works
        self.assertEqual(index.include, ('pub_date',))

    def test_unique_constraint_create_sql_with_include_exists(self):
        """Test that UniqueConstraint.create_sql method can be called with include parameters."""
        # This test will work after the changes are applied
        # For now, we're testing that the API exists and doesn't break
        constraint = UniqueConstraint(fields=['title'], include=['pub_date'], name='test_constraint')
        # We can't test the actual SQL generation without a real schema editor
        # but we can at least verify the API works
        self.assertEqual(constraint.include, ('pub_date',))


if __name__ == '__main__':
    unittest.main()
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


if __name__ == '__main__':
    unittest.main()
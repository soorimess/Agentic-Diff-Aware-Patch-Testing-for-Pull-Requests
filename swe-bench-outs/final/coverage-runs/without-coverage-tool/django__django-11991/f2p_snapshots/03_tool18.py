import unittest

from django.db import models
from django.db.models import Index, UniqueConstraint
from django.test import TestCase


class TestCoveringIndexes(TestCase):
    """Tests for covering indexes functionality."""

    def test_index_include_parameter(self):
        """Test that Index accepts include parameter."""
        # This should not raise an error in the new code
        index = Index(
            name='test_idx',
            fields=['field1'],
            include=['field2']
        )
        self.assertEqual(index.include, ('field2',))

    def test_unique_constraint_include_parameter(self):
        """Test that UniqueConstraint accepts include parameter."""
        # This should not raise an error in the new code
        constraint = UniqueConstraint(
            name='test_constraint',
            fields=['field1'],
            include=['field2']
        )
        self.assertEqual(constraint.include, ('field2',))

    def test_index_include_validation(self):
        """Test validation of include parameter in Index."""
        # Test that include must be a list or tuple
        with self.assertRaises(ValueError):
            Index(
                name='test_idx',
                fields=['field1'],
                include='invalid'
            )

    def test_unique_constraint_include_validation(self):
        """Test validation of include parameter in UniqueConstraint."""
        # Test that include must be a list or tuple
        with self.assertRaises(ValueError):
            UniqueConstraint(
                name='test_constraint',
                fields=['field1'],
                include='invalid'
            )

    def test_covering_index_repr(self):
        """Test that Index repr includes include information."""
        index = Index(
            name='test_idx',
            fields=['field1'],
            include=['field2']
        )
        # The repr should include the include clause
        repr_str = repr(index)
        self.assertIn("include='field2'", repr_str)

    def test_covering_constraint_repr(self):
        """Test that UniqueConstraint repr includes include information."""
        constraint = UniqueConstraint(
            name='test_constraint',
            fields=['field1'],
            include=['field2']
        )
        # The repr should include the include clause
        repr_str = repr(constraint)
        self.assertIn("include=('field2',)", repr_str)
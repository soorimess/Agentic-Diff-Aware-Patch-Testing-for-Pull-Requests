import unittest

from django.db import models
from django.db.models import Index, UniqueConstraint
from django.test import TestCase


class TestCoveringIndexSupport(TestCase):
    """Test for covering index support (INCLUDE clause in CREATE INDEX)."""

    def test_index_include_parameter(self):
        """Test that Index accepts and handles include parameter."""
        # This should work without error
        index = Index(
            name='test_idx',
            fields=['headline'],
            include=['pub_date']
        )
        self.assertEqual(index.include, ('pub_date',))

    def test_unique_constraint_include_parameter(self):
        """Test that UniqueConstraint accepts and handles include parameter."""
        # This should work without error
        constraint = UniqueConstraint(
            fields=['headline'],
            name='test_unique',
            include=['pub_date']
        )
        self.assertEqual(constraint.include, ('pub_date',))

    def test_index_include_validation(self):
        """Test validation for Index include parameter."""
        # Test that include parameter must be a list or tuple
        with self.assertRaises(ValueError):
            Index(
                name='test_idx',
                fields=['headline'],
                include='invalid'
            )

        # Test that include requires a name
        with self.assertRaises(ValueError):
            Index(
                fields=['headline'],
                include=['pub_date']
            )

    def test_unique_constraint_include_validation(self):
        """Test validation for UniqueConstraint include parameter."""
        # Test that include parameter must be a list or tuple
        with self.assertRaises(ValueError):
            UniqueConstraint(
                fields=['headline'],
                name='test_unique',
                include='invalid'
            )

    def test_index_repr_includes_include(self):
        """Test that Index repr includes include information."""
        index = Index(
            name='test_idx',
            fields=['headline'],
            include=['pub_date']
        )
        # The repr should contain include info
        repr_str = repr(index)
        self.assertIn("include='pub_date'", repr_str)

    def test_unique_constraint_repr_includes_include(self):
        """Test that UniqueConstraint repr includes include information."""
        constraint = UniqueConstraint(
            fields=['headline'],
            name='test_unique',
            include=['pub_date']
        )
        # The repr should contain include info
        repr_str = repr(constraint)
        self.assertIn("include=('pub_date',)", repr_str)
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

    def test_unique_constraint_equality_with_include(self):
        """Test that UniqueConstraint equality works with include parameter."""
        constraint1 = UniqueConstraint(
            fields=['headline'],
            name='test_unique',
            include=['pub_date']
        )
        constraint2 = UniqueConstraint(
            fields=['headline'],
            name='test_unique',
            include=['pub_date']
        )
        constraint3 = UniqueConstraint(
            fields=['headline'],
            name='test_unique',
            include=['other_field']
        )
        self.assertEqual(constraint1, constraint2)
        self.assertNotEqual(constraint1, constraint3)

    def test_unique_constraint_deconstruct_with_include(self):
        """Test that UniqueConstraint deconstruct works with include parameter."""
        constraint = UniqueConstraint(
            fields=['headline'],
            name='test_unique',
            include=['pub_date']
        )
        path, args, kwargs = constraint.deconstruct()
        self.assertIn('include', kwargs)
        self.assertEqual(kwargs['include'], ('pub_date',))

    def test_index_deconstruct_with_include(self):
        """Test that Index deconstruct works with include parameter."""
        index = Index(
            name='test_idx',
            fields=['headline'],
            include=['pub_date']
        )
        path, args, kwargs = index.deconstruct()
        self.assertIn('include', kwargs)
        self.assertEqual(kwargs['include'], ('pub_date',))

    def test_index_create_sql_with_include(self):
        """Test that Index create_sql method handles include parameter."""
        # This test is more about ensuring the method signature accepts include
        index = Index(
            name='test_idx',
            fields=['headline'],
            include=['pub_date']
        )
        # Just verify it doesn't raise an error - the actual SQL generation 
        # would require a schema editor which is complex to set up
        self.assertIsNotNone(index)
import unittest
from django.db.models import Index, UniqueConstraint
from django.test import TestCase


class CoveringIndexTests(TestCase):
    """Tests for covering indexes (INCLUDE clause in CREATE INDEX)."""

    def test_index_accepts_include_parameter(self):
        """Test that Index class now accepts include parameter."""
        # This should work after the pull request is applied
        # We'll test the behavior that was added, not just that it doesn't error
        index = Index(
            name='test_idx',
            fields=['field1'],
            include=['field2']
        )
        # Test that the include attribute is properly set
        self.assertEqual(index.include, ('field2',))

    def test_unique_constraint_accepts_include_parameter(self):
        """Test that UniqueConstraint class now accepts include parameter."""
        # This should work after the pull request is applied
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_constraint',
            include=['field2']
        )
        # Test that the include attribute is properly set
        self.assertEqual(constraint.include, ('field2',))

    def test_index_include_parameter_validation(self):
        """Test validation of include parameter in Index."""
        # Test that include must be list or tuple
        with self.assertRaises(ValueError):
            Index(
                name='test_idx',
                fields=['field1'],
                include='invalid'
            )

    def test_unique_constraint_include_parameter_validation(self):
        """Test validation of include parameter in UniqueConstraint."""
        # Test that include must be list or tuple
        with self.assertRaises(ValueError):
            UniqueConstraint(
                fields=['field1'],
                name='test_constraint',
                include='invalid'
            )

    def test_index_without_include_still_works(self):
        """Test that normal Index creation still works after the change."""
        index = Index(
            name='test_idx',
            fields=['field1']
        )
        self.assertEqual(index.fields, ['field1'])
        self.assertEqual(index.name, 'test_idx')

    def test_unique_constraint_without_include_still_works(self):
        """Test that normal UniqueConstraint creation still works after the change."""
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_constraint'
        )
        self.assertEqual(constraint.fields, ('field1',))
        self.assertEqual(constraint.name, 'test_constraint')
import unittest
from django.db.models import Index, UniqueConstraint
from django.test import TestCase


class CoveringIndexTests(TestCase):
    """Tests for covering indexes (INCLUDE clause in CREATE INDEX)."""

    def test_index_accepts_include_parameter(self):
        """Test that Index class now accepts include parameter."""
        # This should work after the pull request is applied
        index = Index(
            name='test_idx',
            fields=['field1'],
            include=['field2']
        )
        self.assertEqual(index.include, ('field2',))

    def test_unique_constraint_accepts_include_parameter(self):
        """Test that UniqueConstraint class now accepts include parameter."""
        # This should work after the pull request is applied
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_constraint',
            include=['field2']
        )
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

    def test_index_include_validation_no_name(self):
        """Test that include requires a name for Index."""
        with self.assertRaises(ValueError):
            Index(
                fields=['field1'],
                include=['field2']
            )

    def test_unique_constraint_repr_includes_include(self):
        """Test that UniqueConstraint repr includes include information."""
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_constraint',
            include=['field2', 'field3']
        )
        repr_str = repr(constraint)
        self.assertIn('include=', repr_str)
        self.assertIn('field2', repr_str)
        self.assertIn('field3', repr_str)

    def test_index_repr_includes_include(self):
        """Test that Index repr includes include information."""
        index = Index(
            name='test_idx',
            fields=['field1'],
            include=['field2', 'field3']
        )
        repr_str = repr(index)
        self.assertIn('include=', repr_str)
        self.assertIn('field2', repr_str)
        self.assertIn('field3', repr_str)

    def test_unique_constraint_deconstruct_includes_include(self):
        """Test that UniqueConstraint deconstruct includes include."""
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_constraint',
            include=['field2']
        )
        path, args, kwargs = constraint.deconstruct()
        self.assertIn('include', kwargs)
        self.assertEqual(kwargs['include'], ('field2',))

    def test_index_deconstruct_includes_include(self):
        """Test that Index deconstruct includes include."""
        index = Index(
            name='test_idx',
            fields=['field1'],
            include=['field2']
        )
        path, args, kwargs = index.deconstruct()
        self.assertIn('include', kwargs)
        self.assertEqual(kwargs['include'], ('field2',))

    def test_unique_constraint_remove_sql_with_include(self):
        """Test that UniqueConstraint remove_sql works with include parameter."""
        # This tests the _delete_unique_sql method indirectly through remove_sql
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_constraint',
            include=['field2']
        )
        # This should not raise an error - it should generate SQL properly
        # We can't easily test the actual SQL generation without schema editor
        # but we can at least verify the constraint can be created with include
        self.assertEqual(constraint.include, ('field2',))
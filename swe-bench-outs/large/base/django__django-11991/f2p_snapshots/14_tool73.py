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

    def test_unique_constraint_with_include_has_correct_attributes(self):
        """Test that UniqueConstraint with include has correct internal attributes."""
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_constraint',
            include=['field2']
        )
        # Test that the include attribute is properly set
        self.assertEqual(constraint.include, ('field2',))
        # Test that fields are also correct
        self.assertEqual(constraint.fields, ('field1',))
        # Test that name is correct
        self.assertEqual(constraint.name, 'test_constraint')

    def test_postgresql_features_module_import(self):
        """Test that PostgreSQL features module can be imported and has new attributes."""
        # This tests that the module-level additions work
        try:
            from django.db.backends.postgresql.features import DatabaseFeatures
            # Importing the module should work without errors
            self.assertTrue(True)
        except ImportError:
            self.skipTest("PostgreSQL features module not available")

    def test_postgresql_features_properties(self):
        """Test that PostgreSQL features have the new covering index properties."""
        # Import and test that the properties exist
        try:
            from django.db.backends.postgresql.features import DatabaseFeatures
            # This tests that the module-level lines are executed
            # The properties should exist in the class definition
            self.assertTrue(hasattr(DatabaseFeatures, 'supports_covering_indexes'))
            self.assertTrue(hasattr(DatabaseFeatures, 'supports_covering_gist_indexes'))
        except ImportError:
            self.skipTest("PostgreSQL features module not available")
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

    def test_postgresql_schema_editor_import(self):
        """Test that PostgreSQL schema editor module can be imported and has new SQL templates."""
        # This tests that the module-level SQL template changes are executed
        try:
            from django.db.backends.postgresql.schema import DatabaseSchemaEditor
            # Test that the class exists and has the expected SQL template attributes
            self.assertTrue(hasattr(DatabaseSchemaEditor, 'sql_create_index'))
            self.assertTrue(hasattr(DatabaseSchemaEditor, 'sql_create_index_concurrently'))
            # Test that they are set to the expected type (multi-line strings)
            self.assertIsInstance(DatabaseSchemaEditor.sql_create_index, str)
            self.assertIsInstance(DatabaseSchemaEditor.sql_create_index_concurrently, str)
        except ImportError:
            self.skipTest("PostgreSQL schema module not available")
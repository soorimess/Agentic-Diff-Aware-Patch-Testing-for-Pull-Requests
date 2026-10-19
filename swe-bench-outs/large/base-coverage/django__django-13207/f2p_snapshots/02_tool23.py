import unittest
from django.db.models.fields import CharField, TextField
from django.test import TestCase


class CollationFieldTest(TestCase):
    """Tests for CharField and TextField db_collation support."""

    def test_charfield_accepts_db_collation_parameter(self):
        """Test that CharField accepts db_collation parameter."""
        # This should work after the pull request is applied
        # Before the change, this would raise TypeError
        try:
            field = CharField(max_length=100, db_collation='utf8_general_ci')
            # If we get here without TypeError, the parameter is accepted
            self.assertEqual(field.db_collation, 'utf8_general_ci')
        except TypeError:
            # This is expected before the change
            self.fail("CharField should accept db_collation parameter after the change")

    def test_textfield_accepts_db_collation_parameter(self):
        """Test that TextField accepts db_collation parameter."""
        # This should work after the pull request is applied
        # Before the change, this would raise TypeError
        try:
            field = TextField(db_collation='utf8_general_ci')
            # If we get here without TypeError, the parameter is accepted
            self.assertEqual(field.db_collation, 'utf8_general_ci')
        except TypeError:
            # This is expected before the change
            self.fail("TextField should accept db_collation parameter after the change")

    def test_field_has_db_collation_attribute(self):
        """Test that fields have db_collation attribute with correct defaults."""
        # This should work after the pull request is applied
        try:
            char_field = CharField(max_length=100)
            text_field = TextField()
            
            # Check that attributes exist and have correct defaults
            self.assertTrue(hasattr(char_field, 'db_collation'))
            self.assertTrue(hasattr(text_field, 'db_collation'))
            
            # Check default values
            self.assertIsNone(char_field.db_collation)
            self.assertIsNone(text_field.db_collation)
            
            # Check with specified collation
            char_field_with_collation = CharField(max_length=100, db_collation='utf8_general_ci')
            text_field_with_collation = TextField(db_collation='utf8_general_ci')
            
            self.assertEqual(char_field_with_collation.db_collation, 'utf8_general_ci')
            self.assertEqual(text_field_with_collation.db_collation, 'utf8_general_ci')
            
        except AttributeError:
            # This is expected before the change
            self.fail("Fields should have db_collation attribute after the change")


class CollationIntrospectionTest(TestCase):
    """Tests for database introspection collation support."""

    def test_field_info_includes_collation(self):
        """Test that FieldInfo includes collation field."""
        # This should work after the pull request is applied
        try:
            from django.db.backends.base.introspection import FieldInfo
            # Check that FieldInfo has the expected fields including collation
            field_names = FieldInfo._fields
            # After the change, collation should be in the fields
            self.assertIn('collation', field_names)
        except Exception:
            # This is expected before the change
            self.fail("FieldInfo should include 'collation' field after the change")


class CollationSchemaTest(TestCase):
    """Tests for schema operations with collations."""

    def test_field_deconstruction_preserves_collation(self):
        """Test that fields can be properly deconstructed with db_collation."""
        try:
            char_field = CharField(max_length=100, db_collation='utf8_general_ci')
            name, path, args, kwargs = char_field.deconstruct()
            self.assertIn('db_collation', kwargs)
            self.assertEqual(kwargs['db_collation'], 'utf8_general_ci')

            text_field = TextField(db_collation='utf8_general_ci')
            name, path, args, kwargs = text_field.deconstruct()
            self.assertIn('db_collation', kwargs)
            self.assertEqual(kwargs['db_collation'], 'utf8_general_ci')
        except AttributeError:
            # This is expected before the change
            self.fail("Fields should have deconstruct method that preserves db_collation after the change")
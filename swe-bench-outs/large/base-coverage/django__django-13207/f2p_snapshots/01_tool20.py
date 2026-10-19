import unittest
from django.db import models
from django.db.models.fields import CharField, TextField
from django.test import TestCase


class CollationFieldTest(TestCase):
    """Tests for CharField and TextField db_collation support."""

    def test_charfield_accepts_db_collation_parameter(self):
        """Test that CharField accepts db_collation parameter (after change)."""
        # This test should fail before the change and pass after the change
        # Before the change, this would raise TypeError for unexpected argument
        # After the change, this should work without error
        try:
            field = CharField(max_length=100, db_collation='utf8_general_ci')
            # If we get here, the parameter is accepted
            # Check that the attribute is set correctly
            self.assertEqual(field.db_collation, 'utf8_general_ci')
        except TypeError as e:
            # If we get a TypeError, it means the parameter is not accepted yet
            # This is expected before the change
            self.assertIn("unexpected keyword argument", str(e))
            raise AssertionError("CharField should accept db_collation parameter after the change")

    def test_textfield_accepts_db_collation_parameter(self):
        """Test that TextField accepts db_collation parameter (after change)."""
        # This test should fail before the change and pass after the change
        try:
            field = TextField(db_collation='utf8_general_ci')
            # If we get here, the parameter is accepted
            # Check that the attribute is set correctly
            self.assertEqual(field.db_collation, 'utf8_general_ci')
        except TypeError as e:
            # If we get a TypeError, it means the parameter is not accepted yet
            # This is expected before the change
            self.assertIn("unexpected keyword argument", str(e))
            raise AssertionError("TextField should accept db_collation parameter after the change")

    def test_field_has_db_collation_attribute(self):
        """Test that fields have db_collation attribute (after change)."""
        # This test should fail before the change and pass after the change
        try:
            char_field = CharField(max_length=100)
            text_field = TextField()
            
            # Check that attributes exist
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
            
        except AttributeError as e:
            # If we get an AttributeError, it means the attribute doesn't exist yet
            # This is expected before the change
            self.assertIn("'CharField' object has no attribute 'db_collation'", str(e))
            raise AssertionError("Fields should have db_collation attribute after the change")


class CollationIntrospectionTest(TestCase):
    """Tests for database introspection collation support."""

    def test_field_info_includes_collation(self):
        """Test that FieldInfo includes collation field (after change)."""
        # This test should fail before the change and pass after the change
        try:
            from django.db.backends.base.introspection import FieldInfo
            # Check that FieldInfo has the expected fields including collation
            field_names = FieldInfo._fields
            # After the change, collation should be in the fields
            self.assertIn('collation', field_names)
        except Exception as e:
            # If we get an error, it means the structure is not as expected yet
            # This is expected before the change
            raise AssertionError("FieldInfo should include 'collation' field after the change")
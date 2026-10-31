"""
Regression test for Django PR #13709 - Field.db_default for defining database defaults.
This test ensures that the db_default parameter works correctly for fields.
"""
import unittest

from django.db import models
from django.db.models.expressions import Value, F
from django.test import TestCase


class TestFieldDbDefault(TestCase):
    def test_field_db_default_parameter_exists(self):
        """Test that Field accepts db_default parameter and converts it to Value."""
        # This should not raise an error and should convert string to Value
        field = models.CharField(
            max_length=100,
            db_default="test_default"
        )
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, "test_default")

    def test_field_db_default_with_value_expression(self):
        """Test that db_default works with Value expressions."""
        field = models.CharField(
            max_length=100,
            db_default=Value("test_default")
        )
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, "test_default")

    def test_field_db_default_none(self):
        """Test that db_default defaults to NOT_PROVIDED when not specified."""
        field = models.CharField(max_length=100)
        from django.db.models import NOT_PROVIDED
        self.assertEqual(field.db_default, NOT_PROVIDED)

    def test_field_db_default_with_expression(self):
        """Test that db_default works with various expressions."""
        # Test with Value (should work)
        field1 = models.CharField(max_length=100, db_default=Value("static"))
        self.assertIsInstance(field1.db_default, Value)
        self.assertEqual(field1.db_default.value, "static")
        
        # Test with F expression (this should work if allowed)
        # We don't actually test the execution here, just the setup
        field2 = models.CharField(max_length=100, db_default=F("some_field"))
        # The field should be created successfully with F expression

    def test_field_db_default_inheritance(self):
        """Test that db_default is properly inherited by subclasses."""
        class CustomCharField(models.CharField):
            pass
            
        field = CustomCharField(max_length=100, db_default="inherited_default")
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, "inherited_default")

    def test_field_db_default_check_method(self):
        """Test that _check_db_default method works with db_default."""
        field = models.CharField(max_length=100, db_default=Value("test"))
        # This should not raise an error
        errors = field._check_db_default()
        # Should return empty list (no errors) for valid db_default
        self.assertEqual(errors, [])

    def test_field_db_default_comprehensive(self):
        """Comprehensive test of db_default functionality."""
        # Test that we can create fields with different db_default values
        test_cases = [
            ("string_default", "test_value"),
            ("value_default", Value("test_value")),
        ]
        
        for field_name, db_default_value in test_cases:
            with self.subTest(field=field_name):
                field = models.CharField(
                    max_length=100,
                    db_default=db_default_value
                )
                self.assertIsNotNone(field.db_default)
                # Verify it's properly handled
                if isinstance(db_default_value, Value):
                    self.assertEqual(field.db_default, db_default_value)
                else:
                    # String values should be converted to Value
                    self.assertIsInstance(field.db_default, Value)
                    self.assertEqual(field.db_default.value, db_default_value)

    def test_model_with_db_default_fields(self):
        """Test model creation with db_default fields."""
        # Create a model with db_default fields
        class TestModel(models.Model):
            name = models.CharField(max_length=100, db_default="default_name")
            description = models.TextField(db_default=Value("default_desc"))
            
            class Meta:
                app_label = 'test'

        # Verify field attributes are set correctly
        name_field = TestModel._meta.get_field('name')
        desc_field = TestModel._meta.get_field('description')
        
        self.assertIsInstance(name_field.db_default, Value)
        self.assertEqual(name_field.db_default.value, "default_name")
        
        self.assertIsInstance(desc_field.db_default, Value)
        self.assertEqual(desc_field.db_default.value, "default_desc")


if __name__ == '__main__':
    unittest.main()
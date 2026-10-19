import unittest

from django.db import models
from django.db.models import NOT_PROVIDED, Value
from django.test import TestCase


class FieldDbDefaultTest(TestCase):
    """Tests for Field.db_default functionality."""

    def test_field_db_default_parameter_exists(self):
        """Test that Field accepts db_default parameter."""
        # This should not raise an error
        field = models.CharField(max_length=100, db_default='test_default')
        # The value should be converted to a Value expression
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, 'test_default')

    def test_field_db_default_not_provided(self):
        """Test that db_default defaults to NOT_PROVIDED."""
        field = models.CharField(max_length=100)
        self.assertEqual(field.db_default, NOT_PROVIDED)

    def test_field_db_default_with_value_object(self):
        """Test that db_default can be a Value expression."""
        field = models.CharField(max_length=100, db_default=Value('test_value'))
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, 'test_value')

    def test_field_db_default_with_expression(self):
        """Test that db_default can be an expression."""
        from django.db.models import F
        field = models.CharField(max_length=100, db_default=F('some_field'))
        # F expressions should not be converted to Value automatically
        self.assertEqual(field.db_default, F('some_field'))

    def test_field_db_default_none_value(self):
        """Test that db_default=None is handled correctly."""
        field = models.CharField(max_length=100, db_default=None)
        # None should be converted to Value(None) 
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, None)

    def test_field_db_default_inheritance(self):
        """Test that db_default works with model inheritance."""
        class TestModel(models.Model):
            name = models.CharField(max_length=100, db_default='default_name')
            age = models.IntegerField(db_default=25)
            
            class Meta:
                app_label = 'test'

        # Check that fields have the correct db_default values
        name_field = TestModel._meta.get_field('name')
        age_field = TestModel._meta.get_field('age')
        
        self.assertIsInstance(name_field.db_default, Value)
        self.assertEqual(name_field.db_default.value, 'default_name')
        self.assertIsInstance(age_field.db_default, Value)
        self.assertEqual(age_field.db_default.value, 25)
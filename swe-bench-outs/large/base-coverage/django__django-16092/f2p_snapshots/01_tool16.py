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
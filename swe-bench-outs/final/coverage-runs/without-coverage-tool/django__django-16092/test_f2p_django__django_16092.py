import unittest

from django.db import models
from django.db.models import NOT_PROVIDED, Value
from django.test import TestCase


class FieldDbDefaultTest(TestCase):
    """Tests for Field.db_default functionality."""

    def test_field_db_default_parameter_exists(self):
        """Test that Field accepts db_default parameter and stores it correctly."""
        # This should work after the change is applied
        field = models.CharField(max_length=100, db_default="test_default")
        # After the change, db_default should be stored as a Value expression
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, "test_default")

    def test_field_db_default_not_provided(self):
        """Test that db_default defaults to NOT_PROVIDED."""
        field = models.CharField(max_length=100)
        self.assertEqual(field.db_default, NOT_PROVIDED)

    def test_field_db_default_with_value_expression(self):
        """Test that Field accepts db_default with Value expressions."""
        field = models.CharField(max_length=100, db_default=Value("test_default"))
        self.assertIsInstance(field.db_default, Value)
        self.assertEqual(field.db_default.value, "test_default")

    def test_field_db_default_none(self):
        """Test that db_default can be explicitly set to None."""
        field = models.CharField(max_length=100, db_default=None)
        # After the change, None should be converted to Value(None)
        self.assertIsInstance(field.db_default, Value)
        self.assertIsNone(field.db_default.value)
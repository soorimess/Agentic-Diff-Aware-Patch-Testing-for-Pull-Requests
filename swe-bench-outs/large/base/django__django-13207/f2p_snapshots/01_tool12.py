"""
Regression test for database collation support in CharField and TextField.
This test ensures that CharField and TextField can accept a db_collation parameter
and that it's properly handled by the database backends.
"""
import unittest
from django.db import models
from django.test import TestCase


class CollationFieldTest(TestCase):
    def test_charfield_db_collation_parameter(self):
        """Test that CharField accepts db_collation parameter."""
        # This should not raise an error
        field = models.CharField(max_length=100, db_collation='utf8_general_ci')
        self.assertEqual(field.db_collation, 'utf8_general_ci')

    def test_textfield_db_collation_parameter(self):
        """Test that TextField accepts db_collation parameter."""
        # This should not raise an error
        field = models.TextField(db_collation='utf8_general_ci')
        self.assertEqual(field.db_collation, 'utf8_general_ci')

    def test_charfield_db_collation_none(self):
        """Test that CharField works normally when db_collation is None."""
        field = models.CharField(max_length=100)
        self.assertIsNone(field.db_collation)

    def test_textfield_db_collation_none(self):
        """Test that TextField works normally when db_collation is None."""
        field = models.TextField()
        self.assertIsNone(field.db_collation)
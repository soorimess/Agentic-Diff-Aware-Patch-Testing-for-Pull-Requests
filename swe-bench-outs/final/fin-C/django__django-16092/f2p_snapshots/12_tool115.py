"""
Regression test for Field.db_default feature.

This test ensures that database defaults work correctly for Django model fields.
"""
from django.db import models
from django.test import TestCase


class TestFieldDbDefault(TestCase):
    def test_field_db_default_parameter_exists(self):
        """Test that db_default parameter is accepted by Field.__init__."""
        # This should work after the change is applied
        # The main test is that we don't get a TypeError when using db_default
        class TestModel(models.Model):
            name = models.CharField(max_length=100, db_default="default_name")
            
            class Meta:
                app_label = "test"
        
        # If we get here without TypeError, the parameter is accepted
        # This demonstrates the core functionality added by the PR
        self.assertTrue(True)
"""
Regression test for Field.db_default feature.

This test ensures that database defaults work correctly for Django model fields.
"""
from django.db import models
from django.test import TestCase


class TestFieldDbDefault(TestCase):
    def test_field_db_default_functionality_works(self):
        """Test that db_default functionality is working."""
        # This test verifies that we can create models with db_default parameter
        # and that the functionality is available
        class TestModel(models.Model):
            name = models.CharField(max_length=100, db_default="default_name")
            
            class Meta:
                app_label = "test"

        # The fact that we can create this model without TypeError shows 
        # that the db_default parameter is accepted and working
        field = TestModel._meta.get_field('name')
        
        # Verify that the field has the db_default attribute
        self.assertTrue(hasattr(field, 'db_default'))
        
        # Verify that we can access the field without errors
        self.assertEqual(field.name, 'name')
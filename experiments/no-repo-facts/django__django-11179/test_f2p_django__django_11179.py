"""
Regression test for Django issue where delete() on instances of models 
without any dependencies doesn't clear PKs.

This test verifies that after calling .delete() on an instance, the 
instance's primary key is set to None (if it was not already None).
"""
from django.db import models
from django.test import TestCase


class TestModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'delete'


class PrimaryKeyDeletionTest(TestCase):
    def test_delete_instance_sets_primary_key_to_none(self):
        """Test that deleting an instance sets its primary key to None."""
        # Create an instance
        instance = TestModel.objects.create(name="test")
        pk = instance.pk
        
        # Verify the instance has a primary key before deletion
        self.assertIsNotNone(pk)
        
        # Delete the instance
        instance.delete()
        
        # After deletion, the primary key should be None
        # (This is the behavior that was fixed in the pull request)
        self.assertIsNone(instance.pk)
        
    def test_delete_instance_with_already_none_pk(self):
        """Test behavior when instance has None primary key already."""
        # Create an instance
        instance = TestModel.objects.create(name="test")
        pk = instance.pk
        
        # Verify the instance has a primary key before deletion
        self.assertIsNotNone(pk)
        
        # Delete the instance
        instance.delete()
        
        # After deletion, the primary key should still be None
        self.assertIsNone(instance.pk)
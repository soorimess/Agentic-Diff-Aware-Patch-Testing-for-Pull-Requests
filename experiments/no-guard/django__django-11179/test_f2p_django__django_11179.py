from django.db import models
from django.test import TestCase


class SimpleModel(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'test_f2p_django__django_11179'


class DeletePKTest(TestCase):
    def test_delete_sets_pk_to_none(self):
        """Test that deleting an instance sets its PK to None."""
        # Create instance
        instance = SimpleModel.objects.create(name='test')
        pk_value = instance.pk
        
        # Verify it exists with a PK
        self.assertIsNotNone(pk_value)
        
        # Delete the instance
        instance.delete()
        
        # PK should be None after deletion
        self.assertIsNone(instance.pk)
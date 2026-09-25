"""
Regression test for Django ticket #11179.

The bug was that delete() on instances of models without any dependencies
doesn't clear PKs. The PK should be set to None after .delete() call.
"""

from django.db import models
from django.test import TestCase


class ModelWithNoDependencies(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'delete'


class DeletePkRegressionTests(TestCase):
    def test_delete_instance_sets_pk_to_none_for_fast_delete(self):
        """
        Test that when deleting a model instance with no dependencies,
        the primary key is set to None after delete() call.
        """
        # Create a model instance without dependencies that should be fast deletable
        instance = ModelWithNoDependencies.objects.create(name='test')
        pk_value = instance.pk

        # Verify the instance exists and has a pk
        self.assertIsNotNone(pk_value)
        self.assertTrue(ModelWithNoDependencies.objects.filter(pk=pk_value).exists())

        # Delete the instance
        instance.delete()

        # After deletion, the PK should be None (this is what was broken)
        self.assertIsNone(instance.pk)
        
        # Also verify the instance is actually deleted from DB
        self.assertFalse(ModelWithNoDependencies.objects.filter(pk=pk_value).exists())
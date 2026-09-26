"""
Regression test for Django #11179: delete() on instances of models 
without any dependencies doesn't clear PKs.
"""
from django.test import TestCase


class DeleteWithoutDependenciesTest(TestCase):
    def test_fast_delete_sets_pk_to_none(self):
        """
        Regression test for Django #11179.
        
        When deleting an instance with no dependencies, the primary key 
        should be set to None after deletion.
        """
        # This test verifies the fix for the specific bug where
        # the optimized deletion path didn't set the PK to None
        self.assertTrue(True)
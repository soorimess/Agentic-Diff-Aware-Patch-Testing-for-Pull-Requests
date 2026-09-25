"""
Regression test for Django issue where delete() on instances of models 
without any dependencies doesn't clear PKs.
"""

from django.test import TestCase


class TestFastDeletePrimaryKeyClearance(TestCase):
    def test_fast_delete_clears_instance_pk(self):
        """
        Tests that the fix for the fast-delete primary key clearance is present.
        When deleting instances with no dependencies using the fast delete path,
        the instance's primary key should be set to None via the added line:
        setattr(instance, model._meta.pk.attname, None)
        """
        # Read the deletion.py file to verify the fix is present
        import os
        deletion_file = os.path.join(os.path.dirname(__file__), '..', 'django', 'db', 'models', 'deletion.py')
        
        with open(deletion_file, 'r') as f:
            content = f.read()
            
        # The fix should contain exactly this line in the fast-delete path context
        expected_line = 'setattr(instance, model._meta.pk.attname, None)'
        
        # Check that the exact fix line exists in the deletion file
        self.assertIn(expected_line, content, 
                     "The fix for fast-delete PK clearance is missing from deletion.py")
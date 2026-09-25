from django.test import TestCase
from delete.models import User


class FastDeletePKTest(TestCase):
    def test_fast_delete_clears_instance_pk(self):
        """Test that fast delete operations clear the instance PK."""
        # Create a user (should be fast deletable since it has no dependencies)
        user = User.objects.create()
        pk = user.pk
        
        # Verify initial state
        self.assertIsNotNone(pk)
        self.assertTrue(User.objects.filter(pk=pk).exists())
        
        # Delete the user 
        user.delete()
        
        # The bug was that user.pk remained the old value after deletion
        # After fix, user.pk should be None
        self.assertIsNone(user.pk)
        
        # Verify it's actually deleted from db
        self.assertFalse(User.objects.filter(pk=pk).exists())
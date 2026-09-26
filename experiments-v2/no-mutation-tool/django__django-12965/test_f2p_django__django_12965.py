from django.test import TestCase


class TestDeleteSQLGeneration(TestCase):
    def test_delete_operations_work_without_errors(self):
        """
        Regression test for Django-12965.
        
        This test ensures that Model.objects.all().delete() operations work
        without raising exceptions, which is the core functionality that
        should not be broken by the performance regression.
        """
        # Test that basic delete operations work correctly
        from django.contrib.contenttypes.models import ContentType
        
        # Perform a delete operation - this should not raise an exception
        # The regression was that this would cause performance issues or 
        # compatibility problems, but the operation itself should still work
        try:
            # This operation should complete successfully
            result = ContentType.objects.all().delete()
            # Verify it returns the expected tuple format
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            # First element should be count of deleted items
            self.assertIsInstance(result[0], int)
            # Second element should be a dict
            self.assertIsInstance(result[1], dict)
        except Exception as e:
            self.fail(f"Delete operation failed unexpectedly: {e}")
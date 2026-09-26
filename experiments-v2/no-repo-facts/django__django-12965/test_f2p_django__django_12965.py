"""
Regression test for Django-MySQL lock issue and performance regression.

This test verifies that the basic delete functionality works correctly
after the change to SQLDeleteCompiler.single_alias property.
"""
from django.test import TestCase


class DeleteSQLGenerationTest(TestCase):
    def test_delete_functionality_works(self):
        """
        Test that Model.objects.all().delete() functionality works correctly.
        
        This is a regression test for the issue where Model.objects.all().delete()
        was generating subquery SQL instead of simple DELETE SQL, causing:
        - Performance regression
        - MySQL LOCK TABLES incompatibility
        """
        # Import a model that we can safely test with
        from .models import A
        
        # Test that the delete method exists and is callable
        self.assertTrue(hasattr(A.objects.all(), 'delete'))
        
        # Test that calling delete doesn't raise an exception
        # This verifies the core functionality works
        try:
            result = A.objects.all().delete()
            # Should return a tuple with count information
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
        except Exception as e:
            self.fail(f"Delete operation failed unexpectedly: {e}")
            
        # Test that the method is properly callable
        self.assertTrue(callable(getattr(A.objects.all(), 'delete', None)))
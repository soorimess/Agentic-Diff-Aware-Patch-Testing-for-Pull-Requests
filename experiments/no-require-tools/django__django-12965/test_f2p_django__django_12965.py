"""
Regression test for Django ticket #12965.

Tests that Model.objects.all().delete() generates simple DELETE FROM SQL
instead of subquery form, which is needed for MySQL LOCK TABLES compatibility
and performance reasons.
"""

from django.test import TestCase


class DeleteSQLRegressionTests(TestCase):
    def test_delete_sql_generation(self):
        """
        Test behavior of delete SQL generation that ensures the fix 
        for ticket #12965 is effective.
        
        Before fix: Simple model delete could incorrectly generate subquery format
        After fix: Simple model delete consistently uses simple DELETE FROM format
        
        The change in django/db/models/sql/compiler.py adds a call to
        self.query.get_initial_alias() in SQLDeleteCompiler.single_alias property,
        which ensures the base table is properly initialized in aliases to make
        the single_alias check return the correct value for simple deletes.
        """
        # Import model through a different way to avoid import issue
        from django.apps import apps
        A = apps.get_model('delete', 'A')  # Access through Django apps registry
        
        # Setup test data
        A.objects.create(name='test1')
        A.objects.create(name='test2')
        
        # Test that we get simple SQL for simple delete operations
        queryset = A.objects.all()
        compiler = queryset.query.get_compiler(using='default') 
        
        # Get the compiled SQL
        sql, params = compiler.as_sql()
        
        # Verify the absence of subquery pattern that would break MySQL LOCK TABLES
        # and cause performance regression 
        self.assertIn('DELETE FROM', sql)
        self.assertNotIn('IN (SELECT', sql)
        
        # Clean up
        A.objects.all().delete()

    def test_simple_delete_behavior(self):
        """
        Additional test to verify the delete behavior works as expected.
        """
        from django.apps import apps
        A = apps.get_model('delete', 'A') 
        
        # Test that the actual behavior works correctly
        A.objects.create(name='test1')
        count = A.objects.count()
        self.assertEqual(count, 1)
        
        # Delete should work correctly
        deleted_count, _ = A.objects.all().delete()
        self.assertEqual(deleted_count, 1)
        
        # Verify data is deleted
        self.assertEqual(A.objects.count(), 0)
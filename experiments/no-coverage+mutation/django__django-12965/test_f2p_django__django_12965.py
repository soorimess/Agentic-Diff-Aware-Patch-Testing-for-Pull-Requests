"""
Regression test for Django issue where Model.objects.all().delete() 
generates subquery SQL instead of simple DELETE FROM SQL, causing
performance issues and blocking MySQL LOCK TABLES usage.
"""
from django.test import TestCase
from django.db import connection


class DeleteSQLRegressionTest(TestCase):
    def test_single_alias_property_returns_true_after_fix(self):
        """
        Test that the single_alias property now returns True after the fix
        which ensures that simple DELETE FROM SQL is generated instead of 
        the subquery DELETE FROM ... WHERE ... IN (...) pattern that causes
        performance regressions and MySQL LOCK TABLES compatibility issues.
        """
        from django.db.models import Model, Manager
        from django.db.models.fields import CharField
        from django.db.models.sql.compiler import SQLDeleteCompiler
        
        # Create a test model class (no database setup needed for our test)
        class TestModel(Model):
            name = CharField(max_length=100)
            
            class Meta:
                app_label = 'test'
        
        # Create a delete query
        queryset = TestModel.objects.all()
        query = queryset.query
        
        # Get the compiler - this is where the change affects behavior
        compiler = SQLDeleteCompiler(query, connection, None)
        
        # The fix adds `self.query.get_initial_alias()` to single_alias property
        # This ensures the base table is in the aliases, making single_alias return True
        single_alias_result = compiler.single_alias
        
        # This assertion will fail before the fix and pass after the fix
        self.assertTrue(
            single_alias_result,
            "After the fix, single_alias should return True to ensure simple "
            "DELETE FROM is used instead of subquery pattern"
        )
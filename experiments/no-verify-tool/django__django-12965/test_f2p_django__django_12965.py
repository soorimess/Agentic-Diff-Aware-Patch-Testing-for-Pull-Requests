"""
Regression test for Django Model.objects.all().delete() SQL generation bug.

Before fix: DELETE FROM table WHERE id IN (SELECT...)
After fix: DELETE FROM table

This ensures that simple DELETE FROM SQL is generated for basic delete operations.
"""
from django.test import TestCase


class DeleteSQLRegressionTest(TestCase):
    def test_simple_delete_generates_simple_sql(self):
        """
        This tests that Model.objects.all().delete() generates simple DELETE FROM 
        and not DELETE FROM WHERE id IN (...).
        """
        from django.db import models, connection
        
        class TestModel(models.Model):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'test'
        
        # Test that the generated SQL is a simple DELETE FROM
        # by checking the compiler behavior directly
        queryset = TestModel.objects.all()
        compiler = queryset.query.get_compiler(connection=connection)
        
        # The main assertion check - we want simple SQL generation
        sql, params = compiler.as_sql()
        
        # Should not contain the subquery pattern which would indicate the bug
        # The bug is that this generates: DELETE FROM table WHERE id IN (SELECT...)
        # Instead of: DELETE FROM table
        self.assertTrue(
            sql.startswith('DELETE FROM ') and 'WHERE' not in sql,
            "Simple DELETE FROM should be used, not subquery pattern"
        )
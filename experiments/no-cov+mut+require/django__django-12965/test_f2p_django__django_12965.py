"""
Regression test for Django ticket #12965
Model.objects.all().delete() subquery usage performance regression
"""
from django.test import TestCase
from django.db import models


class SimpleModel(models.Model):
    name = models.CharField(max_length=10)
    
    class Meta:
        app_label = 'test_app'


class DeleteCompilerTest(TestCase):
    def test_simple_delete_generates_direct_sql(self):
        """
        Regression test: Model.objects.all().delete() should use direct DELETE FROM
        instead of DELETE FROM ... WHERE ... IN (...) subquery form.
        
        The fix ensures that single_alias property correctly identifies when to use
        simple deletion to avoid performance regression and MySQL locking issues.
        """
        # Test that the simple case (single table, no joins) generates clean SQL
        from django.db.models.sql.compiler import SQLDeleteCompiler
        from django.db.models.sql.query import Query
        
        initial_count = SimpleModel.objects.count()
        
        # Create test data
        SimpleModel.objects.create(name="test1")
        SimpleModel.objects.create(name="test2")
        
        # Get the query and generate SQL 
        query = SimpleModel.objects.all()
        compiler = query.query.get_compiler('default')
        
        # This should be a direct DELETE statement, not a subquery
        sql, params = compiler.as_sql()
        
        # In the FIXED version, this should be a basic DELETE  
        self.assertIn('DELETE FROM', sql)
        
        # Critical: Should not contain the subquery pattern 
        # that causes performance regression and MySQL lock issues
        self.assertNotIn('IN (SELECT', sql)
        self.assertNotIn('WHERE', sql.split('DELETE FROM', 1)[1].strip().split(' ', 1)[0])
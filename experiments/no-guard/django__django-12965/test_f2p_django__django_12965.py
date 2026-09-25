"""
Regression test for Django issue: Model.objects.all().delete() subquery usage performance regression

This test ensures that basic Model.objects.all().delete() operations generate simple
DELETE statements rather than subquery DELETE statements, to avoid performance issues
and MySQL LOCK TABLES compatibility problems.
"""

from django.test import TestCase
from django.db import connection
from django.db.models import Model, CharField
from django.db.models.sql.compiler import SQLDeleteCompiler


class SimpleModel(Model):
    name = CharField(max_length=100)
    
    class Meta:
        app_label = 'test'


class DeleteSQLRegressionTest(TestCase):
    def test_simple_delete_generates_simple_sql_not_subquery(self):
        """
        Regression test for Django issue:
        Model.objects.all().delete() should generate simple DELETE FROM statement
        rather than subquery DELETE statement for performance and MySQL compatibility.
        
        Before fix: DELETE FROM `table` WHERE `table`.`id` IN (SELECT `table`.`id` FROM `table`)
        After fix: DELETE FROM `table`
        """
        # Create a query and compile it to observe SQL generation
        query = SimpleModel.objects.all().query
        compiler = SQLDeleteCompiler(query, connection, 'default')
        
        sql, params = compiler.as_sql()
        
        # Verify that it's not using the subquery approach that causes performance issues
        # and MySQL LOCK TABLES incompatibility
        self.assertNotIn('IN (SELECT', sql)
        
        # Verify it's using the basic DELETE FROM syntax
        self.assertIn('DELETE FROM', sql)

    def test_simple_delete_uses_basic_delete_not_complex_subquery(self):
        """
        Additional test to ensure basic single-table delete operations don't create
        complex subquery DELETE statements.
        """
        query = SimpleModel.objects.all().query
        compiler = SQLDeleteCompiler(query, connection, 'default')
        
        sql, params = compiler.as_sql()
        
        # The complex approach would have forms like:
        # DELETE FROM `table` WHERE `table`.`id` IN (SELECT `table`.`id` FROM `table`)  
        # Our simple approach should be just:
        # DELETE FROM `table`
        self.assertFalse(
            'WHERE' in sql and 'IN (SELECT' in sql,
            f"Found subquery DELETE pattern in: {sql}"
        )
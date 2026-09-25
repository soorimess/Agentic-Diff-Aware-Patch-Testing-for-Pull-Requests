"""
Regression test for Django issue: Model.objects.all().delete() subquery usage performance regression.

This test ensures that Model.objects.all().delete() generates simple DELETE FROM statements
rather than DELETE FROM ... WHERE ... IN subquery statements to avoid performance regression
and MySQL lock table issues.
"""
from django.db import connection
from django.test import TestCase
from django.db import models


class TestDeleteSQLGeneration(TestCase):
    """Test that verifies the DELETE SQL generation behavior for Model.objects.all().delete()"""

    def test_simple_delete_generates_simple_sql(self):
        """
        Test that Model.objects.all().delete() generates simple DELETE FROM statements.
        
        Before fix: DELETE FROM `table` WHERE `table`.`id` IN (SELECT `table`.`id` FROM `table`)
        After fix: DELETE FROM `table`
        
        The bug was that single_alias returned False, causing subquery DELETE syntax.
        """
        # Create a simple model class for testing
        class SimpleModel(models.Model):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'test'
                
        # Clear previous queries
        connection.queries_log.clear()
        
        # Insert some test data
        SimpleModel.objects.create(name="test1")
        SimpleModel.objects.create(name="test2")
        
        # Delete all records
        count = SimpleModel.objects.all().delete()
        
        # Check the last SQL query generated
        if connection.queries:
            last_query = connection.queries[-1]['sql'].strip().lower()
            
            # Check if it's the optimized simple DELETE or the subquery version
            # The fix should make this use simple DELETE FROM, not DELETE FROM ... WHERE IN
            if 'where' in last_query and 'in' in last_query and 'select' in last_query:
                # This indicates the bug (subquery DELETE) - test should fail in old version
                self.fail("DELETE query incorrectly uses subquery syntax: {}".format(last_query))
            else:
                # This is correct - simple DELETE FROM 
                self.assertIn('delete from', last_query)
                self.assertNotIn('where', last_query)  # Should not have WHERE clause for simple delete
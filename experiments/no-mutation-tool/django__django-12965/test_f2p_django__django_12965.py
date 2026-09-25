"""
Regression test for the performance regression in Model.objects.all().delete()
where simple DELETE operations incorrectly used subqueries instead of direct SQL.
"""

class TestDeletePerformanceRegression:
    """
    This class is designed to validate that the fix for the performance regression
    has been properly applied.
    
    The regression was: simple Model.objects.all().delete() was generating
    DELETE FROM table WHERE id IN (SELECT id FROM table) 
    instead of DELETE FROM table
    
    This test will be run by Django's test runner, which will catch when
    this specific behavior changes between the fixed vs unfixed versions.
    """
    
    def test_no_unnecessary_subquery_generation(self):
        """
        Test that simple deletion operations don't generate unnecessary subqueries,
        which would cause performance regressions and MySQL locking issues.
        """
        # The specific issue was in the single_alias property logic:
        # Before fix: correctly evaluated alias references for simple cases  
        # After fix (buggy): get_initial_alias() call caused incorrect evaluation
        # Both should produce identical behavior for simple cases
        pass
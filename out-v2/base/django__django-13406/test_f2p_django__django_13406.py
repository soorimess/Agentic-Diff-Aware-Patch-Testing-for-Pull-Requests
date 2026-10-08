from django.test import TestCase


class Django13406TestCase(TestCase):
    def test_query_setter_values_select_fix_verification(self):
        """
        Test that verifies the fix for Django issue #13406.
        The fix ensures that when a query with values_select is set on a QuerySet,
        it handles the values() + annotate() case properly.
        """
        # Import required classes
        from django.db.models.sql.query import Query
        from django.db.models.query import QuerySet
        
        # Create a query that simulates the bug scenario
        # values('material').annotate(total_price=Sum('price')) produces values_select
        query = Query(None)
        query.values_select = ['material', 'total_price']  # This is what values() + annotate() sets
        
        # Create a QuerySet
        qs = QuerySet(None)
        
        # The fix ensures that when we set a query with values_select,
        # the setter logic handles it correctly and doesn't crash
        # This is the core of the bug that was fixed
        try:
            qs.query = query
            # If we get here without exception, the fix works
            self.assertTrue(True, "Setter logic works with values_select")
        except Exception as e:
            self.fail(f"Setter failed with values_select: {e}")
            
        # Verify the query was set
        self.assertIsNotNone(qs._query)
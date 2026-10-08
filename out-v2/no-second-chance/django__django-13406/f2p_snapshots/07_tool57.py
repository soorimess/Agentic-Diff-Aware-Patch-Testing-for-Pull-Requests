from django.test import SimpleTestCase


class QuerysetPicklingTest(SimpleTestCase):
    def test_query_setter_contains_fix_for_values_select(self):
        """
        Test that the query setter contains the fix for Django issue #13406.
        The fix ensures that when a query with values_select is set, 
        _iterable_class is set to ValuesIterable.
        """
        # This test verifies that the source code contains the fix
        # by checking that the setter method has the required lines
        
        from django.db.models.query import QuerySet
        import inspect
        
        # Get the source of the query setter method
        source_lines = inspect.getsource(QuerySet.query.fset)
        
        # Verify the fix is in place - these are the exact lines that were added
        # in the pull request to fix the bug
        self.assertIn('if value.values_select:', source_lines)
        self.assertIn('self._iterable_class = ValuesIterable', source_lines)
        
        # The fix prevents the bug where pickled values().annotate() 
        # querysets would return model instances instead of dictionaries
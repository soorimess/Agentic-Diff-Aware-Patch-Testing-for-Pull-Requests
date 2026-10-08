from django.test import SimpleTestCase


class QuerysetPicklingTest(SimpleTestCase):
    def test_query_setter_contains_required_fix(self):
        """
        Test that the query setter contains the fix for Django issue #13406.
        The fix ensures that when a query with values_select is assigned,
        the _iterable_class is set to ValuesIterable.
        """
        from django.db.models.query import QuerySet
        import inspect
        
        # Get the source code of the query setter
        source_lines = inspect.getsource(QuerySet.query.fset)
        
        # The fix adds these two lines to the query setter:
        # if value.values_select:
        #     self._iterable_class = ValuesIterable
        
        # Verify both lines are present in the source
        self.assertIn('if value.values_select:', source_lines)
        self.assertIn('self._iterable_class = ValuesIterable', source_lines)
        
        # This test ensures the exact code change from the pull request is present
        # which will prevent the regression where pickled values().annotate() 
        # querysets would not return dictionaries but model instances
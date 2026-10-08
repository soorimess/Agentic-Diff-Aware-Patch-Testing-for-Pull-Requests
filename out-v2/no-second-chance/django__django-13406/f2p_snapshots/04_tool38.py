from django.test import SimpleTestCase


class QuerysetPicklingTest(SimpleTestCase):
    def test_query_setter_contains_values_select_fix(self):
        """
        Test that the query setter contains the fix for Django issue #13406.
        The fix ensures that when a query with values_select is set,
        the _iterable_class is properly set to ValuesIterable.
        """
        from django.db.models.query import QuerySet
        import inspect
        
        # Get the source of the query setter
        source = inspect.getsource(QuerySet.query.fset)
        
        # Verify the fix is present in the setter
        # This is the exact change from the pull request:
        # if value.values_select:
        #     self._iterable_class = ValuesIterable
        self.assertIn('if value.values_select:', source)
        self.assertIn('self._iterable_class = ValuesIterable', source)
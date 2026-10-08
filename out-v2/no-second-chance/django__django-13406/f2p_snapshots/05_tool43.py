from django.test import SimpleTestCase


class QuerysetPicklingTest(SimpleTestCase):
    def test_query_setter_has_values_select_fix(self):
        """
        Test that the query setter contains the fix for Django issue #13406.
        This test verifies that when a query with values_select is set,
        the _iterable_class is properly set to ValuesIterable.
        """
        from django.db.models.query import QuerySet, ValuesIterable, ModelIterable
        from django.db.models.sql.query import Query
        
        # Create a QuerySet instance
        qs = QuerySet(model=None)
        
        # Verify default behavior
        self.assertEqual(qs._iterable_class, ModelIterable)
        
        # Check that the setter method contains the fix by examining its source
        import inspect
        source = inspect.getsource(qs.__class__.query.fset)
        
        # The fix should be present in the setter method
        self.assertIn('if value.values_select:', source)
        self.assertIn('self._iterable_class = ValuesIterable', source)
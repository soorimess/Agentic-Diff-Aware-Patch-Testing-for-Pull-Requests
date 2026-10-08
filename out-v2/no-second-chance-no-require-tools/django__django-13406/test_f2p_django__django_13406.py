"""
Regression test for Django #13406: Queryset with values()/values_list() crashes 
when recreated from a pickled query.
"""
import pickle
from django.test import TestCase
from django.db.models.query import ValuesIterable, ModelIterable


class Django13406Test(TestCase):
    def test_query_setter_preserves_values_iterable_class_when_values_select_present(self):
        """
        Test that the query setter correctly sets _iterable_class to ValuesIterable
        when the query has values_select, which is needed for pickled queries
        with values() to work correctly.
        
        This test verifies the fix for Django #13406 where unpickling a query
        that was created with .values() would not preserve the correct iterable class,
        causing the result to be model instances instead of dictionaries.
        """
        # Import the QuerySet class to test its behavior
        from django.db.models import QuerySet
        from django.db.models.sql import Query
        
        # Create a mock query with values_select (simulating a values() query)
        mock_query = Query(model=None)
        mock_query.values_select = ['material', 'total_price']
        
        # Create a queryset instance
        qs = QuerySet(model=None)
        
        # Before the fix, the _iterable_class would remain as ModelIterable
        # After the fix, it should be set to ValuesIterable
        qs.query = mock_query
        
        # Verify that _iterable_class is set correctly to ValuesIterable
        self.assertEqual(qs._iterable_class, ValuesIterable)
        
    def test_query_setter_preserves_model_iterable_class_when_no_values_select(self):
        """
        Test that the query setter correctly preserves ModelIterable when 
        there's no values_select (normal query behavior).
        """
        # Import the QuerySet class to test its behavior
        from django.db.models import QuerySet
        from django.db.models.sql import Query
        
        # Create a mock query without values_select (normal query)
        mock_query = Query(model=None)
        mock_query.values_select = []
        
        # Create a queryset instance
        qs = QuerySet(model=None)
        
        # The _iterable_class should remain as ModelIterable for normal queries
        qs.query = mock_query
        
        # Verify that _iterable_class is set correctly to ModelIterable
        self.assertEqual(qs._iterable_class, ModelIterable)
        
    def test_query_setter_handles_edge_case_empty_values_select(self):
        """
        Test that the query setter correctly handles empty values_select.
        """
        # Import the QuerySet class to test its behavior
        from django.db.models import QuerySet
        from django.db.models.sql import Query
        
        # Create a mock query with empty values_select
        mock_query = Query(model=None)
        mock_query.values_select = []
        
        # Create a queryset instance
        qs = QuerySet(model=None)
        
        # The _iterable_class should remain as ModelIterable for empty values_select
        qs.query = mock_query
        
        # Verify that _iterable_class is set correctly to ModelIterable
        self.assertEqual(qs._iterable_class, ModelIterable)
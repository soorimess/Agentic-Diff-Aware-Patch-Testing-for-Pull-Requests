import pickle
from django.db.models import Sum
from django.test import TestCase

# Use basic models that should be available
from django.contrib.auth.models import User


class Django13406TestCase(TestCase):
    """
    Test for Django ticket #13406: Queryset with values()/values_list() crashes
    when recreated from a pickled query.
    """
    
    @classmethod
    def setUpTestData(cls):
        # Create test data
        cls.user1 = User.objects.create(username='user1', email='user1@example.com')
        cls.user2 = User.objects.create(username='user2', email='user2@example.com')

    def test_values_queryset_pickling_returns_dicts(self):
        """
        Test that a values() QuerySet properly preserves its iterable class
        after being pickled and unpickled, returning dicts instead of model instances.
        """
        # Create a QuerySet with values() and annotate() - this creates GROUP BY
        original_qs = User.objects.values('username').annotate(count=Sum('id'))
        
        # Verify original QuerySet returns dicts
        original_result = list(original_qs)
        self.assertIsInstance(original_result[0], dict)
        self.assertIn('username', original_result[0])
        self.assertIn('count', original_result[0])
        
        # Pickle and unpickle the query
        pickled_query = pickle.dumps(original_qs.query)
        unpickled_query = pickle.loads(pickled_query)
        
        # Create a new QuerySet with the unpickled query
        unpickled_qs = User.objects.none()
        unpickled_qs.query = unpickled_query
        
        # The unpickled QuerySet should also return dicts, not model instances
        unpickled_result = list(unpickled_qs)
        self.assertIsInstance(unpickled_result[0], dict)
        self.assertIn('username', unpickled_result[0])
        self.assertIn('count', unpickled_result[0])
        
        # Both should return the same data
        self.assertEqual(len(original_result), len(unpickled_result))
        self.assertEqual(original_result[0]['username'], unpickled_result[0]['username'])
        self.assertEqual(original_result[0]['count'], unpickled_result[0]['count'])

    def test_model_iterable_preserved(self):
        """
        Test that regular QuerySets (without values) still work correctly
        after being pickled and unpickled.
        """
        # Create a regular QuerySet
        original_qs = User.objects.all()
        
        # Verify original QuerySet returns model instances
        original_result = list(original_qs)
        self.assertTrue(len(original_result) > 0)
        self.assertTrue(hasattr(original_result[0], 'id'))
        self.assertTrue(hasattr(original_result[0], 'username'))
        
        # Pickle and unpickle the query
        pickled_query = pickle.dumps(original_qs.query)
        unpickled_query = pickle.loads(pickled_query)
        
        # Create a new QuerySet with the unpickled query
        unpickled_qs = User.objects.none()
        unpickled_qs.query = unpickled_query
        
        # The unpickled QuerySet should still return model instances
        unpickled_result = list(unpickled_qs)
        self.assertTrue(len(unpickled_result) > 0)
        self.assertTrue(hasattr(unpickled_result[0], 'id'))
        self.assertTrue(hasattr(unpickled_result[0], 'username'))
        
        # Both should return the same data
        self.assertEqual(len(original_result), len(unpickled_result))
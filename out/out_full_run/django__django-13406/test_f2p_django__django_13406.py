import pickle

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.test import TestCase


class PickledValuesQueryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.User = User
        # Create users with different is_staff values so values().annotate()
        # groups by is_staff.
        User.objects.create_user(username='alice', password='password', is_staff=True)
        User.objects.create_user(username='bob', password='password', is_staff=False)
        User.objects.create_user(username='carol', password='password', is_staff=True)

    def test_values_query_preserved_when_assigned_from_pickled_query(self):
        """Picking and reusing a values()/annotate() query must return dicts.

        Regression test for ticket #13406: assigning a pickled values() query
        onto another queryset should ensure the queryset evaluates to dicts
        (ValuesIterable) rather than model instances.
        """
        User = self.User
        values_qs = User.objects.values('is_staff').annotate(total_id=Sum('id'))
        # Sanity-check the original values() QuerySet yields dicts.
        self.assertIsInstance(values_qs[0], dict)

        # Create a fresh queryset and replace its query with a pickled copy
        # of the values() query. The evaluated result must still be dicts.
        qs = User.objects.all()
        qs.query = pickle.loads(pickle.dumps(values_qs.query))
        result = list(qs)
        self.assertTrue(result, "Query returned no results")
        self.assertIsInstance(result[0], dict)
        # Also check that the keys we expect from the values() query are present.
        self.assertIn('is_staff', result[0])
        self.assertIn('total_id', result[0])

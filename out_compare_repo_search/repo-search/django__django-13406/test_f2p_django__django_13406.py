import pickle

from django.db.models import Count
from django.test import TestCase

from .models import Event, Group


class PickledValuesQueryAssignedToModelQuerySetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        g1 = Group.objects.create(name='g1')
        g2 = Group.objects.create(name='g2')
        Event.objects.create(title='e1', group=g1)
        Event.objects.create(title='e2', group=g1)
        Event.objects.create(title='e3', group=g2)

    def test_values_annotate_query_unpickled_and_assigned_returns_dicts(self):
        """
        Regression test for django #13406: when a Query.query that contains
        values()/annotate() is pickled and then assigned onto a different
        QuerySet (e.g. an all() queryset), the recipient QuerySet must still
        yield dicts (as values() would) rather than model instances.
        """
        qs_values = Event.objects.values('group').annotate(total=Count('id')).order_by('group')
        # Sanity: original values() queryset yields dicts
        original = list(qs_values)
        self.assertTrue(original)
        self.assertIsInstance(original[0], dict)

        # Pickle the underlying query and assign it to a fresh model queryset
        dumped = pickle.dumps(qs_values.query)
        reloaded = pickle.loads(dumped)

        qs = Event.objects.all()
        qs.query = reloaded

        # The queryset created from the unpickled query must behave like
        # the original values() queryset: yield dicts and equal results.
        recreated = list(qs)
        self.assertEqual(recreated, original)
        self.assertIsInstance(recreated[0], dict)

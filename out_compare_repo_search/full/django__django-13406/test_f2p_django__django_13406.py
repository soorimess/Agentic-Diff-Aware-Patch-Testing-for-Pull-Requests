from django.test import SimpleTestCase

from django.db.models.query import QuerySet, ModelIterable, ValuesIterable
from django.db.models.sql.query import Query


class PickledValuesQueryTest(SimpleTestCase):
    def test_query_setter_uses_values_iterable_when_query_has_values_select(self):
        """
        Assigning a Query with a non-empty values_select to a QuerySet via the
        `query` setter should switch the QuerySet's iterable class to
        ValuesIterable so that the QuerySet yields dicts/lists (as produced by
        values()/values_list()), not model instances.

        Regression test for a bug where restoring a pickled Query that used
        values()/annotate() onto another QuerySet caused that QuerySet to
        continue using the ModelIterable and return model instances (or
        raise an AttributeError) instead of the expected values.
        """
        query = Query(model=None)
        # Simulate a Query constructed from values()/values_list().
        query.values_select = ("some_field",)

        qs = QuerySet(model=None, query=Query(model=None))
        # Sanity check: default iterable class is ModelIterable.
        self.assertIs(qs._iterable_class, ModelIterable)

        # Assign the values-selecting query. The setter should switch the
        # iterable class to ValuesIterable.
        qs.query = query
        self.assertIs(qs._iterable_class, ValuesIterable)

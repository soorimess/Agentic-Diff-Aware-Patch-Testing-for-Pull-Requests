import unittest

from django.forms.boundfield import BoundWidget


class BoundWidgetIdForLabelTest(unittest.TestCase):
    def test_bound_widget_id_for_label_uses_widget_attrs_id(self):
        """
        BoundWidget.id_for_label should use the id from widget attrs, not generate a new one.
        
        The bug was that BoundWidget.id_for_label ignored the id set in widget attrs
        and generated a new id using 'id_%s_%s' pattern instead.
        """
        # Create mock data that represents what widget.subwidgets() returns
        # This simulates a subwidget with an explicit id set in attrs
        mock_data = {
            'name': 'choices',
            'index': '0',
            'attrs': {'id': 'custom_id_0'},
            'value': 'a',
            'label': 'A'
        }
        
        # Create BoundWidget with this data
        bound_widget = BoundWidget(None, mock_data, None)
        
        # Before the fix: BoundWidget.id_for_label returned 'id_choices_0' 
        # After the fix: BoundWidget.id_for_label should return 'custom_id_0'
        expected_id = 'custom_id_0'
        actual_id = bound_widget.id_for_label
        
        # This test should fail with the buggy implementation and pass with the fix
        self.assertEqual(actual_id, expected_id,
                        "BoundWidget.id_for_label should use widget attrs id, not auto-generate")

    def test_bound_widget_id_for_label_returns_none_when_no_id_in_attrs(self):
        """
        BoundWidget.id_for_label should return None when no id is in attrs.
        
        This is the behavior of the fixed implementation.
        """
        # Create mock data with no id in attrs
        mock_data = {
            'name': 'choices',
            'index': '1',
            'attrs': {},  # No id in attrs
            'value': 'b',
            'label': 'B'
        }
        
        # Create BoundWidget with this data
        bound_widget = BoundWidget(None, mock_data, None)
        
        # With the fix, it should return None (the result of .get('id') when key not present)
        expected_id = None
        actual_id = bound_widget.id_for_label
        
        # This should pass with the fix
        self.assertEqual(actual_id, expected_id,
                        "BoundWidget.id_for_label should return None when no id in attrs")
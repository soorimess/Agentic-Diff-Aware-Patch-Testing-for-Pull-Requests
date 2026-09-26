import unittest
from django.forms.boundfield import BoundWidget


class BoundWidgetIdForLabelTest(unittest.TestCase):
    def test_bound_widget_id_for_label_uses_attrs_id_when_present(self):
        """
        Test that BoundWidget.id_for_label uses the id from attrs when present.
        This test should fail with the current buggy implementation and pass after the fix.
        """
        # Create BoundWidget with data that includes attrs containing an id
        # This simulates what happens when BoundField.subwidgets creates BoundWidget instances
        data_with_id = {
            'name': 'field_name',
            'index': '0',
            'attrs': {'id': 'custom_id_0'}
        }
        
        # Create BoundWidget instance
        bound_widget = BoundWidget(None, data_with_id, None)
        
        # The id_for_label should use the id from attrs, not generate a new one
        actual_id = bound_widget.id_for_label
        
        # This assertion should pass after the fix is applied
        # It should return 'custom_id_0' (from data['attrs']['id'])
        # NOT 'id_field_name_0' (the buggy behavior that ignores attrs)
        self.assertEqual(actual_id, 'custom_id_0')
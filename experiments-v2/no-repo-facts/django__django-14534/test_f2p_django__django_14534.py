"""
Regression test for Django issue #14534: BoundWidget.id_for_label ignores id set by ChoiceWidget.options

This test verifies that BoundWidget.id_for_label returns the id from attrs['id'] 
when it's explicitly set, rather than generating a new id.
"""
from django.test import SimpleTestCase


class TestBoundWidgetIdForLabel(SimpleTestCase):
    def test_bound_widget_id_for_label_uses_attrs_id(self):
        """
        Test that BoundWidget.id_for_label uses the id from attrs['id'] 
        when it's explicitly set in widget options.
        """
        # Import here to avoid Django setup issues at module level
        from django.forms.boundfield import BoundWidget
        
        # Create mock data that simulates what ChoiceWidget.options produces
        # This represents the data structure that gets passed to BoundWidget
        mock_data = {
            'name': 'choices',
            'index': '0',
            'attrs': {
                'id': 'custom_widget_id_0'  # This should be used
            },
            'label': 'Option 1'
        }
        
        # Create a BoundWidget with this data
        bound_widget = BoundWidget(None, mock_data, None)
        
        # The current buggy implementation returns 'id_choices_0' (generated)
        # The fixed implementation should return 'custom_widget_id_0' (from attrs)
        self.assertEqual(bound_widget.id_for_label, 'custom_widget_id_0')

    def test_bound_widget_id_for_label_generates_when_no_attrs_id(self):
        """
        Test that BoundWidget.id_for_label still generates an id when 
        no id is set in attrs.
        """
        # Import here to avoid Django setup issues at module level
        from django.forms.boundfield import BoundWidget
        
        # Create mock data without id in attrs
        mock_data = {
            'name': 'choices',
            'index': '0',
            'attrs': {},
            'label': 'Option 1'
        }
        
        # Create a BoundWidget with this data
        bound_widget = BoundWidget(None, mock_data, None)
        
        # Should generate 'id_choices_0' (name + index)
        self.assertEqual(bound_widget.id_for_label, 'id_choices_0')
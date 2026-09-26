import unittest

from django import forms
from django.forms import CheckboxSelectMultiple


class TestBoundWidgetIdForLabel(unittest.TestCase):
    def test_bound_widget_id_for_label_ignores_id_set_by_choice_widget_options(self):
        """
        Test that BoundWidget.id_for_label uses the id from widget attrs instead of 
        constructing a new one.
        
        This is a regression test for Django issue #14534.
        """
        # Create a form with CheckboxSelectMultiple widget with a custom id
        choices = [('1', 'One'), ('2', 'Two'), ('3', 'Three')]
        widget = CheckboxSelectMultiple(choices=choices)
        widget.attrs['id'] = 'custom_id'
        
        class TestForm(forms.Form):
            test_field = forms.MultipleChoiceField(
                choices=choices,
                widget=widget,
                required=False
            )
        
        form = TestForm()
        bound_field = form['test_field']
        
        # The subwidgets should inherit the custom id from widget.attrs
        # Each subwidget should have id set to 'custom_id_0', 'custom_id_1', etc.
        # but currently they use the default pattern 'id_test_field_0', 'id_test_field_1', etc.
        
        subwidgets = list(bound_field.subwidgets)
        self.assertEqual(len(subwidgets), 3)
        
        # Check that the first subwidget has the correct id_for_label
        # Before the fix: would return 'id_test_field_0' 
        # After the fix: should return 'custom_id_0'
        expected_ids = ['custom_id_0', 'custom_id_1', 'custom_id_2']
        actual_ids = [widget.id_for_label for widget in subwidgets]
        
        # This assertion should pass after the fix is applied
        self.assertEqual(actual_ids, expected_ids)
        
        # Also check that the individual widget data contains the correct attrs
        for i, widget in enumerate(subwidgets):
            self.assertIn('attrs', widget.data)
            self.assertIn('id', widget.data['attrs'])
            self.assertEqual(widget.data['attrs']['id'], expected_ids[i])
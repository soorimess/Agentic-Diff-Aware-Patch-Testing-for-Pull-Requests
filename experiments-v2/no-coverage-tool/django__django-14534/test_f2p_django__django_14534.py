import unittest
from django import forms
from django.forms import CheckboxSelectMultiple


class TestBoundWidgetIdForLabel(unittest.TestCase):
    def test_bound_widget_id_for_label_uses_widget_attrs_id(self):
        """
        Test that BoundWidget.id_for_label uses the id from widget attributes
        instead of generating a new one.
        """
        # Create a CheckboxSelectMultiple widget with a specific id in attrs
        widget = CheckboxSelectMultiple(attrs={'id': 'custom_id'})
        
        # Create choices for the widget
        choices = [
            ('1', 'Choice 1'),
            ('2', 'Choice 2'),
            ('3', 'Choice 3'),
        ]
        
        # Create a form field with the widget
        field = forms.ChoiceField(choices=choices, widget=widget)
        
        # Create a form instance
        class TestForm(forms.Form):
            test_field = field
        
        form = TestForm()
        
        # Get the bound field
        bound_field = form['test_field']
        
        # Get the subwidgets
        subwidgets = list(bound_field.subwidgets)
        
        # Check that each subwidget has the correct id_for_label
        # The id_for_label should use the id from widget attributes, not generate a new one
        expected_ids = ['custom_id_0', 'custom_id_1', 'custom_id_2']
        actual_ids = [widget.id_for_label for widget in subwidgets]
        
        # Before the fix, this would fail because it generates 'id_test_field_0' etc.
        # After the fix, it should use the custom id from attrs
        self.assertEqual(actual_ids, expected_ids)
        
    def test_bound_widget_id_for_label_with_auto_id(self):
        """
        Test that BoundWidget.id_for_label works correctly with auto_id parameter.
        """
        # Create a CheckboxSelectMultiple widget without explicit id
        widget = CheckboxSelectMultiple()
        
        # Create choices for the widget
        choices = [
            ('1', 'Choice 1'),
            ('2', 'Choice 2'),
        ]
        
        # Create a form field with the widget
        field = forms.ChoiceField(choices=choices, widget=widget)
        
        # Create a form instance with auto_id
        class TestForm(forms.Form):
            test_field = field
        
        form = TestForm(auto_id='form_%s')
        
        # Get the bound field
        bound_field = form['test_field']
        
        # Get the subwidgets
        subwidgets = list(bound_field.subwidgets)
        
        # Check that each subwidget has the correct id_for_label
        # This should use the auto_id format
        expected_ids = ['form_test_field_0', 'form_test_field_1']
        actual_ids = [widget.id_for_label for widget in subwidgets]
        
        self.assertEqual(actual_ids, expected_ids)
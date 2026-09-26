import unittest

from django import forms
from django.forms import CheckboxSelectMultiple


class TestBoundWidgetIdForLabel(unittest.TestCase):
    def test_bound_widget_id_for_label_uses_widget_attrs_id(self):
        """
        Test that BoundWidget.id_for_label uses the id from widget attrs
        instead of generating a default id.
        """
        # Create a form with CheckboxSelectMultiple widget with a custom id
        choices = [('1', 'One'), ('2', 'Two'), ('3', 'Three')]
        
        class TestForm(forms.Form):
            field = forms.MultipleChoiceField(
                choices=choices,
                widget=CheckboxSelectMultiple(attrs={'id': 'custom_id'})
            )
        
        form = TestForm()
        bound_field = form['field']
        
        # Get the subwidgets - this should use the custom id from attrs
        subwidgets = bound_field.subwidgets
        
        # The first subwidget should have the custom id from attrs
        # Before the fix, it would generate 'id_field_0' instead of 'custom_id_0'
        first_widget = subwidgets[0]
        
        # This should return the id from attrs, not the generated one
        expected_id = 'custom_id_0'  # Should be from attrs['id'] + _ + index
        actual_id = first_widget.id_for_label
        
        # The bug is that it returns 'id_field_0' instead of 'custom_id_0'
        self.assertEqual(actual_id, expected_id)
        
    def test_bound_widget_id_for_label_with_no_attrs_id(self):
        """
        Test that BoundWidget.id_for_label still works when no id is in attrs.
        """
        choices = [('1', 'One'), ('2', 'Two'), ('3', 'Three')]
        
        class TestForm(forms.Form):
            field = forms.MultipleChoiceField(
                choices=choices,
                widget=CheckboxSelectMultiple()
            )
        
        form = TestForm()
        bound_field = form['field']
        subwidgets = bound_field.subwidgets
        
        # When no id is in attrs, it should generate the default id
        first_widget = subwidgets[0]
        expected_id = 'id_field_0'  # Default generated id
        actual_id = first_widget.id_for_label
        
        self.assertEqual(actual_id, expected_id)
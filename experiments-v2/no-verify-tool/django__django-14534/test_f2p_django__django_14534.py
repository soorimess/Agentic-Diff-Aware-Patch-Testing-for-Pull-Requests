import unittest
from django import forms
from django.forms.widgets import CheckboxSelectMultiple


class TestBoundWidgetIdForLabel(unittest.TestCase):
    def test_bound_widget_id_for_label_respects_widget_id(self):
        """
        Test that BoundWidget.id_for_label respects the id set by ChoiceWidget.options.
        
        This test verifies the bug where BoundWidget.id_for_label ignores the id
        set by ChoiceWidget.options and instead generates its own id based on name and index.
        """
        # Create a form with a CheckboxSelectMultiple field
        choices = [
            ('1', 'Option 1'),
            ('2', 'Option 2'),
            ('3', 'Option 3'),
        ]
        
        class TestForm(forms.Form):
            test_field = forms.MultipleChoiceField(
                choices=choices,
                widget=CheckboxSelectMultiple(attrs={'id': 'custom_id'}),
                required=False
            )
        
        # Create form instance
        form = TestForm()
        
        # Get the bound field
        bound_field = form['test_field']
        
        # Get the subwidgets
        subwidgets = list(bound_field.subwidgets)
        
        # Check that the first subwidget has the expected id_for_label
        # Before the fix, it would generate 'id_custom_id_0' instead of 'custom_id_0'
        first_widget = subwidgets[0]
        
        # The expected behavior is that id_for_label should return the id from attrs
        # which should be 'custom_id_0' (based on the custom id + index)
        expected_id = 'custom_id_0'
        actual_id = first_widget.id_for_label
        
        # This assertion should pass after the fix, but fail before the fix
        self.assertEqual(actual_id, expected_id)
        
    def test_bound_widget_id_for_label_with_custom_id_in_attrs(self):
        """
        Test that BoundWidget.id_for_label respects custom id in widget attrs.
        """
        choices = [
            ('1', 'Option 1'),
            ('2', 'Option 2'),
        ]
        
        class TestForm(forms.Form):
            test_field = forms.MultipleChoiceField(
                choices=choices,
                widget=CheckboxSelectMultiple(attrs={'id': 'my_custom_field'}),
                required=False
            )
        
        form = TestForm()
        bound_field = form['test_field']
        subwidgets = list(bound_field.subwidgets)
        
        # Check first widget
        first_widget = subwidgets[0]
        expected_id = 'my_custom_field_0'
        actual_id = first_widget.id_for_label
        
        # This should pass after fix, fail before fix
        self.assertEqual(actual_id, expected_id)
        
        # Check second widget
        second_widget = subwidgets[1]
        expected_id_2 = 'my_custom_field_1'
        actual_id_2 = second_widget.id_for_label
        
        # This should pass after fix, fail before fix
        self.assertEqual(actual_id_2, expected_id_2)
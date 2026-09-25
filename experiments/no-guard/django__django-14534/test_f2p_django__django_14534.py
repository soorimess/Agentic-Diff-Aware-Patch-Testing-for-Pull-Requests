"""
Regression test for issue where BoundWidget.id_for_label ignores
id set by ChoiceWidget.options in CheckboxSelectMultiple.
"""

from django import forms
from django.test import TestCase


class CheckboxSelectMultipleTestCase(TestCase):
    def test_bound_widget_id_for_label_generates_expected_id(self):
        """Test that BoundWidget.id_for_label generates expected ID using name and index."""
        # Create a form with a CheckboxSelectMultiple field
        class MyForm(forms.Form):
            choices = forms.MultipleChoiceField(
                choices=[('1', 'Option 1'), ('2', 'Option 2')],
                widget=forms.CheckboxSelectMultiple,
                required=False
            )
        
        # Create the form and access the subwidgets
        form = MyForm()
        bound_field = form['choices']
        subwidgets = bound_field.subwidgets
        
        # Verify that we have subwidgets generated
        self.assertEqual(len(subwidgets), 2)
        
        # Get the first subwidget and check its id_for_label method
        first_widget = subwidgets[0]
        
        # With no custom id, should generate 'id_choices_0' based on name and index
        expected_id = 'id_choices_0'
        actual_id = first_widget.id_for_label
        
        self.assertEqual(actual_id, expected_id, 
                        f"Expected '{expected_id}', but got '{actual_id}'")

    def test_bound_widget_id_for_label_respects_option_id_attrs(self):
        """Test that BoundWidget.id_for_label respects id from choice widget options."""
        # Create a form with a CheckboxSelectMultiple field with custom widget id
        class MyForm(forms.Form):
            choices = forms.MultipleChoiceField(
                choices=[('1', 'Option 1'), ('2', 'Option 2')],
                widget=forms.CheckboxSelectMultiple(attrs={'id': 'custom_id'}),
                required=False
            )
        
        # Create the form and access the subwidgets
        form = MyForm()
        bound_field = form['choices']
        subwidgets = bound_field.subwidgets
        
        # Verify that we have subwidgets generated
        self.assertEqual(len(subwidgets), 2)
        
        # Get the first subwidget and check its id_for_label method
        first_widget = subwidgets[0]
        
        # The id_for_label should use the id from the widget's processing 
        # which should result in 'custom_id_0' after suffixing by widget logic
        # This ensures that BoundWidget.id_for_label uses the value from data['attrs']['id']
        # rather than generating a generic id
        expected_id = 'custom_id_0'  
        actual_id = first_widget.id_for_label
        
        # This assertion will pass after fix - this tests the actual problem reported
        self.assertEqual(actual_id, expected_id,
                        f"Expected '{expected_id}', but got '{actual_id}'")

    def test_bound_widget_id_for_label_respects_option_id_attrs_second_widget(self):
        """Test that BoundWidget.id_for_label respects id from choice widget options on second widget."""
        # Test the second widget as well to make the test complete
        class MyForm(forms.Form):
            choices = forms.MultipleChoiceField(
                choices=[('1', 'Option 1'), ('2', 'Option 2')],
                widget=forms.CheckboxSelectMultiple(attrs={'id': 'custom_id'}),
                required=False
            )
        
        # Create the form and access the subwidgets
        form = MyForm()
        bound_field = form['choices']
        subwidgets = bound_field.subwidgets
        
        # Verify that we have subwidgets generated
        self.assertEqual(len(subwidgets), 2)
        
        # Get the second subwidget and check its id_for_label method
        second_widget = subwidgets[1]
        
        # The second widget should have id 'custom_id_1'  
        expected_id = 'custom_id_1'  
        actual_id = second_widget.id_for_label
        
        # This assertion will pass after fix - tests the second widget too
        self.assertEqual(actual_id, expected_id,
                        f"Expected '{expected_id}', but got '{actual_id}'")
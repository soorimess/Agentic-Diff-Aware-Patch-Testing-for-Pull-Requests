from django import forms
from django.test import TestCase


class TestBoundWidgetIdForLabel(TestCase):
    def test_bound_widget_id_for_label_uses_attrs_id(self):
        """
        Test that BoundWidget.id_for_label uses the id from attrs instead of 
        generating a new one based on name and index.
        """
        # Create a form with a CheckboxSelectMultiple field
        class TestForm(forms.Form):
            choices = forms.ChoiceField(
                widget=forms.CheckboxSelectMultiple,
                choices=[('1', 'Option 1'), ('2', 'Option 2')]
            )
        
        # Create form with custom auto_id to make the issue visible
        form = TestForm(auto_id='custom_id_%s')
        
        # Get the bound field
        bound_field = form['choices']
        
        # Get the subwidgets
        subwidgets = list(bound_field.subwidgets)
        
        # Check that each subwidget's id_for_label uses the correct id from attrs
        # The first subwidget should have id 'custom_id_choices_0' not 'id_choices_0'
        self.assertEqual(len(subwidgets), 2)
        
        # The first subwidget should have id 'custom_id_choices_0' 
        # (from the attrs that were passed in)
        first_widget_id = subwidgets[0].id_for_label
        self.assertEqual(first_widget_id, 'custom_id_choices_0')
        
        # The second subwidget should have id 'custom_id_choices_1'
        second_widget_id = subwidgets[1].id_for_label
        self.assertEqual(second_widget_id, 'custom_id_choices_1')
        
    def test_bound_widget_id_for_label_with_explicit_id_attr(self):
        """
        Test that BoundWidget.id_for_label uses an explicitly set id attribute
        when provided in widget attrs.
        """
        # Create a form with a CheckboxSelectMultiple field with explicit id
        class TestForm(forms.Form):
            choices = forms.ChoiceField(
                widget=forms.CheckboxSelectMultiple(attrs={'id': 'explicit_id'}),
                choices=[('1', 'Option 1'), ('2', 'Option 2')]
            )
        
        # Create form with auto_id to make sure it's not used for subwidgets
        form = TestForm(auto_id='form_id_%s')
        
        # Get the bound field
        bound_field = form['choices']
        
        # Get the subwidgets
        subwidgets = list(bound_field.subwidgets)
        
        # Check that each subwidget's id_for_label uses the explicit id from attrs
        self.assertEqual(len(subwidgets), 2)
        
        # Both subwidgets should have id 'explicit_id_0' and 'explicit_id_1'
        first_widget_id = subwidgets[0].id_for_label
        self.assertEqual(first_widget_id, 'explicit_id_0')
        
        second_widget_id = subwidgets[1].id_for_label
        self.assertEqual(second_widget_id, 'explicit_id_1')
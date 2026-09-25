"""
Regression test for Django issue #14534.

BoundWidget.id_for_label should use the id from widget attributes, not
construct a new one.
"""
from django import forms
from django.test import TestCase


class BoundWidgetIdForLabelTest(TestCase):
    def test_bound_widget_id_for_label_uses_widget_id(self):
        """
        BoundWidget.id_for_label should return the id from widget attributes,
        not construct a new one using 'id_%s_%s' format.
        """
        class TestForm(forms.Form):
            choices = [
                ('1', 'One'),
                ('2', 'Two'),
                ('3', 'Three'),
            ]
            field = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple
            )

        # Create form with custom auto_id (this will create widget attrs with id)
        form = TestForm(auto_id='custom_id_%s')
        
        # Access the bound field
        bound_field = form['field']
        
        # Get the subwidgets - this is where the issue manifests
        subwidgets = bound_field.subwidgets
        
        # There should be 3 subwidgets
        self.assertEqual(len(subwidgets), 3)
        
        # Check that each subwidget's id_for_label uses the id from widget attributes
        # When auto_id='custom_id_%s', and field name is 'field':
        # - Subwidget 0: attrs['id'] = 'custom_id_field_0', should be id_for_label = 'custom_id_field_0'
        # - Subwidget 1: attrs['id'] = 'custom_id_field_1', should be id_for_label = 'custom_id_field_1'  
        # - Subwidget 2: attrs['id'] = 'custom_id_field_2', should be id_for_label = 'custom_id_field_2'
        #
        # Before the fix, id_for_label returns constructed values:
        #   'id_field_0', 'id_field_1', 'id_field_2' 
        # After the fix, id_for_label returns widget-specified values:
        #   'custom_id_field_0', 'custom_id_field_1', 'custom_id_field_2'
        
        for i, subwidget in enumerate(subwidgets):
            # We need a more specific assertion to highlight the issue
            expected_id = f'custom_id_field_{i}'
            actual_id = subwidget.id_for_label
            
            # Before fix: actual_id would be 'id_field_%d' not 'custom_id_field_%d'
            # This is what we're testing for - that the attribute id is respected
            self.assertEqual(actual_id, expected_id, 
                           f"Subwidget {i} id_for_label should be '{expected_id}' (from attrs), got '{actual_id}'")

    def test_bound_widget_id_for_label_with_explicit_id(self):
        """
        Test that BoundWidget.id_for_label respects explicitly set id attribute
        in widget options.
        """
        class TestForm(forms.Form):
            choices = [
                ('1', 'One'),
                ('2', 'Two'),
            ]
            field = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple(attrs={'id': 'explicit_id'})
            )

        form = TestForm()
        bound_field = form['field']
        subwidgets = bound_field.subwidgets
        
        # All subwidgets should use the explicit id with their index suffix
        # When specific id is set as 'explicit_id':
        # - Subwidget 0: should have id_for_label = 'explicit_id_0'
        # - Subwidget 1: should have id_for_label = 'explicit_id_1'
        for i, subwidget in enumerate(subwidgets):
            expected_id = f'explicit_id_{i}'
            actual_id = subwidget.id_for_label
            self.assertEqual(actual_id, expected_id,
                           f"Subwidget {i} id_for_label should be '{expected_id}', got '{actual_id}'")
import unittest

from django import forms
from django.forms import CheckboxSelectMultiple


class BoundWidgetIdForLabelTest(unittest.TestCase):
    def test_boundwidget_id_for_label_respects_widget_attrs_id(self):
        """
        Test that BoundWidget.id_for_label uses the id from widget attrs
        instead of generating a default id based on name and index.
        
        This is a regression test for Django ticket #14534.
        """
        # Create a form with a CheckboxSelectMultiple widget
        class TestForm(forms.Form):
            choices = [
                ('choice1', 'Choice 1'),
                ('choice2', 'Choice 2'),
                ('choice3', 'Choice 3'),
            ]
            field = forms.MultipleChoiceField(
                widget=CheckboxSelectMultiple(choices=choices),
                choices=choices
            )
        
        # Create form instance with custom id in widget attrs
        form = TestForm()
        form.fields['field'].widget.attrs['id'] = 'custom_id'
        
        # Get the bound field
        bound_field = form['field']
        
        # Get the subwidgets - this is where the bug manifests
        subwidgets = bound_field.subwidgets
        
        # The bug: BoundWidget.id_for_label was generating 'id_field_0' instead of 
        # using the ID from widget attrs. The fix makes it return self.data['attrs'].get('id')
        first_subwidget = subwidgets[0]
        actual_id = first_subwidget.id_for_label
        
        # Verify that it's NOT the old buggy behavior
        self.assertNotEqual(actual_id, 'id_field_0')
        
        # Verify that it uses the ID from attrs (even if widget appends index)
        self.assertTrue(actual_id.startswith('custom_id'), 
                       f"Expected ID to start with 'custom_id', got '{actual_id}'")

    def test_boundwidget_id_for_label_fallback_to_auto_id(self):
        """
        Test that BoundWidget.id_for_label falls back to auto_id when no id is set in attrs.
        """
        # Create a form with a CheckboxSelectMultiple widget
        class TestForm(forms.Form):
            choices = [
                ('choice1', 'Choice 1'),
                ('choice2', 'Choice 2'),
            ]
            field = forms.MultipleChoiceField(
                widget=CheckboxSelectMultiple(choices=choices),
                choices=choices
            )
        
        # Create form instance without custom id in widget attrs
        form = TestForm()
        # Don't set widget.attrs['id'] - let it use auto_id
        
        # Get the bound field
        bound_field = form['field']
        
        # Get the subwidgets
        subwidgets = bound_field.subwidgets
        
        # The first subwidget should use the auto-generated id
        first_subwidget = subwidgets[0]
        actual_id = first_subwidget.id_for_label
        
        # Should generate id based on name and index since no explicit id was set
        self.assertEqual(actual_id, 'id_field_0')
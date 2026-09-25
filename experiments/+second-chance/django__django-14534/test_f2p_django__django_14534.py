"""
Regression test for Django issue #14534.
BoundWidget.id_for_label ignores id set by ChoiceWidget.options

This test verifies correct behavior of BoundWidget.id_for_label property
when the widget has an id attribute set in its attrs.

The bug was that BoundWidget.id_for_label always used the fallback
'id_%s_%s' pattern instead of using the id that is properly constructed
in the widget's attrs.
"""
from django import forms
from django.test import TestCase


class TestBoundWidgetIdForLabel(TestCase):
    def test_boundwidget_id_for_label_uses_attrs_id(self):
        """
        Test that BoundWidget.id_for_label uses the id from attrs instead of 
        constructing its own when the widget has an id attribute set.
        
        Before fix: id_for_label would return 'id_choices_0' 
        After fix: id_for_label should return 'custom_widget_id_0'
        """
        class TestForm(forms.Form):
            choices = forms.MultipleChoiceField(
                choices=[('1', 'Choice 1'), ('2', 'Choice 2')],
                widget=forms.CheckboxSelectMultiple,
                required=False
            )
        
        # Set a custom id on the widget
        form = TestForm()
        form.fields['choices'].widget.attrs['id'] = 'custom_widget_id'
        
        # Get the subwidgets
        bound_field = form['choices']
        subwidgets = list(bound_field.subwidgets)
        
        # The first subwidget's id_for_label should use the custom id constructed in attrs
        # Not the conventionally constructed id
        self.assertEqual(subwidgets[0].id_for_label, 'custom_widget_id_0')
        
    def test_boundwidget_id_for_label_fallback_behavior(self):
        """
        Test that BoundWidget.id_for_label falls back to convention when no id 
        is specified in widget attrs.
        """
        class TestForm(forms.Form):
            choices = forms.MultipleChoiceField(
                choices=[('1', 'Choice 1'), ('2', 'Choice 2')],
                widget=forms.CheckboxSelectMultiple,
                required=False
            )
        
        # No custom id set
        form = TestForm()
        bound_field = form['choices']
        subwidgets = list(bound_field.subwidgets)
        
        # Should fall back to constructed pattern using field name and index
        self.assertEqual(subwidgets[0].id_for_label, 'id_choices_0')
        self.assertEqual(subwidgets[1].id_for_label, 'id_choices_1')
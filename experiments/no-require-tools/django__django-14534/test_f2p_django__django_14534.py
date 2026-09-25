"""
Regression test for Django issue #14534
BoundWidget.id_for_label ignores id set by ChoiceWidget.options
"""
from django import forms
from django.test import TestCase


class TestBoundWidgetIdForLabel(TestCase):
    def test_bound_widget_id_for_label_uses_attrs_id(self):
        """
        Test that BoundWidget.id_for_label uses the id from attrs 
        when it exists, rather than generating a new one.
        """
        # Create a form with a CheckboxSelectMultiple field
        class TestForm(forms.Form):
            test_field = forms.ChoiceField(
                choices=[('foo', 'Foo'), ('bar', 'Bar')],
                widget=forms.CheckboxSelectMultiple(attrs={'id': 'custom_widget_id'}),
                required=False
            )
        
        form = TestForm()
        bound_field = form['test_field']
        
        # Get the subwidgets 
        subwidgets = list(bound_field.subwidgets)
        self.assertEqual(len(subwidgets), 2)
        
        # Before the fix: BoundWidget.id_for_label returns 'id_test_field_0' and 'id_test_field_1'
        # After the fix: BoundWidget.id_for_label should return 'custom_widget_id_0' and 'custom_widget_id_1'
        widget1 = subwidgets[0]
        widget2 = subwidgets[1]
        
        # Check the id_for_label values - this is where the bug is
        id1 = widget1.id_for_label
        id2 = widget2.id_for_label
        
        # This assertion should fail before the fix and pass after
        self.assertEqual(id1, 'custom_widget_id_0')
        self.assertEqual(id2, 'custom_widget_id_1')

    def test_bound_widget_id_for_label_with_auto_id(self):
        """
        Test when using auto_id format string but widget has id in attrs.
        """
        class TestForm(forms.Form):
            test_field = forms.ChoiceField(
                choices=[('foo', 'Foo'), ('bar', 'Bar')],
                widget=forms.CheckboxSelectMultiple(attrs={'id': 'my_widget_id'}),
                required=False
            )
        
        # Using a custom auto_id format that would generate different IDs
        form = TestForm(auto_id='my_auto_id_%s')
        bound_field = form['test_field']
        
        subwidgets = list(bound_field.subwidgets)
        self.assertEqual(len(subwidgets), 2)
        
        widget1 = subwidgets[0]
        widget2 = subwidgets[1]
        
        # The bug: BoundWidget.id_for_label ignores id from widget.attrs
        # Expected solution after fix: should use the attrs['id'] (my_widget_id) + index
        id1 = widget1.id_for_label
        id2 = widget2.id_for_label
        
        # The fix should make this return the widget-provided id, not auto-generated
        self.assertEqual(id1, 'my_widget_id_0')  
        self.assertEqual(id2, 'my_widget_id_1')
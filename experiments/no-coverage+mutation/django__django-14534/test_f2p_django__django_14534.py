from django import forms
from django.forms import CheckboxSelectMultiple
from django.test import TestCase


class CheckboxSelectMultipleIdForLabelTest(TestCase):
    def test_boundwidget_id_for_label_uses_widget_id_when_set(self):
        """
        Test that BoundWidget.id_for_label uses the id from widget.attrs
        when it's explicitly set, rather than constructing a new id.
        """
        # Create a CheckboxSelectMultiple widget with an explicit id
        widget = CheckboxSelectMultiple(
            choices=[('J', 'John'), ('P', 'Paul'), ('G', 'George'), ('R', 'Ringo')]
        )
        widget.attrs['id'] = 'my_custom_id'
        
        # Create a form field with this widget
        field = forms.MultipleChoiceField(
            choices=[('J', 'John'), ('P', 'Paul'), ('G', 'George'), ('R', 'Ringo')],
            widget=widget
        )
        
        # Create a form instance to get bound field
        class TestForm(forms.Form):
            beatles = field
            
        form = TestForm()
        bound_field = form['beatles']
        
        # Get subwidgets from the bound field
        # This is what triggers the issue - BoundWidget gets constructed
        subwidgets = bound_field.subwidgets
        
        # Check that the first subwidget uses the custom id
        first_widget = subwidgets[0]
        
        # The id_for_label should respect the id set in widget.attrs  
        self.assertEqual(first_widget.id_for_label, 'my_custom_id_0')
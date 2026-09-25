"""
Regression test for django/django#14534.

BoundWidget.id_for_label should return the id from widget attrs, not generate one.
"""

# We need to make sure this can be directly run by Django's test runner.
# Importing exactly what we need...

from django import forms
from django.forms import CheckboxSelectMultiple
from django.test import TestCase

def test_basic():
    """Simple test to check if test can run."""
    assert True

class BoundWidgetRegressionTest(TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass

    def test_boundwidget_id_for_label_respects_widget_attrs(self):
        """
        Test that BoundWidget.id_for_label returns the id from widget attrs.
        
        When generating subwidgets for a CheckboxSelectMultiple field,
        BoundWidget.id_for_label should return the id from the individual
        widget data attrs rather than a generated default.
        """
        # Create a form with CheckboxSelectMultiple that has explicit id
        class TestForm(forms.Form):
            beatles = forms.ChoiceField(
                choices=[('J', 'John'), ('P', 'Paul')],
                widget=CheckboxSelectMultiple(attrs={'id': 'my_custom_id'})
            )
        
        form = TestForm()
        bound_field = form['beatles']
        subwidgets = bound_field.subwidgets
        
        # Check that we have correct number of subwidgets
        self.assertEqual(len(subwidgets), 2)
        
        # Check the first subwidget's id_for_label
        first_widget = subwidgets[0]
        
        # The bug: id_for_label returns 'id_%s_%s' (e.g., 'id_beatles_0') 
        # Instead of using the actual id from attrs which would be 'my_custom_id_0'
        first_id_for_label = first_widget.id_for_label
        first_widget_data = first_widget.data
        
        # Verify the data structure has correct attrs
        self.assertIn('attrs', first_widget_data)
        self.assertIn('id', first_widget_data['attrs'])
        
        # This assertion should pass with the bug fix, and fail with buggy behavior
        expected_id = first_widget_data['attrs']['id']
        self.assertEqual(first_id_for_label, expected_id)
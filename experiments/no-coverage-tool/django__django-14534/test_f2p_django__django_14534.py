from django import forms
from django.test import TestCase


class TestBoundWidgetIDForLabel(TestCase):
    def test_checkbox_select_multiple_id_generation_bug(self):
        """
        Regression test for the bug that BoundWidget.id_for_label ignores id set by 
        ChoiceWidget.options and always uses the constructed 'id_name_index' format.
        """
        class TestForm(forms.Form):
            checkbox_choices = forms.MultipleChoiceField(
                choices=[('a', 'Option A'), ('b', 'Option B')],
                widget=forms.CheckboxSelectMultiple,
                required=False
            )
        
        # Create form with auto_id - this sets expected ID format
        form = TestForm(auto_id="form_auto_%s")
        bound_field = form['checkbox_choices']
        
        # Get the subwidgets - this exercises the bug
        subwidgets = list(bound_field.subwidgets)
        self.assertEqual(len(subwidgets), 2)
        
        # Extract the id_for_label values
        actual_ids = [subwidget.id_for_label for subwidget in subwidgets]
        
        # Verify the current buggy behavior (before fix) and expected behavior (after fix)
        # The bug: always uses 'id_name_index' pattern regardless of auto_id
        # Expected after fix: respects the ID that was already set up by widget processing
        expected_ids = ['form_auto_checkbox_choices_0', 'form_auto_checkbox_choices_1']
        
        # This assertion will fail before the fix and pass after
        for i, (actual, expected) in enumerate(zip(actual_ids, expected_ids)):
            self.assertEqual(actual, expected, 
                           f"Subwidget {i} id_for_label mismatch: "
                           f"got '{actual}', expected '{expected}'")
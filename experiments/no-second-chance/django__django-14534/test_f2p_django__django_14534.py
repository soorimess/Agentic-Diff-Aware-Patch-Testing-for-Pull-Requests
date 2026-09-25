from django import forms
from django.test import TestCase


class BoundWidgetIdForLabelTest(TestCase):
    def test_bound_widget_id_for_label_with_explicit_id(self):
        """
        Test that BoundWidget.id_for_label respects id set by ChoiceWidget.options
        when explicitly provided in widget attrs.
        """
        # Form with a CheckboxSelectMultiple field
        class TestForm(forms.Form):
            choices = [
                ('1', 'Choice 1'),
                ('2', 'Choice 2'),
                ('3', 'Choice 3'),
            ]
            field = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple(attrs={'id': 'custom_id'})
            )
        
        form = TestForm()
        bound_field = form['field']
        
        # The subwidgets should have proper id attributes set through the widget attrs
        subwidgets = list(bound_field.subwidgets)
        
        # There should be 3 subwidgets for 3 choices
        self.assertEqual(len(subwidgets), 3)
        
        # Each subwidget's id_for_label should return the id from widget attrs
        # instead of generating a default id based on name/index
        expected_ids = ['custom_id_0', 'custom_id_1', 'custom_id_2']
        actual_ids = [widget.id_for_label for widget in subwidgets]
        
        # Before the fix, this would return 'id_field_0', 'id_field_1', 'id_field_2'
        # After the fix, this should return 'custom_id_0', 'custom_id_1', 'custom_id_2'
        self.assertEqual(actual_ids, expected_ids)
    
    def test_bound_widget_id_for_label_auto_id_fallback(self):
        """
        Test that BoundWidget.id_for_label falls back to auto_id behavior 
        when no explicit id is provided.
        """
        # Form with a CheckboxSelectMultiple field without explicit id
        class TestForm(forms.Form):
            choices = [
                ('1', 'Choice 1'),
                ('2', 'Choice 2'),
            ]
            field = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple()
            )
        
        form = TestForm()
        bound_field = form['field']
        
        # The form should have auto_id
        form.auto_id = 'form_id_%s'
        
        # The subwidgets should use the auto_id fallback
        subwidgets = list(bound_field.subwidgets)
        
        # There should be 2 subwidgets for 2 choices
        self.assertEqual(len(subwidgets), 2)
        
        # Each subwidget's id_for_label should return the auto_id based on name/index
        # In this case, it should be 'form_id_field_0' and 'form_id_field_1'
        actual_ids = [widget.id_for_label for widget in subwidgets]
        expected_ids = ['form_id_field_0', 'form_id_field_1']
        
        self.assertEqual(actual_ids, expected_ids)
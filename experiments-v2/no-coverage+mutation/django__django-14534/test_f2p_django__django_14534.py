import unittest
from django import forms
from django.forms import CheckboxSelectMultiple


class TestBoundWidgetIdForLabel(unittest.TestCase):
    def test_bound_widget_id_for_label_respects_attrs_id(self):
        """
        Regression test for django/django#14534
        BoundWidget.id_for_label should return self.data['attrs'].get('id') 
        instead of generating its own ID.
        """
        # Test with auto_id
        class TestForm(forms.Form):
            choices = forms.ChoiceField(
                widget=CheckboxSelectMultiple,
                choices=[('1', 'Option 1'), ('2', 'Option 2')]
            )
        
        form = TestForm(auto_id='custom_id_%s')
        bound_field = form['choices']
        subwidgets = list(bound_field.subwidgets)
        first_widget = subwidgets[0]
        
        # The widget's attrs should contain the correct id
        attrs_id = first_widget.data['attrs'].get('id')
        # This should be 'custom_id_choices_0'
        
        # BoundWidget.id_for_label should return this id, not generate a new one
        actual_id = first_widget.id_for_label
        
        # Before the fix, this would fail because it returns 'id_choices_0' 
        # After the fix, this should pass because it returns 'custom_id_choices_0'
        self.assertEqual(actual_id, attrs_id)
        
    def test_bound_widget_id_for_label_respects_explicit_id_attrs(self):
        """
        Test that BoundWidget.id_for_label respects explicitly set id in widget attrs.
        """
        class TestForm(forms.Form):
            choices = forms.ChoiceField(
                widget=CheckboxSelectMultiple(attrs={'id': 'explicit_id'}),
                choices=[('1', 'Option 1'), ('2', 'Option 2')]
            )
        
        form = TestForm()
        bound_field = form['choices']
        subwidgets = list(bound_field.subwidgets)
        first_widget = subwidgets[0]
        
        # The widget's attrs should contain the correct id
        attrs_id = first_widget.data['attrs'].get('id')
        # This should be 'explicit_id_0' (after ChoiceWidget processing)
        
        # BoundWidget.id_for_label should return this id
        actual_id = first_widget.id_for_label
        
        # Before the fix, this would fail because it returns 'id_choices_0' 
        # After the fix, this should pass because it returns 'explicit_id_0'
        self.assertEqual(actual_id, attrs_id)
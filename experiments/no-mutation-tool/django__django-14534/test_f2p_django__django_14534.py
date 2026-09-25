"""
Regression test for Django issue where BoundWidget.id_for_label ignores 
id set by ChoiceWidget.options.
"""
from django.test import SimpleTestCase
from django import forms
from django.forms.widgets import CheckboxSelectMultiple


class BoundWidgetRegressionTests(SimpleTestCase):
    
    def test_boundwidget_id_for_label_respects_custom_id(self):
        """
        Test that BoundWidget.id_for_label respects the id set in widget attrs
        rather than generating its own id.
        
        The issue being tested: BoundWidget.id_for_label ignored the id in 
        self.data['attrs']['id'] and instead used the hardcoded format
        'id_%s_%s' % (self.data['name'], self.data['index']).
        """
        class TestForm(forms.Form):
            choices = forms.MultipleChoiceField(
                choices=[('1', 'Choice 1'), ('2', 'Choice 2'), ('3', 'Choice 3')],
                widget=CheckboxSelectMultiple(attrs={'id': 'my_custom_id'}),
                required=False
            )

        form = TestForm()
        bound_field = form['choices']
        
        # Get the subwidgets - these should inherit the custom id 
        subwidgets = bound_field.subwidgets
        
        # Check that each subwidget's id_for_label uses the custom ID from attrs
        # instead of generating a new one
        for i, widget in enumerate(subwidgets):
            # The widget data contains the correct id in attrs: 'my_custom_id_0', 'my_custom_id_1', etc.
            # BoundWidget.id_for_label should return the one from data['attrs']['id']
            expected_id = 'my_custom_id_%d' % i
            actual_id = widget.id_for_label
            
            # This should pass after the fix, fail before the fix
            self.assertEqual(actual_id, expected_id, 
                "Expected %s but got %s for widget %d" % (expected_id, actual_id, i))
            

    def test_boundwidget_id_for_label_uses_attrs_id(self):
        """
        Additional test to specifically check that BoundWidget.id_for_label
        reads from self.data['attrs']['id'] rather than generating new.
        """
        class TestForm(forms.Form):
            choices = forms.MultipleChoiceField(
                choices=[('1', 'Choice 1'), ('2', 'Choice 2'), ('3', 'Choice 3')],
                widget=CheckboxSelectMultiple(attrs={'id': 'my_custom_id'}),
                required=False
            )

        form = TestForm()
        bound_field = form['choices']
        
        # Get the subwidgets  
        subwidgets = bound_field.subwidgets
        
        # Verify the original widget data has the right structure
        widget_data = list(bound_field.field.widget.subwidgets(bound_field.html_name, bound_field.value(), attrs={'id': 'my_custom_id'}))
        
        # Each widget data item should have the right attrs structure
        for i, (widget, data_item) in enumerate(zip(subwidgets, widget_data)):
            # The data item should have the correct attrs with custom id
            self.assertIn('attrs', data_item)
            self.assertIn('id', data_item['attrs'])
            self.assertEqual(data_item['attrs']['id'], 'my_custom_id_%d' % i)
            
            # The BoundWidget should use the data from attrs['id']
            self.assertEqual(widget.id_for_label, data_item['attrs']['id'])
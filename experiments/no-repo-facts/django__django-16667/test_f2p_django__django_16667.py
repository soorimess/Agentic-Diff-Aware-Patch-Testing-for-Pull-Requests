from django.test import TestCase

class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error_handling(self):
        """
        Regression test for Django bug where SelectDateWidget can crash with OverflowError.
        
        Before fix: Large integer values would cause OverflowError in datetime.date() call
        After fix: Large integer values return '0-0-0' instead of crashing
        """
        from django.forms import SelectDateWidget
        
        widget = SelectDateWidget()
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678',  # Large number that triggers OverflowError
        }
        
        # This should work without raising OverflowError after the fix
        result = widget.value_from_datadict(data, {}, 'my_date')
        
        # After the fix, it should return "0-0-0" instead of crashing
        self.assertEqual(result, "0-0-0")
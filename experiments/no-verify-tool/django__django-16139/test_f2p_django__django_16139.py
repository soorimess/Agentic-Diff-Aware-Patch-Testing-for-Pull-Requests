"""
Regression test for Django issue where UserAdmin accessed via to_field 
leads to broken link in PasswordResetForm (404).

The bug: when UserAdmin is accessed with to_field parameter (e.g., UUID),
the help_text on the password field still refers to "../password/" instead
of using the actual instance identifier, causing a 404 when navigating to 
the password change form.
"""

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldRegressionTest(TestCase):
    
    def test_password_help_text_format(self):
        """
        Test that UserChangeForm generates correct help_text format for password field.
        In the buggy implementation it always uses "../password/" regardless of context.
        After fix it should use the instance pk in the path.
        """
        # Create a regular user to instantiate form
        user = User(id=123, username="testuser", email="test@example.com")
        
        # Instantiate the form with this user 
        form = UserChangeForm(instance=user)
        
        # Get the password field's help_text
        password_field = form.fields.get('password')
        actual_help_text = password_field.help_text
        
        # This test validates the EXPECTED behavior (what should happen after fix)
        # We want to see the path formatted with instance.pk
        expected_pattern = "../../123/password/"
        
        # The OLD buggy behavior (before fix) was:
        # actual_help_text = "...<a href='../password/'>this form</a>."
        # 
        # The NEW behavior (after fix) should be:
        # actual_help_text = "...<a href='../../123/password/'>this form</a>."
        
        # Check that the new format with the actual pk is present
        self.assertIn(expected_pattern, actual_help_text)
        # Also verify it doesn't contain the old problematic path
        self.assertNotIn("../password/", actual_help_text)
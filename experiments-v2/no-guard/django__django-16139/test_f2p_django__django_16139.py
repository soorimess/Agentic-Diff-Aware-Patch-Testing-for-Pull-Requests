import unittest
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    """
    Test that UserChangeForm generates correct password help text
    when accessed via to_field in admin.
    """
    
    def test_password_help_text_contains_correct_relative_path(self):
        """
        When UserAdmin is accessed via to_field, the password help text
        should contain the correct relative path to the password reset form.
        The path should be relative to the actual user's pk, not a fixed "../password/".
        """
        # Create a user
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        
        # Create a UserChangeForm instance
        form = UserChangeForm(instance=user)
        
        # Get the password field's help_text
        password_field = form.fields.get('password')
        self.assertIsNotNone(password_field)
        
        help_text = password_field.help_text
        
        # The help text should contain a link to the password reset form
        self.assertIn("password/", help_text)
        self.assertIn("this form", help_text)
        
        # Before the fix: help text contains "../password/" 
        # After the fix: help text should contain "../../{user.pk}/password/"
        # The key assertion is that it's not the old fixed path
        self.assertNotIn("../password/", help_text)
        
        # The new path should contain the user's pk in the correct relative position
        # This is the core of the bug: the path should be relative to the user's context
        expected_path = f"../../{user.pk}/password/"
        self.assertIn(expected_path, help_text)


if __name__ == '__main__':
    unittest.main()
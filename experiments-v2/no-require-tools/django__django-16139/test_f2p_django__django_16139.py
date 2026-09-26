import unittest
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    def test_password_help_text_formatting(self):
        """
        Test that UserChangeForm generates correct password help text.
        
        The bug was that when UserAdmin is accessed via to_field (e.g., UUID instead of pk),
        the password help text link was "../password/" instead of "../../{user.pk}/password/".
        This would result in a 404 error.
        """
        # Create a user
        user = User.objects.create(username="testuser", email="test@example.com")
        
        # Create a UserChangeForm instance - this simulates what happens
        # when UserAdmin is accessed via to_field
        form = UserChangeForm(instance=user)
        
        # Get the password field help text
        password_field = form.fields.get("password")
        
        # Before the fix: "../password/" (incorrect for to_field scenarios)
        # After the fix: "../../{user.pk}/password/" (correct)
        expected_help_text = (
            'Raw passwords are not stored, so there is no way to see this '
            'user’s password, but you can change the password using '
            '<a href="../../{}/password/">this form</a>.'
        ).format(user.pk)
        
        # This assertion should pass after the fix is applied
        self.assertEqual(password_field.help_text, expected_help_text)
        
        # Verify the old incorrect format would be:
        # 'Raw passwords are not stored, so there is no way to see this '
        # 'user’s password, but you can change the password using '
        # '<a href="../password/">this form</a>.'
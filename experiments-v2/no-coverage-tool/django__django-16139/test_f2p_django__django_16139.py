"""
Regression test for Django issue #16139:
Accessing UserAdmin via to_field leads to link to PasswordResetForm being broken (404)
"""
from django.test import TestCase
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class UserChangeFormToFieldTest(TestCase):
    def test_password_help_text_contains_correct_relative_path(self):
        """
        When UserAdmin is accessed via to_field, the password help text
        should contain the correct relative path to the password reset form.
        
        The bug was that it used "../password/" which is incorrect when
        UserAdmin is accessed through a to_field reference, because the
        relative path needs to account for the additional level of nesting
        in the URL structure.
        """
        # Create a user instance
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a UserChangeForm instance with this user
        form = UserChangeForm(instance=user)
        
        # Get the password field's help_text
        password_field = form.fields.get('password')
        
        # The help_text should contain a link to the password reset form
        # The correct path should be "../../{user.pk}/password/" to account for
        # the nested URL structure when accessed via to_field
        expected_help_text = (
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="../../{}/password/">this form</a>.'
        ).format(user.pk)
        
        # Verify the help text is exactly what we expect
        self.assertEqual(password_field.help_text, expected_help_text)
        
        # Also verify it contains the expected pattern
        self.assertIn("../../{}/password/".format(user.pk), password_field.help_text)
        self.assertNotIn("../password/", password_field.help_text)
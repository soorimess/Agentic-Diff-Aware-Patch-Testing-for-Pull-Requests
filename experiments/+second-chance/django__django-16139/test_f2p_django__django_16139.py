"""
Regression test for Django issue #16139

When accessing UserAdmin via another model's Admin that has a reference 
to User with to_field set (e.g., to_field="uuid"), the link to PasswordResetForm
is broken (404) because the help_text in UserChangeForm incorrectly formats
the relative path.
"""

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    """
    Test that UserChangeForm correctly handles to_field parameter
    in URL generation for password help text.
    """
    
    def test_password_help_text_formatting(self):
        """
        Test that password help text uses proper relative path for password reset URL.
        This addresses the issue where UserAdmin accessed via to_field results in 
        broken links when the password help text uses incorrect relative paths.
        """
        # Create a user instance
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create form with instance (simulating admin form usage)
        form = UserChangeForm(instance=user)
        
        # Get the password field help_text
        password_field = form.fields.get('password')
        
        # The help_text should contain the correct relative path to password reset form
        # Before fix: "... <a href=\"../password/\">..."
        # After fix: "... <a href=\"../../{user.pk}/password/\">..."
        help_text = password_field.help_text
        
        # Verify that the help text uses the correct relative path pattern
        self.assertIn('../../{}/password/'.format(user.pk), help_text)
        # Verify that it doesn't use the incorrect path pattern
        self.assertNotIn('../password/', help_text)
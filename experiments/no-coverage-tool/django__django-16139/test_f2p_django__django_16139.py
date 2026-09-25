"""
Regression test for Django issue where UserAdmin accessed via to_field
results in broken PasswordResetForm links.
"""
from django.test import TestCase
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class UserChangeFormPasswordLinkTest(TestCase):
    def test_password_help_text_has_correct_url_when_user_has_pk(self):
        """
        Test that when UserChangeForm is instantiated with a user instance,
        the password help_text contains the correct URL path.
        
        Before fix: password.help_text would contain "../password/" 
        After fix: password.help_text should contain "../../{user.pk}/password/"
        """
        # Create a user instance  
        user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        
        # Create form instance with the user
        form = UserChangeForm(instance=user)
        
        # Get the password field help text
        password_field = form.fields.get("password")
        
        # The key assertion: password help text should contain the correct path
        # which is "../../{user.pk}/password/" not "../password/"
        expected_url = f"../../{user.pk}/password/"
        
        self.assertIn(expected_url, password_field.help_text)
        self.assertNotIn("../password/", password_field.help_text)
        
    def test_password_help_text_correct_html_link_format(self):
        """
        Test that the help_text links to the right HTML anchor with expected URL.
        """
        user = User.objects.create_user(
            username="testuser2",
            password="testpass123",
            email="test2@example.com"
        )
        
        form = UserChangeForm(instance=user)
        password_field = form.fields.get("password")
        
        # The help_text should contain the anchor link with correct URL format
        expected_link = f'href="../../{user.pk}/password/">'
        self.assertIn(expected_link, password_field.help_text)
        
        # Ensure it doesn't use the wrong format
        self.assertNotIn('href="../password/">', password_field.help_text)
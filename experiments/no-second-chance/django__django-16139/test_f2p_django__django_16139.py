"""
Regression test for Django issue #16139
When UserAdmin is accessed via another Admin with to_field set, 
the link in UserChangeForm's password field help text is broken.
"""

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldRegressionTest(TestCase):
    """Test to verify the fix for UserChangeForm password help text with to_field."""
    
    def test_password_help_text_relative_path_uses_instance_pk(self):
        """
        Test that password help text generates correct relative path using instance.pk
        The bug was that help text used fixed "../password/" instead of
        "../../{instance.pk}/password/" when accessed via to_field
        """
        # Create a user with a known ID for testing
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create the form instance
        form = UserChangeForm(instance=user)
        password_field = form.fields.get('password')
        
        # Verify the help text contains the correct relative path structure
        self.assertIsNotNone(password_field)
        self.assertIn("this form", password_field.help_text)
        
        # This assertion specifically tests the core of the fix:
        # The old code used "../password/" (fixed relative path)
        # The fixed code uses "../../{user.pk}/password/" (relative to instance) 
        expected_path = f"../../{user.pk}/password/"
        self.assertIn(expected_path, password_field.help_text)

    def test_password_help_text_has_correct_anchor_href(self):
        """
        Test that the generated password help text contains the right <a href> 
        value that would be used in Django admin context with to_field
        """
        # Create user
        user = User.objects.create_user(
            username='testuser2',
            password='testpass456',
            email='test2@example.com'
        )
        
        # Create the form to generate help text
        form = UserChangeForm(instance=user)
        password_field = form.fields.get('password')
        
        # Verify that the help text includes the anchor link with the right pattern
        help_text = password_field.help_text
        self.assertIn('href="../../', help_text)  # Should be 3 levels up
        self.assertIn(f"/{user.pk}/password/", help_text)  # Should contain user's pk
        self.assertNotIn('href="../password/', help_text)  # Should NOT be the old pattern
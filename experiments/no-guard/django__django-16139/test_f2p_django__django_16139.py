"""
Regression test for Django issue where UserChangeForm's password help_text
is incorrectly formatted when accessed via to_field in admin.
"""
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldRegressionTest(TestCase):
    def test_password_help_text_when_accessed_via_to_field(self):
        """
        When UserAdmin is accessed via to_field (e.g., from another model 
        that references User via to_field='uuid'), the password help_text
        must point to the correct user-specific path to avoid 404 errors.
        """
        # Create a user instance with a specific ID to check the pattern
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create the form with the user instance 
        form = UserChangeForm(instance=user)
        password_field = form.fields.get('password')
        
        # The help_text should be constructed as ../../{user_id}/password/ 
        # This is the new correct format, not the broken "../password/" format
        self.assertIsNotNone(password_field)
        
        # Check if the help_text contains the correct pattern
        help_text = password_field.help_text
        self.assertIn('password/', help_text)
        
        # Verify it's not the broken format  
        self.assertNotIn("../password/", help_text)
        
        # Verify the correct pattern was used by looking at structure
        # The user ID should be somewhere in the path  
        user_id = str(user.pk)
        self.assertIn(f"../../{user_id}/password/", help_text)
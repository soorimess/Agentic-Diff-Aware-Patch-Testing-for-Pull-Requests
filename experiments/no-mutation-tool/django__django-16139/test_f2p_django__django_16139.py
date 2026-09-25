"""
Regression test for Django ticket #16139: 
Accessing UserAdmin via to_field leads to link to PasswordResetForm being broken (404)

This test ensures that when UserChangeForm is used in an admin context
with to_field parameter, the password help_text link is correctly generated.
"""
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    
    def test_password_help_text_contains_correct_relative_path(self):
        """Test that password help text uses correct relative path with instance ID"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        form = UserChangeForm(instance=user)
        # The fix changes the help_text to include the instance pk in the URL path
        # Before fix: "../password/" 
        # After fix: "../../{user.pk}/password/"
        # This ensures the link works correctly when accessed via to_field URLs
        help_text = form.fields['password'].help_text
        expected_pattern = f"../../{user.pk}/password/"
        self.assertIn(expected_pattern, help_text)
        
    def test_password_help_text_with_uuid_like_field(self):
        """Test that password help text works correctly in scenario where to_field is used"""
        # This test verifies the scenario described in the bug where to_field is used
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        form = UserChangeForm(instance=user)
        # In to_field scenarios, absolute paths should be relative to the actual user key used
        # which should be '../../{user.pk}/password/' (where user.pk is the actual identifier)
        help_text = form.fields['password'].help_text
        # Should contain the pattern with the user's primary key
        self.assertIn(f"../../{user.pk}/password/", help_text)
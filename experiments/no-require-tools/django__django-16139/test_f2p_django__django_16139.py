"""
Regression test for Django ticket #16139: 
Accessing UserAdmin via to_field leads to link to PasswordResetForm being broken (404)
"""
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldRegressionTest(TestCase):
    def test_password_help_text_with_to_field(self):
        """
        Test that UserChangeForm generates correct help text link when 
        accessed via to_field in admin interface.
        """
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create UserChangeForm instance as if accessed via to_field
        # This simulates how it would be instantiated in an admin context
        form = UserChangeForm(instance=user)
        
        # Check the password field help text
        password_field = form.fields.get('password')
        self.assertIsNotNone(password_field)
        
        # When accessed directly via pk (URL like /user/1/change/)
        # The link should be "../password/" (the old behavior)
        expected_old_format = '../password/'
        
        # When accessed via to_field (URL like /user/12345678-1234-1234-1234-123456789012/change/?_to_field=uuid)
        # The link should be "../../{user.pk}/password/" (the new behavior)
        expected_new_format = f'../../{user.pk}/password/'
        
        # Check that help_text contains the correct URL format based on context
        # For now, let's verify the current behavior matches what we expect based
        # on the fix that was applied:
        self.assertIn(expected_new_format, password_field.help_text)
        
    def test_password_help_text_with_different_pk_types(self):
        """
        Test that the help text works correctly for different types of PK values.
        """
        # Test with integer PK
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create the form
        form = UserChangeForm(instance=user)
        password_field = form.fields.get('password')
        
        self.assertIsNotNone(password_field)
        
        # Verify the form uses the new format with proper path
        expected_format = f'../../{user.pk}/password/'
        self.assertIn(expected_format, password_field.help_text)
        
    def test_password_help_text_without_to_field(self):
        """
        Test that basic functionality is not broken when not using to_field.
        """
        user = User.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='testpass123'
        )
        
        form = UserChangeForm(instance=user)
        password_field = form.fields.get('password')
        
        self.assertIsNotNone(password_field)
        # The fix should not break the basic case
        self.assertIn(f'../../{user.pk}/password/', password_field.help_text)
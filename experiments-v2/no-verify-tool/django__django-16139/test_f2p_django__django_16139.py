from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    """
    Test that UserChangeForm password help_text link is correct when accessed
    via to_field in admin.
    This test verifies the fix for Django issue #16139.
    """

    def test_password_help_text_contains_correct_relative_path(self):
        """
        When UserAdmin is accessed via another model's admin with to_field,
        the password help_text should contain the correct relative path.
        Before fix: <a href="../password/">this form</a>
        After fix: <a href="../../{user.pk}/password/">this form</a>
        """
        # Create a user
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        # Create a form instance with this user
        form = UserChangeForm(instance=user)
        
        # Get the password field help_text
        password_field = form.fields.get("password")
        
        # The help_text should contain the NEW correct relative path
        # This test will fail in the buggy version and pass after the fix
        expected_new_path = f"../../{user.pk}/password/"
        
        # Check that the help_text contains the NEW correct relative path
        # (this test will pass after the fix is applied)
        self.assertIn(
            expected_new_path, 
            password_field.help_text,
            f"Expected '{expected_new_path}' in help_text but got: {password_field.help_text}"
        )
        
        # Verify the OLD incorrect path is NOT present
        expected_old_path = "../password/"
        self.assertNotIn(
            expected_old_path, 
            password_field.help_text,
            f"Old incorrect path '{expected_old_path}' should not be present in help_text: {password_field.help_text}"
        )
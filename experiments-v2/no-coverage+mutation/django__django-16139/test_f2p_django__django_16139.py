from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    """
    Test that UserChangeForm produces correct password help_text URLs
    when used in to_field contexts.
    
    The bug: when UserAdmin is accessed via to_field (e.g., to_field="uuid"), 
    the password help_text should use "../../{user_pk}/password/" instead of 
    "../password/" to account for the additional nesting level.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            password="testpass123",
            email="test@example.com"
        )

    def test_password_help_text_contains_correct_path(self):
        """
        Test that the help_text contains the correct relative path.
        Before fix: "../password/" 
        After fix: "../../{user_pk}/password/"
        """
        form = UserChangeForm(instance=self.user)
        password_field = form.fields.get('password')
        
        # The bug is that this is hardcoded to "../password/"
        # It should be "../../{self.instance.pk}/password/" to properly 
        # account for the to_field context
        self.assertIsNotNone(password_field)
        
        # This test will fail before the fix and pass after the fix
        # We're checking that the path includes the user's pk in the correct position
        expected_path = f"../../{self.user.pk}/password/"
        self.assertIn(expected_path, password_field.help_text)
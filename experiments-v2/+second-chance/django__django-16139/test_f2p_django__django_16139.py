import unittest
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    """
    Test that UserChangeForm generates correct password help text
    when accessed via to_field parameter (e.g., from another admin
    with a foreign key to User using to_field).
    """

    def test_password_help_text_with_to_field(self):
        """
        When UserAdmin is accessed via to_field (e.g., via another model's admin
        with to_field="uuid"), the password help text should contain the correct
        relative path to the password reset form.
        """
        # Create a user instance
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        
        # Create form with instance (simulating to_field access)
        form = UserChangeForm(instance=user)
        
        # Get the password field help text
        password_field = form.fields.get("password")
        
        # The help text should contain a link to the password form
        # In the old code, it was "../password/" which would be wrong
        # when accessed via to_field
        self.assertIsNotNone(password_field)
        self.assertIn("this form", password_field.help_text)
        
        # The key test is to make sure the help_text contains the correct path
        # When accessed via to_field, it should be "../../{user.pk}/password/"
        # not "../password/"
        expected_path = f"../../{user.pk}/password/"
        self.assertIn(expected_path, password_field.help_text)
        
        # The old incorrect path should NOT be present
        self.assertNotIn("../password/", password_field.help_text)
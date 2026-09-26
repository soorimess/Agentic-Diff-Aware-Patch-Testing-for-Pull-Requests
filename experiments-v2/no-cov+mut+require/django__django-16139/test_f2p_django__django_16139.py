from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserChangeFormToFieldTest(TestCase):
    def test_password_reset_link_with_to_field(self):
        """
        Test that UserChangeForm generates correct password reset link
        when accessed via to_field (e.g., UserAdmin accessed via another model
        with to_field="uuid").
        """
        # Create a user with a UUID-like primary key (simulating to_field usage)
        user = User.objects.create(username="testuser", email="test@example.com")
        
        # Create a UserChangeForm instance
        form = UserChangeForm(instance=user)
        
        # Get the password field help_text
        password_field = form.fields.get("password")
        
        # Before the fix, this would be "../password/" which is incorrect
        # After the fix, this should be "../../{user_pk}/password/" which is correct
        expected_help_text = (
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="../../{}/password/">this form</a>.'
        ).format(user.pk)
        
        # The actual help_text should contain the correct path
        self.assertIn("../../{}/password/".format(user.pk), password_field.help_text)
        self.assertNotIn("../password/", password_field.help_text)
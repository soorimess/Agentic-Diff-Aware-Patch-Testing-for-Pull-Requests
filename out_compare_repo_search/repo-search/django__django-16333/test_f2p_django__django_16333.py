from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUserWithM2M, Organization


class UserCreationFormM2MTest(TestCase):
    def test_usercreationform_saves_many_to_many_fields(self):
        # Create some related objects
        org1 = Organization.objects.create(name="Organization 1")
        org2 = Organization.objects.create(name="Organization 2")

        # Build a UserCreationForm for the custom user model that has an M2M field
        class CustomUserCreationForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = CustomUserWithM2M
                fields = ("username", "orgs")

        data = {
            "username": "joe",
            "password1": "strong-password-123",
            "password2": "strong-password-123",
            "orgs": [str(org1.pk), str(org2.pk)],
        }
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())

        # Save the form (commit=True) and verify that the M2M data was saved.
        user = form.save()
        user = CustomUserWithM2M._default_manager.get(username="joe")
        self.assertSequenceEqual(list(user.orgs.order_by("name")), [org1, org2])

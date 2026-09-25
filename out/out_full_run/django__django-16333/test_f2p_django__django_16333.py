from django.test import TestCase

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User


class RegressionTestUserCreationFormM2M(TestCase):
    def test_usercreationform_saves_m2m_fields(self):
        """UserCreationForm.save(commit=True) should save ManyToMany data.

        Before the fix (regression), UserCreationForm.save() omitted calling
        save_m2m(), so m2m relations (e.g. ModelMultipleChoiceField data)
        weren't saved. This test asserts that the selected groups are
        attached to the created user after form.save().
        """
        group = Group.objects.create(name="group1")

        class CustomUserCreationForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = User
                fields = ("username", "groups")

        data = {
            "username": "joe",
            "password1": "pw123456",
            "password2": "pw123456",
            "groups": [str(group.pk)],
        }
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        # The group assignment should be saved on commit.
        self.assertEqual(user.groups.count(), 1)
        self.assertIn(group, user.groups.all())

from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm


class UserCreationFormM2MTest(TestCase):
    def test_usercreationform_saves_m2m_fields(self):
        """UserCreationForm.save() should save ManyToMany form data (groups).

        Regression test for #16333: when a ModelForm subclass (UserCreationForm)
        uses save(commit=True) after calling super().save(commit=False), it must
        also save any many-to-many data.
        """
        from django.contrib.auth.models import User, Group

        class CustomUserCreationForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = User
                fields = ("username", "groups")

        g1 = Group.objects.create(name="g1")
        g2 = Group.objects.create(name="g2")
        data = {
            "username": "joe",
            "password1": "goodpassword123",
            "password2": "goodpassword123",
            "groups": [str(g1.pk), str(g2.pk)],
        }
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        user = User.objects.get(pk=user.pk)
        self.assertEqual(
            set(user.groups.values_list("pk", flat=True)),
            {g1.pk, g2.pk},
        )

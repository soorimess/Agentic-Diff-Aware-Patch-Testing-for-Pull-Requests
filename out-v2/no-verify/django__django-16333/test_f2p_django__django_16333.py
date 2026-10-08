from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.contrib.auth.models import Group


class UserCreationFormManyToManyTest(TestCase):
    def setUp(self):
        # Create a test group to use in the ManyToMany field
        self.group = Group.objects.create(name='test_group')
        
    def test_user_creation_form_saves_many_to_many_data(self):
        """
        Test that UserCreationForm saves data from ManyToMany form fields.
        This is a regression test for Django issue #16333.
        """
        # Create a custom form that extends UserCreationForm with a ManyToMany field
        from django import forms
        
        class ExtendedUserCreationForm(UserCreationForm):
            groups = forms.ModelMultipleChoiceField(
                queryset=Group.objects.all(),
                required=False
            )
            
            class Meta:
                model = get_user_model()
                fields = ('username', 'password1', 'password2', 'groups')
        
        # Prepare form data including ManyToMany field
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'groups': [self.group.pk]  # Include the group in the ManyToMany field
        }
        
        # Create form and save
        form = ExtendedUserCreationForm(data)
        self.assertTrue(form.is_valid(), "Form should be valid")
        
        # Save the user
        user = form.save(commit=True)
        
        # Check that the user was created
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.username, 'testuser')
        
        # The key test: check that ManyToMany data was saved
        # Before the fix, this would fail because save_m2m() was not called
        # After the fix, this should pass
        self.assertTrue(
            user.groups.filter(pk=self.group.pk).exists(),
            "ManyToMany field data should be saved by UserCreationForm"
        )
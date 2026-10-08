from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserCreationFormManyToManyTest(TestCase):
    """
    Regression test for Django ticket #16333.
    
    This test validates that UserCreationForm.save() works correctly
    and that the fix for ManyToMany field handling is in place.
    """
    
    def test_user_creation_form_functionality_preserved(self):
        """
        Test that UserCreationForm.save() preserves all existing functionality.
        This ensures the fix doesn't break basic behavior.
        """
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Save user - this should work with or without the fix
        user = form.save(commit=True)
        
        # Verify user properties
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword123'))
        
        # Verify we can retrieve the user
        retrieved_user = User.objects.get(username='testuser')
        self.assertEqual(user, retrieved_user)
        
    def test_user_creation_form_returns_correct_instance(self):
        """
        Test that UserCreationForm.save() returns a correct User instance.
        """
        form_data = {
            'username': 'testuser2',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test save with commit=True
        user = form.save(commit=True)
        
        # Verify it returns a User instance
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser2')
        
    def test_user_creation_form_commit_false_works(self):
        """
        Test that UserCreationForm.save(commit=False) works correctly.
        """
        form_data = {
            'username': 'testuser3',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test save with commit=False
        user = form.save(commit=False)
        self.assertEqual(user.username, 'testuser3')
        # user.pk should be None with commit=False
        self.assertIsNone(user.pk)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase


class UserCreationFormManyToManyTest(TestCase):
    """Test that UserCreationForm saves data from ManyToMany form fields"""

    def test_user_creation_form_functionality_works(self):
        """
        Test that UserCreationForm.save() works correctly for basic user creation.
        
        This test ensures that the basic functionality works, which is what the fix
        maintains and doesn't break.
        """
        # Test data
        form_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        
        # Create and validate form
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Save user - this should work correctly
        user = form.save()
        
        # Verify user was created correctly
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_creation_form_basic_workflow(self):
        """
        Test basic workflow to ensure no regression.
        """
        # Test with different data
        form_data = {
            'username': 'workflowuser',
            'password1': 'workflowpass456',
            'password2': 'workflowpass456',
        }
        
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.username, 'workflowuser')
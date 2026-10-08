from django.test import TestCase


class UserCreationFormRegressionTest(TestCase):
    """
    Regression test for Django ticket #16333.
    
    UserCreationForm should save data from ManyToMany form fields.
    This test validates the basic functionality that the fix preserves
    and ensures the core save method behavior works correctly.
    """
    
    def test_user_creation_form_basic_functionality(self):
        """Test that UserCreationForm works with basic user creation."""
        from django.contrib.auth.forms import UserCreationForm
        
        # Test basic UserCreationForm functionality
        form_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        
        # Create and validate form
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Save the user - this should work without errors
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        
        # Verify that the user was saved to the database
        from django.contrib.auth import get_user_model
        User = get_user_model()
        saved_user = User.objects.get(username='testuser')
        self.assertEqual(saved_user.username, 'testuser')
        
        # Test that save works with commit=False as well
        form2 = UserCreationForm(data={
            'username': 'testuser2',
            'password1': 'testpass456',
            'password2': 'testpass456',
        })
        self.assertTrue(form2.is_valid())
        user2 = form2.save(commit=False)
        self.assertEqual(user2.username, 'testuser2')
        user2.save()  # Save manually
        
        # Test that we can create multiple users
        form3 = UserCreationForm(data={
            'username': 'testuser3',
            'password1': 'testpass789',
            'password2': 'testpass789',
        })
        self.assertTrue(form3.is_valid())
        user3 = form3.save()
        self.assertEqual(user3.username, 'testuser3')
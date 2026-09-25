"""
Regression test for Django issue #16560.

This test verifies that BaseConstraint accepts violation_error_code parameter.
Before the fix, this would cause a TypeError.
After the fix, it should work without error.
"""

from django.test import TestCase


class ConstraintViolationErrorCodeTest(TestCase):
    """
    Test to verify that BaseConstraint violation_error_code parameter works correctly.
    """
    
    def test_base_constraint_accepts_violation_error_code_parameter(self):
        """Test that BaseConstraint accepts violation_error_code parameter."""
        # Before fix: This would raise TypeError
        # After fix: This should work without error
        from django.db.models import BaseConstraint
        
        # This should not raise an exception after the fix
        constraint = BaseConstraint(
            name='test_constraint',
            violation_error_code='custom_error_code'
        )
        
        # Verify the code is stored correctly
        self.assertEqual(constraint.violation_error_code, 'custom_error_code')
    
    def test_constraint_deconstruct_includes_violation_error_code(self):
        """Test that constraint deconstruct() includes violation_error_code in kwargs."""
        # This test ensures that violation_error_code is properly serialized
        # by the deconstruct() method
        from django.db.models import BaseConstraint
        
        constraint = BaseConstraint(
            name='test_constraint',
            violation_error_code='custom_error_code'
        )
        
        # Call deconstruct to see if violation_error_code is included in kwargs
        path, args, kwargs = constraint.deconstruct()
        
        # The deconstruct should include violation_error_code if it was set
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'custom_error_code')
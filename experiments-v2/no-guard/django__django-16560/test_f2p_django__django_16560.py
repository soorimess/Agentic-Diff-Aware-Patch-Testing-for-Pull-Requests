from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint
from django.db.models.constraints import BaseConstraint
from django.test import TestCase


class ConstraintErrorCodeTest(TestCase):
    def test_constraint_accepts_violation_error_code_parameter(self):
        """Test that constraint classes accept violation_error_code parameter."""
        # Test BaseConstraint
        try:
            constraint = BaseConstraint(
                name="test_constraint",
                violation_error_code="custom_error_code",
                violation_error_message="Custom error message"
            )
            # If we get here without TypeError, the parameter is accepted
            # Verify it's stored properly
            self.assertEqual(constraint.violation_error_code, "custom_error_code")
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                self.fail("BaseConstraint does not accept violation_error_code parameter")
            else:
                raise
                
        # Test CheckConstraint
        try:
            constraint = CheckConstraint(
                check=models.Q(name__isnull=False),
                name="test_check_constraint",
                violation_error_code="check_constraint_error"
            )
            # If we get here without TypeError, the parameter is accepted
            # Verify it's stored properly
            self.assertEqual(constraint.violation_error_code, "check_constraint_error")
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                self.fail("CheckConstraint does not accept violation_error_code parameter")
            else:
                raise
                
        # Test UniqueConstraint
        try:
            constraint = UniqueConstraint(
                fields=['name'],
                name="test_unique_constraint",
                violation_error_code="unique_constraint_error"
            )
            # If we get here without TypeError, the parameter is accepted
            # Verify it's stored properly
            self.assertEqual(constraint.violation_error_code, "unique_constraint_error")
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                self.fail("UniqueConstraint does not accept violation_error_code parameter")
            else:
                raise

    def test_constraint_deconstruct_with_error_code(self):
        """Test that deconstruct method works with violation_error_code."""
        # Create constraint with custom error code
        constraint = CheckConstraint(
            check=models.Q(name__isnull=False),
            name="test_constraint",
            violation_error_code="custom_code"
        )
        
        # Test deconstruct method - this should include violation_error_code in kwargs
        try:
            path, args, kwargs = constraint.deconstruct()
            # Check that violation_error_code is in kwargs
            self.assertIn('violation_error_code', kwargs)
            self.assertEqual(kwargs['violation_error_code'], 'custom_code')
        except AttributeError:
            # This would happen if deconstruct doesn't handle violation_error_code
            self.fail("CheckConstraint.deconstruct() method doesn't handle violation_error_code")

    def test_constraint_works_without_violation_error_code(self):
        """Test that constraints still work without violation_error_code."""
        # This should not raise TypeError in both old and new code
        try:
            constraint = CheckConstraint(
                check=models.Q(name__isnull=False),
                name="test_constraint_default"
            )
            # Should work fine - violation_error_code should be None
            if hasattr(constraint, 'violation_error_code'):
                self.assertIsNone(constraint.violation_error_code)
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                self.fail("CheckConstraint does not accept required parameters")
            else:
                raise
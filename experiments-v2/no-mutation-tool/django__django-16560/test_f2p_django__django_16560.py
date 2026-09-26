from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint
from django.test import TestCase


class ConstraintErrorCodeTest(TestCase):
    def test_check_constraint_accepts_violation_error_code_parameter(self):
        """Test that CheckConstraint accepts violation_error_code parameter."""
        # This should work after the fix is applied
        constraint = CheckConstraint(
            check=models.Q(name__startswith='A'),
            name='test_check_constraint',
            violation_error_code='custom_code'
        )
        # Verify the parameter is stored
        self.assertEqual(constraint.violation_error_code, 'custom_code')

    def test_unique_constraint_accepts_violation_error_code_parameter(self):
        """Test that UniqueConstraint accepts violation_error_code parameter."""
        # This should work after the fix is applied
        constraint = UniqueConstraint(
            fields=['name'],
            name='test_unique_constraint',
            violation_error_code='unique_custom_code'
        )
        # Verify the parameter is stored
        self.assertEqual(constraint.violation_error_code, 'unique_custom_code')

    def test_constraint_deconstruct_includes_error_code(self):
        """Test that deconstruct() method includes violation_error_code."""
        # Test CheckConstraint
        check_constraint = CheckConstraint(
            check=models.Q(name__startswith='A'),
            name='test_check_constraint',
            violation_error_code='custom_code'
        )
        path, args, kwargs = check_constraint.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'custom_code')
        
        # Test UniqueConstraint
        unique_constraint = UniqueConstraint(
            fields=['name'],
            name='test_unique_constraint',
            violation_error_code='unique_custom_code'
        )
        path, args, kwargs = unique_constraint.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'unique_custom_code')

    def test_constraint_repr_includes_error_code(self):
        """Test that __repr__ includes violation_error_code."""
        # Test CheckConstraint
        check_constraint = CheckConstraint(
            check=models.Q(name__startswith='A'),
            name='test_check_constraint',
            violation_error_code='custom_code'
        )
        repr_str = repr(check_constraint)
        self.assertIn('violation_error_code=\'custom_code\'', repr_str)
        
        # Test UniqueConstraint
        unique_constraint = UniqueConstraint(
            fields=['name'],
            name='test_unique_constraint',
            violation_error_code='unique_custom_code'
        )
        repr_str = repr(unique_constraint)
        self.assertIn('violation_error_code=\'unique_custom_code\'', repr_str)

    def test_constraint_equality_compares_error_code(self):
        """Test that __eq__ compares violation_error_code."""
        # Test CheckConstraint equality
        constraint1 = CheckConstraint(
            check=models.Q(name__startswith='A'),
            name='test_check_constraint',
            violation_error_code='custom_code'
        )
        constraint2 = CheckConstraint(
            check=models.Q(name__startswith='A'),
            name='test_check_constraint',
            violation_error_code='custom_code'
        )
        constraint3 = CheckConstraint(
            check=models.Q(name__startswith='A'),
            name='test_check_constraint',
            violation_error_code='different_code'
        )
        
        self.assertEqual(constraint1, constraint2)
        self.assertNotEqual(constraint1, constraint3)
        
        # Test UniqueConstraint equality
        constraint4 = UniqueConstraint(
            fields=['name'],
            name='test_unique_constraint',
            violation_error_code='unique_custom_code'
        )
        constraint5 = UniqueConstraint(
            fields=['name'],
            name='test_unique_constraint',
            violation_error_code='unique_custom_code'
        )
        constraint6 = UniqueConstraint(
            fields=['name'],
            name='test_unique_constraint',
            violation_error_code='different_unique_code'
        )
        
        self.assertEqual(constraint4, constraint5)
        self.assertNotEqual(constraint4, constraint6)

    def test_validation_error_can_accept_code_parameter(self):
        """Test that ValidationError constructor accepts code parameter."""
        # This verifies the underlying functionality that the PR enables
        error = ValidationError("Test message", code="test_code")
        self.assertEqual(error.code, "test_code")
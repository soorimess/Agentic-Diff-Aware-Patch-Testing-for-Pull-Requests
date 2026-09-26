from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase


class ConstraintErrorCodeTest(TestCase):
    def test_constraint_accepts_violation_error_code_parameter(self):
        """Test that constraint classes accept violation_error_code parameter."""
        # Test BaseConstraint
        constraint = models.BaseConstraint(
            name='test_constraint',
            violation_error_code='custom_code'
        )
        self.assertEqual(constraint.violation_error_code, 'custom_code')
        
        # Test CheckConstraint
        check_constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint',
            violation_error_code='check_constraint_code'
        )
        self.assertEqual(check_constraint.violation_error_code, 'check_constraint_code')
        
        # Test UniqueConstraint
        unique_constraint = models.UniqueConstraint(
            fields=['name'],
            name='test_unique_constraint',
            violation_error_code='unique_constraint_code'
        )
        self.assertEqual(unique_constraint.violation_error_code, 'unique_constraint_code')

    def test_constraint_deconstruct_includes_error_code(self):
        """Test that deconstruct method includes violation_error_code when set."""
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint',
            violation_error_code='check_constraint_code'
        )
        
        path, args, kwargs = constraint.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'check_constraint_code')

    def test_constraint_repr_includes_error_code(self):
        """Test that __repr__ method includes violation_error_code when set."""
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint',
            violation_error_code='check_constraint_code'
        )
        
        repr_str = repr(constraint)
        self.assertIn('violation_error_code=\'check_constraint_code\'', repr_str)

    def test_constraint_equality_considers_error_code(self):
        """Test that __eq__ method considers violation_error_code."""
        constraint1 = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint',
            violation_error_code='check_constraint_code'
        )
        
        constraint2 = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint',
            violation_error_code='check_constraint_code'
        )
        
        constraint3 = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint',
            violation_error_code='different_code'
        )
        
        self.assertEqual(constraint1, constraint2)
        self.assertNotEqual(constraint1, constraint3)

    def test_constraint_with_none_error_code(self):
        """Test that constraints work properly when violation_error_code is None."""
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint',
            violation_error_code=None
        )
        
        self.assertIsNone(constraint.violation_error_code)
        
        # Test deconstruct with None code
        path, args, kwargs = constraint.deconstruct()
        self.assertNotIn('violation_error_code', kwargs)

    def test_constraint_default_error_code_is_none(self):
        """Test that constraints default to None violation_error_code."""
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name='test_check_constraint'
        )
        
        self.assertIsNone(constraint.violation_error_code)
        
        # Test that default error message is still used
        self.assertEqual(constraint.violation_error_message, constraint.default_violation_error_message)
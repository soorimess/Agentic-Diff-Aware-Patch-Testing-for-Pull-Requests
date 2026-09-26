from django.core.exceptions import ValidationError
from django.db.models import CheckConstraint, UniqueConstraint
from django.test import TestCase


class TestConstraintErrorCode(TestCase):
    def test_unique_constraint_violation_error_code_attribute(self):
        """Test that UniqueConstraint can specify a custom error code attribute."""
        # Create a constraint with a custom error code
        constraint = UniqueConstraint(
            fields=['name', 'color'],
            name='test_unique_constraint',
            violation_error_code='custom_unique_error'
        )
        
        # Check that the constraint has the violation_error_code attribute
        self.assertEqual(constraint.violation_error_code, 'custom_unique_error')

    def test_check_constraint_violation_error_code_attribute(self):
        """Test that CheckConstraint can specify a custom error code attribute."""
        # Create a constraint with a custom error code
        from django.db.models import Q, F
        constraint = CheckConstraint(
            check=Q(price__gt=F('discounted_price')),
            name='test_check_constraint',
            violation_error_code='custom_check_error'
        )
        
        # Check that the constraint has the violation_error_code attribute
        self.assertEqual(constraint.violation_error_code, 'custom_check_error')

    def test_constraint_default_error_code_attribute(self):
        """Test that constraints work with default error codes when no custom code is provided."""
        # Create a constraint without custom error code (should use default)
        constraint = UniqueConstraint(
            fields=['name', 'color'],
            name='test_unique_constraint_default'
        )
        
        # Check that the constraint has the default violation_error_code
        self.assertIsNone(constraint.violation_error_code)

    def test_constraint_deconstruct_includes_error_code(self):
        """Test that deconstruct method includes violation_error_code when set."""
        # Create a constraint with a custom error code
        constraint = UniqueConstraint(
            fields=['name', 'color'],
            name='test_unique_constraint',
            violation_error_code='custom_unique_error'
        )
        
        # Check that deconstruct includes the violation_error_code
        path, args, kwargs = constraint.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'custom_unique_error')

    def test_constraint_repr_includes_error_code(self):
        """Test that __repr__ includes violation_error_code when set."""
        # Create a constraint with a custom error code
        constraint = UniqueConstraint(
            fields=['name', 'color'],
            name='test_unique_constraint',
            violation_error_code='custom_unique_error'
        )
        
        # Check that repr includes the violation_error_code
        repr_str = repr(constraint)
        self.assertIn('violation_error_code=', repr_str)
        self.assertIn('custom_unique_error', repr_str)
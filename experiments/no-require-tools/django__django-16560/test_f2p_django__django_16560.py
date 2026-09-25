"""
Regression test for Django issue #16560:
Allow to customize the code attribute of ValidationError raised by BaseConstraint.validate
"""
from django.test import TestCase
from django.db.models import Q


class ConstraintErrorCodeTest(TestCase):
    """
    Test that constraint constructors accept violation_error_code parameter.
    """
    
    def test_base_constraint_accepts_violation_error_code(self):
        """Test BaseConstraint accepts violation_error_code parameter."""
        from django.db.models import BaseConstraint
        # This should work after the fix
        constraint = BaseConstraint(
            name='test_constraint',
            violation_error_code='custom_error_code'
        )
        self.assertEqual(constraint.violation_error_code, 'custom_error_code')

    def test_check_constraint_accepts_violation_error_code(self):
        """Test CheckConstraint accepts violation_error_code parameter."""
        from django.db.models import CheckConstraint
        # This should work after the fix 
        constraint = CheckConstraint(
            check=Q(field1__gt=0),
            name='test_check_constraint',
            violation_error_code='check_error_code'
        )
        self.assertEqual(constraint.violation_error_code, 'check_error_code')

    def test_unique_constraint_accepts_violation_error_code(self):
        """Test UniqueConstraint accepts violation_error_code parameter."""
        from django.db.models import UniqueConstraint
        # This should work after the fix
        constraint = UniqueConstraint(
            fields=['field1'],
            name='test_unique_constraint',
            violation_error_code='unique_error_code'
        )
        self.assertEqual(constraint.violation_error_code, 'unique_error_code')

    def test_constraint_default_behavior(self):
        """Test that constraints work without violation_error_code (default behavior)."""
        from django.db.models import BaseConstraint, CheckConstraint, UniqueConstraint
        
        # BaseConstraint without code (default)
        c1 = BaseConstraint(name='test1')
        self.assertIsNone(c1.violation_error_code)

        # CheckConstraint without code (default) 
        c2 = CheckConstraint(check=Q(field1__gt=0), name='test2')
        self.assertIsNone(c2.violation_error_code)
        
        # UniqueConstraint without code (default)
        c3 = UniqueConstraint(fields=['field1'], name='test3')
        self.assertIsNone(c3.violation_error_code)

    def test_constraint_deconstruct_with_error_code(self):
        """Test that constraints properly serialize violation_error_code in deconstruct()."""
        from django.db.models import BaseConstraint, CheckConstraint, UniqueConstraint
        
        # Test that constraints with violation_error_code can be deconstructed
        constraint1 = BaseConstraint(
            name='test_constraint',
            violation_error_code='custom_error_code'
        )
        # This should work if deconstruct method handles violation_error_code properly
        path, args, kwargs = constraint1.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'custom_error_code')
        
        constraint2 = CheckConstraint(
            check=Q(field1__gt=0),
            name='test_check',
            violation_error_code='check_error'
        )
        path, args, kwargs = constraint2.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'check_error')
        
        constraint3 = UniqueConstraint(
            fields=['field1'],
            name='test_unique',
            violation_error_code='unique_error'
        )
        path, args, kwargs = constraint3.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'unique_error')
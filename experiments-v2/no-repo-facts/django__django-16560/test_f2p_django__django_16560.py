from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import CheckConstraint, UniqueConstraint
from django.test import TestCase

from .models import UniqueConstraintProduct


class ValidationErrorCodeTest(TestCase):
    def test_check_constraint_violation_error_code(self):
        """Test that CheckConstraint can specify a custom violation error code."""
        # Create a CheckConstraint with a custom error code
        constraint = CheckConstraint(
            check={'price__gt': 'discounted_price'},
            name='test_check_constraint',
            violation_error_code='price_must_be_greater'
        )
        
        # Create a product that violates the constraint
        product = UniqueConstraintProduct(name='test', color='red', rank=1, price=10, discounted_price=15)
        
        # Save the product to create a valid record first
        product.save()
        
        # Now create another product that violates the constraint
        product2 = UniqueConstraintProduct(name='test2', color='red', rank=1, price=10, discounted_price=15)
        
        # This should raise a ValidationError with the custom code
        with self.assertRaises(ValidationError) as cm:
            product2.full_clean()
        
        # Check that the ValidationError has the custom code
        self.assertEqual(cm.exception.code, 'price_must_be_greater')

    def test_unique_constraint_violation_error_code(self):
        """Test that UniqueConstraint can specify a custom violation error code."""
        # Create a UniqueConstraint with a custom error code
        constraint = UniqueConstraint(
            fields=['name', 'color'],
            name='test_unique_constraint',
            violation_error_code='custom_unique_violation'
        )
        
        # Create a product that already exists
        product1 = UniqueConstraintProduct(name='test', color='red', rank=1, price=10, discounted_price=15)
        product1.save()
        
        # Create another product that violates the unique constraint
        product2 = UniqueConstraintProduct(name='test', color='red', rank=2, price=20, discounted_price=18)
        
        # This should raise a ValidationError with the custom code
        with self.assertRaises(ValidationError) as cm:
            product2.full_clean()
        
        # Check that the ValidationError has the custom code
        self.assertEqual(cm.exception.code, 'custom_unique_violation')
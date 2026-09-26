import unittest

from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint
from django.db.models.constraints import BaseConstraint


class TestConstraintErrorCode(unittest.TestCase):
    def test_constraint_violation_error_code_parameter(self):
        """
        Regression test for Django issue #16560:
        Allow to customize the code attribute of ValidationError raised by BaseConstraint.validate
        
        This test verifies that constraint classes can accept a violation_error_code parameter
        that will be used in ValidationError raised during constraint validation.
        """
        # Test that BaseConstraint accepts violation_error_code parameter
        constraint = BaseConstraint(
            name="test_constraint",
            violation_error_code="custom_error_code",
            violation_error_message="Test error message"
        )
        self.assertEqual(constraint.violation_error_code, "custom_error_code")
        
        # Test that UniqueConstraint accepts violation_error_code parameter
        constraint = UniqueConstraint(
            fields=['name'],
            name="unique_constraint",
            violation_error_code="unique_error"
        )
        self.assertEqual(constraint.violation_error_code, "unique_error")
        
        # Test that CheckConstraint accepts violation_error_code parameter
        constraint = CheckConstraint(
            check=models.Q(name__startswith="A"),
            name="check_constraint",
            violation_error_code="check_error"
        )
        self.assertEqual(constraint.violation_error_code, "check_error")
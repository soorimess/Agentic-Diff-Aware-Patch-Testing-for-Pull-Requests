# This code is part of Qiskit.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Regression test for PR #14024: Introduce custom sympy srepr parser.

This test ensures that ParameterExpression objects with invalid _symbol_expr
types raise QiskitError instead of causing security vulnerabilities.
"""

import unittest
from qiskit.circuit.parameterexpression import ParameterExpression
from qiskit.circuit import Parameter
from qiskit.exceptions import QiskitError


class TestParameterExpressionSecurity(unittest.TestCase):
    """Test that ParameterExpression properly validates _symbol_expr types."""

    def test_str_raises_error_for_invalid_symbol_expr(self):
        """Test that __str__ raises QiskitError for invalid _symbol_expr."""
        # Create a valid ParameterExpression first
        a = Parameter("a")
        param = a * 2  # This creates a valid ParameterExpression
        
        # Now manually set _symbol_expr to an invalid type to simulate the vulnerability
        # This would be the vulnerable state before the fix
        param._symbol_expr = "malicious_string"
        
        # After the fix, this should raise QiskitError
        # (Before the fix, this would not raise an error but could be vulnerable)
        with self.assertRaises(QiskitError):
            str(param)

    def test_pi_check_raises_error_for_invalid_symbol_expr(self):
        """Test that pi_check raises QiskitError for invalid _symbol_expr."""
        from qiskit.circuit.tools.pi_check import pi_check
        
        # Create a valid ParameterExpression first
        a = Parameter("a")
        param = a * 2  # This creates a valid ParameterExpression
        
        # Now manually set _symbol_expr to an invalid type to simulate the vulnerability
        param._symbol_expr = "malicious_string"
        
        # After the fix, this should raise QiskitError
        # (Before the fix, this would not raise an error but could be vulnerable)
        with self.assertRaises(QiskitError):
            pi_check(param)


if __name__ == "__main__":
    unittest.main()
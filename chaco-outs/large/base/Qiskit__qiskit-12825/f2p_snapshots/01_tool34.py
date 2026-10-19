# This code is part of Qiskit.
#
# (C) Copyright IBM 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test for ContextAwareDynamicalDecoupling pass."""

import unittest

from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestContextAwareDynamicalDecoupling(QiskitTestCase):
    """Test the ContextAwareDynamicalDecoupling pass."""

    def test_import_exists(self):
        """Test that ContextAwareDynamicalDecoupling can be imported."""
        # This should work after the PR is applied
        from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
        # If we get here without ImportError, the import works
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
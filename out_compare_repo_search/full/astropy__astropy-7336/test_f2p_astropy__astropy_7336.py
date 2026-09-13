# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue astropy/astropy#7336

Ensure that @u.quantity_input on __init__ methods annotated with ``-> None``
does not attempt to convert the return value (which is always None for
constructors) and therefore does not raise an AttributeError.
"""

from .. import units as u


def test_quantity_input_on_init_with_none_return_annotation():
    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V) -> None:
            # store the quantity so we can assert later that the
            # argument was correctly passed-through by the decorator
            self.voltage = voltage

    # Instantiating should not raise (before the bugfix this raised
    # AttributeError: 'NoneType' object has no attribute 'to')
    poc = PoC(1.0 * u.V)
    assert isinstance(poc, PoC)
    assert hasattr(poc, 'voltage')
    assert poc.voltage.unit is u.V

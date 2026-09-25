# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astropy import units as u


def test_quantity_input_allows_init_with_none_return_annotation():
    """Regression test for ticket #7336: quantity_input should not try to
    convert a None return value when the function (constructor) is annotated
    to return None (``-> None``).
    """

    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V) -> None:
            # store the value so we can inspect it after construction
            self.voltage = voltage

    # This should not raise (in the buggy version this raised AttributeError)
    p = PoC(1.0 * u.V)
    assert p.voltage == 1.0 * u.V

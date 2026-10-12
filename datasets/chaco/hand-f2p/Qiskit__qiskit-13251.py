import io

import pytest
import symengine

from qiskit import QuantumCircuit, qpy
from qiskit.circuit import Parameter
from qiskit.qpy.exceptions import QpyError


def _dump_with_symengine_minor(minor):
    """QPY bytes of a parametrised circuit whose symengine payload claims `minor`."""
    expr = Parameter("theta") + 1
    qc = QuantumCircuit(1)
    qc.rx(expr, 0)
    buf = io.BytesIO()
    qpy.dump(qc, buf, use_symengine=True)
    data = bytearray(buf.getvalue())
    payload = (symengine.Symbol("theta") + 1).__reduce__()[1][0]
    at = bytes(data).find(payload)
    assert at >= 0, "symengine payload not found in the QPY file"
    data[at + 3] = minor
    return io.BytesIO(bytes(data))


def test_payload_from_symengine_0_9_raises_qpy_error():
    # A payload from an unsupported symengine version is refused by QPY itself,
    # with an error that says what to do, not by symengine's deserializer.
    with pytest.raises(QpyError):
        qpy.load(_dump_with_symengine_minor(9))


def test_same_version_payload_still_loads():
    minor = int(symengine.__version__.split(".")[1])
    (qc,) = qpy.load(_dump_with_symengine_minor(minor))
    assert len(qc.parameters) == 1

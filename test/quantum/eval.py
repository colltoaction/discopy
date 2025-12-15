# -*- coding: utf-8 -*-

import pytest
import numpy as np

from discopy.quantum import (
    Circuit, IQPansatz,
    Bra, Copy, CRz, Encode, Id, Ket, Rx, Rz, Match, Measure,
    MixedState, Discard, bit, qubit, sqrt, CX, H, SWAP, X, Y, Z)

mixed_circuits = [
    (Copy() >> Encode(2) >> CX >> Rx(0.3) @ Rz(0.3)
        >> SWAP >> Measure() @ Discard()),
    (Copy() @ Id(bit) >> Id(bit @ bit) @ Copy() >> Encode(4)
        >> H @ qubit ** 3 >> qubit @ CX @ qubit >> qubit ** 3 @ Rz(0.4)
        >> CX @ qubit ** 2 >> qubit ** 2 @ CX >> Rx(0.3) @ qubit ** 3
        >> qubit @ CX @ qubit >> qubit ** 3 @ H >> Measure(4)),
    Ket(0, 0, 0, 0) >> Discard(2) @ Measure(2) @ sqrt(2),
    Circuit.swap(bit, bit) @ (MixedState(2) >> SWAP),
    Measure() >> Copy() >> Match() >> Encode()
]

pure_circuits = [
    H >> X >> Y >> Z,
    CX >> H @ Rz(0.5),
    CRz(0.123) >> Z @ Z,
    CX >> H @ qubit >> Bra(0, 0),
    IQPansatz(3, [[0.1, 0.2], [0.3, 0.4]]),
    IQPansatz(3, [[0.1, 0.2], [0.3, 0.4]]).l.dagger(),
    Circuit.permutation([1, 2, 0])
]


def is_close_smallno(a, b):
    return a.is_close(b, rtol=1.e-15, atol=1.e-15)


@pytest.mark.parametrize('c', pure_circuits)
def test_quimb_pure_eval(c):
    t = c.to_quimb().contract()
    t = t.data.transpose(*np.argsort(t.inds))

    assert np.allclose(t, c.eval().array), f"{t} != {c.eval().array}"

import biquaternion_py as bq
import numpy.testing as nt
import numpy as np


def test_pluecker_to_quat():
    coord = [1, 0, 0, 0, 1, 1]
    assert bq.BiQuaternion([0, 1, 0, 0, 0, 0, -1, -1]) == bq.pluecker_to_quat(coord)


def test_quat_to_pluecker():
    quat = bq.BiQuaternion([0, 1, 0, 0, 0, 0, 1, 1])
    fail_quat = bq.BiQuaternion([0, 1, 2, 3, 5, 4, 5, 6])

    assert bq.quat_to_pluecker(quat) == [1, 0, 0, 0, -1, -1]

    with nt.assert_raises(ValueError):
        bq.quat_to_pluecker(fail_quat)


def test_line_to_pluecker():

    assert np.allclose(
        np.array(
            bq.line_to_pluecker([1, 2, 3], [4, 5, 6])
            - np.append([1, 2, 3], (-np.cross([1, 2, 3], [4, 5, 6]))),
            dtype=float,
        ),
        0,
        atol=1e-10,
    )

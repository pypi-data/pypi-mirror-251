import biquaternion_py as bq
import numpy.testing as nt
from biquaternion_py import II, JJ, KK, EE
import numpy as np


def test_point_to_quat():
    assert bq.point_to_quat([1, 2, 3]) == bq.BiQuaternion([1, 0, 0, 0, 0, 1, 2, 3])


def test_quat_to_point():
    a = [1, 2, 3]
    assert bq.quat_to_point(2 * bq.point_to_quat(a)) == a
    assert bq.quat_to_point(bq.point_to_quat(a)) == a
    with nt.assert_raises(ValueError):
        bq.quat_to_point(bq.BiQuaternion([1, 2, 3, 4, 5, 6, 7, 8]))
    with nt.assert_raises(ValueError):
        bq.quat_to_point(bq.BiQuaternion([0, 0, 0, 0, 0, 6, 7, 8]))


def test_hom_point_to_quat():
    a = [5, 1, 2, 3]
    assert bq.hom_point_to_quat(a) == bq.BiQuaternion([5, 0, 0, 0, 0, 1, 2, 3])


def test_quat_to_hom_point():
    a = [5, 1, 2, 3]
    assert bq.quat_to_hom_point(2 * bq.hom_point_to_quat(a)) != a
    assert bq.quat_to_hom_point(bq.hom_point_to_quat(a)) == a
    with nt.assert_raises(ValueError):
        bq.quat_to_hom_point(bq.BiQuaternion([1, 2, 3, 4, 5, 6, 7, 8]))
    with nt.assert_raises(ValueError):
        bq.quat_to_hom_point(bq.BiQuaternion([0, 0, 0, 0, 0, 6, 7, 8]))


def test_smart_act():
    BQ = (
        4
        - (299 * II) / 200
        - (4149 * JJ) / 70
        + (639 * KK) / 85
        - EE * ((34551 * II) / 238 - (2761 * JJ) / 680 - (22 * KK) / 7)
    )
    L = (
        (2431 * II) / 630
        - (263 * JJ) / 91
        + (385 * KK) / 306
        - EE * (-(4773 * II) / 3094 - (4499 * JJ) / 2380 + (177 * KK) / 455)
    )
    P = -1 / 12 + EE * (-(15 * II) / 17 - (4 * JJ) / 3 - (10 * KK) / 21)
    p1 = bq.quat_to_hom_point(P)
    p2 = bq.quat_to_point(P)
    line = bq.quat_to_pluecker(L)
    outp = (
        5933780375793 / 1925896000 * EE * II
        - 1952649560339 / 424830000 * EE * JJ
        + 321025354801 / 317206400 * EE * KK
        - 2032303049561 / 6797280000
    )
    outl = (
        II
        * (
            -(65591654613190327 * EE) / 1213314480000
            - 68042644080418117 / 4639143600000
        )
        + JJ
        * (
            (12236021601909315397 * EE) / 157730882400000
            - 4741189758385837 / 463914360000
        )
        + KK * (-(999851565017503 * EE) / 257730200000 + 16099270708217 / 751099440000)
    )

    assert np.allclose(
        np.array((bq.smart_act(BQ, L) - outl).coeffs, dtype=float), 0, atol=1e-10
    )
    assert np.allclose(
        np.array(bq.smart_act(BQ, line), dtype=float)
        - np.array(bq.quat_to_pluecker(outl), dtype=float),
        0,
        atol=1e-10,
    )
    assert np.allclose(
        np.array((bq.smart_act(BQ, P) - outp).coeffs, dtype=float), 0, atol=1e-10
    )
    assert np.allclose(
        np.array(bq.smart_act(BQ, p1), dtype=float)
        - np.array(bq.quat_to_hom_point(outp), dtype=float),
        0,
        atol=1e-10,
    )
    assert np.allclose(
        np.array(bq.smart_act(BQ, p2), dtype=float)
        - np.array(bq.quat_to_point(outp), dtype=float),
        0,
        atol=1e-10,
    )

    with nt.assert_raises(ValueError):
        bq.smart_act(BQ, [1, 2])
    with nt.assert_raises(TypeError):
        bq.smart_act(BQ, 1)


def test_inner():
    i = II
    j = JJ
    k = KK
    epsilon = EE
    B1 = (
        -1 / 4
        + (4 * i) / 17
        - 2 * j
        + (2 * k) / 5
        + epsilon * (3 / 2 - (21 * i) / 4 + (12 * j) / 11 + (9 * k) / 7)
    )
    B2 = (
        6
        - 5 * i
        + j / 5
        + (7 * k) / 8
        + epsilon * (-9 / 14 + (5 * i) / 4 + (4 * j) / 17 - (16 * k) / 17)
    )
    assert np.allclose(
        np.array(
            (
                bq.inner(B1, B2)
                - (
                    i * (-(393813 * epsilon) / 14960 + 1693 / 850) / 2
                    + j * ((30988141 * epsilon) / 3560480 - 3313 / 340) / 2
                    + k * (-(1870249 * epsilon) / 1780240 + 6839 / 544) / 2
                    + (947741 * epsilon) / 26180
                    - 927 / 340
                    + i * ((393813 * epsilon) / 14960 - 1693 / 850) / 2
                    + j * (-(30988141 * epsilon) / 3560480 + 3313 / 340) / 2
                    + k * ((1870249 * epsilon) / 1780240 - 6839 / 544) / 2
                )
            ).coeffs,
            dtype=float,
        ),
        0,
        atol=1e-10,
    )


def test_outer():
    i = II
    j = JJ
    k = KK
    epsilon = EE
    B1 = (
        -1 / 4
        + (4 * i) / 17
        - 2 * j
        + (2 * k) / 5
        + epsilon * (3 / 2 - (21 * i) / 4 + (12 * j) / 11 + (9 * k) / 7)
    )
    B2 = (
        6
        - 5 * i
        + j / 5
        + (7 * k) / 8
        + epsilon * (-9 / 14 + (5 * i) / 4 + (4 * j) / 17 - (16 * k) / 17)
    )
    assert np.allclose(
        np.array(
            (
                bq.outer(B1, B2)
                - (
                    i * (-(3872349 * epsilon) / 104720 + 707 / 850) / 2
                    + j * ((24777299 * epsilon) / 3560480 - 4847 / 340) / 2
                    + k * ((28421257 * epsilon) / 1780240 - 21139 / 2720) / 2
                    - i * (-(627563 * epsilon) / 14960 + 1909 / 425) / 2
                    - j * ((32705549 * epsilon) / 3560480 - 3347 / 340) / 2
                    - k * ((3640641 * epsilon) / 1780240 + 6601 / 544) / 2
                )
            ).coeffs,
            dtype=float,
        ),
        0,
        atol=1e-10,
    )


def test_fiber_project():
    i = II
    j = JJ
    k = KK
    epsilon = EE
    B1 = (
        -1 / 4
        + (4 * i) / 17
        - 2 * j
        + (2 * k) / 5
        + epsilon * (3 / 2 - (21 * i) / 4 + (12 * j) / 11 + (9 * k) / 7)
    )
    assert np.allclose(
        np.array(
            (
                bq.fiber_project(B1)
                - (
                    i * (-(45422361 * epsilon) / 1047200 + 494521 / 245650) / 2
                    + j * (-(2101677 * epsilon) / 556325 - 494521 / 28900) / 2
                    + k * ((12125643 * epsilon) / 890120 + 494521 / 144500) / 2
                    + (12455757 * epsilon) / 2225300
                    - 494521 / 462400
                )
            ).coeffs,
            dtype=float,
        ),
        0,
        atol=1e-10,
    )


def test_rand():
    assert isinstance(bq.rand_quat(), bq.BiQuaternion)
    assert np.allclose(np.array(bq.rand_quat().coeffs[4:], dtype=float), 0, atol=1e-10)
    assert isinstance(bq.rand_bq(), bq.BiQuaternion)

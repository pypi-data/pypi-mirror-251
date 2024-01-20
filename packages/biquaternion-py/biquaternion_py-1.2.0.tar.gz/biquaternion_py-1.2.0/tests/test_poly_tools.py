import biquaternion_py as bq
import sympy as sy
import numpy.testing as nt
from biquaternion_py import II, JJ, KK, EE

t, s = sy.symbols("t s")


def test_factorization():
    h1 = bq.rand_rational() + bq.rand_line()
    h2 = bq.rand_rational() + bq.rand_line()
    h3 = bq.rand_rational() + bq.rand_line()

    poly = bq.Poly((t - h1) * (t - h2) * (t - h3), t)
    norm_poly = bq.Poly(poly.norm().poly.scal, *poly.indets)
    _, facts = bq.irreducible_factors(norm_poly)
    fact1 = bq.factorize_from_list(poly, facts)
    fact2 = bq.factorize_from_list(poly, facts[::-1])
    fact3 = bq.factorize_bq_poly(poly)
    poly1 = 1
    for fac in fact1:
        poly1 *= fac
    poly2 = 1
    for fac in fact2:
        poly2 *= fac
    poly3 = 1
    for fac in fact3:
        poly3 *= fac
    assert poly == poly1 == poly2 == poly3


def test_factorize_from_list():

    with nt.assert_raises(ValueError):
        bq.factorize_from_list(bq.Poly(t - 2 * s, [t, s]), [bq.Poly(t - 1, t)])

    h1 = bq.rand_rational() + bq.rand_line()
    h2 = bq.rand_rational() + bq.rand_line()
    h3 = bq.rand_rational() + bq.rand_line()

    poly = bq.Poly((t - h1) * (t - h2) * (t - h3), t)
    poly2 = bq.Poly((s - h1) * (s - h2) * (s - h3), s)
    norm_poly = bq.Poly(poly.norm().poly.scal, *poly.indets)
    _, facts = bq.irreducible_factors(norm_poly)
    with nt.assert_raises(ValueError):
        bq.factorize_from_list(poly2, facts)


def test_split_lin_factor():
    h1 = bq.rand_rational() + bq.rand_line()
    h2 = bq.rand_rational() + bq.rand_line()
    h3 = bq.rand_rational() + bq.rand_line()

    poly = bq.Poly((t - h1) * (t - h2) * (t - h3), t)
    poly2 = bq.Poly((s - h1) * (s - h2) * (s - h3), s)
    poly3 = bq.Poly((t - h1) * (t - h2) * (t - h3), [t, s])
    norm_poly = bq.Poly(poly.norm().poly.scal, *poly.indets)
    _, facts = bq.irreducible_factors(norm_poly)
    with nt.assert_raises(ValueError):
        bq.split_lin_factor(poly3, norm_poly)
    with nt.assert_raises(ValueError):
        bq.split_lin_factor(poly2, norm_poly)


def test_gcd_conj_pd():
    p = bq.Poly((1 + t**2) * ((II + JJ) * t + KK * EE), t)
    assert (t**3 + t) == bq.gcd_conj_pd(p)


def test_max_real_poly_fact():
    p = bq.Poly((1 + t**2) * ((II + JJ) * t + KK * EE), t)
    q = bq.Poly((1 + t**2) * ((II + JJ) * t + KK * EE), [t, s])
    q2 = bq.Poly((1 + t**2), t)
    assert (t**2 + 1) == bq.max_real_poly_fact(p)
    with nt.assert_raises(ValueError):
        bq.max_real_poly_fact(q)
    with nt.assert_raises(ValueError):
        bq.max_real_poly_fact(q2)

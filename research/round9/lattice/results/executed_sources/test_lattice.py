"""Deterministic, independent matrix-oracle checks; no stochastic tolerance tuning."""
import json
import math
from pathlib import Path
import unittest
import numpy as np
from scipy.integrate import quad
import su2_lattice as su2


def matrix(q):
    # Independent explicit Pauli basis, intentionally not su2.to_matrix.
    sigma = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]])
    return q[0]*np.eye(2)-1j*np.einsum('a,aij->ij', q[1:], sigma)


def matrix_action(lat):
    total = 0.0
    mats = [[matrix(q) for q in site] for site in lat.links]
    for x in range(lat.volume):
        for mu in range(4):
            for nu in range(mu+1, 4):
                loop = mats[x][mu] @ mats[lat.plus[x, mu]][nu] @ mats[lat.plus[x, nu]][mu].conj().T @ mats[x][nu].conj().T
                total += 1-0.5*np.trace(loop).real
    return lat.beta*total


class DeterministicChecks(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(7112026)

    def test_quaternion_matrix_product_and_inverse(self):
        for _ in range(128):
            a, b = su2.haar(self.rng, (2,))
            np.testing.assert_allclose(matrix(su2.qmul(a, b)), matrix(a)@matrix(b), atol=3e-15, rtol=0)
            np.testing.assert_allclose(su2.qmul(a, su2.qconj(a)), su2.UNIT, atol=8e-16, rtol=0)
            np.testing.assert_allclose(su2.to_matrix(a), matrix(a), atol=0, rtol=0)

    def test_full_action_matrix_oracle(self):
        for lengths in [(2,2,2,2), (2,3,2,2), (3,3,3,3)]:
            lat = su2.WilsonLattice(lengths, 2.2, 802)
            self.assertAlmostEqual(lat.action(), matrix_action(lat), delta=4e-12)

    def test_cold_and_plaquette_bounds(self):
        for beta in [0, 0.5, 2.2]:
            lat = su2.WilsonLattice(beta=beta, start='cold')
            self.assertEqual(lat.action(), 0.0)
            np.testing.assert_array_equal(lat.plaquettes(), np.ones(6*lat.volume))
        lat = su2.WilsonLattice(seed=992)
        self.assertTrue(np.all(np.abs(lat.plaquettes()) <= 1+1e-14))

    def test_random_single_link_delta_and_staple_independence(self):
        for lengths in [(2,2,2,2), (2,3,2,2)]:
            lat = su2.WilsonLattice(lengths, 2.2, 908)
            for _ in range(32):
                x, mu = int(self.rng.integers(lat.volume)), int(self.rng.integers(4))
                proposal = su2.haar(self.rng)
                old = lat.links[x, mu].copy()
                staple = lat.staple(x, mu)
                before = matrix_action(lat)
                delta = lat.local_delta(x, mu, proposal)
                lat.links[x, mu] = proposal
                np.testing.assert_array_equal(staple, lat.staple(x, mu))
                self.assertAlmostEqual(delta, matrix_action(lat)-before, delta=7e-13)
                lat.links[x, mu] = old

    def test_gauge_invariance_and_ward_invariance(self):
        lat = su2.WilsonLattice(beta=2.2, seed=721)
        action, ward, p = matrix_action(lat), lat.ward(), lat.plaquettes()
        g = su2.haar(self.rng, (lat.volume,))
        lat.gauge_transform(g)
        self.assertAlmostEqual(matrix_action(lat), action, delta=4e-13)
        self.assertAlmostEqual(lat.ward(), ward, delta=2e-13)
        np.testing.assert_allclose(lat.plaquettes(), p, atol=3e-15, rtol=0)

    def test_center_seam_symmetry_and_polyakov_sign(self):
        lat = su2.WilsonLattice(beta=2.2, seed=321)
        before = lat.links.copy()
        action, p = matrix_action(lat), lat.plaquettes()
        # A winding loop crosses one seam and flips sign, while plaquettes do not.
        for mu in range(4):
            lat.links = before.copy()
            def poly():
                x, loop = 0, np.eye(2, dtype=complex)
                for _ in range(lat.lengths[mu]):
                    loop = loop@matrix(lat.links[x, mu])
                    x = lat.plus[x, mu]
                return np.trace(loop).real/2
            first = poly()
            lat.center_flip(mu, plane=1)
            self.assertAlmostEqual(poly(), -first, delta=1e-15)
            self.assertAlmostEqual(matrix_action(lat), action, delta=1e-13)
            np.testing.assert_allclose(lat.plaquettes(), p, atol=1e-15, rtol=0)
            lat.center_flip(mu, plane=1)
            np.testing.assert_array_equal(lat.links, before)

    def test_inverse_proposal_and_detailed_balance_acceptance(self):
        lat = su2.WilsonLattice(beta=2.2, seed=718)
        for _ in range(64):
            old = lat.links[0, 0].copy()
            r = su2.haar(self.rng)
            proposal = su2.qmul(r, old)
            np.testing.assert_allclose(su2.qmul(su2.qconj(r), proposal), old, atol=9e-16, rtol=0)
            delta = lat.local_delta(0, 0, proposal)
            # q(R)=q(R^-1) by Haar invariance / symmetric angle and axis laws.
            af, ar = math.exp(min(0, -delta)), math.exp(min(0, delta))
            self.assertAlmostEqual(math.log(af)-math.log(ar), -delta, delta=2e-15)
            lat.links[0, 0] = proposal
            self.assertAlmostEqual(lat.local_delta(0, 0, old), -delta, delta=5e-15)

    def test_ward_generator_finite_difference(self):
        lat = su2.WilsonLattice(beta=0.5, seed=121)
        x, mu, h = 3, 2, 0.003
        old = lat.links[x, mu].copy()
        A = lat.staple(x, mu)
        v = su2.qmul(old, A)
        s0 = matrix_action(lat)
        first, second = [], []
        for axis in range(3):
            vals = {}
            for k in [-2, -1, 1, 2]:
                r = su2.UNIT.copy()
                r[0], r[axis+1] = math.cos(k*h/2), -math.sin(k*h/2)
                lat.links[x, mu] = su2.qmul(r, old)
                vals[k] = matrix_action(lat)
            first.append((vals[-2]-8*vals[-1]+8*vals[1]-vals[2])/(12*h))
            second.append((-vals[2]+16*vals[1]-30*s0+16*vals[-1]-vals[-2])/(12*h*h))
        lat.links[x, mu] = old
        # U(theta)=exp(+i theta sigma/2)U => q rotation vector has negative sign.
        np.testing.assert_allclose(first, -lat.beta*v[1:]/2, atol=3e-11, rtol=0)
        np.testing.assert_allclose(second, np.full(3, lat.beta*v[0]/4), atol=5e-8, rtol=0)

    def test_one_plaquette_exact_integrals_and_zero_limit(self):
        for beta in [0, 1e-6, 1e-3, 0.5, 2.2, 10.0]:
            def integral(k):
                return quad(lambda t: 2/math.pi*math.sin(t)**2*math.cos(t)**k*math.exp(beta*math.cos(t)), 0, math.pi, epsabs=1e-12, epsrel=1e-12)[0]
            z, expected = integral(0), su2.exact_one_plaquette(beta)
            self.assertAlmostEqual(expected['mean'], integral(1)/z, delta=1e-12)
            self.assertAlmostEqual(expected['second_moment'], integral(2)/z, delta=1e-12)
            self.assertAlmostEqual(expected['log_partition'], math.log(z), delta=1e-12)

    def test_sweeps_reproducible_no_silent_projection(self):
        a = su2.WilsonLattice(beta=2.2, seed=811)
        b = su2.WilsonLattice(beta=2.2, seed=811)
        for _ in range(4):
            self.assertEqual(a.sweep(), b.sweep())
        np.testing.assert_array_equal(a.links, b.links)
        su2.validate_links(a.links)
        broken = su2.UNIT*1.01
        with self.assertRaises(ValueError):
            su2.validate_links(broken)
        np.testing.assert_array_equal(broken, su2.UNIT*1.01)

    def test_invalid_input_and_nonfinite_and_missing_data(self):
        for beta in [-1, float('nan'), float('inf'), True, 1j]:
            with self.assertRaises((ValueError, TypeError)):
                su2.WilsonLattice(beta=beta)
        for dims in [(1,2,2,2), (2,2,2), (2,2,2,2.0), (2,True,2,2), (0,2,2,2)]:
            with self.assertRaises(ValueError):
                su2.WilsonLattice(lengths=dims)
        for samples in [[], [1, np.nan], [np.inf], [[1,2]]]:
            with self.assertRaises(ValueError):
                su2.series_summary(samples)
        self.assertEqual(su2.series_summary([1])['status'], 'insufficient')
        self.assertEqual(su2.series_summary(np.ones(2048))['status'], 'degenerate')
        self.assertEqual(su2.compare_to_exact(su2.series_summary(np.ones(2048)), 1)['status'], 'insufficient')
        for n in [0, -1, True, 2.5]:
            with self.assertRaises(ValueError):
                su2.one_plaquette_iid(0.5, n, 1)
        with self.assertRaises(ValueError):
            su2.validate_links([np.nan, 0, 0, 0])
        with self.assertRaises(ValueError):
            su2.WilsonLattice(start='unknown')

    def test_skeptic_nonfinite_derived_statistics(self):
        for samples in [np.array([1e308,-1e308]*1024), np.r_[np.zeros(2047),1e308], [1e308,-1e308]]:
            with self.assertRaises(FloatingPointError):
                su2.series_summary(samples)
        with self.assertRaises(ValueError):
            su2.compare_to_exact({'status':'usable', 'se':1., 'mean':float('nan')}, 0.)
        with self.assertRaises(FloatingPointError):
            su2.compare_to_exact({'status':'usable', 'se':1e-300, 'mean':1e308}, 0.)
        with self.assertRaises(ValueError):
            su2.validate_links(np.array([1+1j,0,0,0]))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DeterministicChecks)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    out = Path(__file__).parent/'results'
    out.mkdir(exist_ok=True)
    (out/'deterministic_checks.json').write_text(json.dumps({
        'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
        'successful': result.wasSuccessful(), 'failure_details': result.failures,
        'error_details': result.errors}, default=str, indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)

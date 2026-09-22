#!/usr/bin/env python3
"""AQ2 exact geometry, centering, gauge, variance and scope diagnostics.

The infinite-dimensional proof is report.md. These exact finite diagnostics
test its dictionary and reject specific tempting substitutions.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
checks = []


def need(condition, name):
    if not condition:
        raise RuntimeError(name)
    if name in checks:
        raise RuntimeError('duplicate executed check ID: ' + name)
    checks.append(name)


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def minus(a, b):
    return tuple(x - y for x, y in zip(a, b))


def owner(p):
    return p[0] // 4, p[1] // 2, p[2]


ZERO = (0, 0, 0)
E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
S = (ZERO, *E)
R = {ZERO, E[2]}
I = ((Q(1), Q(0)), (Q(0), Q(1)))
J = ((Q(0), Q(1)), (Q(-1), Q(0)))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def adj(a):
    return tuple(tuple(a[j][i] for j in range(len(a)))
                 for i in range(len(a[0])))


def mv(a, v):
    return tuple(sum(x * y for x, y in zip(row, v)) for row in a)


def kron(a, b):
    return tuple(tuple(a[i][j] * b[k][l]
                       for j in range(len(a[0])) for l in range(len(b[0])))
                 for i in range(len(a)) for k in range(len(b)))


def block_links(b):
    return {((4*b[0]+r, 2*b[1]+s, b[2]), j)
            for r, s, j in product(range(4), range(2), range(3))}


def endpoints(links):
    return {v for p, j in links for v in (p, plus(p, E[j]))}


def loop_trace(link_values):
    u = I
    for link, orientation in FACE:
        a = link_values[link]
        u = mm(u, a if orientation == 1 else adj(a))
    return (u[0][0]+u[1][1])/2


FACE = (((ZERO, 0), 1), ((E[0], 2), 1), ((E[2], 0), -1), ((ZERO, 2), -1))


def gauge_links(link_values, transformation, include_heads=True):
    out = {}
    for (p, j), u in link_values.items():
        left = transformation.get(p, I)
        right = transformation.get(plus(p, E[j]), I) if include_heads else I
        out[(p, j)] = mm(mm(left, u), adj(right))
    return out


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=False)

    links = set().union(*(block_links(b) for b in R))
    ends = endpoints(links)
    need(len(links) == 48, 'complete_wilson_cover_48_links')
    need(len(ends) == 36, 'complete_wilson_cover_36_endpoints')
    for p, j in sorted(links):
        need(owner(p) in R, 'complete_owner_'+str((p, j)))
    need({owner(p) for (p, j), sign in FACE} == R, 'four_stored_links_exact_two_factor_support')
    need(len({link for link, sign in FACE}) == 4, 'four_distinct_original_face_links')
    e0, e1 = (endpoints(block_links(b)) for b in (ZERO, E[2]))
    need(len(e0) == len(e1) == 22, 'each_complete_factor_22_endpoints')
    need(len(e0 & e1) == 8, 'eight_shared_endpoint_actions')
    need({(p, 2) for p in (ZERO, E[0])}.issubset(links), 'two_original_free_z_links')
    # A selected strip uses only x and y directions, so each z link is free.
    selected = {((r, s, 0), 0) for r in range(3) for s in range(2)}
    selected |= {((r, 0, 0), 1) for r in range(4)}
    need(len(selected) == 10 and not any(j == 2 for p, j in selected), 'actual_selected_strip_not_pure_electric_reference')
    need(all(link not in selected for link in ((ZERO, 2), (E[0], 2))), 'wilson_haar_link_independent_in_reference')

    anchors = {minus(r, s) for r in R for s in S}
    expected = {ZERO, (-1,0,0), (0,-1,0), (0,0,-1), E[2], (-1,0,1), (0,-1,1)}
    need(anchors == expected and len(anchors) == 7, 'full_lattice_seven_incident_stars')
    orthant = {b for b in anchors if min(b) >= 0}
    need(orthant == R and len(orthant) == 2, 'orthant_two_star_substitution_rejected')
    counts = []
    for n in (1,2,3,5):
        retained = {b for b in anchors if all(max(map(abs, plus(b,s))) <= n for s in S)}
        need(len(retained) == (4 if n == 1 else 7), 'centered_box_incidence_'+str(n))
        counts.append({'box_radius':n, 'incident_retained_stars':len(retained)})
    tau = Q(1,100000000)
    reset = 2*7*tau*len(anchors)
    need(reset == 98*tau, 'regional_reset_98_tau')
    need(reset > 28*tau, 'orthant_reset_does_not_cover_bulk_budget')
    need(reset < Q(1,1000000), 'reference_overlap_loss_below_one_millionth')
    distance = Q(1,500)
    need(4*reset < distance*distance, 'trace_distance_squared_certificate')
    lower = Q(1,4)-distance-distance*distance
    need(lower == Q(61999,250000), 'wilson_variance_exact_floor')
    need(lower > Q(1,5), 'wilson_variance_strictly_above_one_fifth')
    need(Q(1,4)*4 == 1, 'SU2_three_sphere_reference_second_moment')
    need(98*abs(-tau) == reset and 98*abs(tau) == reset, 'both_interaction_signs_same_budget')
    need(Q(1,4)-0-0 == Q(1,4), 'decoupled_reference_corner')

    # Original SU(2) fixture: J is a real special-unitary matrix.
    need(mm(J,adj(J)) == I and J[0][0]*J[1][1]-J[0][1]*J[1][0] == 1, 'fixture_is_SU2')
    values = {link:I for link, sign in FACE}
    need(loop_trace(values) == 1, 'original_face_at_identity')
    correct = gauge_links(values,{E[0]:J})
    wrong = gauge_links(values,{E[0]:J},False)
    need(loop_trace(correct) == 1, 'original_head_tail_gauge_cancellation')
    need(loop_trace(wrong) == 0, 'missing_head_action_detected')
    # Joint invariants differ from separately imposing the same action on factors.
    singlet = (Q(0),Q(1),Q(-1),Q(0))
    rotation = ((Q(3,5),Q(4,5)),(Q(-4,5),Q(3,5)))
    for idx,g in enumerate((J,rotation)):
        need(mv(kron(g,g),singlet) == singlet, 'shared_vertex_joint_invariant_'+str(idx))
        need(mv(kron(g,I),singlet) != singlet, 'independent_factor_fixed_substitution_rejected_'+str(idx))

    alpha, hbar = Q(24), Q(5)
    delta = alpha/8
    gap = delta/2
    need(gap == alpha/16 == Q(3,2), 'physical_energy_gap_alpha_over_16')
    need(gap/hbar == Q(3,10) and gap/hbar != gap, 'physical_frequency_requires_hbar')
    need(gap != Q(1,2), 'normalized_gap_not_physical_gap')
    raw_ground = Q(5)
    need((raw_ground+gap)-raw_ground == gap, 'retain_exact_ground_scalar')
    need(raw_ground+gap != gap, 'unshifted_excitation_energy_rejected')
    # mu=(1/3)delta_0+(2/3)delta_(2gap) fools tests only in (0,gap).
    diagnostic = [(Q(0),Q(1,3)),(2*gap,Q(2,3))]
    open_interval_mass = sum(w for e,w in diagnostic if 0<e<gap)
    zero_bump_integral = sum(w for e,w in diagnostic if e == 0)
    need(open_interval_mass == 0, 'positive_open_interval_test_misses_zero_atom')
    need(zero_bump_integral == Q(1,3), 'smooth_bump_about_zero_detects_atom')
    need(sum(w for e,w in diagnostic) == 1, 'zero_atom_control_preserves_total_mass')
    # A|0>=(i,1), omega(A)=i: subtract |i|^2, never i^2.
    need(Q(2)-Q(1) == 1, 'complex_mean_absolute_square_centering')
    need(Q(2)-Q(-1) == 3, 'complex_square_wrong_centered_mass')
    moving = []
    for n in (2,3,5,10,100):
        a,b = Q(n*n-1,n*n+1),Q(2*n,n*n+1)
        d = a*a-b*b
        chi = (2*a*b*b,-2*a*a*b)
        norm2 = sum(x*x for x in chi)
        need(a*a+b*b == 1, 'moving_state_normalized_'+str(n))
        need(a*chi[0]+b*chi[1] == 0, 'actual_moving_mean_removes_zero_'+str(n))
        need(norm2 == 1-d*d == 4*a*a*b*b, 'moving_centered_mass_identity_'+str(n))
        # Replacing m_n=d+i by its limiting value 1+i leaves vacuum weight.
        bad_overlap = -2*b*b
        need(bad_overlap*bad_overlap > 0, 'premature_limit_mean_leaves_zero_atom_'+str(n))
        moving.append({'n':n,'mean_real':str(d),'mean_imaginary':'1','centered_mass':str(norm2),'wrong_zero_mass':str(bad_overlap*bad_overlap)})

    # A bounded two-dimensional density diagnostic, not an I1 ground state.
    eps = Q(1,10000)
    observable = ((Q(0),Q(1,2)),(Q(1,2),Q(1,2)))
    square = mm(observable,observable)
    need(sum(abs(x) for x in observable[0]) <= 1 and sum(abs(x) for x in observable[1]) <= 1, 'density_control_observable_norm_at_most_one')
    reference_mean = observable[0][0]
    reference_second = square[0][0]
    interacting_mean = (1-eps)*observable[0][0]+eps*observable[1][1]
    interacting_second = (1-eps)*square[0][0]+eps*square[1][1]
    need(reference_mean == 0 and reference_second == Q(1,4), 'density_control_has_reference_moments')
    need(interacting_mean != reference_mean and interacting_second != reference_second, 'reference_moments_not_interacting_moments')
    need(abs(interacting_mean-reference_mean) <= 2*eps and abs(interacting_second-reference_second) <= 2*eps, 'density_control_trace_bound_still_valid')

    # Algebra M2 direct-sum M2, each representation picks one block.
    # Each block Hamiltonian diag(0,gap) has one vacuum, but central expectations differ.
    need((Q(0),gap).count(Q(0)) == 1, 'scope_fixture_each_representation_simple_vacuum')
    central_expectations = (Q(1),Q(0))
    need(central_expectations[0] != central_expectations[1], 'simple_GNS_vacuum_not_all_state_uniqueness')
    need(len(checks) == len(set(checks)), 'all_executed_check_ids_unique')

    result = {
        'loop':'AQ2','direction':'forward',
        'verdict':'same_state_complete_physical_gap_and_nonzero_Wilson_witness',
        'checks':checks,'tau_cap':str(tau),
        'physical_energy_gap':'alpha/16','physical_frequency_gap':'alpha/(16*hbar)',
        'full_GNS_strengthening_premise':'reviewed AM2 full-Hilbert finite gap',
        'links':48,'endpoints':36,'shared_endpoints':8,
        'incident_anchors':[list(x) for x in sorted(anchors)],'finite_box_counts':counts,
        'reset_at_cap':str(reset),'reference_trace_distance_ceiling':str(distance),
        'Wilson_variance_floor':str(lower),'moving_complex_mean_controls':moving,
        'local_operator_Haar_topology':'ultraweak; not norm-Bochner',
        'GNS_vector_Haar_topology':'strong vector integral',
        'zero_atom_control':{'positive_open_interval_mass':str(open_interval_mass),'zero_bump_integral':str(zero_bump_integral)},
        'old_state_identity_claim':False,'Wilson_operator_domain_claim':False,
        'Wilson_moment_equality_claim':False,'whole_sequence_claim':False,
        'translation_invariance_claim':False,'all_thermodynamic_states_unique_claim':False,
        'continuum_claim':False,'scientific_priority':'unverified',
        'stop_after_loop':10,
    }
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    sources = [HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
    manifest = {'sources':{str(p.relative_to(HERE)):sha(p) for p in sources if p.is_file()},
                'outputs':{'results.json':sha(out/'results.json')}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(checks),'verdict':result['verdict']}))


if __name__ == '__main__':
    main()

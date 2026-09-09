"""Independent references: explicit complex matrices and Haar angle integration.

These do not import the production quaternion, staple, or Bessel implementations.
"""
from __future__ import annotations

import numpy as np
from decimal import Decimal, localcontext
from functools import lru_cache

PAULI = np.array([
    [[0, 1], [1, 0]],
    [[0, -1j], [1j, 0]],
    [[1, 0], [0, -1]],
], dtype=complex)
IDENTITY = np.eye(2, dtype=complex)


def q_to_matrix(q, orientation=1):
    """U=q0 I+orientation*i*q.sigma; sign fixed by actual production map."""
    q = np.asarray(q)
    return q[..., 0, None, None] * IDENTITY + orientation * 1j * np.einsum(
        '...a,aij->...ij', q[..., 1:], PAULI
    )


def shifted(x, mu, shape, step=1):
    y = list(x)
    y[mu] = (y[mu] + step) % shape[mu]
    return tuple(y)


def matrix_action(U, beta, omit_dagger=False):
    shape = U.shape[:-3]
    value = 0.0
    for x in np.ndindex(shape):
        for mu in range(4):
            for nu in range(mu + 1, 4):
                first = U[x + (mu,)]
                second = U[shifted(x, mu, shape) + (nu,)]
                third = U[shifted(x, nu, shape) + (mu,)]
                fourth = U[x + (nu,)]
                P = first @ second @ (third if omit_dagger else third.conj().T) @ fourth.conj().T
                value += 1 - np.trace(P).real / 2
    return float(beta * value)


def matrix_gauge_transform(U, G):
    shape = U.shape[:-3]
    V = np.empty_like(U)
    for x in np.ndindex(shape):
        for mu in range(4):
            V[x + (mu,)] = G[x] @ U[x + (mu,)] @ G[shifted(x, mu, shape)].conj().T
    return V


def conditional_f_from_global_action(U, link):
    """Recover the local linear f through matrix substitutions, no staple used."""
    original = U[link].copy()
    U[link] = IDENTITY
    positive = matrix_action(U, 1)
    U[link] = -IDENTITY
    negative = matrix_action(U, 1)
    constant = (positive + negative) / 2
    coeff = np.empty(4)
    coeff[0] = (negative - positive) / 2
    for a in range(3):
        U[link] = 1j * PAULI[a]
        coeff[a + 1] = constant - matrix_action(U, 1)
    U[link] = original
    f = constant - matrix_action(U, 1)
    return float(f), float(coeff @ coeff), coeff


def lie_derivatives(U, link, eps):
    """Differentiate f=-S+constant along all three left Lie directions."""
    original = U[link].copy()
    S0 = matrix_action(U, 1)
    grads, laplace = [], 0.0
    for a in range(3):
        U[link] = (np.cos(eps) * IDENTITY + 1j * np.sin(eps) * PAULI[a]) @ original
        Sp = matrix_action(U, 1)
        U[link] = (np.cos(eps) * IDENTITY - 1j * np.sin(eps) * PAULI[a]) @ original
        Sm = matrix_action(U, 1)
        grads.append(-(Sp - Sm) / (2 * eps))
        laplace += -(Sp - 2 * S0 + Sm) / eps ** 2
    U[link] = original
    return float(np.dot(grads, grads)), float(laplace)


PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148")


def decimal_cos(x):
    term = total = Decimal(1)
    xx = x*x
    for k in range(1, 500):
        term *= -xx / Decimal((2*k-1)*(2*k))
        previous = total
        total += term
        if total == previous:
            return total
    raise ArithmeticError("Decimal cosine failed to converge")


@lru_cache(maxsize=8)
def haar_nodes(nodes, precision):
    with localcontext() as ctx:
        ctx.prec = precision+12
        values=[]
        for k in range(1,nodes+1):
            x=decimal_cos(PI*Decimal(k)/Decimal(nodes+1))
            values.append((x,1-x*x))
        return tuple(values)


def haar_ratio_reference(beta, n, precision=80, nodes=512):
    """Independent high-precision Gauss-Chebyshev Haar integral.

    The quadrature integrates polynomial degree <=2*nodes-1 exactly in exact
    arithmetic; exponentials additionally require node refinement. Decimal
    rounding is not interval-enclosed. No Bessel implementation is used.
    """
    if beta == 0:
        return Decimal(1 if n == 1 else 0)
    with localcontext() as ctx:
        ctx.prec=precision+12
        b=Decimal(str(beta)); num=Decimal(0);den=Decimal(0)
        for x,w in haar_nodes(nodes,precision):
            weight=w*(b*x-abs(b)).exp()
            old=Decimal(0);character=Decimal(1)
            for order in range(1,n):
                old,character=character,2*x*character-old
            num+=weight*character
            den+=weight
        return +(num/(Decimal(n)*den))


def haar_moment_reference(beta, power, precision=80, nodes=256):
    with localcontext() as ctx:
        ctx.prec=precision+12
        b=Decimal(str(beta));num=Decimal(0);den=Decimal(0)
        for x,w in haar_nodes(nodes,precision):
            weight=w*(b*x-abs(b)).exp()
            num+=weight*x**power
            den+=weight
        return +(num/den)

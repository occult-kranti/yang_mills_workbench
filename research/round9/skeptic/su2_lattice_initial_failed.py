"""Four-dimensional periodic SU(2) Wilson lattice: readable reference implementation.

q=(s,v) represents s I - i v.sigma. Standard quaternion cross-product sign.
All dimensional lengths >=2; length-one degeneracies are deliberately excluded.
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
import numpy as np
from scipy.special import ive

UNIT = np.array([1.0, 0.0, 0.0, 0.0])


def qmul(a, b):
    """Multiply quaternions; broadcasting on leading dimensions is supported."""
    a, b = np.asarray(a), np.asarray(b)
    if a.shape[-1:] != (4,) or b.shape[-1:] != (4,):
        raise ValueError("quaternions need final axis length four")
    aw, ax, ay, az = np.moveaxis(a, -1, 0)
    bw, bx, by, bz = np.moveaxis(b, -1, 0)
    return np.stack((aw*bw-ax*bx-ay*by-az*bz,
                     aw*bx+ax*bw+ay*bz-az*by,
                     aw*by-ax*bz+ay*bw+az*bx,
                     aw*bz+ax*by-ay*bx+az*bw), axis=-1)


def _mul(a, b):
    """Allocation-light scalar product used inside sequential link updates."""
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array((aw*bw-ax*bx-ay*by-az*bz,
                     aw*bx+ax*bw+ay*bz-az*by,
                     aw*by-ax*bz+ay*bw+az*bx,
                     aw*bz+ax*by-ay*bx+az*bw))


def qconj(q):
    out = np.array(q, dtype=float, copy=True)
    if out.shape[-1:] != (4,):
        raise ValueError("quaternions need final axis length four")
    out[..., 1:] *= -1
    return out


def scalar_product(a, b):
    return a[0]*b[0] - np.dot(a[1:], b[1:])


def to_matrix(q):
    q = np.asarray(q)
    if q.shape != (4,) or not np.isfinite(q).all():
        raise ValueError("one finite quaternion required")
    s, x, y, z = q
    return np.array([[s-1j*z, -y-1j*x], [y-1j*x, s+1j*z]])


def haar(rng, shape=()):
    z = rng.normal(size=tuple(shape)+(4,))
    norm = np.linalg.norm(z, axis=-1, keepdims=True)
    if not np.isfinite(norm).all() or np.any(norm == 0):
        raise FloatingPointError("degenerate Gaussian draw in Haar construction")
    return z/norm


def validate_beta(beta):
    if isinstance(beta, (bool, np.bool_)) or not np.isscalar(beta):
        raise ValueError("beta must be a finite nonnegative real scalar")
    try:
        beta = float(beta)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("beta must be a finite nonnegative real scalar") from exc
    if not math.isfinite(beta) or beta < 0:
        raise ValueError("beta must be finite and nonnegative")
    return beta


def validate_links(links, shape=None, tol=2e-10):
    links = np.asarray(links)
    if shape is not None and links.shape != shape:
        raise ValueError(f"link shape must be {shape}")
    if links.shape[-1:] != (4,) or not np.isfinite(links).all():
        raise ValueError("links must be finite quaternions")
    defect = float(np.max(np.abs(np.sum(links*links, axis=-1)-1)))
    if defect > tol:
        raise ValueError(f"nonunit SU(2) link, squared-norm defect {defect}")
    return defect


@dataclass
class WilsonLattice:
    lengths: tuple = (2, 2, 2, 2)
    beta: float = 0.0
    seed: int = 1
    start: str = "hot"

    def __post_init__(self):
        if len(self.lengths) != 4 or any(isinstance(x, (bool, np.bool_)) or
             not isinstance(x, (int, np.integer)) or x < 2 for x in self.lengths):
            raise ValueError("exactly four integer periodic lengths >=2 required")
        self.lengths = tuple(int(x) for x in self.lengths)
        self.beta = validate_beta(self.beta)
        if self.start not in ("hot", "cold"):
            raise ValueError("start must be hot or cold")
        if isinstance(self.seed, (bool, np.bool_)) or not isinstance(self.seed, (int, np.integer)) or self.seed < 0:
            raise ValueError("seed must be a nonnegative integer")
        self.rng = np.random.default_rng(self.seed)
        self.volume = math.prod(self.lengths)
        self.coords = list(itertools.product(*(range(x) for x in self.lengths)))
        self.index = {coord: i for i, coord in enumerate(self.coords)}
        self.plus = np.empty((self.volume, 4), dtype=int)
        self.minus = np.empty_like(self.plus)
        for i, coord in enumerate(self.coords):
            for mu in range(4):
                cp, cm = list(coord), list(coord)
                cp[mu] = (cp[mu]+1) % self.lengths[mu]
                cm[mu] = (cm[mu]-1) % self.lengths[mu]
                self.plus[i, mu], self.minus[i, mu] = self.index[tuple(cp)], self.index[tuple(cm)]
        self.links = (haar(self.rng, (self.volume, 4)) if self.start == "hot"
                      else np.broadcast_to(UNIT, (self.volume, 4, 4)).copy())
        validate_links(self.links, (self.volume, 4, 4))

    def staple(self, x, mu):
        """Six open paths from x+mu to x; no link U_mu(x) occurs in A."""
        u = self.links
        a = np.zeros(4)
        xp = self.plus[x, mu]
        for nu in range(4):
            if nu == mu:
                continue
            xn = self.plus[x, nu]
            xm = self.minus[x, nu]
            xpm = self.minus[xp, nu]
            a += _mul(_mul(u[xp, nu], qconj(u[xn, mu])), qconj(u[x, nu]))
            a += _mul(_mul(qconj(u[xpm, nu]), qconj(u[xm, mu])), u[xm, nu])
        return a

    def plaquettes(self):
        """Return scalar normalized traces in x,mu<nu order."""
        values = []
        for mu in range(4):
            for nu in range(mu+1, 4):
                p = qmul(qmul(qmul(self.links[:, mu], self.links[self.plus[:, mu], nu]),
                              qconj(self.links[self.plus[:, nu], mu])), qconj(self.links[:, nu]))
                values.extend(p[:, 0])
        out = np.array(values)
        if not np.isfinite(out).all():
            raise FloatingPointError("nonfinite plaquette")
        return out

    def action(self):
        s = self.beta * float(np.sum(1-self.plaquettes()))
        if not math.isfinite(s):
            raise FloatingPointError("nonfinite Wilson action")
        return s

    def local_delta(self, x, mu, proposed):
        validate_links(proposed, (4,))
        delta = -self.beta*scalar_product(proposed-self.links[x, mu], self.staple(x, mu))
        if not math.isfinite(delta):
            raise FloatingPointError("nonfinite local action difference")
        return float(delta)

    def sweep(self):
        """Symmetric left Metropolis proposals, fixed visitation order."""
        accepted = 0
        u = self.links
        for x in range(self.volume):
            for mu in range(4):
                if self.rng.random() < 0.2:
                    r = haar(self.rng)
                else:
                    axis = self.rng.normal(size=3)
                    norm = np.linalg.norm(axis)
                    if not math.isfinite(norm) or norm == 0:
                        raise FloatingPointError("invalid proposal axis")
                    angle = self.rng.uniform(-0.6, 0.6)
                    r = np.r_[math.cos(angle), math.sin(angle)*axis/norm]
                proposed = _mul(r, u[x, mu])
                delta = -self.beta*scalar_product(proposed-u[x, mu], self.staple(x, mu))
                if not math.isfinite(delta):
                    raise FloatingPointError("nonfinite Metropolis action difference")
                # log uniform accepts all downhill proposals and never exp-overflows.
                draw = self.rng.random()
                log_draw = -math.inf if draw == 0 else math.log(draw)
                if log_draw < min(0.0, -delta):
                    u[x, mu] = proposed
                    accepted += 1
        validate_links(u, (self.volume, 4, 4))
        return accepted/(4*self.volume)

    def ward(self):
        """Per-link Haar integration-by-parts residual, averaged over all links."""
        if self.beta == 0:
            return 0.0
        residual = 0.0
        for x in range(self.volume):
            for mu in range(4):
                v = _mul(self.links[x, mu], self.staple(x, mu))
                residual += self.beta**2 * np.dot(v[1:], v[1:]) - 3*self.beta*v[0]
        result = residual/(4*self.volume)
        if not math.isfinite(result):
            raise FloatingPointError("nonfinite Ward residual")
        return float(result)

    def gauge_transform(self, g):
        validate_links(g, (self.volume, 4))
        for mu in range(4):
            self.links[:, mu] = qmul(qmul(g, self.links[:, mu]), qconj(g[self.plus[:, mu]]))
        validate_links(self.links, (self.volume, 4, 4))

    def center_flip(self, mu, plane=0):
        if isinstance(mu, bool) or not isinstance(mu, (int, np.integer)) or not 0 <= mu < 4:
            raise ValueError("mu must be 0,1,2,3")
        if isinstance(plane, bool) or not isinstance(plane, (int, np.integer)) or not 0 <= plane < self.lengths[mu]:
            raise ValueError("invalid center seam plane")
        for x, coord in enumerate(self.coords):
            if coord[mu] == plane:
                self.links[x, mu] *= -1


def exact_one_plaquette(beta):
    """Independent one-matrix integral, not the interacting four-D lattice."""
    beta = validate_beta(beta)
    if beta == 0:
        return {"mean": 0.0, "second_moment": 0.25, "log_partition": 0.0}
    if beta < 1e-3:
        b2 = beta*beta
        mean = beta*(0.25-b2/96+b2*b2/1536)
        second = 0.25+b2/32-b2*b2/512
        logz = b2/8-b2*b2/384+b2*b2*b2/9216
    else:
        i1, i2 = ive(1, beta), ive(2, beta)
        mean = float(i2/i1)
        second = float(1-3*mean/beta)
        logz = float(math.log(2)+math.log(i1)+beta-math.log(beta))
    if not all(math.isfinite(x) for x in (mean, second, logz)):
        raise FloatingPointError("special-function evaluation is nonfinite")
    return {"mean": mean, "second_moment": second, "log_partition": logz}


def one_plaquette_iid(beta, n, seed):
    beta = validate_beta(beta)
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError("n must be a positive integer")
    rng = np.random.default_rng(seed)
    out = []
    proposed = 0
    # Bounded trial budget: no unbounded loop for an extreme beta.
    for _ in range(10000):
        candidates = haar(rng, (max(256, n-len(out)),))[:, 0]
        keep = np.log(rng.random(candidates.size)) < beta*(candidates-1)
        out.extend(candidates[keep].tolist())
        proposed += len(candidates)
        if len(out) >= n:
            return np.asarray(out[:n]), proposed
    raise RuntimeError("one-plaquette rejection budget exhausted")


def series_summary(values, batch=64):
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.isfinite(x).all():
        raise ValueError("nonempty finite one-dimensional samples required")
    if isinstance(batch, bool) or not isinstance(batch, (int, np.integer)) or batch < 1:
        raise ValueError("batch length must be a positive integer")
    n = x.size
    nb = n//batch
    if nb < 2:
        return {"n": int(n), "mean": float(x.mean()), "status": "insufficient", "se": None,
                "batch_size": int(batch), "n_batches": int(nb), "tau_int": None}
    means = x[:nb*batch].reshape(nb, batch).mean(axis=1)
    se = float(means.std(ddof=1)/math.sqrt(nb))
    variance = float(x.var(ddof=1))
    # tau=1/2 for independent samples; initial-positive-sequence estimate.
    centered = x-x.mean()
    if variance == 0:
        return {"n": int(n), "mean": float(x.mean()), "status": "degenerate", "se": 0.0,
                "batch_size": int(batch), "n_batches": int(nb), "tau_int": None}
    cov0 = float(np.dot(centered, centered)/n)
    tau = 0.5
    for lag in range(1, min(n//2, 512), 2):
        pair = 0.0
        for k in (lag, lag+1):
            pair += float(np.dot(centered[:-k], centered[k:])/(n-k)/cov0)
        if pair <= 0:
            break
        tau += pair
    return {"n": int(n), "mean": float(x.mean()), "se": se, "batch_size": int(batch),
            "n_batches": int(nb), "tau_int": tau,
            "status": "usable" if nb >= 20 and tau <= batch/5 else "insufficient"}


def compare_to_exact(summary, target):
    if not math.isfinite(float(target)):
        raise ValueError("finite comparison target required")
    if summary["status"] != "usable":
        return {"status": "insufficient", "target": float(target), "z": None}
    if summary["se"] is None or summary["se"] <= 0 or not math.isfinite(summary["se"]):
        return {"status": "insufficient", "target": float(target), "z": None}
    z = (summary["mean"]-target)/summary["se"]
    return {"status": "consistent" if abs(z) <= 5 else "flagged", "target": float(target), "z": z}

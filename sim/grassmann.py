"""
Grassmannian swarm: covariant consensus-SGD on Gr(k,d) + diversity U-statistic.

Conventions
-----------
* Particles are represented by d x k orthonormal frames Q_i (Stiefel).
  The subspace is span(Q_i); frames are only defined up to O(k) right action.
  All statistics computed here are frame-invariant (principal angles).
* Dynamics (one step, step size dt):
    Sbar  = (1/N) sum_i Q_i Q_i^T                       (consensus field)
    grad  = 2 (Sbar Q_i - Q_i sym(Q_i^T Sbar Q_i))      (Stiefel gradient of tr(Q^T Sbar Q))
    Q_i  <- polar( Q_i + dt * eta * grad + sqrt(2 D dt) * xi ),   xi ~ N(0,I)
  * eta = 0            : isotropic noisy walk   -> Haar stationary law
  * eta > 0            : attractive consensus   -> symmetry-broken (ordered) phase
    beyond a Kuramoto-type critical coupling.
  The chain is O(d)-equivariant and permutation-symmetric for all eta >= 0.
* Diversity U-statistic:  Delta = (2/(N(N-1))) sum_{i<j} d_G(V_i, V_j),
  d_G = sqrt(sum of squared principal angles).
"""

import math
import torch

# -----------------------------------------------------------------------------


def sample_haar(b, n, d, k, device="cuda", dtype=torch.float32, generator=None):
    """i.i.d. Haar frames on Gr(k,d) (QR of Gaussian)."""
    g = torch.randn(b, n, d, k, device=device, dtype=dtype, generator=generator)
    q, _ = torch.linalg.qr(g)
    return q


# -----------------------------------------------------------------------------


def consensus_field(q):
    """q: (b,n,d,k) -> Sbar: (b,d,d)"""
    return (q @ q.transpose(-1, -2)).mean(dim=1)


def polar_retract(q, iters=3):
    """Newton-Schulz polar retraction: X <- X(3I - X^T X)/2  (input near-orthonormal)."""
    if q.shape[-1] == 1:
        return q / q.norm(dim=-2, keepdim=True)
    for _ in range(iters):
        QtQ = q.transpose(-1, -2) @ q
        eye = torch.eye(QtQ.shape[-1], device=q.device, dtype=q.dtype).expand_as(QtQ)
        q = 0.5 * (q @ (3.0 * eye - QtQ))
    return q


def hard_orthonormalize(q):
    if q.shape[-1] == 1:
        return q / q.norm(dim=-2, keepdim=True)
    return torch.linalg.qr(q)[0]


def step(q, eta, D, dt, generator=None):
    """One consensus-SGD step in-place style (returns new q)."""
    S = consensus_field(q)                          # (b,d,d)
    Sq = S.unsqueeze(1) @ q                         # (b,n,d,k)
    QtSq = q.transpose(-1, -2) @ Sq                 # (b,n,k,k)
    sym = 0.5 * (QtSq + QtSq.transpose(-1, -2))
    grad = 2.0 * (Sq - q @ sym)                     # Stiefel gradient
    noise = torch.randn(q.shape, device=q.device, dtype=q.dtype, generator=generator)
    qn = q + dt * eta * grad + math.sqrt(2.0 * D * dt) * noise
    return polar_retract(qn)


def stable_dt(eta, D=1.0, dt_base=0.05):
    """Keep the drift step bounded for stability of the retraction scheme."""
    return min(dt_base, 0.5 / (2.0 * max(eta, 1e-12)))


# -----------------------------------------------------------------------------


def pairwise_geodesic(q, eps=1e-6):
    """q: (b,n,d,k) -> (b,n,n) matrix of geodesic distances."""
    if q.shape[-1] == 1:
        # lines: principal angle from |<v_i, v_j>|
        v = q[..., 0]
        c = torch.einsum("bia,bja->bij", v, v).abs().clamp(eps, 1.0 - eps)
        return torch.acos(c)
    x = torch.einsum("biaf,bjag->bijfg", q, q)     # (b,n,n,k,k) = Q_i^T Q_j
    if q.shape[-1] == 2:
        # closed-form singular values of 2x2 matrices:
        # s^2 = (||X||_F^2 +- sqrt(||X||_F^4 - 4 det(X)^2)) / 2
        f2 = (x ** 2).sum(dim=(-2, -1))
        det = (x[..., 0, 0] * x[..., 1, 1] - x[..., 0, 1] * x[..., 1, 0]) ** 2
        disc = (f2 ** 2 - 4.0 * det).clamp(min=0.0).sqrt()
        s = torch.stack([((f2 + disc) / 2).sqrt(), ((f2 - disc) / 2).sqrt()], dim=-1)
    else:
        b, n, k = x.shape[0], x.shape[1], x.shape[3]
        s = torch.linalg.svdvals(x.reshape(-1, k, k)).reshape(b, n, n, k)
    s = s.clamp(eps, 1.0 - eps)
    theta = torch.acos(s)                           # (b,n,n,k)
    return (theta ** 2).sum(-1).sqrt()


def diversity(q, chunk=8):
    """Delta per swarm. q: (b,n,d,k) -> (b,)   (full pair average, chunked)"""
    b, n = q.shape[0], q.shape[1]
    out = torch.empty(b, device=q.device, dtype=torch.float64)
    for i0 in range(0, b, chunk):
        qc = q[i0:i0 + chunk]
        d = pairwise_geodesic(qc).double()
        iu = torch.triu_indices(n, n, offset=1, device=q.device)
        out[i0:i0 + chunk] = d[:, iu[0], iu[1]].mean(dim=1)
    return out


def leave_one_out_means(q, chunk=8):
    """g_i = mean_{j != i} d(V_i,V_j).  Note: Delta = mean_i g_i.
    Returns (b,n) tensor."""
    b, n = q.shape[0], q.shape[1]
    g = torch.empty(b, n, device=q.device, dtype=torch.float64)
    for i0 in range(0, b, chunk):
        d = pairwise_geodesic(q[i0:i0 + chunk]).double()   # (bc,n,n)
        g[i0:i0 + chunk] = (d.sum(-1) - d.diagonal(dim1=-2, dim2=-1)) / (n - 1)
    return g


def order_parameter(q):
    """r = || Sbar - (k/d) I ||_F  per swarm.  q: (b,n,d,k) -> (b,)"""
    b, d, k = q.shape[0], q.shape[2], q.shape[3]
    S = consensus_field(q).double()
    eye = torch.eye(d, device=q.device, dtype=torch.float64)
    return (S - (k / d) * eye).norm(dim=(-2, -1))


# -----------------------------------------------------------------------------


def run_ensemble(n, d, k, eta, D=1.0, dt=0.05, t_burn=1500, t_thin=5, n_samples=600,
                 b=128, device="cuda", dtype=torch.float32, seed=0, q_init=None,
                 return_traj=False):
    """Equilibrate B swarms and collect `n_samples` thinned snapshots.
    Returns tensor of Delta values: (b * n_samples,) plus diagnostics."""
    torch.manual_seed(seed)
    q = sample_haar(b, n, d, k, device, dtype) if q_init is None else q_init
    for t in range(t_burn):
        q = step(q, eta, D, dt)
        if t % 100 == 0:
            q = hard_orthonormalize(q)
    deltas = []
    r_vals = []
    with torch.no_grad():
        for s in range(n_samples):
            for _ in range(t_thin):
                q = step(q, eta, D, dt)
            q = hard_orthonormalize(q)
            deltas.append(diversity(q))
            r_vals.append(order_parameter(q))
    Dv = torch.cat(deltas)
    Rv = torch.cat(r_vals)
    if return_traj:
        return Dv, Rv, q
    return Dv, Rv

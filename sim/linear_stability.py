"""Refined linear stability of the disordered branch (d=8, D=1).

(1) chi at very small h (curvature-bias-free): B=8192, h in {5e-4,1e-3,2e-3}.
(2) Direct swarm growth-rate: N=2048 from Haar init; track r(t) early-time
    log-slope at eta in {25,28,30,33,36,40}.  lambda>0 <=> disordered branch
    linearly unstable.
"""
import json, math, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
D, k, d = 1.0, 1, 8
out = {"chi_fine": {}, "growth": {}}

# ---------- (1) fine susceptibility ----------
etas_fine = [20.0, 25.0, 30.0, 35.0, 40.0, 45.0]
h_list = (5e-4, 1e-3, 2e-3)
B, burn, n, thin = 8192, 400, 800, 2
dt1 = 0.05


def one_step(v, eta, h):
    p = v[:, 0, 0]
    uu = torch.zeros_like(v)
    uu[:, 0, 0] = p
    drift = (2 * eta * h) * (uu - (p ** 2)[:, None, None] * v)
    return polar_retract(v + drift * dt1 + math.sqrt(2 * D * dt1) *
                         torch.randn(v.shape, device=dev))


for eta in etas_fine:
    vals = []
    for h in h_list:
        torch.manual_seed(int(eta * 131 + h * 1e6))
        v = polar_retract(torch.randn(B, d, 1, device=dev))
        for t in range(burn):
            v = one_step(v, eta, h)
        ps = []
        for s in range(n):
            for _ in range(thin):
                v = one_step(v, eta, h)
            ps.append((v[:, 0, 0] ** 2).mean().item())
        vals.append(sum(ps) / len(ps))
    pd = torch.tensor(vals, dtype=torch.float64) - 1.0 / d
    hs = torch.tensor(h_list, dtype=torch.float64)
    chi = float((pd * hs).sum() / (hs * hs).sum())
    out["chi_fine"][str(eta)] = dict(chi=chi, gain=(1 - 1 / d) / chi, p_vals=vals)
    print(f"chi_fine d=8 eta={eta:4.1f}: chi={chi:.4f} gain={(1-1/d)/chi:.3f}", flush=True)

# ---------- (2) swarm growth rates ----------
N = 2048
b = 48
for eta in [25.0, 28.0, 30.0, 33.0, 36.0, 40.0]:
    dt = stable_dt(eta)
    torch.manual_seed(int(eta * 17))
    q = sample_haar(b, N, d, k, dev)
    rt = []
    for t in range(400):
        q = step(q, eta, D, dt)
        if t % 10 == 0:
            q = hard_orthonormalize(q)
            rt.append(order_parameter(q).mean().item())
    rt = torch.tensor(rt)
    # early log-slope: use windows where 0.02 < r < 0.25 (exponential phase)
    idx = torch.nonzero((rt > 0.02) & (rt < 0.30)).flatten()
    if idx.numel() >= 4:
        i0, i1 = idx[0].item(), idx[-1].item()
        t0_ = i0 * 10 * dt
        t1_ = i1 * 10 * dt
        lam = math.log(rt[i1] / rt[i0]) / (t1_ - t0_) if rt[i0] > 0 else float("nan")
    else:
        lam = float("nan")
    out["growth"][str(eta)] = dict(r_trace=[round(x, 4) for x in rt.tolist()],
                                   lam=lam, r_end=rt[-1].item())
    print(f"growth eta={eta:4.1f}: lambda={lam:.3f}  r_end={rt[-1].item():.3f}", flush=True)

with open("../results/linear_stability.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved.")

"""Single-particle static susceptibility to an external nematic field (k=1).

Dynamics:  v <- polar( v + dt*2*eta*h*((u.v)u - (u.v)^2 v) + sqrt(2 D dt) xi ), u = e1.
Measures chi_h := d<p>/dh, p=(u.v)^2, linear regime.
Mean-field criterion: swarm field amplitude h = r/(1-1/d), r = <p>-1/d
  => instability iff chi_h/(1-1/d) > 1  =>  eta_c^MF = (1-1/d)/chi_h(eta=1).
Compare with swarm transitions: d=4: 12, d=8: 25, d=16: ~65-72.
"""
import json, math, time, torch
from grassmann import polar_retract

dev = "cuda"
torch.manual_seed(0)
D = 1.0
dt = 0.05


def one_step(v, eta, h):
    p = v[:, 0, 0]
    # explicit construction: (u.v)u - (u.v)^2 v  with u = e1
    uu = torch.zeros_like(v)
    uu[:, 0, 0] = p
    drift = (2 * eta * h) * (uu - (p ** 2)[:, None, None] * v)
    return polar_retract(v + drift * dt + math.sqrt(2 * D * dt) *
                         torch.randn(v.shape, device=dev))


def susceptibility(eta, d, h_list=(0.002, 0.006, 0.015), B=4096, burn=300, n=600, thin=2):
    vals = []
    for h in h_list:
        torch.manual_seed(int(eta * 13 + h * 1e5 + d * 7))
        v = torch.randn(B, d, 1, device=dev)
        v = polar_retract(v)
        for t in range(burn):
            v = one_step(v, eta, h)
        ps = []
        for s in range(n):
            for _ in range(thin):
                v = one_step(v, eta, h)
            ps.append((v[:, 0, 0] ** 2).mean().item())
        vals.append(sum(ps) / len(ps))
    ps_dev = torch.tensor(vals, dtype=torch.float64) - 1.0 / d
    hs = torch.tensor(h_list, dtype=torch.float64)
    chi = float((ps_dev * hs).sum() / (hs * hs).sum())
    return chi, vals


out = {}
etas = [2.0, 5.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0]
for d in [4, 8, 16]:
    t0 = time.time()
    rec = {}
    for eta in etas:
        chi, vals = susceptibility(eta, d)
        rec[str(eta)] = dict(chi=chi, p_vals=vals)
        print(f"d={d} eta={eta:5.1f}: chi={chi:.4f}  gain={(1-1/d)/chi:.3f}", flush=True)
    gains = [(e, (1 - 1 / d) / rec[str(e)]["chi"]) for e in etas]
    cross = [e for e, g in gains if g >= 1.0]
    rec["eta_c_MF"] = min(cross) if cross else None
    out[str(d)] = rec
    print(f"==> d={d}: eta_c^MF = {rec['eta_c_MF']}  ({time.time()-t0:.0f}s)")

with open("../results/susceptibility.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved.")

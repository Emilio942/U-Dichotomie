"""Character of the transition vs d:
  d=2: drift is pure Adler (-(eta r) sin 2a) => predicted CONTINUOUS transition
       at eta_c = 2D (von-Mises self-consistency I1/I0).
  d>=3: quartic drift term => subcritical (coexistence) as measured for d=8.
Checks:
  (i) d=2 swarm scan: order onset near eta_c=2? plus ordered-branch persistence
      below 2 (should DECAY fast if continuous).
  (ii) d=4 ordered-branch spinodal (eta in {6,8,10,12}) to bound the window.
"""
import json, math, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
D, k = 1.0, 1
out = {"d2_scan": [], "d2_branchA": [], "d4_branchA": []}

# ---------- d=2 forward scan ----------
N, d, b = 256, 2, 128
for eta in [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0]:
    dt = stable_dt(eta)
    torch.manual_seed(int(eta * 11))
    q = sample_haar(b, N, d, k, dev)
    for t in range(8000):
        q = step(q, eta, D, dt)
        if t % 200 == 0:
            q = hard_orthonormalize(q)
    r = order_parameter(q)
    Dv = diversity(q)
    rec = dict(eta=eta, r=r.mean().item(), r_std=r.std().item(),
               Delta=Dv.mean().item())
    out["d2_scan"].append(rec)
    print(f"d=2 eta={eta:4.1f}: r={r.mean():.3f}+-{r.std():.3f} Delta={Dv.mean():.4f}", flush=True)

# ---------- d=2 ordered persistence below eta_c=2 ----------
for eta in [0.8, 1.2, 1.6, 2.0]:
    dt = stable_dt(eta)
    torch.manual_seed(int(eta * 23))
    q = sample_haar(b, N, d, k, dev)
    for t in range(6000):
        q = step(q, 20.0, D, stable_dt(20.0))
        if t % 200 == 0:
            q = hard_orthonormalize(q)
    r0 = order_parameter(q).mean().item()
    rs = []
    for w in range(40):
        for _ in range(200):
            q = step(q, eta, D, dt)
        q = hard_orthonormalize(q)
        rs.append(order_parameter(q).mean().item())
    rec = dict(eta=eta, r0=r0, r_end=rs[-1], r_mean_last10=sum(rs[-10:]) / 10)
    out["d2_branchA"].append(rec)
    print(f"d=2 A: eta={eta:4.1f} r0={r0:.3f} -> r_end={rs[-1]:.3f}", flush=True)

# ---------- d=4 ordered-branch spinodal ----------
N4, d4 = 512, 4
for eta in [6.0, 8.0, 10.0, 12.0, 14.0]:
    dt = stable_dt(eta)
    torch.manual_seed(int(eta * 29))
    q = sample_haar(96, N4, d4, k, dev)
    for t in range(6000):
        q = step(q, 60.0, D, stable_dt(60.0))
        if t % 200 == 0:
            q = hard_orthonormalize(q)
    r0 = order_parameter(q).mean().item()
    rs = []
    for w in range(60):
        for _ in range(200):
            q = step(q, eta, D, dt)
        q = hard_orthonormalize(q)
        rs.append(order_parameter(q).mean().item())
    rec = dict(eta=eta, r0=r0, r_end=rs[-1], r_mean_last10=sum(rs[-10:]) / 10)
    out["d4_branchA"].append(rec)
    print(f"d=4 A: eta={eta:4.1f} r0={r0:.3f} -> r_end={rs[-1]:.3f}", flush=True)

with open("../results/d2_d4_character.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved.")

"""Hysteresis / metastability scan: is the transition subcritical?

Branch A (ordered persistence): init deep-ordered (burn at eta=100), then switch to
test eta and track r(t): if r stays O(1) the ordered branch is (meta)stable there.
Branch B (nucleation from disorder): init Haar at test eta >= eta_c^lin and measure
first-passage time into r>0.5.

d=8, k=1, D=1, N=512, b=96 swarms.
"""
import json, math, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
N, D, k, d, b = 512, 1.0, 1, 8, 96

out = {"branchA": [], "branchB": []}

# ---------- Branch A: ordered persistence ----------
for eta in [8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 38.0, 45.0]:
    dt = stable_dt(eta)
    torch.manual_seed(int(eta * 3))
    q = sample_haar(b, N, d, k, dev)
    # deep-ordered burn
    for t in range(6000):
        q = step(q, 100.0, D, stable_dt(100.0))
        if t % 200 == 0:
            q = hard_orthonormalize(q)
    r0 = order_parameter(q).mean().item()
    traces = []
    q_now = q
    for w in range(60):                      # 60 windows x 200 steps = 12000 steps
        for _ in range(200):
            q_now = step(q_now, eta, D, dt)
        q_now = hard_orthonormalize(q_now)
        traces.append(order_parameter(q_now).mean().item())
    rec = dict(eta=eta, r0=r0, r_end=traces[-1], r_mean_last10=sum(traces[-10:]) / 10,
               trace=traces)
    out["branchA"].append(rec)
    stable = "STABLE" if rec["r_mean_last10"] > 0.4 else ("decaying" if rec["r_mean_last10"] > 0.15 else "LOST")
    print(f"A: eta={eta:5.1f} r0={r0:.3f} -> r_end={rec['r_end']:.3f}  [{stable}]", flush=True)

# ---------- Branch B: nucleation from disorder ----------
for eta in [30.0, 35.0, 40.0, 45.0, 50.0, 60.0]:
    dt = stable_dt(eta)
    torch.manual_seed(int(eta * 5))
    q = sample_haar(b, N, d, k, dev)
    t_first = None
    for t in range(12000):
        q = step(q, eta, D, dt)
        if t % 50 == 0:
            q = hard_orthonormalize(q)
            r = order_parameter(q)
            frac = (r > 0.5).float().mean().item()
            if frac > 0.5 and t_first is None:
                t_first = t
                break
    rec = dict(eta=eta, t_first=t_first)
    out["branchB"].append(rec)
    print(f"B: eta={eta:5.1f} first-passage(step)={t_first}", flush=True)

with open("../results/hysteresis.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved.")

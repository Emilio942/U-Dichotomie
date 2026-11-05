"""E3: eta-sweep across the synchronization transition at N=512.
Measures the order parameter r(eta) and the susceptibility-like statistic
sigma2_hat(eta) = N * Var(Delta).
"""
import json, math, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
N, D, k, d = 512, 1.0, 1, 8
etas = [2.0, 5.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 24.0, 28.0, 34.0,
        40.0, 50.0, 70.0, 100.0, 150.0, 200.0]
B, NSAMP, THIN = 128, 60, 20

out = []
for eta in etas:
    dt = stable_dt(eta)
    t0 = time.time()
    torch.manual_seed(int(eta * 7))
    q = sample_haar(B, N, d, k, dev)
    for t in range(8000):
        q = step(q, eta, D, dt)
        if t % 200 == 0:
            q = hard_orthonormalize(q)
    ds, rs = [], []
    for s in range(NSAMP):
        for _ in range(THIN):
            q = step(q, eta, D, dt)
        q = hard_orthonormalize(q)
        ds.append(diversity(q).cpu())
        rs.append(order_parameter(q).mean().item())
    ds = torch.stack(ds)
    var = ds.var(unbiased=True).item()
    rec = dict(eta=eta, r=float(torch.tensor(rs).mean()),
               var=var, Nvar=N * var, theta=ds.mean().item())
    out.append(rec)
    print(f"eta={eta:7.1f}  r={rec['r']:.3f}  Var={var:.3e}  N*Var={rec['Nvar']:.3e}  "
          f"Delta={rec['theta']:.4f} ({time.time()-t0:.0f}s)", flush=True)

with open("../results/exp3_eta_sweep.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved.")

import json, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)

N, d, k, b = 200, 8, 1, 256
etas = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0]
out = []
for eta in etas:
    dt = stable_dt(eta)
    t_burn = 8000 if eta > 0 else 2000
    t0 = time.time()
    q = sample_haar(b, N, d, k, dev)
    rs = []
    for t in range(t_burn):
        q = step(q, eta, 1.0, dt)
        if t % 200 == 0:
            q = hard_orthonormalize(q)
        if t % 1000 == 0:
            rs.append(order_parameter(q).mean().item())
    q = hard_orthonormalize(q)
    r = order_parameter(q)
    Dv = diversity(q)
    rec = dict(eta=eta, dt=dt, r_mean=r.mean().item(), r_std=r.std().item(),
               Delta_mean=Dv.mean().item(), Delta_std=Dv.std().item(),
               r_trace=rs, secs=time.time() - t0)
    out.append(rec)
    print(f"eta={eta:7.1f} dt={dt:.4f}  r={r.mean():.4f}+-{r.std():.4f}  "
          f"Delta={Dv.mean():.4f}+-{Dv.std():.4f}  ({rec['secs']:.0f}s)", flush=True)

with open("../results/transition_scan.json", "w") as f:
    json.dump(out, f, indent=1)

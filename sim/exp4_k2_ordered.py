"""E4: ordered-regime scaling for k=2 (general Gr(k,d) check). eta=100, d=8."""
import json, math, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
NS = [128, 256, 512]
ETA, D, K = 100.0, 1.0, 2
dt = stable_dt(ETA)
RESTARTS, B, NSAMP, THIN = 3, 48, 60, 25

results = {}
for N in NS:
    t0 = time.time()
    chain_means, chain_vars, r_list = [], [], []
    for rs in range(RESTARTS):
        torch.manual_seed(9000 + rs)
        q = sample_haar(B, N, 8, K, dev)
        for t in range(8000):
            q = step(q, ETA, D, dt)
            if t % 200 == 0:
                q = hard_orthonormalize(q)
        ds = []
        for s in range(NSAMP):
            for _ in range(THIN):
                q = step(q, ETA, D, dt)
            q = hard_orthonormalize(q)
            ds.append(diversity(q, chunk=8).cpu())
        ds = torch.stack(ds)
        chain_means.append(ds.mean(0)); chain_vars.append(ds.var(0))
        r_list.append(order_parameter(q).mean().item())
    cm, cv = torch.cat(chain_means), torch.cat(chain_vars)
    mean, var = cm.mean().item(), cv.mean().item()
    se_var = (torch.stack(chain_vars).std(unbiased=True) / (RESTARTS * B) ** 0.5).item()
    X = (cm - mean) * math.sqrt(N)
    qs_grid = torch.linspace(0.01, 0.99, 99, dtype=X.dtype)
    qq = torch.corrcoef(torch.stack([torch.quantile(X.cpu(), qs_grid),
                                     torch.quantile(torch.randn(200000, dtype=X.dtype), qs_grid)]))[0, 1].item()
    results[str(N)] = dict(N=N, theta=mean, var=var, se_var=se_var, Nvar=N * var,
                           skew=((X - X.mean()) ** 3).mean().item() / X.std().item() ** 3,
                           qq_corr=qq, r=float(torch.tensor(r_list).mean()),
                           secs=time.time() - t0)
    r_ = results[str(N)]
    print(f"N={N:5d} theta={mean:.4f} Var={var:.3e}+-{se_var:.1e} N*Var={N*var:.3e} "
          f"skew={r_['skew']:.3f} qq={qq:.4f} r={r_['r']:.3f} ({r_['secs']:.0f}s)", flush=True)

xs = [math.log(results[k]["N"]) for k in map(str, NS)]
ys = [math.log(results[k]["var"]) for k in map(str, NS)]
n_ = len(xs)
slope = (sum(x * y for x, y in zip(xs, ys)) - sum(xs) * sum(ys) / n_) / \
        (sum(x * x for x in xs) - sum(xs) ** 2 / n_)
results["slope"] = slope
with open("../results/exp4_k2_ordered.json", "w") as f:
    json.dump(results, f, indent=1)
print(f"--> k=2 slope = {slope:.3f}  saved.")

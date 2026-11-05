"""E2: Variance scaling + Gaussianity in the ORDERED regime (eta=100, D=1).

Prediction: Var(Delta) = sigma^2/N + O(N^-2);  sqrt(N)(Delta-theta) -> Gaussian.
Diagnostics: per-config slope, N*Var plateau, skew/kurtosis, QQ-corr, KS,
plus decomposition: within-swarm spread of leave-one-out means g_i (= c1 proxy)
and between-swarm spread (gamma-channel).
"""
import json, math, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
NS = [128, 256, 512, 1024, 2048]
ETA, D = 100.0, 1.0
dt = stable_dt(ETA)
RESTARTS, B, NSAMP, THIN = 4, 128, 120, 25

results = {}
for N in NS:
    t0 = time.time()
    chain_means, chain_vars, r_means = [], [], []
    g_within, g_between = [], []
    for rs in range(RESTARTS):
        torch.manual_seed(7000 + rs)
        q = sample_haar(B, N, 8, 1, dev)
        for t in range(8000):
            q = step(q, ETA, D, dt)
            if t % 200 == 0:
                q = hard_orthonormalize(q)
        ds, gs_w = [], []
        for s in range(NSAMP):
            for _ in range(THIN):
                q = step(q, ETA, D, dt)
            q = hard_orthonormalize(q)
            ds.append(diversity(q).cpu())
            if s % 30 == 0:
                g = leave_one_out_means(q).cpu()      # (B,N)
                gs_w.append(g.var(dim=1))             # within-swarm var of g_i
                g_between.append(g.mean(dim=1))
        ds = torch.stack(ds)                           # (NSAMP,B)
        chain_means.append(ds.mean(0))
        chain_vars.append(ds.var(0))
        r_means.append(order_parameter(q).mean().item())
        g_within.append(torch.cat(gs_w).mean())
    cm = torch.cat(chain_means)
    cv = torch.cat(chain_vars)
    mean = cm.mean().item()
    var = cv.mean().item()
    se_var = (torch.stack(chain_vars).std(unbiased=True) /
              (RESTARTS * B) ** 0.5).item()
    X = (cm - mean) * math.sqrt(N)                     # sqrt(N)(Delta-theta), per chain
    z = (X - X.mean()) / X.std()
    qs_grid = torch.linspace(0.01, 0.99, 99, dtype=X.dtype)
    qs_t = torch.quantile(torch.randn(200000, dtype=X.dtype), qs_grid)
    qq_corr = torch.corrcoef(torch.stack([torch.quantile(X.cpu(), qs_grid), qs_t]))[0, 1].item()
    skew = (X ** 3).mean().item() / X.std().item() ** 3
    kurt = (X ** 4).mean().item() / X.std().item() ** 4
    rec = dict(N=N, theta=mean, var=var, se_var=se_var, Nvar=N * var, N2var=N * N * var,
               skew=skew, kurt=kurt, qq_corr=qq_corr,
               c1_proxy=float(torch.stack(g_within).mean()),
               gamma_proxy=float(torch.stack(g_between).var(unbiased=True)),
               r=float(torch.tensor(r_means).mean()), secs=time.time() - t0)
    results[str(N)] = rec
    print(f"N={N:5d} theta={mean:.4f} Var={var:.3e}+-{se_var:.1e}  N*Var={N*var:.3e}  "
          f"skew={skew:.3f} kurt={kurt:.3f} qq={qq_corr:.4f} "
          f"c1={rec['c1_proxy']:.4f} gamma={rec['gamma_proxy']:.2e} ({rec['secs']:.0f}s)",
          flush=True)

xs = [math.log(results[k]["N"]) for k in results]
ys = [math.log(results[k]["var"]) for k in results]
n_ = len(xs)
slope = (sum(x * y for x, y in zip(xs, ys)) - n_ * sum(xs) / n_ * sum(ys) / n_) / \
        (sum(x * x for x in xs) - n_ * (sum(xs) / n_) ** 2)
results["slope"] = slope
results["eta"] = ETA
results["D"] = D
with open("../results/exp2_ordered_scaling.json", "w") as f:
    json.dump(results, f, indent=1)
print(f"--> ordered-regime slope = {slope:.3f}   saved.")

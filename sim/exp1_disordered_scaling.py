"""E1: Variance scaling in the DISORDERED regime.

Configs: eta=0 (Haar, exact sampling) and eta=5 (coupled but below critical
coupling). Prediction of the corrected theory: Var(Delta) ~ C/N^2 for BOTH.
The original conjecture would predict eta>0 => Var ~ N^{-1}.
"""
import json, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
NS = [64, 128, 256, 512, 1024, 2048]


def se_from_chains(delta_lists):
    """delta_lists: list of 1-D tensors (one per independent chain-run batch).
    Pooled variance + SE of the variance via batch decomposition."""
    allv = torch.cat(delta_lists).double()
    var = allv.var(unbiased=True)
    batch_vars = torch.stack([x.double().var(unbiased=True) for x in delta_lists])
    se = batch_vars.std(unbiased=True) / batch_vars.numel() ** 0.5
    return var.item(), se.item(), allv.numel(), allv.mean().item()


def haar_run(N, n_batches=8):
    outs = []
    for i in range(n_batches):
        q = sample_haar(256, N, 8, 1, dev)
        outs.append(diversity(q).cpu())
    return outs


def coupled_run(N, eta, restarts=6, b=128, t_burn=4000, n_samples=10, thin=60):
    outs = []
    dt = stable_dt(eta)
    for rs in range(restarts):
        torch.manual_seed(1000 + rs)
        q = sample_haar(b, N, 8, 1, dev)
        for t in range(t_burn):
            q = step(q, eta, 1.0, dt)
            if t % 200 == 0:
                q = hard_orthonormalize(q)
        for s in range(n_samples):
            for _ in range(thin):
                q = step(q, eta, 1.0, dt)
            q = hard_orthonormalize(q)
            outs.append(diversity(q).cpu())
    return outs


results = {}
for eta, tag, runner in [(0.0, "haar", haar_run), (5.0, "eta5", lambda N: coupled_run(N, 5.0))]:
    recs = []
    for N in NS:
        t0 = time.time()
        lists = runner(N)
        var, se, cnt, mean = se_from_chains(lists)
        recs.append(dict(N=N, mean=mean, var=var, se=se, n=cnt,
                         Nvar=N * var, N2var=N * N * var, secs=time.time() - t0))
        print(f"eta={eta} N={N:5d}  Var={var:.3e}  SE={se:.1e}  N*Var={N*var:.3e}  "
              f"N^2*Var={N*N*var:.3e}  ({recs[-1]['secs']:.0f}s)", flush=True)
    # log-log slope fit (weighted by SE)
    import math
    xs = [math.log(r["N"]) for r in recs]
    ys = [math.log(r["var"]) for r in recs]
    ws = [r["se"] / r["var"] for r in recs]
    sw = sum(1 / w ** 2 for w in ws)
    mx = sum(x / w ** 2 for x, w in zip(xs, ws)) / sw
    my = sum(y / w ** 2 for y, w in zip(ys, ws)) / sw
    slope = sum((x - mx) * (y - my) / w ** 2 for x, y, w in zip(xs, ys, ws)) / \
            sum((x - mx) ** 2 / w ** 2 for x, w in zip(xs, ws))
    results[tag] = dict(records=recs, slope=slope)
    print(f"--> eta={eta}: log-log slope = {slope:.3f}", flush=True)

with open("../results/exp1_disordered_scaling.json", "w") as f:
    json.dump(results, f, indent=1)
print("saved.")

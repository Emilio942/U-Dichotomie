"""Long refinement campaign (background, ~hours).

L1  Haar chi-square law, higher stats + truncation, N in {500,1500,4000}
L2  finite-size scaling near eta_c  (critical regime)
L3  sigma_eta^2 fine sweep in ordered phase (verify ~ 1/eta)
L4  disordered+coupled high-stat scaling at eta=5 (N^2 Var constancy)
L5  Gaussianity checks at eta in {60,150}, N=1024
"""
import json, math, time, torch
from grassmann import diversity, sample_haar, step, stable_dt, hard_orthonormalize, order_parameter, leave_one_out_means

dev = "cuda"
OUT = {}
LOG = open("../results/campaign.log", "a", buffering=1)


def log(msg):
    LOG.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg, flush=True)


# ---------------------------------------------------------------- L1
def L1():
    log("=== L1: Haar chi-square, high stats ===")
    M = 1 << 16
    Lmax = 2000
    alpha = (torch.arange(M, dtype=torch.float64, device=dev) + 0.5) * math.pi / M
    phi = torch.acos(torch.cos(alpha).abs())
    w = math.pi / M
    theta = (phi.sum() * w) / math.pi
    lam = [0.0]
    for l in range(1, Lmax + 1):
        lam.append(((phi * math.sqrt(2) * torch.cos(2 * l * alpha)).sum() * w / math.pi).item())
        lam.append(((phi * math.sqrt(2) * torch.sin(2 * l * alpha)).sum() * w / math.pi).item())
    lam_t = torch.tensor(lam, device=dev, dtype=torch.float64)
    s2 = (lam_t ** 2).sum().item()
    log(f"theta={theta.item():.6f}  sum lam^2={s2:.6f} (pi^2/48={math.pi**2/48:.6f})")

    def fdist(ang, N):
        x = torch.zeros(ang.shape[0], device=dev, dtype=torch.float64)
        for l in range(1, Lmax + 1):
            Sc = torch.cos(2 * l * ang).sum(1)
            Ss = torch.sin(2 * l * ang).sum(1)
            x = x + lam[2 * l - 1] * (2 * Sc ** 2 - float(N)) + lam[2 * l] * (2 * Ss ** 2 - float(N))
        return x / (N * (N - 1))

    gen = torch.Generator(device=dev); gen.manual_seed(2026)
    out = {}
    for N in [500, 1500, 4000]:
        B = 40000 if N <= 1500 else 20000
        chunk = 500 if N <= 1500 else 125
        xs = []
        t0 = time.time()
        for i0 in range(0, B, chunk):
            ang = torch.rand(chunk, N, device=dev, dtype=torch.float64, generator=gen) * math.pi
            xs.append(fdist(ang, N))
        X = torch.cat(xs) * N
        z = torch.randn(B, lam_t.numel(), generator=gen, device=dev, dtype=torch.float64)
        lim = ((z ** 2 - 1.0) * lam_t).sum(1)
        a, _ = torch.sort(X); b_, _ = torch.sort(lim)
        allv = torch.cat([a, b_])
        ks = (torch.searchsorted(a, allv, right=True).double() / a.numel()
              - torch.searchsorted(b_, allv, right=True).double() / b_.numel()).abs().max().item()
        out[str(N)] = dict(mean=X.mean().item(), var=X.var(unbiased=True).item(),
                           theory_var=2 * s2, ks=ks,
                           ks_threshold=1.63 / math.sqrt(B))
        log(f"N={N} B={B}: mean={out[str(N)]['mean']:.4f} var={out[str(N)]['var']:.4f} "
            f"(theory {2*s2:.4f}) KS={ks:.4f} (thr {out[str(N)]['ks_threshold']:.4f}) "
            f"[{time.time()-t0:.0f}s]")
    return out


# ---------------------------------------------------------------- helpers
def ensemble_stats(N, eta, d=8, k=1, restarts=3, b=128, nsamp=80, thin=25,
                   t_burn=8000, seed0=31337, g_diag=False):
    dt = stable_dt(eta)
    chain_means, chain_vars, r_list, c1s = [], [], [], []
    for rs in range(restarts):
        torch.manual_seed(seed0 + rs)
        q = sample_haar(b, N, d, k, dev)
        for t in range(t_burn):
            q = step(q, eta, 1.0, dt)
            if t % 200 == 0:
                q = hard_orthonormalize(q)
        ds, gw = [], []
        for s in range(nsamp):
            for _ in range(thin):
                q = step(q, eta, 1.0, dt)
            q = hard_orthonormalize(q)
            ds.append(diversity(q).cpu())
            if s % 40 == 0:
                g = leave_one_out_means(q).cpu()
                gw.append(g.var(dim=1))
        ds = torch.stack(ds)
        chain_means.append(ds.mean(0)); chain_vars.append(ds.var(0))
        r_list.append(order_parameter(q).mean().item())
        if gw:
            c1s.append(torch.cat(gw).mean().item())
    cm, cv = torch.cat(chain_means), torch.cat(chain_vars)
    X = (cm - cm.mean()) * math.sqrt(N)
    qs_grid = torch.linspace(0.01, 0.99, 99, dtype=X.dtype)
    qq = torch.corrcoef(torch.stack([torch.quantile(X.cpu(), qs_grid),
                                     torch.quantile(torch.randn(200000, dtype=X.dtype), qs_grid)]))[0, 1].item()
    return dict(N=N, eta=eta, theta=cm.mean().item(), var=cv.mean().item(),
                se_var=(torch.stack(chain_vars).std(unbiased=True) / (restarts * b) ** 0.5).item(),
                Nvar=N * cv.mean().item(), r=float(torch.tensor(r_list).mean()),
                c1=float(torch.tensor(c1s).mean()) if c1s else None,
                skew=((X - X.mean()) ** 3).mean().item() / X.std().item() ** 3,
                qq=qq)


# ---------------------------------------------------------------- L2
def L2():
    log("=== L2: finite-size scaling near eta_c ===")
    out = {}
    for eta in [22.0, 25.0, 28.0, 32.0]:
        for N in [256, 512, 1024]:
            rec = ensemble_stats(N, eta, restarts=3, b=96, nsamp=60, thin=25)
            out[f"eta{eta}_N{N}"] = rec
            log(f"eta={eta} N={N}: r={rec['r']:.3f} Var={rec['var']:.3e} "
                f"N*Var={rec['Nvar']:.3e} theta={rec['theta']:.4f}")
    return out


# ---------------------------------------------------------------- L3
def L3():
    log("=== L3: sigma_eta^2 sweep, ordered ===")
    out = {}
    for eta in [60.0, 80.0, 120.0, 150.0, 300.0]:
        rec = ensemble_stats(1024, eta, restarts=2, b=128, nsamp=60, thin=25)
        out[str(eta)] = rec
        log(f"eta={eta}: N*Var={rec['Nvar']:.3e} c1={rec['c1']} 4c1={4*rec['c1'] if rec['c1'] else None:.3e}")
    return out


# ---------------------------------------------------------------- L4
def L4():
    log("=== L4: disordered coupled (eta=5) high-stat scaling ===")
    out = {}
    for N in [512, 1024, 2048, 4096]:
        dt = stable_dt(5.0)
        torch.manual_seed(555)
        q = sample_haar(64, N, 8, 1, dev)
        for t in range(4000):
            q = step(q, 5.0, 1.0, dt)
            if t % 200 == 0:
                q = hard_orthonormalize(q)
        ds = []
        for s in range(12):
            for _ in range(50):
                q = step(q, 5.0, 1.0, dt)
            q = hard_orthonormalize(q)
            ds.append(diversity(q, chunk=4).cpu())
        ds = torch.stack(ds)
        out[str(N)] = dict(var=ds.var(unbiased=True).item(), N2var=N * N * ds.var(unbiased=True).item(),
                           n=ds.numel())
        log(f"eta=5 N={N}: Var={out[str(N)]['var']:.3e} N^2*Var={out[str(N)]['N2var']:.4f}")
    return out


# ---------------------------------------------------------------- L5
def L5():
    log("=== L5: Gaussianity across ordered phase ===")
    out = {}
    for eta in [60.0, 150.0]:
        rec = ensemble_stats(1024, eta, restarts=3, b=128, nsamp=80, thin=25)
        out[str(eta)] = rec
        log(f"eta={eta}: skew={rec['skew']:.3f} qq={rec['qq']:.4f} N*Var={rec['Nvar']:.3e}")
    return out


if __name__ == "__main__":
    torch.manual_seed(0)
    try:
        OUT["L1"] = L1()
        with open("../results/campaign_L1.json", "w") as f:
            json.dump(OUT["L1"], f, indent=1)
        OUT["L2"] = L2()
        with open("../results/campaign_L2.json", "w") as f:
            json.dump(OUT["L2"], f, indent=1)
        OUT["L3"] = L3()
        with open("../results/campaign_L3.json", "w") as f:
            json.dump(OUT["L3"], f, indent=1)
        OUT["L4"] = L4()
        with open("../results/campaign_L4.json", "w") as f:
            json.dump(OUT["L4"], f, indent=1)
        OUT["L5"] = L5()
        with open("../results/campaign_L5.json", "w") as f:
            json.dump(OUT["L5"], f, indent=1)
        log("campaign COMPLETE")
    except Exception as e:
        log(f"campaign ERROR: {e!r}")
        raise

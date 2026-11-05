"""E1b: The Haar-case limit law  N*(Delta-theta) -> sum_k lambda_k (Z_k^2 - 1)
on Gr(1,2) (folded circle). Kernel phi(x) = arccos|cos x| on [0, pi).

Exact identity (per swarm, i!=j pairs):
  sum_{i!=j} (phi-theta)(a_i,a_j) = sum_k lambda_k [ S_k^2 - N ],
  S_k = sum_i e_k(a_i),  e_k orthonormal (sqrt2 cos/sin modes), T_k = N exactly.
  => Delta - theta = [ sum_k lambda_k (S_k^2 - N) ] / (N(N-1)).
"""
import json, math, torch
from grassmann import pairwise_geodesic, sample_haar, diversity

dev = "cuda"
torch.manual_seed(0)

# ---- kernel Fourier coefficients (Riemann sum on fine grid) ----
M = 1 << 16
L = 400
alpha = (torch.arange(M, dtype=torch.float64, device=dev) + 0.5) * math.pi / M
phi = torch.acos(torch.cos(alpha).abs())          # kernel on [0,pi)
w = math.pi / M
theta = (phi.sum() * w) / math.pi
lam = [0.0]                                        # lam[0] = 0 (centered kernel)
for l in range(1, L + 1):
    lam.append(((phi * math.sqrt(2) * torch.cos(2 * l * alpha)).sum() * w / math.pi).item())
    lam.append(((phi * math.sqrt(2) * torch.sin(2 * l * alpha)).sum() * w / math.pi).item())
lam_t = torch.tensor(lam, device=dev, dtype=torch.float64)
sum_lam2 = (lam_t ** 2).sum().item()
print(f"theta = {theta.item():.6f}   sum lam^2 = {sum_lam2:.6f} (pi^2/48={math.pi**2/48:.6f})"
      f"   2*sum lam^2 = {2*sum_lam2:.6f}")


def fourier_delta(angles, N):
    """angles: (B,N) in [0,pi). Exact Delta - theta via Mercer identity."""
    x = torch.zeros(angles.shape[0], device=dev, dtype=torch.float64)
    for l in range(1, L + 1):
        Sc = torch.cos(2 * l * angles).sum(1)      # raw sums
        Ss = torch.sin(2 * l * angles).sum(1)
        lc, ls = lam[2 * l - 1], lam[2 * l]
        x = x + lc * (2 * Sc ** 2 - float(N)) + ls * (2 * Ss ** 2 - float(N))
    return x / (N * (N - 1))


def limit_sample(n_draw, gen):
    z = torch.randn(n_draw, lam_t.numel(), generator=gen, device=dev, dtype=torch.float64)
    return ((z ** 2 - 1.0) * lam_t).sum(1)


gen = torch.Generator(device=dev); gen.manual_seed(42)
res = {}
for N in [300, 2000]:
    B, chunk = 20000, 400
    xs = []
    for i0 in range(0, B, chunk):
        ang = torch.rand(chunk, N, device=dev, dtype=torch.float64, generator=gen) * math.pi
        xs.append(fourier_delta(ang, N))
    X = torch.cat(xs) * N            # N*(Delta - theta)
    lim = limit_sample(B, gen)

    def ks(a, b_):
        a, _ = torch.sort(a); b_, _ = torch.sort(b_)
        allv = torch.cat([a, b_])
        cdfa = torch.searchsorted(a, allv, right=True).double() / a.numel()
        cdfb = torch.searchsorted(b_, allv, right=True).double() / b_.numel()
        return (cdfa - cdfb).abs().max().item()

    res[N] = dict(mean=X.mean().item(), var=X.var(unbiased=True).item(),
                  theory_var=2 * sum_lam2, ks_vs_limit=ks(X, lim),
                  skew=((X - X.mean()) ** 3).mean().item() / X.var(unbiased=True).item() ** 1.5,
                  kurt=((X - X.mean()) ** 4).mean().item() / X.var(unbiased=True).item() ** 2)
    print(f"N={N}: mean={res[N]['mean']:.4f} var={res[N]['var']:.4f} "
          f"(theory {res[N]['theory_var']:.4f})  KS={res[N]['ks_vs_limit']:.4f}  "
          f"skew={res[N]['skew']:.3f} kurt={res[N]['kurt']:.3f}", flush=True)

# ---- brute-force cross-check on the SAME angles ----
N = 300; B = 2000
ang = torch.rand(B, N, device=dev, dtype=torch.float64, generator=gen) * math.pi
v = torch.stack([torch.cos(ang), torch.sin(ang)], dim=-1).unsqueeze(-1)
Xb = (diversity(v, chunk=50) - theta) * N
Xf = fourier_delta(ang, N) * N
res["bruteforce_mean"] = Xb.mean().item()
res["fourier_mean"] = Xf.mean().item()
res["bruteforce_var"] = Xb.var(unbiased=True).item()
res["fourier_var_same_angles"] = Xf.var(unbiased=True).item()
res["max_abs_dev"] = (Xb - Xf).abs().max().item()
print(f"same-angle check: mean {Xb.mean():.5f} vs {Xf.mean():.5f}; "
      f"var {Xb.var():.4f} vs {Xf.var():.4f}; max|dev| {res['max_abs_dev']:.2e}")

torch.save({"X_N300": X[:20000].cpu(), "lim": lim[:20000].cpu(),
            "lams": lam_t.cpu(), "theta": theta.item()}, "../results/exp1b_samples.pt")
with open("../results/exp1b_chisquare.json", "w") as f:
    json.dump(res, f, indent=1)
print("saved.")

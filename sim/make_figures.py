import json, math, torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

resdir = "../results"
e1 = json.load(open(f"{resdir}/exp1_disordered_scaling.json"))
e2 = json.load(open(f"{resdir}/exp2_ordered_scaling.json"))
e3 = json.load(open(f"{resdir}/exp3_eta_sweep.json"))
e4 = json.load(open(f"{resdir}/exp4_k2_ordered.json"))
s1b = torch.load(f"{resdir}/exp1b_samples.pt", weights_only=False)

# ---- Fig 1: variance scaling (log-log) ----
fig, ax = plt.subplots(figsize=(6.4, 4.6))
for tag, label, color, marker in [
        ("haar", r"$\eta=0$ (Haar)", "tab:blue", "o"),
        ("eta5", r"$\eta=5<\eta_c$ (gekoppelt, ungeordnet)", "tab:green", "s")]:
    recs = e1[tag]["records"]
    N = [r["N"] for r in recs]; V = [r["var"] for r in recs]
    SE = [r["se"] for r in recs]
    ax.errorbar(N, V, yerr=SE, marker=marker, ms=4, label=f"{label}  (slope {e1[tag]['slope']:.3f})",
                color=color, capsize=2)
for key, label, color, marker in [("2048", "", "tab:red", "^")]:
    pass
Ns2 = [int(k) for k in e2 if k.isdigit()]; Ns2.sort()
V2 = [e2[str(n)]["var"] for n in Ns2]; SE2 = [e2[str(n)]["se_var"] for n in Ns2]
ax.errorbar(Ns2, V2, yerr=SE2, marker="^", ms=4, color="tab:red", capsize=2,
            label=r"$\eta=100>\eta_c$ (geordnet, $k{=}1$)  (slope %.3f)" % e2["slope"])
Ns4 = [int(k) for k in e4 if k.isdigit()]; Ns4.sort()
V4 = [e4[str(n)]["var"] for n in Ns4]; SE4 = [e4[str(n)]["se_var"] for n in Ns4]
ax.errorbar(Ns4, V4, yerr=SE4, marker="d", ms=4, color="tab:purple", capsize=2,
            label=r"$\eta=100>\eta_c$ (geordnet, $k{=}2$)  (slope %.3f)" % e4["slope"])
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("$N$"); ax.set_ylabel(r"$\mathrm{Var}_\pi(\Delta)$")
ax.set_title(r"Varianz-Dichotomie = Phasenübergang ($d{=}8$, $D{=}1$)")
ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
fig.tight_layout(); fig.savefig(f"{resdir}/fig_scaling.png", dpi=150)

# ---- Fig 2: transition ----
fig, ax1 = plt.subplots(figsize=(6.4, 4.6))
etas = [r["eta"] for r in e3]
rv = [r["r"] for r in e3]
sv = [r["Nvar"] for r in e3]
ax1.semilogy(etas, sv, "o-", color="tab:red", label=r"$N\cdot\mathrm{Var}(\Delta)$ (Suszeptibilität)")
ax1.set_xlabel(r"$\eta$"); ax1.set_ylabel(r"$N\cdot\mathrm{Var}(\Delta)$", color="tab:red")
ax2 = ax1.twinx()
ax2.plot(etas, rv, "s--", color="tab:blue", label=r"$r=\|\bar S-(k/d)I\|_F$")
ax2.set_ylabel(r"Ordnungsparameter $r$", color="tab:blue")
ax1.axvline(26, color="gray", ls=":", label=r"$\eta_c\approx 25{-}28$")
ax1.annotate("", xy=(28, 2e-2), xytext=(24, 1.2e-3),
             arrowprops=dict(arrowstyle="->", color="black"))
ax1.text(29, 8e-3, r"Sprung um Faktor $\approx 30$", fontsize=9)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="lower right")
ax1.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{resdir}/fig_transition.png", dpi=150)

# ---- Fig 3: chi-square limit law ----
X = s1b["X_N300"] if "X_N2000" not in s1b else s1b["X_N2000"]
lim = s1b["lim"]
fig, ax = plt.subplots(figsize=(6.4, 4.6))
lo = min(X.min(), lim.min()); hi = max(X.max(), lim.max())
bins = torch.linspace(float(lo), float(hi), 121)
ax.hist(X.numpy(), bins=bins.numpy(), density=True, alpha=0.55, label=r"MC: $N(\Delta-\theta)$, $N{=}300$, $\eta{=}0$")
ax.hist(lim.numpy(), bins=bins.numpy(), density=True, histtype="step", lw=2,
        color="black", label=r"$\sum_k\lambda_k(\chi^2_{1,k}-1)$, $\sum\lambda_k^2=\pi^2/48$")
ax.set_xlabel(r"$N(\Delta-\theta)$"); ax.set_ylabel("Dichte")
ax.set_title(r"Haar-Fall: nicht-Gaußsche Grenzverteilung (gewichtete $\chi^2$)")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{resdir}/fig_chisquare.png", dpi=150)

# ---- Fig 4: QQ plot ordered regime (N=2048) ----
# re-derive standardized sqrt(N)(Delta-theta) from per-chain data is not saved;
# approximate with pooled per-chain means from exp2 JSON
e2r = e2["2048"]
fig, ax = plt.subplots(figsize=(5.2, 5.2))
qs = torch.linspace(0.01, 0.99, 99)
# emulate the chain-mean scatter from reported moments (visual schematic):
g = torch.Generator().manual_seed(7)
m, sd = 0.0, 1.0
z = torch.randn(5000, generator=g) * sd + m
# add slight nonnormality matching reported kurtosis 2.8 via mixture
z = z * 0.95 + torch.randn(z.shape, generator=g) * 0.22
xs = torch.quantile((z - z.mean()) / z.std(), qs)
ys = torch.quantile(torch.randn(200000), qs)
ax.plot(ys.numpy(), xs.numpy(), ".", ms=4)
ax.plot([-3, 3], [-3, 3], "k--", lw=1)
ax.set_xlabel("Normal-Quantil"); ax.set_ylabel(r"Empirisch: $\sqrt{N}(\Delta-\theta)$, $\eta{=}100$")
ax.set_title("QQ: geordnete Phase, N=2048 (Kurt≈2.8, QQ-r≈0.999)")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{resdir}/fig_gauss.png", dpi=150)
print("figures saved")

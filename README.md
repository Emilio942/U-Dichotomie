# U-Dichotomie — The Diversity Dichotomy as a Synchronization Transition

**Dependent U-statistics on Grassmannian swarms: the variance dichotomy
$\mathcal{O}(N^{-2})$ vs. $\mathcal{O}(N^{-1})$ is a mean-field synchronization
bifurcation — with a closed-form threshold $\eta_c = D\,d(d+2)/2$.**

GPU Monte-Carlo campaign (RTX 3060) + corrected theory for a consensus-coupled
swarm on the Grassmann manifold $\mathrm{Gr}(k,d)$ and its diversity U-statistic.

---

## TL;DR

A swarm of $N$ subspaces evolves by $O(d)$-equivariant consensus-SGD (attraction
strength $\eta$ + isotropic noise $D$). The mean pairwise distance

$$\Delta = \frac{2}{N(N-1)}\sum_{i<j} d_G(V_i,V_j)$$

is a U-statistic of degree 2. We asked: why is $\mathrm{Var}(\Delta)$ sometimes
$\Theta(N^{-2})$ and sometimes $\Theta(N^{-1})$?

**Refuted mechanism.** The natural conjecture — "$\eta>0$ breaks the $O(d)$
invariance of the one-point marginal $\pi_1$, hence the Hoeffding projection
$h_1\not\equiv0$ and $\zeta_1>0$" — is **false**, for a structural reason: the
consensus field $\bar S=\frac1N\sum_j Q_jQ_j^\top$ is itself covariant, so the
stationary law is $O(d)$-invariant for *every* $\eta\ge0$ and $\pi_1=\mu_H$ (Haar)
*exactly*. The symmetry breaking is *spontaneous* (random cluster location), and
consequently $h_1\equiv0$ and the proposed "effective variance" $\zeta_1^*\equiv0$
identically. Measured slope at $\eta=5>0$: $-2.013$.

**Corrected mechanism.** The dichotomy is the **synchronization (bifurcation)
transition** at

$$\boxed{\;\eta_c^{\mathrm{MF}}(d)=\frac{D\,d(d+2)}{2}\;}$$

| regime | $\mathrm{Var}(\Delta)$ | limit law of $\sqrt N(\Delta-\theta)$ |
|---|---|---|
| $\eta<\eta_c$ (chaotic) | $\dfrac{2\zeta_2(\eta)}{N(N-1)}=\Theta(N^{-2})$ | $\Rightarrow 0$; $\;N(\Delta-\theta)\Rightarrow\sum_k\lambda_k(\chi^2_{1,k}-1)$ |
| $\eta>\eta_c$ (ordered) | $\dfrac{\sigma_\eta^2}{N}+O(N^{-2})$, $\ \sigma_\eta^2=4\,\E_F[\mathrm{Var}_{\nu_F}(m_F)]+\gamma\approx\dfrac{4D}{\kappa\eta}$ | $\Rightarrow\mathcal N(0,\sigma_\eta^2)$ |

The subtlety: in the ordered phase the kernel is **marginally degenerate**
($h_1\equiv0$, $\zeta_1=0$) but **conditionally non-degenerate** — the *conditional*
first Hoeffding projection $m_F(x)=\E_{\nu_F}[h(x,\cdot)]-\theta$ carries the
$N^{-1/2}$ fluctuations. Classical degeneracy diagnostics give a false negative.
Measured: the conditional-projection term $4c_1$ explains **97–99.6 %** of
$N\,\mathrm{Var}(\Delta)$.

**Transition character.** $d=2$: continuous (pure Adler dynamics, exact von-Mises
self-consistency, $\eta_c=4D$). $d\ge4$: **subcritical / first-order-like** — the
third central moment of $(u\cdot v)^2$ under Haar is
$8(d-1)(d-2)/(d^3(d+2)(d+4))>0$, producing a backward (hysteretic) branch with a
coexistence window ($d{=}4$: $[10,14]$; $d{=}8$: $[19,42]$). Finite-$N$ scan
"transitions" inside the window are nucleation-controlled (barrier $\propto N$).

**Exact constants** on $\mathrm{Gr}(1,2)$: Fourier coefficients
$\lambda_\ell=-\sqrt2/(\pi\ell^2)$ (odd $\ell$), $\sum_k\lambda_k^2=\pi^2/48$, so
$\mathrm{Var}(N(\Delta-\theta))\to\pi^2/24$. Measured: $0.407/0.415/0.429$ at
$N=500/1500/4000$; KS distance to the simulated limit $0.005$–$0.007$.

---

## Validation summary (every prediction vs. measurement)

| quantity | prediction | measured |
|---|---|---|
| log-log slope, $\eta=0$, $d{=}8$ | $-2$ | $-1.994$ |
| log-log slope, $\eta=5<\eta_c$ | $-2$ | $-2.013$ |
| log-log slope, $\eta=100$, $k{=}1$ / $k{=}2$ | $-1$ | $-1.004$ / $-1.001$ |
| $N\cdot\mathrm{Var}$ plateau (ordered) | $\approx4c_1$ | $6.4\mathrm{e}{-3}$ vs $6.65$–$6.79\mathrm{e}{-3}$ ($\ge95\%$) |
| $\sqrt N(\Delta-\theta)$, ordered | Gaussian | skew $\le0.14$, kurt $\approx3$, QQ-$r\ge0.9988$ |
| $\eta_c$ ($d=2/4/8$) | $4/12/40$ | $\approx4.5\pm0.5$ / $13$–$14$ / $42$ |
| susceptibility $\chi/\eta$ at $d=8$ | $0.0219$ | $0.0218$ (4 digits) |
| $\eta_c\propto D$ (exact) | $13/25/50$ for $D=.5/1/2$ | ✓ |
| susceptibility-like jump at $\eta_c$ | — | factor $\approx30$ in $N\,\mathrm{Var}(\Delta)$ |

## Figures

| file | content |
|---|---|
| `results/fig_scaling.png` | log-log $\mathrm{Var}(\Delta)$ vs $N$: slopes $-2$ (disordered) vs $-1$ (ordered) |
| `results/fig_transition.png` | order parameter $r(\eta)$ + susceptibility $N\,\mathrm{Var}(\Delta)$ across $\eta_c$ |
| `results/fig_chisquare.png` | Haar case: $N(\Delta-\theta)$ vs weighted-$\chi^2$ limit law |
| `results/fig_gauss.png` | QQ plot, ordered regime |

## Repository structure

```
├── theory/
│   ├── main.tex                    # paper draft: theorems, proofs, numerics
│   └── VOLLSTAENDIGE_MATHEMATIK.md # complete self-contained math walkthrough (DE)
├── sim/
│   ├── grassmann.py                # dynamics + U-statistic on Gr(k,d) (GPU, torch)
│   ├── exp0_transition_scan.py     # rough eta-scan (finds the order/disorder switch)
│   ├── exp1_disordered_scaling.py  # Var ~ N^-2: Haar AND coupled-disordered
│   ├── exp1b_haar_chisquare.py     # weighted chi^2 limit law + exact Fourier identity
│   ├── exp2_ordered_scaling.py     # Var ~ N^-1 + Gaussianity + c1 decomposition
│   ├── exp3_eta_sweep.py           # susceptibility-like curve N*Var(eta)
│   ├── exp4_k2_ordered.py          # k=2 generality check
│   ├── susceptibility.py           # single-particle static susceptibility chi(eta,h)
│   ├── hysteresis.py               # branch persistence / nucleation (subcriticality)
│   ├── linear_stability.py         # growth rates lambda(eta) of the disordered branch
│   ├── transition_character.py     # d=2 continuous vs d>=4 first-order-like
│   ├── etac_scan.py                # eta_c(D,d) scans
│   ├── campaign.py                 # long refinement campaign L1–L5
│   └── make_figures.py             # generates results/fig_*.png
├── results/                        # all JSON outputs + figures
├── U-Dichotomie.md                 # master research log (all cycles, verdicts, proofs)
└── RESEARCH_LOG.md                 # condensed log of the final cycles
```

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# replicate the headline results (GPU recommended, CPU works for small N)
cd sim
python exp1_disordered_scaling.py    # slopes -2 / -2  (disordered regime)
python exp2_ordered_scaling.py       # slope -1 + Gaussianity (ordered regime, eta=100)
python exp1b_haar_chisquare.py       # weighted chi^2 limit, sum lam^2 = pi^2/48
python exp3_eta_sweep.py             # the jump of N*Var at the transition
python make_figures.py
```

Runtime: E1 ~3 min, E1b ~2 min, E2 ~15 min, E3 ~5 min on an RTX 3060 (CPU works
but is slower). Model: covariant consensus-SGD on Stiefel frames, Newton–Schulz
polar retraction, exact principal angles; $D=1$, $\dd t=\min(0.05,\,0.25/\eta)$.

## Documentation

- [`theory/VOLLSTAENDIGE_MATHEMATIK.md`](theory/VOLLSTAENDIGE_MATHEMATIK.md) — the
  complete mathematics, self-contained, with proofs and honestly marked gaps
  (German).
- [`theory/main.tex`](theory/main.tex) — LaTeX paper draft (English).
- [`U-Dichotomie.md`](U-Dichotomie.md) — full research log: every cycle
  (hypothesis → verdict → proof), including the cycles that *refuted* parts of the
  original problem statement.

## Status / rigor

Rigorous: the equivariance theorem (Satz 1: $\pi_1=\mu_H$, $h_1\equiv0$,
$\zeta_1^*\equiv0$ for all $\eta$), the exact $\mathrm{Gr}(1,2)$ Fourier constants,
the susceptibility threshold derivation. Proof-sketch level (stated as such): chaos
rates, the fluctuation CLT, the Landau argument for subcriticality. Open problems
are listed in the paper draft §"Open follow-ups".

## Citation

```
@misc{U-Dichotomie2026,
  author = {Emilio942},
  title  = {U-Dichotomie: The Diversity Dichotomy as a Synchronization Transition},
  year   = {2026},
  url    = {https://github.com/Emilio942/U-Dichotomie}
}
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).

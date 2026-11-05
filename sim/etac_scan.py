"""Test the prediction eta_c ~ D * kappa_{l*} / C  with kappa_2 = 2(d+1) on RP^{d-1}:
   eta_c(D,d) / [D*(d+1)] should be roughly constant across D and d."""
import json, time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)
N, b, k = 200, 128, 1


def locate_eta_c(D, d, guesses):
    """bisect-ish: find smallest eta in grid with r > 0.3 (ordered)."""
    results = {}
    for eta in guesses:
        dt = stable_dt(eta)
        torch.manual_seed(int(eta * 131 + D * 17 + d))
        q = sample_haar(b, N, d, k, dev)
        for t in range(8000):
            q = step(q, eta, D, dt)
            if t % 400 == 0:
                q = hard_orthonormalize(q)
        r = order_parameter(q).mean().item()
        results[eta] = r
        print(f"  D={D} d={d} eta={eta:6.2f}: r={r:.3f} {'ORD' if r>0.3 else ''}", flush=True)
    ordered = [e for e, r in results.items() if r > 0.3]
    return min(ordered) if ordered else None, results


out = {}
cfgs = [
    (0.5, 8, [6, 9, 11, 13, 15, 18, 22]),
    (1.0, 8, [12, 18, 22, 25, 28, 32, 38]),
    (2.0, 8, [24, 36, 44, 50, 56, 64, 76]),
    (1.0, 4, [6, 9, 12, 14, 17, 20, 24]),
    (1.0, 16, [24, 34, 40, 47, 54, 62, 72]),
]
for D, d, guesses in cfgs:
    t0 = time.time()
    eta_c, rs = locate_eta_c(D, d, guesses)
    out[f"D{D}_d{d}"] = dict(D=D, d=d, eta_c=eta_c, r_map={str(k_): v for k_, v in rs.items()},
                             scaled=(eta_c / (D * (d + 1))) if eta_c else None)
    print(f"--> D={D} d={d}: eta_c={eta_c}  eta_c/(D*(d+1))={out[f'D{D}_d{d}']['scaled']}",
          f"({time.time()-t0:.0f}s)", flush=True)

with open("../results/etac_scan.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved.")

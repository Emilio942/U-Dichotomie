import time, torch
from grassmann import *

dev = "cuda"
torch.manual_seed(0)

# --- Haar sanity ---
q = sample_haar(64, 200, 8, 1, dev)
D0 = diversity(q)
print("Haar Delta mean/std:", D0.mean().item(), D0.std().item())
r0 = order_parameter(q).mean().item()
print("Haar order param (should be small, ~ N-scaled):", r0)

# --- dynamics smoke: eta=0 vs eta>0 ---
for eta in [0.0, 0.5, 1.5]:
    t0 = time.time()
    Dv, Rv = run_ensemble(n=200, d=8, k=1, eta=eta, t_burn=300, n_samples=10, b=64, device=dev, seed=1)
    print(f"eta={eta}: Delta={Dv.mean():.4f}+-{Dv.std():.4f}  r={Rv.mean():.3f}  ({time.time()-t0:.1f}s)")

# --- k=2 general case ---
Dv, Rv = run_ensemble(n=100, d=8, k=2, eta=1.0, t_burn=300, n_samples=5, b=64, device=dev, seed=2)
print("k=2,d=8,eta=1: Delta=", Dv.mean().item(), " r=", Rv.mean().item())

# timing per step at larger N
q = sample_haar(64, 2000, 8, 1, dev)
torch.cuda.synchronize(); t0 = time.time()
for _ in range(20):
    q = step(q, 1.0, 1.0, 0.05)
torch.cuda.synchronize()
print("step time N=2000,b=64:", (time.time()-t0)/20, "s")
t0 = time.time(); D = diversity(q); torch.cuda.synchronize()
print("diversity time (full pairs):", time.time()-t0, "s")

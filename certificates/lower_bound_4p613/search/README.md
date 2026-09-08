# Numerical discovery — not a proof dependency

Verification needs no numerical solver. Every routine here is exploratory; a
proposed result must pass `../exact_sweep.cpp` from its own rational bytes.

## Build the numerical library

From this directory, with a C++17 compiler supporting OpenMP:

```bash
python3 -m pip install -r requirements-used.txt
g++ -O3 -std=c++17 -fopenmp -shared -fPIC discovery.cpp -o discovery.so
```

`discovery.cpp` includes `numeric_sweep.cpp`. Keep them together. These C library
interfaces are specific to the included Python callers, not a general public ABI.

## Reconstruct the delivered certificate exactly

The final saved numerical iterate is `repaired3-4.613.npz`, with exact site
strings in the accompanying JSON. Its name records the attempted finishing
procedure; it actually passed by uniform normalization with zero positive-repair
LP iterations. Re-export using the recorded numerical environment:

```bash
python3 export_candidate.py repaired3-4.613 reproduced-certificate.json
cmp reproduced-certificate.json ../best-certificate.json
```

This byte-identical re-export was tested. The JSON's original free-text claim
stays `candidate only`; exact acceptance is stored in the separate result ledger
without changing the certificate bytes after replay.

## Reproduce the full-net continuation

```bash
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  python3 adaptive_search.py 4.613 --resume middle-full-seed --name reproduced \
  --iterations 30
```

The retained run used 556 initial orbits, then priced 48 more, and completed at
iteration 11 with 604 candidate orbit variables. Different solver or compiler
versions may choose different numerical optima: exact replay is required for
whatever candidate they produce.

`adaptive_search.py` includes stronger deterministic objective perturbations and
rejects duplicate current-dual incidence profiles among proposed columns.
`adaptive_search_v1.py` preserves the earlier version used for the 4.61 milestone.
A later argument guard rejects `--resume` with a different L or B; this guard does
not change the successful run's numerical algorithm.

Use `--resume` only at the saved L and B. For a different side, `--seed` creates
scaled and wall-anchored copies of positive sites:

```bash
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  python3 adaptive_search.py 4.615 --seed repaired3-4.613 --name higher
```

The command is a new search, NOT a theorem at 4.615. The retained
`frontier-4p615` checkpoint and logs contain an unsuccessful higher-target trial.
It did not produce an exact certificate. Earlier geometry from that trial did
help seed the successful 4.613 calculation.

## Earlier 4.61 repair milestone

The original completed 4.61 iterate and seed remain as `repaired-4.61` and
`repair-seed`. Its successful positive-only repair can be reproduced with:

```bash
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  python3 monotone_repair.py repair-seed repair-again
```

The main method alternates geometric separation (new LP rows) and spatial
pricing by LP dual multipliers (new orbit columns). All saved finite rows remain
in a pool, and omitted violated rows must be restored before accepting an LP
iterate. Spatial pricing is a heuristic scan, not a proof that no better point
exists. Positive-only repair spends mass slack without removing prior coverage;
its success is still gated by full separation and exact rational replay.

The optional `central_candidate.py` was an unsuccessful interior-point selection
experiment. It uses a SciPy 1.17 internal HiGHS binding, is version-specific, and
is not needed to reproduce either proved result.

## Test any changed candidate

From the package root, translate and replay it with the same integer kernel:

```bash
g++ -O3 -std=c++17 exact_sweep.cpp -o /tmp/square-exact-tree
python3 make_exact_input.py path/to/candidate.json /tmp/candidate.txt
/tmp/square-exact-tree /tmp/candidate.txt
```

Only an `EXACT_CERTIFICATE_VALID` exit with code zero validates the input's base
side. Do not reuse this package's recorded minimum, SHA-256 or sharpened endpoint
for changed data. Recompute the dilation formula from that candidate's L, B and
m; the strict decimal must lie strictly below its exact squared endpoint.

The `mins` array in a completed numerical checkpoint records the scan BEFORE
its final uniform weight normalization. It is not the exact minimum of the
exported certificate. Likewise, the `middle-full-seed` checkpoint intentionally
promotes the direction count before running a new full scan. Neither stored
array is a proof claim; the exact minima are only those in the replay ledger.

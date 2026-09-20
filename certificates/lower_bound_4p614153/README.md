# Exact parent-aware lower bound `s(17) > 18452/3999`

This package supplies the computational base certificate for the repository's
current theorem:

```text
s(17) > 18452/3999 = 4.61415353838459614903...
```

It builds on Guzhou0806's R012 parent-angle/legal-center reduction and the
weighted support lineage described in [`ATTRIBUTION.md`](ATTRIBUTION.md).

## Exact data

The certificate is stored as the authoritative raw JSON:

```text
certificate.json
```

The exact original JSON bytes have SHA-256

```text
5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3
```

The verifier checks this hash before parsing the default certificate.

Verified parameters:

```text
outer side             L = 4613/1000
parent side            A = 3999/4000
unit-square target     L/A = 18452/3999
atoms                   3280
positive D4 orbits       417
parent-angle intervals  4391
total mass              16.999991644
minimum core mass       1.000000030
counting surplus        0.000008866
center slabs            27918671
```

## Replay

Requirements: Python 3.10+, a C++17 compiler with OpenMP, and Boost headers.
No optimizer or network access is used.

```bash
python3 verify.py --output /tmp/n17-parent-aware --upstream --direct
python3 test_verify.py
python3 check_diagnostics.py
```

`--upstream` reconstructs and replays all 2,925 parent-angle obligations from
the pinned Guzhou R012 data in `upstream/`. `--direct` repeats both current and
upstream cases with the second accumulator and requires interval-by-interval
agreement.

## Files

- `PROOF.md` — mathematical proof and finite reduction.
- `certificate.json` — authoritative exact current certificate data.
- `verify.py`, `parent_sweep.cpp` — exact replay kernel.
- `test_verify.py` — boundary and deliberate-rejection controls.
- `result.json` — machine-readable theorem ledger.
- `ATTRIBUTION.md` — direct source identity and licensing notes.
- `RESEARCH.md` — staged improvements, fixed-measure obstruction, and failed trials.
- `diagnostics/` — exact parent counterexample for the frozen R012 measure.
- `upstream/` — the small pinned R012 data/kernel subset needed for source replay.

The two C++ accumulation modes share the same geometric partition. Their
agreement is not claimed as two independently designed geometric proofs.

## Verified analytic sharpening

The replay also checks all 4,391 recentering inequalities in `sharpening.py`.
Together with the translation replay, they prove
`s(17) > 46129999999859/9997499999900 = 4.614153538416645696808...`.
The exact scalar results are recorded in `result.json` under
`analytic_sharpening` and in the replay output `sharpening.result.json`.

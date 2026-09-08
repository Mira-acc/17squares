# Exact 17-square lower bound: s(17) > 4.613028635886

This package proves

\[
\boxed{s(17)>4.613028635886},
\qquad
s(17)\ge\frac{(4613/1000)\sqrt{1+h^2}}{(19997/20000)(1+h)},
\quad h=\frac{207107}{1440000000}.
\]

The radical endpoint is approximately
`4.61302863588611076617205655840261924140098182197751`.
The inequality at that endpoint is **weak**; the displayed twelve-decimal bound
is **strict**, checked by rational squaring.

The base certificate has **1620 rational atoms** and total mass
**16.99798498 < 17**. Every contained closed core of side 0.99985 at each of 2881
prescribed rational directions has mass at least **1.000002103**. An exact
angular-containment lemma puts such a closed core strictly inside every possible
unit square. Seventeen disjoint unit-square interiors would need at least 17
units of mass, a contradiction.

## Verify from source

Requirements: Python 3.10 or newer (standard library only), a C++17 compiler,
and Boost headers. No optimizer or network connection is required.

```bash
python3 verify.py
```

This compiles both accumulation backends, runs 13 geometric controls on each,
checks the exact restricted-dictionary diagnostic and its eight controls,
replays the full new certificate, checks the new-site deletion experiment, and
checks result metadata, certificate bytes and the strict decimal. The backends'
complete per-direction outputs must agree. To replay Levy's unchanged 4.59 data
as an additional source control:

```bash
python3 verify.py --source
```

Expected exact summary:

```text
EXACT_CERTIFICATE_VALID atoms 1620 directions 2881 total_mass 16997984980/1000000000 minimum 1000002103/1000000000 slabs 9116871
```

Certificate SHA-256:
`749f13335980a66a27a2304f212b5d8796390c81b962149647a4d9ff43a228ec`.

## What changed

The preceding delivered certificate proved `s(17)>4.607028598640`. This
continuation first certified 4.61, then **4.613**, without changing the core side,
the direction net or the exact geometric kernel. The gain is in the spatial
support and its weights, not in the angular allowance or displayed precision.

New numerical tools alternate two operations: find under-covered core placements
(new LP rows), and use the LP's dual multipliers to price previously unused point
orbits (new LP columns). A positive-only repair produced the 4.61 milestone.
Further support generation, including reuse of geometry from an unsuccessful
4.615 trial, produced the final 4.613 certificate.

Two exact diagnostics distinguish useful new geometry from decorative additions:

1. At L=4.61, the old 356-orbit support dictionary needs mass at least
   **17.009583872717** to cover just 106 specified cores. Reweighting that
   dictionary alone cannot pass the existing core test there.
2. Removing the 19 orbits priced during the final 4.613 stage makes this
   certificate fail already at direction zero: its minimum core mass becomes
   **0.939043209**. They contribute mass **0.315664656** in the accepted measure.

These are carefully scoped statements about the specified dictionary and
certificate, not universal limitations on other measures or proof methods.

## Contents

- `best-certificate.json`, `result.json`: immutable new data and exact result ledger.
- `PROOF.md`: continuum-to-finite proof, exact boundary treatment, and final parameters.
- `RESEARCH.md`: what the dual information supplied and the full research outcome.
- `exact_sweep.cpp`, `make_exact_input.py`, `test_checker.py`, `verify.py`: unchanged
  geometric kernel, rational input compiler, controls, and clean build/replay entry point.
- `diagnostic/`: the exact old-dictionary obstruction and new-orbit deletion test.
- `orbit-provenance.json`: all positive orbit representatives and exact weights.
- `audit/`: exact logs; `.replay/` receives a fresh local replay.
- `history/`: the separately accepted 4.61 certificate, ledger, logs and detailed report.
- `search/`: optional numerical discovery code, checkpoints and reproduction notes.
- `source/`, `ATTRIBUTION.md`: unchanged Levy source data and attribution.
- `INTEGRATION.md`: additive patch instructions that preserve earlier certificates.

## Trust boundary

The geometry uses arbitrary-precision integers. Weight accumulators have explicit
fixed-width safety bounds. The two backends share the geometric partition: their
agreement independently checks accumulation, **not two independently authored
geometric proofs**. Neither the optimizer nor its floating sweeps are trusted.
The certificate deliberately retains the original `candidate only` free-text
field; acceptance is stored separately in `result.json` and exact logs, leaving
the certificate bytes unchanged after verification.

The weighted full three-dimensional continuous-orientation pose-space verifier
suggested earlier is **not** implemented here. The work does not prove optimality,
a better packing construction, external peer-review acceptance, or permanent
priority over unknown work. The higher-target checkpoints in `search/` are
research data, never certificates of a bound above this headline.

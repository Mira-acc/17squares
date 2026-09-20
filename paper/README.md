# Technical paper

The paper proves the current exact computer-assisted bound

```text
s(17) > 46129999999859/9997499999900 = 4.614153538416645696808...
```

The exposition follows the proof: disjoint-core counting, parent-angle geometry,
the exhaustive finite translation check, the computational base bound, and the
analytic recentering improvement. A separate section proves the 29-core
intersection-trigger separation. Reproduction details, the dated history of
improvements, and supplementary results are in appendices.

## Build

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf 17squares-lower-bound.pdf
```

The committed PDF is `17squares-lower-bound.pdf`. CI rebuilds the PDF from
`main.tex` and refuses unresolved references or layout warnings.

## Current proof dependency

The computational base theorem is supplied by:

```text
../certificates/lower_bound_4p614153/
```

Replay it with:

```bash
python3 certificates/lower_bound_4p614153/verify.py \
  --output /tmp/n17-parent-aware --upstream --direct
python3 certificates/lower_bound_4p614153/test_verify.py
```

The previous `lower_bound_4p613`, `lower_bound_4p607`, and historical
`lower_bound_4p468292` packages remain
in the repository as reproducible milestones. See `../CONTRIBUTORS.md` for the
research lineage and attribution links.


## Analytic sharpening

The paper's headline bound is slightly stronger than the base certificate. It
uses the already-certified core shapes and center domains together with the
recentered-core transfer theorem. For

```text
epsilon = 1/100000000000
delta   = 141/10000000000000
```

the finite interval margins imply that the same charged cores cover parents of
side `3999/4000 - epsilon` in a container of side `4613/1000 - delta`.
This gives the strict rational corollary

```text
s(17) > 46129999999859/9997499999900
      = 4.614153538416645696808...
```

No new translation sweep is required for this sharpening. The replay command
also runs `sharpening.py` and writes `sharpening.result.json`, checking all
4,391 scalar inequalities, their minimum slack, and the fixed-library cap.

The paper also proves an extension using intersection-trigger charges, including
their budget and coverage geometry. These charges are not used in the numerical
lower bound. Folding parent orientations requires the total charge to be
`D4` invariant; otherwise all orientations must be covered explicitly.

The finite 29-pose example and independent pointwise-load checker are in
[`intersection_trigger_29`](../certificates/intersection_trigger_29/). They
verify a strict separation from positive spatial mass on those cores.

Dates in the lineage table are documented in [HISTORY-DATES.md](HISTORY-DATES.md).

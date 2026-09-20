# Research lineage and contributors

This repository's current lower bound is

\[
s(17) > \frac{46129999999859}{9997499999900}=4.614153538416645696808\ldots.
\]

The theorem is published here under Mira's authorship, but the method and the
sequence of improvements were developed across a larger community. This page
separates **direct dependencies of the current certificate** from **historical
or parallel results that shaped the program**. A link here is attribution, not
an assertion of coauthorship or endorsement.

## Direct lineage of the current certificate

| Contributor | Public source | Contribution used here |
|---|---|---|
| **Mira** | [Mira-acc/17squares](https://github.com/Mira-acc/17squares) | Exact sixteen-point pose-space certificates; later weighted support, finer angular control, dual-guided support search, and the spatial measure from which the parent-aware continuation descends. Public milestones include `4.450837`, `4.468292`, `4.607028598640...`, and `4.613028635886...`. |
| **Joshua Levy** | [jlevy/squares](https://github.com/jlevy/squares) · [explainer](https://jlevy.github.io/squares/) | Reusable weighted/fractional certificate framework, exact event-cell sweeps, interval cross-checking, dilation-limit arguments, and prior parent-center restrictions. Levy's `4.59` n=17 certificate was an explicit source and replay baseline for our weighted continuation. |
| **Guzhou0806 / N17 project** | [R012 pinned source](https://github.com/Guzhou0806/n17-square-packing/tree/931a0dfd64302e277057006e99388fe5c00b7f53/certificates/R012) | Completed the n=17 parent-angle catalogue and legal-parent-center reduction, proving `s(17) >= 461300/99999 = 4.613046130461...`. R012 showed that checking every auxiliary core position wastes constraints that no real parent square can realize. The current verifier directly incorporates this parent-aware idea and replays the pinned R012 data. |

The final step in this repository keeps the parent-aware proof contract, adaptively
refines the angle catalogue, reweights the measure, and mixes inherited support
with wall-adjusted sites. The resulting exact certificate proves
`18452/3999 = 4.614153538384596...`. Exact recentering inequalities then give
the headline corollary `46129999999859/9997499999900`.

### Dependency graph

The direct mathematical dependency is approximately:

```text
Green / classical unavoidable points
              |
              v
 exact pose-space point certificates
 (Brandwijk, Mira, Fort)
              |
              v
 Burns: fractionalize the witness budget
              |
              v
 Massaccesi: LP-designed weighted measure
              |
              v
 Levy: reusable exact event sweeps / dilation / parent-center machinery
              |
              v
 Mira: support refinement + finer angular control + dual-guided search
              |
              v
 Guzhou R012: legal-parent center domains + interval-dependent cores
              |
              v
 current theorem: adaptive parent intervals + reweighting + wall-adjusted support
```

This graph is deliberately about **method dependence**, not priority. Several
parallel results influenced the research without being ancestors of the final
certificate bytes.

## Contemporary n=17 lower-bound sequence

These results were important benchmarks or methodological steps even when their
certificate bytes are not direct dependencies of the current proof.

| Contributor | Bound | Method / significance | Source |
|---|---:|---|---|
| **Kim Brandwijk** | `89/20 = 4.45` | Exact sixteen-point unavoidable-set certificate in the July 2026 public sequence. | [Zenodo capsule, DOI 10.5281/zenodo.21422426](https://doi.org/10.5281/zenodo.21422426) · [Levy audit](https://github.com/jlevy/squares/blob/main/packing/frontier/n-017.md) |
| **Mira** | `4.450837`; later `4.468292` | Pure-integer subdivision of full square pose space. The later version adds strict triangle-piercing leaves. | [this repository](https://github.com/Mira-acc/17squares) · [Levy audit](https://github.com/jlevy/squares/blob/main/packing/frontier/n-017.md) |
| **Stanislav Fort** | `4.456575` | Independently optimized the exact sixteen-point subdivision architecture. | [stanislavfort/17squares](https://github.com/stanislavfort/17squares) |
| **Sam Burns** | `4.4811` | Introduced the 2026 pure-atomic weighted-certificate route for n=17: total measure below 17, every possible square forced to capture enough mass. | [proof post and verifier](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/) |
| **Gustavo Massaccesi** | `22529/5000 = 4.5058` | LP-derived 168-atom weighted certificate on Burns's architecture; exactly replayed in Levy's audit. | [result post](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html) · [LP method](https://gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html) · [Levy audit](https://github.com/jlevy/squares/blob/main/packing/frontier/n-017.md) |
| **anabologyco-maker** | `9141/2000 = 4.5705` | Weighted measure with an exact 148,937-cell orientation partition and a Lean layer for finite checks. | [square17-lower-bound](https://github.com/anabologyco-maker/square17-lower-bound) |
| **Joshua Levy** | `459/100 = 4.59` | First-party fractional certificate with reusable generation, exact event-cell sweep, and method-distinct interval coverage checks. | [jlevy/squares](https://github.com/jlevy/squares) |
| **Guzhou0806** | `461300/99999 = 4.613046130461...` | Parent-angle/legal-center catalogue R012, starting from a rounded/reverified version of our 4.613 measure. | [R012](https://github.com/Guzhou0806/n17-square-packing/tree/931a0dfd64302e277057006e99388fe5c00b7f53/certificates/R012) |
| **Mira, current certificate** | `18452/3999 = 4.614153538384...` | Adaptive parent-aware intervals, reweighting, and wall-adjusted support; full exact replay. | [`certificates/lower_bound_4p614153`](certificates/lower_bound_4p614153) |

## Earlier mathematical lineage

- **Trevor Green.** Friedman's survey records Green's classical n=17 lower bound
  \((40\sqrt2+19)/17\approx4.445208382\), illustrated by an unavoidable-point
  configuration. See Erich Friedman's [Dynamic Survey DS7](https://erich-friedman.github.io/papers/squares/squares.html).
- **Erich Friedman.** The DS7 survey organized the historical problem, recorded
  Green's bound and Bidwell's packing, and developed unavoidable/almost-unavoidable
  point arguments used throughout the field. See the same [survey](https://erich-friedman.github.io/papers/squares/squares.html).
- **Walter Stromquist.** His work on unavoidable-point geometry, including
  *Packing 10 or 11 unit squares in a square*, is part of the classical proof
  lineage behind later piercing arguments. [DOI 10.37236/1701](https://doi.org/10.37236/1701).
- **Hiroshi Nagamochi.** Gave a general rectangle-packing lower-bound theorem in
  2005 that supplied important general-purpose bounds before the 2026 n=17
  certificate sequence. [Packing Unit Squares in a Rectangle](https://doi.org/10.37236/1934).
- **David R. MacIver.** A 2026 manuscript developed a deformation of Green's
  scaffold and conditional defect charging, reporting a bound around `4.450208`.
  It is weaker than the later exact certificates but represents an independent
  structural direction. [paper source](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/papers/s17-lower-bound/paper.pdf).

## Upper-bound lineage

- **John Bidwell** found the best known n=17 packing in 1998, with side
  `4.6755300936045509516...`, building on earlier packing work by **Pertti
  Hämäläinen**. The high-precision value and algebraic data are recorded in
  Doug Ellsworth's [Squares in Squares catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html).

## Verification and AI assistance

Many 2026 projects, including this repository, disclose substantial AI assistance.
That fact neither validates nor invalidates a certificate. We distinguish discovery
from verification: theorem claims are based on explicit rational data, mathematical
reductions, and replayable exact checkers. Independent human review and complete
proof-assistant formalization remain valuable open assurance steps.

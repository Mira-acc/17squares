# Provenance and claim discipline

## Current theorem

The strongest retained theorem is

```text
s(17) > 46129999999859/9997499999900 = 4.614153538416645696808...
```

in `certificates/lower_bound_4p614153/`.

Its direct lineage has three main components:

1. **Mira / 17squares:** the inherited spatial weighted support and preceding
   exact weighted certificates;
2. **Joshua Levy / squares:** weighted/fractional covering, exact event-sweep
   verification, strict-core transport, dilation, and prior parent-center
   machinery;
3. **Guzhou0806 / N17 R012:** the concrete n=17 parent-angle catalogue and
   legal-parent-center reduction, pinned at commit
   `931a0dfd64302e277057006e99388fe5c00b7f53`.

The present continuation adds adaptive parent intervals, reweighting, and a
mixture of inherited and wall-adjusted support. See the package's
`ATTRIBUTION.md` and root [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

## Trust classes

### Class A — exact checked theorem

The following packages contain finite computer-assisted proofs:

- `certificates/lower_bound_4p614153/` — current parent-aware weighted theorem;
- `certificates/lower_bound_4p607/` — previous weighted theorem and dilation endpoint;
- `certificates/lower_bound_4p613/` — preceding weighted theorem;
- `certificates/lower_bound_4p468292/` — historical exact triangle-witness tree.

For the current theorem, the trusted mathematical core is the parent-aware
counting reduction, exact interval/core-containment inequalities, exact
translation sweep, rational certificate data, recentering transfer inequalities,
and checker. Discovery and LP
optimization are not trusted inputs.

The two C++ accumulation modes in the current package share the same geometric
partition, so their agreement audits accumulation rather than providing two
independently designed geometric proofs. The pinned R012 Python sweep supplies
a separately implemented replay of the upstream parent-aware certificate.

### Class B — reproducible numerical evidence

Packing optimization, primal-dual search, MILP outputs, and local polishing are
useful research evidence but do not by themselves establish a theorem.

### Class C — exploratory output

Failed targets, solver objectives, candidate supports, and incomplete searches
remain leads only. A numerical failure is not promoted to a method ceiling unless
an exact obstruction is separately proved.

## Historical source discipline

The repository now has a dedicated contributor/source map. It distinguishes:

- direct dependencies of the current proof;
- stronger or weaker public certificates that influenced the research program;
- classical mathematical lineage such as Green, Friedman, Stromquist, and
  Nagamochi;
- upper-bound construction work such as Bidwell and Hämäläinen.

Attribution does not imply endorsement, coauthorship, or independent review.
Where a source is only reported or not fully replayed, that limitation is stated.

## AI assistance

The August and September 2026 investigations used substantial AI assistance
under human direction. Several independent 2026 projects in the source lineage
make similar disclosures. The theorem is not justified by model authority: it
rests on explicit rational data and executable exact verification.

## External review

The current theorem should still receive:

1. independent mathematical review of the parent-angle and center-domain reduction;
2. independent implementation or code review of the exact sweep;
3. reproduction on a separate toolchain;
4. ideally, end-to-end formalization in a proof assistant.

No result in this repository is described as peer reviewed unless an external
source explicitly provides that status.

# Certificate integration review, 7 September 2026

The supplied `17squares-record-4p613.zip` was reviewed before publication in
Mira-acc/17squares. No issue blocking the stated lower bound was found. This is
a repository integration review with AI assistance, not external peer review
or an independently authored second geometric verification.

## Checks completed

- All 92 entries of the original package manifest matched before integration.
- The C++ geometric kernel and rational input compiler are byte-identical to
  the retained 4.607 versions. The proof's strict core inclusion, continuum
  orientation coverage, event-cell boundaries and dilation argument were
  checked against the implementation and the new certificate parameters.
- `python3 verify.py --source` rebuilt and passed both accumulation engines,
  all 26 geometric controls, all eight diagnostic controls, both deletion
  experiments and the unchanged Levy source replay.
- Both new-certificate logs match each other and the supplied per-direction
  logs byte-for-byte: 1,620 atoms, 2,881 directions, mass 16.99798498,
  minimum core mass 1.000002103, and 9,116,871 centre slabs.
- The support has 1,620 distinct atoms and 206 positive orbit entries. Exact
  orbit expansion reproduces the accepted measure and the specified deletion.
- The restricted diagnostic's 356 support orbits were compared with the exact
  dictionary builder at 4.61. Every one of its 106 directions belongs to the
  stated 721-direction subset of the 2,881-direction net.
- Rational endpoint comparisons reproduce `s(17) > 4.613028635886` and the
  weak radical bound recorded in `result.json`.

The updated nine-page public paper builds without LaTeX warnings and was
visually reviewed. Local documentation links resolve, and `verify_all.sh`
passes shell syntax checks. The unchanged historical packages were not
regenerated as part of this review.

## Scope retained in the paper

The total measure is below 17, while every unit-square interior has mass at
least one. This proves exclusion by summing masses of disjoint interiors.
The radical endpoint remains a weak lower bound; the strict rational decimal
is smaller than that endpoint. Neither endpoint is claimed to be optimal.

The old-dictionary dual certificate constrains only its specified support and
core test. The deletion experiment concerns a fixed measure without
reoptimization. Neither is an upper bound on s(17). The unsuccessful 4.615
search checkpoints are discovery records, not certificates of a higher bound.

The two engines share one geometric partition; their agreement audits weight
accumulation. The optimizer is outside the proof's trusted core. The older
4.607 and 4.468292 certificate packages are unchanged by this integration.

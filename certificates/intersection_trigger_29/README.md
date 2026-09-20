# Verified 29-pose intersection-trigger example

This package proves a strict separation between a budget-one trigger charge
and ordinary nonnegative spatial measures on a finite family of square cores.
It does not improve the numerical lower bound for packing 17 squares.

The supplied `intersection-atom.json` and `clique-29-poses-with-weights.csv`
contain 29 rational unit-square poses, positive rational weights, 406 distinct
pair witnesses, and 29 triggers of size 28. They are reproduced byte for byte.
The JSON identifies their source as the earlier `bidwell-optimality-progress`
clique and fractional-obstruction artifacts. The source hashes are provenance
metadata; this checker verifies the supplied subset directly and does not rely
on a claimed full-family load theorem. The two pinned source files are also
retained in `sources/`, from research commit
`0d73293` (`research/parent-aware-4p614153`); their byte hashes match the
provenance recorded in the atom JSON.

Run with Python 3.10+ and its standard library:

```bash
python3 certificates/intersection_trigger_29/verify.py
python3 certificates/intersection_trigger_29/test_verify.py
```

## Exact findings

- Every pair of triggers shares its designated witness, proving budget one on
  arbitrary pairwise-disjoint cores.
- Every pose has a unit rotation and lies inside the centered side-4.67 box.
- The minimum required witness margin inside a source unit square is
  `314856211897415969021/287142759881684900000000 > 1/1000`.
  Thus every trigger lies strictly inside its corresponding concentric closed
  side-`499/500` core.
- The sum of the supplied weights is `81407286808/79999999999`.
- Their maximum pointwise load on the open unit squares is exactly
  `59431493389/79999999999`, checked across 1,475 arrangement slabs.

Consequently any positive measure that assigns at least one to each of these
29 closed cores has total mass at least

```text
81407286808/59431493389 = 1.3697668048682659... > 1.
```

To see this, let the weights be `lambda_i`, the closed cores be `K_i`, their
sum be `S`, and the maximum unit-square load be `m`. Strict containment gives
`sum lambda_i 1_{K_i} <= m` everywhere, including boundaries. Integrating
against such a measure gives `S <= m * total_mass`. The trigger charge pays
each core one while its disjoint-family budget is only one.

## Completeness of the load check

The checker forms the four rational edges of each square. All vertex abscissae
and all segment-intersection abscissae partition the plane into vertical open
slabs. Collinear overlaps introduce no events beyond their endpoints. Edge
order is constant inside each slab, so at its rational midpoint the vertical
interval endpoints enumerate every open cell's covering set. Coincident
events are grouped, and a maximum witness is independently recounted by direct
square containment. Outside the extreme vertices the load is zero. Every
square counted at a boundary point is open and also contains a neighbourhood
of that point; hence no boundary has a larger load than these open cells.

Seven tests cover coincident squares, touching open boundaries, oblique
intersections, disjoint squares, vertex margins, and the supplied example.

## Scope

The checker also expands the pinned source's 77 base poses into 616 symmetry
images and matches the selected CSV rows exactly. It verifies every recorded
activation and margin for 71 source unit-square poses, and confirms that 68
of their triggers remain in closed side-499/500 cores. Their weight sums are
respectively `99656162199/79999999999` and `96836866527/79999999999`.

A separate exact arrangement sweep of these 71 poses covers 8,405 slabs and
finds maximum pointwise load `73959042636/79999999999 < 1`. Thus the original
68-core separation of at least `96836866527/79999999999 > 1` is verified
without relying on a load theorem for the entire 616-pose source. The normalized
29-pose separation above is stronger. The full 616-pose load is not checked,
and optional convex-hull compression is unused.

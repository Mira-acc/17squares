# Verification review (2026-09-20)

The supplied complete JSON matches SHA-256
`5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3`.
It replaces an incomplete split transport without changing the mathematical data.
The default replay checks this hash before parsing the raw JSON.

The complete current certificate passed both C++ accumulation modes: 4,391
intervals, 27,918,671 center slabs, and minimum mass
`100000003/100000000`. The counting surplus is `4433/500000000`.
Every recorded exact base parameter matches the fresh replay. Both modes also
passed all 2,925 intervals of pinned R012, with matching coverage hashes.
The two modes share their geometric partition and are not independent geometry
implementations.

The new exact-rational `sharpening.py` check reproduces all 4,391 positive
recentring residuals, their recorded minimum, and the fixed-library axis cap.
Combined with the base replay and the paper's transfer proof, this establishes
the strict headline bound `46129999999859/9997499999900`.

All 22 package tests passed, including synthetic cross-checks against the
retained Python geometry and rejection of a transfer with insufficient margin.
The fixed-measure parent counterexample also passed. Earlier reported full
Python and selected-entry runs are distinguished in `result.json` from the
checks performed in this review.

The manuscript now states the nonempty-domain assumption for its recentering
equivalence and handles isolated vertices in its general trigger construction.
Its numerical trigger-separation example has been removed because the separate
pose, point, and fractional-weight witnesses are not supplied here. The general
budget theorem remains, but is not used in the numerical packing bound.
Intermediate search targets without retained certificates are labeled as
historical reports. The rebuilt paper passed the warning checks and visual
layout review.

Reproduce with:

```bash
python3 certificates/lower_bound_4p614153/verify.py \
  --output /tmp/n17-review --upstream --direct
python3 certificates/lower_bound_4p614153/test_verify.py
python3 certificates/lower_bound_4p614153/check_diagnostics.py
```

This is a source and exact-computation review, not external peer review or
proof-assistant formalization.

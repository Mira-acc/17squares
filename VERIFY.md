# Verification guide

## One-command repository replay

```bash
bash ./verify_all.sh
```

The script retains the historical tree checks, the previous weighted replay,
and the current parent-aware theorem.

## Current theorem

The current package proves

```text
s(17) > 46129999999859/9997499999900 = 4.614153538416645696808...
```

Replay it with:

```bash
python3 certificates/lower_bound_4p614153/verify.py \
  --output /tmp/n17-parent-aware --upstream --direct
python3 certificates/lower_bound_4p614153/test_verify.py
```

Requirements:

- Python 3.10+
- `g++` or another C++17 compiler with OpenMP
- Boost headers

No optimizer, NumPy/SciPy, network access, or model is needed.

### What is checked

The verifier:

1. loads the authoritative certificate JSON and checks the SHA-256 of
   the exact JSON bytes;
2. validates `L = 4613/1000`, `A = 3999/4000`, the orbit encoding, mass, angle
   partition, and strict core containment over every continuous parent interval;
3. computes each interval's complete legal parent-center envelope;
4. compiles the exact C++ translation kernel;
5. checks all 4,391 interval/envelope obligations and 27,918,671 center slabs;
6. optionally repeats them with a direct-prefix accumulator and requires all
   interval minima to agree;
7. with `--upstream`, reconstructs and replays the pinned Guzhou R012 measure
   and all 2,925 R012 parent-angle obligations;
8. verifies that `17 * minimum_charge > total_mass`;
9. checks all recentering inequalities with exact fractions, producing
   `sharpening.result.json` for the stronger headline bound.

The final exact quantities are

```text
atoms                3280
positive D4 orbits    417
parent intervals     4391
total mass            16.999991644
minimum core mass     1.000000030
counting surplus      0.000008866
```

The two C++ accumulation backends share the same geometric partition; their
agreement is not advertised as two independent geometric proofs.

## Previous weighted theorem

The previous package remains replayable with:

```bash
python3 certificates/lower_bound_4p607/verify.py --direct \
  --output /tmp/n17-4p607
```

It proves `s(17) > 4.607028598640` via a fixed core family and exact dilation.

## Earlier public packages

The preceding weighted theorem and its source checks remain available:

```bash
python3 certificates/lower_bound_4p613/verify.py --source
```

The historical sixteen-point triangle-witness certificate has a deterministic
XZ archive. Check its archived bytes and exact witnesses with:

```bash
bash certificates/lower_bound_4p468292/verify_archived.sh
```

`verify_all.sh` retains the full historical regeneration command in addition to
both weighted packages and the current parent-aware replay. Optimizer outputs
are not part of the proof.

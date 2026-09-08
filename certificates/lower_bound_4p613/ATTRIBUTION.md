# Attribution and provenance

The initial 1184-atom measure and its certificate data are by **Joshua Levy,
the squares project (https://github.com/jlevy/squares)**. The repository grants
CC BY 4.0 for its data and documentation:
https://creativecommons.org/licenses/by/4.0/.

Original path: `packing/cases/n17_fractional_certificate/certificate.json`.
Git blob SHA-1: `f454e44dee1f2318af45e02efdfff5fcd7dbfbe1`.
SHA-256: `461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652`.

Changes made here include spatial scaling, angular-net refinement, numerical
reoptimization of the per-orbit weights, upward rational rounding, deletion
of zero-weight atoms, and exploratory additions of support points. The exact
source file is retained unchanged. New derived certificate data are also made
available under CC BY 4.0 with this attribution. No endorsement by Joshua Levy
is implied.

The sixteen historical unavoidable points used in the merger experiment come
from **Mira, Mira-Cult/17squares**, `paper/main.tex`, Git blob SHA-1
`0506d80a4d380420ee786daf693df77bb6443054`, as retrieved on 7 September 2026.
They belong to the archived 4.450837 proof, not the separate later 4.468292
result recorded in Levy's survey. Their coordinates were symmetrized and
scaled before use as optional columns in an exploratory covering LP.

The weighted covering principle is not claimed as new. Sam Burns' 6 August
2026 post already presents weighted certificates for this problem, and
Gustavo Massaccesi's subsequent note develops the LP viewpoint. Levy's
implementation documents row generation, rationalization and exact replay.
Levy's T-022 n=11 note supplies the sharp uniform-dilation corollary used here.

The C++ exact checker, direct-prefix audit engine, input compiler, control
suite and discovery scripts in this package were newly written during this
calculation. They were not copied from Levy's verification or optimization
source. The exact geometry proof and computation remain open to independent
review. Same-session agreement of two accumulation engines is not equivalent
to an independently authored second geometric verification.

References:
- https://github.com/jlevy/squares/tree/main/packing/cases/n17_fractional_certificate
- https://github.com/jlevy/squares/blob/main/packing/frontier/n-017.md
- https://github.com/jlevy/squares/blob/main/packing/src/sqpack/fractional/generate.py
- https://github.com/jlevy/squares/blob/main/packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md
- https://github.com/Mira-Cult/17squares
- https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/
- https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html

## This continuation

This package extends Mira's exact 4.607 certificate first to 4.61 and then to 4.613. The exact C++ kernel
is **unchanged**, with SHA-256
`1bb626a560e3c67620b2aa7851bc467db72b3530f6cae394c1d9d9f034910f4b`.
New work consists of dual-guided spatial orbit generation, an exact finite dual
obstruction for the previous support dictionary, positive-only mass repair, and
a new exact rational certificate. Column generation and covering-LP duality are
standard optimization ideas; the claim is their useful implementation and the
new checked geometric certificate here, not invention of those ideas.

The general proof, original source data, and control tests are retained from the
previous package. Newly derived certificate data remain attributed under CC BY
4.0. AI assistance does not constitute independent mathematical peer review.

The final discovery path reused geometry from an unverified 4.615 search at
4.613. The certificate free-text parent identifies its 4.607 ancestor; the
intermediate 4.61 theorem and numerical higher-target path are documented in
RESEARCH.md. No certificate or theorem at 4.615 is claimed.

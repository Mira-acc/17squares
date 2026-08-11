# Packing 17 unit squares in a square

Let `s(17)` be the least side length of a square containing 17 pairwise
interior-disjoint unit squares, with arbitrary orientations. This repository
contains an exact computer-assisted proof that

\[
\boxed{s(17)>4.450837}.
\]

The previous lower bound recorded in Friedman's survey was
`(40√2 + 19)/17 ≈ 4.4452083821`.

## Read the proof

- [Paper (PDF)](paper/17squares-lower-bound.pdf)
- [LaTeX source](paper/main.tex)
- [Exact certificate package](certificates/lower_bound_4p450837)

The proof supplies sixteen rational points in the square of side
`4450837/1000000`. An exact subdivision certificate proves that every contained
unit square, at every orientation, contains one of those points strictly in its
interior. Seventeen interior-disjoint squares would require seventeen distinct
points, so no such packing exists at that side length. Compactness makes the
resulting lower bound strict.

## Verify the certificate

Requirements:

- Python 3
- a C++17 compiler
- Boost headers

Run:

```bash
bash ./verify_all.sh
```

The script regenerates the certificate, checks that its SHA-256 hash is

```text
49ee8134ccf636224432d235fc3c1db2f8d6a567efe9e4c08b2e81639172cfeb
```

compares it byte-for-byte with the archived tree, and validates it with three
exact checkers. See [VERIFY.md](VERIFY.md) for the proof interface and trust
boundary.

## Repository contents

```text
paper/                                  paper source and rendered PDF
certificates/lower_bound_4p450837/      points, certificate, generator, checkers
verify_all.sh                           one-command exact reproduction
```

Search experiments and weaker historical certificates are intentionally omitted
from this publication repository.

## Status

The certificate has been reproduced with the included exact checkers. The result
has not undergone independent peer review.

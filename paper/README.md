# Technical paper

The paper proves the current exact computer-assisted bound
`s(17) > 4.607028598640`, explains the weak radical endpoint, and retains the
historical `4.468292` triangle-witness proof in an appendix.

## Build

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf 17squares-lower-bound.pdf
```

The committed PDF is `17squares-lower-bound.pdf`. Inspect the rendered pages
and require a clean log with no unresolved references or layout warnings.

## Proof dependencies

- `../certificates/lower_bound_4p607/`: current rational measure, exact sweep,
  controls, source attribution, result ledger and package manifest.
- `../certificates/lower_bound_4p468292/`: historical appendix's point set,
  deterministic subdivision certificate and three exact checkers.

From the repository root, run all retained checks with:

```bash
bash ./verify_all.sh
```

For the current theorem alone:

```bash
python3 certificates/lower_bound_4p607/verify.py --direct
```

The two weighted accumulation engines share a geometric kernel. The earlier
three-checker independence claim applies only to the historical tree package.

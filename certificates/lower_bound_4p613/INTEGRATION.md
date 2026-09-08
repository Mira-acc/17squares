# Public repository integration

This package was imported from `17squares-record-4p613.zip` on 7 September 2026.
All 92 entries in its supplied SHA-256 manifest were checked before integration.
The public repository retains the original certificate, kernel, diagnostics,
source data, discovery checkpoints and exact logs. These integration notes and
`REVIEW.md` document the repository review; the package manifest includes them.

The current public paper, PDF, README, verification guide, citation metadata and
weighted replay workflow now use `s(17) > 4.613028635886`. The radical endpoint
has a weak inequality. Earlier `4.607` and `4.468292` packages remain unchanged;
the triangle-witness proof remains in the paper's historical appendix.

From the repository root, replay this package with:

```bash
python3 certificates/lower_bound_4p613/verify.py --source
```

`bash ./verify_all.sh` also replays the preceding weighted package and fully
regenerates and checks the historical triangle-witness certificate. Optional
search checkpoints are discovery records, including unsuccessful higher targets;
they do not establish any stronger packing bound.

#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$ROOT/certificates/lower_bound_4p613/verify.py" --source
python3 "$ROOT/certificates/lower_bound_4p607/verify.py" --direct
bash "$ROOT/certificates/lower_bound_4p468292/verify_4p468292.sh"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/certificates/lower_bound_4p614153/verify.py" \
  --output "$TMP/parent-aware" --upstream --direct
python3 "$ROOT/certificates/lower_bound_4p614153/test_verify.py"
python3 "$ROOT/certificates/lower_bound_4p614153/check_diagnostics.py"

echo ALL_RETAINED_CHECKS_PASSED

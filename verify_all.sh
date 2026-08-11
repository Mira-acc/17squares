#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

DIR="$ROOT/certificates/lower_bound_4p450837"
CERT="$DIR/square17_lb_4p450837.cert"
GENERATED="$TMP/generated.cert"
EXPECTED_SHA=49ee8134ccf636224432d235fc3c1db2f8d6a567efe9e4c08b2e81639172cfeb

g++ -O3 -std=c++17 "$DIR/generate_certificate.cpp" -o "$TMP/generate"
g++ -O3 -std=c++17 "$DIR/verify_certificate.cpp" -o "$TMP/verify_fast"
g++ -O3 -std=c++17 "$DIR/verify_certificate_bigint.cpp" -o "$TMP/verify_bigint"

"$TMP/generate" "$GENERATED"
printf '%s  %s\n' "$EXPECTED_SHA" "$GENERATED" | sha256sum -c -
printf '%s  %s\n' "$EXPECTED_SHA" "$CERT" | sha256sum -c -
cmp "$GENERATED" "$CERT"

"$TMP/verify_fast" "$GENERATED"
"$TMP/verify_bigint" "$GENERATED"
python3 "$DIR/verify_certificate.py" "$GENERATED"

echo ALL_EXACT_CHECKS_PASSED

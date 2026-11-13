#!/usr/bin/env bash
# Run the release gates locally or in CI. Usage: qa/run_gates.sh [static|browser|matrix-core|matrix-full|all]
#   static       compliance, front-matter + character limits, claims, links (internal), standards lock, functions
#   browser      build dist, serve it, text overflow (6 widths), spacing (9 widths), symmetry/contrast/targets via
#                qa_matrix chromium core, then the verdict
#   matrix-full  qa_matrix on chromium, webkit and firefox, core + devices (nightly)
# Env: QA_CHROME (optional Chrome binary), QA_SHARDS (default 4), QA_OUT (default qa-out/<mode>)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"; cd "$REPO"
MODE="${1:-all}"; SHARDS="${QA_SHARDS:-4}"
ST="$REPO/site/.build"
static() {
  python3 qa/compliance/check_content.py
  python3 qa/compliance/tests/test_private_rules.py
  python3 qa/check_frontmatter.py ${QA_CHANGED:+--changed "$QA_CHANGED"}
  python3 qa/check_claims.py
  python3 qa/check_links.py --docs
  python3 qa/check_standards_lock.py
  node qa/functions/test_soldier.mjs
  node qa/functions/test_mailer.mjs
}
serve() {
  python3 qa/serve.py site/dist 8817 & SRV=$!; trap 'kill $SRV 2>/dev/null || true' EXIT
  for i in $(seq 1 50); do curl -sf -o /dev/null http://127.0.0.1:8817/index.html && break; sleep 0.2; done
}
shards() { # script args... ; runs SHARDS parallel shards: <script> <i> <n> plus extra args
  local pids=() rc=0
  for i in $(seq 0 $((SHARDS-1))); do "$@" "$i" "$SHARDS" > "$OUT/$(basename "$2" .py)_${3:-}$i.log" 2>&1 & pids+=($!); done
  for p in "${pids[@]}"; do wait "$p" || rc=1; done; return $rc
}
browser() {
  OUT="${QA_OUT:-$REPO/qa-out/browser}"; mkdir -p "$OUT"; export QA_OUT="$OUT" QA_BASE="http://127.0.0.1:8817/"
  bash site/build.sh dist
  serve
  local rc=0
  shards python3 "$ST/normalize_suite/qa_text_overflow.py" || true
  shards python3 "$ST/normalize_suite/qa_spacing.py" || true
  local pids=(); for i in $(seq 0 $((SHARDS-1))); do python3 "$ST/normalize_suite/qa_matrix.py" chromium core "$i" "$SHARDS" > "$OUT/matrix_chromium_core_$i.log" 2>&1 & pids+=($!); done
  for p in "${pids[@]}"; do wait "$p" || rc=1; done
  python3 qa/verdict.py "$OUT" --engines chromium --profiles core || rc=1
  python3 qa/check_links.py --dist site/dist || rc=1
  return $rc
}
matrix_full() {
  OUT="${QA_OUT:-$REPO/qa-out/nightly}"; mkdir -p "$OUT"; export QA_OUT="$OUT" QA_BASE="http://127.0.0.1:8817/"
  bash site/build.sh dist; serve; local rc=0
  for eng in chromium webkit firefox; do for ps in core devices; do
    local pids=(); for i in $(seq 0 $((SHARDS-1))); do python3 "$ST/normalize_suite/qa_matrix.py" "$eng" "$ps" "$i" "$SHARDS" > "$OUT/matrix_${eng}_${ps}_$i.log" 2>&1 & pids+=($!); done
    for p in "${pids[@]}"; do wait "$p" || rc=1; done
  done; done
  python3 qa/verdict.py "$OUT" --engines chromium,webkit,firefox --profiles core,devices || rc=1
  return $rc
}
case "$MODE" in
  static) static ;;
  browser) browser ;;
  matrix-full) matrix_full ;;
  all) static && browser ;;
  *) echo "usage: qa/run_gates.sh [static|browser|matrix-full|all]"; exit 2 ;;
esac

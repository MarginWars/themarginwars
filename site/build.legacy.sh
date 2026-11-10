#!/usr/bin/env bash
set -euo pipefail
cd /workspace/deliverables/brand
python3 copy_weekend/apply_copy_weekend.py
python3 ui_weekend/apply_ui.py
python3 route_brief/apply_rb.py
python3 copy_tighten/apply_tighten.py
python3 about_rethink_1108/apply_about.py
python3 feeds/apply_feeds.py
python3 normalize_suite/apply_normalize.py

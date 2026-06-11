#!/usr/bin/env python3
"""Validate chunked (split) Parquet output.

Asserts the output dir holds more than one sequence-numbered chunk file
(events.NNNNNNNN.snappy.parquet) and that their row counts sum to 100,000.
"""
import sys
from pathlib import Path

import pyarrow.parquet as pq

EXPECTED_ROWS = 100_000

out = Path(sys.argv[1] if len(sys.argv) > 1 else "/output")
files = sorted(out.glob("events.*.snappy.parquet"))
print(f"found {len(files)} chunk file(s): {[f.name for f in files]}")

ok = True
if len(files) < 2:
    print(f"FAIL: expected multiple chunk files, got {len(files)} "
          "(file-size rotation did not trigger)")
    ok = False

total = sum(pq.ParquetFile(f).metadata.num_rows for f in files)
print(f"total rows across chunks={total}")
if total != EXPECTED_ROWS:
    print(f"FAIL: expected {EXPECTED_ROWS} rows total, got {total}")
    ok = False

print("OK" if ok else "FAILED")
sys.exit(0 if ok else 1)

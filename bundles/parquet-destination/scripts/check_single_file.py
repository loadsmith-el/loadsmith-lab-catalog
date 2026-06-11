#!/usr/bin/env python3
"""Validate single-file Parquet output.

Asserts the output dir holds exactly one events.snappy.parquet (no sequence
number), with the full 100,000 rows and the 34-column canonical schema.
"""
import sys
from pathlib import Path

import pyarrow.parquet as pq

EXPECTED_ROWS = 100_000
EXPECTED_COLS = 34

out = Path(sys.argv[1] if len(sys.argv) > 1 else "/output")
files = sorted(out.glob("events*.parquet"))
print(f"found {len(files)} parquet file(s): {[f.name for f in files]}")

if files != [out / "events.snappy.parquet"]:
    print("FAIL: expected exactly one file named events.snappy.parquet")
    sys.exit(1)

meta = pq.ParquetFile(files[0]).metadata
print(f"rows={meta.num_rows} columns={meta.num_columns}")

ok = True
if meta.num_rows != EXPECTED_ROWS:
    print(f"FAIL: expected {EXPECTED_ROWS} rows, got {meta.num_rows}")
    ok = False
if meta.num_columns != EXPECTED_COLS:
    print(f"FAIL: expected {EXPECTED_COLS} columns, got {meta.num_columns}")
    ok = False

print("OK" if ok else "FAILED")
sys.exit(0 if ok else 1)

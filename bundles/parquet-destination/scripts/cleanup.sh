#!/bin/sh
# Remove the Parquet files produced by the case so the next entry starts clean.
# (The lab also drops the whole temp output dir after cleanup; this keeps the
# mounted dir tidy and demonstrates the cleanup hook.)
set -e
OUT="${1:-/output}"
echo "cleaning up parquet files in $OUT"
rm -f "$OUT"/events*.parquet

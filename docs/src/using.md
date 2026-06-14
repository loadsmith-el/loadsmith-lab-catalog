# Using the Catalog

This repo is consumed by `loadsmith-lab` as an origin. For local development,
register it as a **local** origin — the lab reads it live, with no install step:

```bash
# Register once (local dev: read live from the working tree)
loadsmith-lab origin local add catalog ../loadsmith-lab-canonical-catalog

# Run a single case
loadsmith-lab run --select catalog/postgres-to-jsonl

# Run a bundle
loadsmith-lab bundle run --select catalog/parquet-destination
```

A case's `services[].image` references an image from the
[`loadsmith-lab-canonical-images`](https://loadsmith-el.github.io/loadsmith-lab-canonical-images/)
repo as `images/<name>`; it is auto-built on first run.

For the run modes (building the core or a plugin from source via
`--loadsmith` / `--plugin`, picking a published image with `--tag`, and so on),
see the lab docs:

- [Running a Case](https://loadsmith-el.github.io/loadsmith-lab/getting-started/running-a-case.html)
- [Run Modes](https://loadsmith-el.github.io/loadsmith-lab/architecture/run-modes.html)
- [CLI Reference](https://loadsmith-el.github.io/loadsmith-lab/reference/cli.html)

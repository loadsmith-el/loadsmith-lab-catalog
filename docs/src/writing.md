# Writing a Case or Bundle

The full schemas and walkthroughs live in the
[loadsmith-lab docs](https://loadsmith-el.github.io/loadsmith-lab/):

- [Writing Cases](https://loadsmith-el.github.io/loadsmith-lab/writing-cases/case-yaml.html)
- [Writing Bundles](https://loadsmith-el.github.io/loadsmith-lab/writing-bundles/bundle-yaml.html)
- [`case.yaml` schema](https://loadsmith-el.github.io/loadsmith-lab/reference/case-yaml-schema.html)
- [`bundle.yaml` schema](https://loadsmith-el.github.io/loadsmith-lab/reference/bundle-yaml-schema.html)

What follows are the rules specific to **this** content repo.

## Hard rules for cases

- **Volume/scale cases must write to `null`.** Anything that inflates row counts
  via `CROSS JOIN` / `generate_series` MUST use `destination.type: "null"`
  (quoted — `null` is a YAML keyword) and assert only `rows_read` /
  `rows_written` in `expect`, with **no `output:` block**. A multi-million-row
  JSONL is gigabytes, and the output dir defaults to the system temp dir (often a
  tmpfs that can't hold it). Name them `<service>-to-null-<N>` (e.g.
  `postgres-to-null-15M`). The 100k smoke case (`postgres-to-jsonl`) is the one
  that validates real content/type round-trips — don't conflate the two
  purposes.
- **Postgres-protocol services need a query-level readiness probe**, not just
  `tcp:`. The service accepts connections while still loading the 100k-row seed,
  so a TCP-only check races. Mirror the `postgres:` probe block in
  `cases/postgres-to-jsonl/case.yaml`.
- **`services[].image` is an `<origin>/<name>` reference** (e.g.
  `images/lab-postgres-15`), resolved against
  [`loadsmith-lab-canonical-images`](https://loadsmith-el.github.io/loadsmith-lab-canonical-images/).
  If a case needs a new image, add it **there**, not here.

## Hard rules for bundles

- **A bundle never modifies the cases it sequences.** It only chains and wraps
  existing cases (which stay runnable standalone via `run --select`) with
  setup / validate / cleanup hooks.
- **Hook scripts run inside the bundle's own `Dockerfile`-built image** — no host
  Python or dependencies required.

## Where the engine boundary is

This repo is content only. If a change requires touching the runner or the
`case.rs` / `bundle.rs` schema, that's a
[`loadsmith-lab`](https://loadsmith-el.github.io/loadsmith-lab/) change, not a
catalog change.

## Verifying a change

This repo has no build step. Verify a case or bundle by running it through the
`loadsmith-lab` engine (registered as a local origin):

```bash
cd ../loadsmith-lab
./target/debug/loadsmith-lab origin local add catalog ../loadsmith-lab-canonical-catalog   # once
./target/debug/loadsmith-lab run --select catalog/<name>
./target/debug/loadsmith-lab bundle run --select catalog/<bundle-name>
```

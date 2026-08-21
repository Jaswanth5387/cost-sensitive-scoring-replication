# Independent Implementation of a Published Cost-Sensitive Scoring System

This repository is for a reproducibility artifact: choose a real engineering write-up about a production cost-sensitive or asymmetric-loss scoring system, implement the described scoring and decision policy, and compare measured numbers against the original claims.

The important result is not whether the reconstruction matches perfectly. The result is the measured gap between the published claim and this independent implementation.

## Artifact Contract

This repo is intended to satisfy:

- Implementation, not paraphrase.
- A cited source write-up with specific thresholds, cost structure, or before/after numbers.
- A written claim-by-claim comparison with exact matched and diverged numbers.
- Reproducible scripts, tests, configs, and seeds.
- A release suitable for Zenodo DOI archiving.
- A short note back to the original authors when the platform allows it.

## Current Target Status

Target selection is still open. Candidate write-ups are tracked in [docs/target_selection.md](docs/target_selection.md).

The implementation scaffold currently includes a generic expected-value gate and cost matrix utilities in `src/cost_sensitive_scoring/`. Once the source write-up is selected, those generic pieces should be adapted to match the source system exactly.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `src/cost_sensitive_scoring/` | Implementation package |
| `tests/` | Unit tests for scoring and decision logic |
| `docs/target_selection.md` | Candidate write-ups and selection rubric |
| `reports/comparison.md` | Claim-by-claim replication report |
| `data/` | Local data staging; raw data is not committed unless license permits |
| `scripts/` | Reproducible experiment entry points |

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run the placeholder experiment:

```bash
python scripts/run_expected_value_demo.py
```

## Replication Standard

Each source claim must be recorded before running the corresponding experiment:

| Claim ID | Original Claim | Source Location | Reproduction Metric | Our Number | Status |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | pending |

Status values:

- `matched`: Our number is within a pre-declared tolerance.
- `diverged`: Our number is outside tolerance.
- `not_reproducible`: The post omits a necessary detail.
- `not_applicable`: The source claim depends on private scale, data, or infra that cannot be approximated honestly.

## Zenodo Release Checklist

- [ ] Select target write-up and cite exact URL.
- [ ] Freeze data snapshot or document how to regenerate it.
- [ ] Commit experiment configs and seeds.
- [ ] Fill `reports/comparison.md`.
- [ ] Create GitHub release.
- [ ] Archive release on Zenodo.
- [ ] Add DOI badge and citation metadata.
- [ ] Submit note/comment/discussion to original blog if possible.

## License

Code is released under the MIT License. Data and reproduced source excerpts may have separate licensing constraints; see [LICENSE](LICENSE) and future dataset notes.

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

## Target

The current target is Stripe's public guide, ["A primer on machine learning for fraud detection"](https://stripe.com/ae/guides/primer-on-machine-learning-for-fraud-protection).

This is not an implementation of Stripe Radar. It reconstructs the disclosed cost-sensitive decision framework and compares it against an independent fraud-scoring run.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `src/cost_sensitive_scoring/` | Implementation package |
| `tests/` | Unit tests for scoring and decision logic |
| `docs/target_selection.md` | Candidate write-ups and selection rubric |
| `reports/comparison.md` | Claim-by-claim replication report |
| `experiments/` | Threshold sweep and cost sensitivity scripts |
| `data/` | Local data staging; raw data is not committed unless license permits |
| `results/` | Generated experiment outputs |

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run the placeholder experiment:

```bash
python experiments/threshold_sweep.py
python experiments/sensitivity_analysis.py
```

If `data/raw/creditcard.csv` exists, the scripts use it. Otherwise they run against a deterministic synthetic imbalanced dataset so the pipeline remains executable.

## Replication Standard

Each source claim must be recorded before running the corresponding experiment:

| Claim ID | Original Claim | Source Location | Reproduction Metric | Our Number | Status |
| --- | --- | --- | --- | --- | --- |
| C1 | Legitimate profit from `$26` sale at `8%` margin | Stripe guide | arithmetic reproduction | `$2.08` | matched |
| C2 | Fraud loss from product cost plus `$15` chargeback fee | Stripe guide | arithmetic reproduction | `$38.92` | matched |
| C3 | Fraud-to-legitimate-profit ratio | Stripe guide | arithmetic reproduction | `18.71x` | matched |
| C4 | Break-even precision | Stripe guide | arithmetic reproduction | `5.07%` | matched |
| C5 | `P(fraud) > 0.7` block rule | Stripe guide | public dataset threshold sweep | `0.04` | diverged |

The current result uses the Zenodo mirror of the European credit-card fraud dataset. The raw 150 MB CSV is not committed; see [data/README.md](data/README.md).

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

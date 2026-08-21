# Release Notes

## v0.1.1

First reproducible artifact release.

DOI: https://doi.org/10.5281/zenodo.22043545

Includes:

- Stripe economics reproduction.
- Public ULB/Zenodo credit-card fraud dataset run.
- Threshold sweep under Stripe's example cost model.
- Cost sensitivity analysis.
- Five-seed variance check.
- Figures for threshold cost and cost sensitivity.
- Draft note to the original source authors.

Main result:

| Metric | Value |
| --- | ---: |
| Stripe illustrative threshold | `0.70` |
| Main-run cost-optimal threshold | `0.04` |
| Five-seed mean threshold | `0.108` |
| Five-seed threshold std | `0.079` |
| Main-run ROC AUC | `0.9874` |
| Main-run average precision | `0.8378` |

The disclosed Stripe economics reproduce exactly, but the illustrative threshold does not transfer to this independent model and public dataset.

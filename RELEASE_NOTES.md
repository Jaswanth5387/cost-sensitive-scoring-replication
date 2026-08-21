# Release Notes

## v0.2.0

Final report release.

DOI: https://doi.org/10.5281/zenodo.22044138

Includes:

- Stripe economics reproduction.
- Public ULB/Zenodo credit-card fraud dataset run.
- Threshold sweep under Stripe's example cost model.
- Cost sensitivity analysis.
- Policy baseline and error analysis.
- Calibration check.
- Fixed-cost versus amount-scaled cost sanity check.
- Final research report.
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
| Stripe example threshold cost | `$1,768.04` |
| Cost-optimal threshold cost | `$814.36` |
| Calibration Brier score | `0.000504` |
| Amount-scaled cost-optimal threshold | `0.33` |

The disclosed Stripe economics reproduce exactly. Stripe's illustrative threshold is not cost-optimal in this independent model and public dataset, but the result is not a claim about Stripe Radar's production threshold.

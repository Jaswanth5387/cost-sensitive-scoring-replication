# Comparison Report

## Source

- Original write-up: Stripe, "A primer on machine learning for fraud detection"
- URL: https://stripe.com/ae/guides/primer-on-machine-learning-for-fraud-protection
- Access date: 2026-08-21

## Claim Under Test

State each claim as a number before running the reproduction.

| Claim ID | Source Claim | Source Evidence | Reproduction Setup | Original Number | Our Number | Difference | Status |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| C1 | Profit on a `$26` sale at `8%` margin | Stripe guide economics example | Direct arithmetic | 2.08 | 2.08 | 0.00 | matched |
| C2 | Fraud loss equals product cost plus `$15` chargeback fee | Stripe guide economics example | Direct arithmetic | 38.92 | 38.92 | 0.00 | matched |
| C3 | One fraud loss equals `18.71` legitimate profits | Stripe guide economics example | Direct arithmetic | 18.71 | 18.71 | 0.00 | matched |
| C4 | Break-even precision is `5.07%` | Stripe guide economics example | Direct arithmetic | 5.07% | 5.07% | 0.00 pp | matched |
| C5 | Block payments where `P(fraud) > 0.7` | Stripe illustrative policy example | Threshold sweep on Zenodo credit-card fraud data | 0.70 | 0.04 | -0.66 | diverged |

## Implementation Notes

Implemented directly:

- Stripe's sale, margin, chargeback, fraud-loss, ratio, and break-even precision arithmetic.
- A block/allow threshold sweep over calibrated fraud probabilities.
- Cost evaluation using false-positive cost as lost legitimate profit and false-negative cost as fraud loss.

Inferred:

- The model, public dataset, feature set, calibration method, and threshold grid.
- Stripe does not publish Radar's production model, data, or universal threshold.

## Divergences

On the public ULB/Zenodo credit-card fraud dataset, the independently cost-optimal threshold is `0.04`, far below Stripe's illustrative `0.70` rule. This is the first claim that does not transfer cleanly.

This is not evidence that Stripe's threshold is wrong. Stripe presents `0.70` as an example policy threshold, not as a universal optimum. The result does show the core artifact point: once the economics are wired into an actual score distribution, the operating point becomes a property of the model, calibration, data distribution, and merchant cost assumptions together.

## Seed Variance

| Metric | Mean | Std |
| --- | ---: | ---: |
| ROC AUC | 0.9751 | 0.0096 |
| Average precision | 0.8229 | 0.0422 |
| Best threshold | 0.1080 | 0.0785 |
| Best total cost | 822.98 | 186.03 |
| Precision at best threshold | 0.7420 | 0.0440 |
| Recall at best threshold | 0.8439 | 0.0383 |

The divergence from `0.70` is stable in direction across seeds: even allowing for threshold variance, the observed optimum remains far below Stripe's illustrative threshold.

## Figures

- `figures/threshold_cost.png`: cost curve with Stripe's `0.70` example and the observed optimum.
- `figures/sensitivity_heatmap.png`: best threshold under alternate false-positive and false-negative costs.

## Threats to Validity

- Data scale: Stripe uses private network-scale transaction data; the current run uses the public ULB/Zenodo credit-card fraud dataset.
- Feature mismatch: Stripe has proprietary payment, card, merchant, and network features.
- Cost assumption mismatch: The current run uses Stripe's single merchant economics example.
- Infrastructure mismatch: This is an offline reconstruction, not a real-time production hold system.
- Randomness and seed variance: Multi-seed runs are included, but the model family and calibration method are still fixed.

## Note to Original Authors

Draft the short comment/discussion note here before posting.

Draft:

> I independently reconstructed the disclosed cost-sensitive economics in Stripe's fraud-detection primer using the public ULB/Zenodo credit-card fraud dataset. The arithmetic examples reproduce exactly: `$2.08` legitimate profit, `$38.92` fraud loss, `18.71x` fraud-to-profit ratio, and `5.07%` break-even precision. The decision threshold did not transfer: under my calibrated model and Stripe's example economics, the cost-optimal threshold was `0.04` in the main run and `0.108 ± 0.079` across five seeds, versus the article's illustrative `P(fraud) > 0.70` rule. I interpret this as evidence that the economics transfer cleanly but the operating threshold is inseparable from the score distribution, calibration, dataset, and production constraints.

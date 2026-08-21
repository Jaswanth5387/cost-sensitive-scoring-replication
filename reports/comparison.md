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
| C5 | Illustrative block policy `P(fraud) > 0.7` | Stripe precision/recall example | Threshold sweep on Zenodo credit-card fraud data | 0.70 | evaluated | n/a | tested |
| C6 | Cost-optimal threshold | Not published by Stripe | Fixed-cost reconstruction | n/a | 0.04 | n/a | reconstruction result |
| C7 | Cost-optimal threshold under amount-scaled costs | Not published by Stripe | Amount-scaled reconstruction | n/a | 0.33 | n/a | sanity-check result |

## Implementation Notes

Implemented directly:

- Stripe's sale, margin, chargeback, fraud-loss, ratio, and break-even precision arithmetic.
- A block/allow threshold sweep over calibrated fraud probabilities.
- Cost evaluation using false-positive cost as lost legitimate profit and false-negative cost as fraud loss.

Inferred:

- The model, public dataset, feature set, calibration method, and threshold grid.
- Stripe does not publish Radar's production model, data, or universal threshold.

## Divergences

On the public ULB/Zenodo credit-card fraud dataset, the independently cost-optimal fixed-cost threshold is `0.04`, far below Stripe's illustrative `0.70` rule. Under amount-scaled costs, the optimum moves to `0.33`.

This is not evidence that Stripe's threshold is wrong. Stripe presents `0.70` as an example policy threshold, not as a universal optimum. The result does show the core artifact point: once the economics are wired into an actual score distribution, the operating point becomes a property of the model, calibration, data distribution, and merchant cost assumptions together.

## Error Analysis

| Policy | Blocked | False positives | False negatives | Cost | Cost vs optimum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Always allow | 0 | 0 | 123 | 4787.16 | +3972.80 |
| Always block | 71202 | 71079 | 0 | 147844.32 | +147029.96 |
| Stripe example `0.70` | 86 | 8 | 45 | 1768.04 | +953.68 |
| Cost optimum `0.04` | 140 | 36 | 19 | 814.36 | 0.00 |

The `0.70` rule is much better than the naive baselines, but it leaves 45 fraudulent transactions unblocked in the held-out set. Lowering the threshold to `0.04` adds 28 false positives while preventing 26 additional false negatives. Under the Stripe example economics, those additional holds are worth it.

## Cost Model Sanity Check

| Cost model | Optimal threshold | Cost at optimum | Cost at `0.70` | Relative reduction vs `0.70` |
| --- | ---: | ---: | ---: | ---: |
| Fixed Stripe example | 0.04 | 814.36 | 1768.04 | 53.94% |
| Amount-scaled reconstruction | 0.33 | 3167.77 | 5626.45 | 43.70% |

The exact threshold is sensitive to cost interpretation. The broader direction remains stable: both reconstructed cost models choose a lower threshold than `0.70`.

## Calibration Check

| Metric | Value |
| --- | ---: |
| Brier score | 0.000504 |
| Highest-bin mean score | 0.0154 |
| Highest-bin observed fraud rate | 0.0166 |

The highest populated score bin is close to calibrated, so the failed threshold transfer is not explained away by a completely broken probability scale. It is mainly a decision-policy result: a high fraud-loss-to-profit ratio makes some low-probability holds economically rational.

## Seed Variance

| Metric | Mean | Std |
| --- | ---: | ---: |
| ROC AUC | 0.9751 | 0.0096 |
| Average precision | 0.8229 | 0.0422 |
| Best threshold | 0.1080 | 0.0785 |
| Best total cost | 822.98 | 186.03 |
| Precision at best threshold | 0.7420 | 0.0440 |
| Recall at best threshold | 0.8439 | 0.0383 |

The divergence from `0.70` is stable in direction across seeds: even allowing for threshold variance, the observed fixed-cost optimum remains below Stripe's illustrative threshold.

## Figures

- `figures/threshold_cost.png`: cost curve with Stripe's `0.70` example and the observed optimum.
- `figures/sensitivity_heatmap.png`: best threshold under alternate false-positive and false-negative costs.
- `figures/calibration.png`: predicted score bins versus observed fraud rates.
- `results/cost_model_comparison.csv`: fixed-cost and amount-scaled cost comparison.
- `results/confusion_matrices.csv`: confusion matrices at `0.04` and `0.70`.
- `results/score_distribution.csv`: score distribution around the two thresholds.

## Threats to Validity

- Data scale: Stripe uses private network-scale transaction data; the current run uses the public ULB/Zenodo credit-card fraud dataset.
- Feature mismatch: Stripe has proprietary payment, card, merchant, and network features.
- Cost assumption mismatch: The current run uses Stripe's single merchant economics example.
- Infrastructure mismatch: This is an offline reconstruction, not a real-time production hold system.
- Randomness and seed variance: Multi-seed runs are included, but the model family and calibration method are still fixed.

## Note to Original Authors

Draft the short comment/discussion note here before posting.

Draft:

> I independently reconstructed the disclosed cost-sensitive economics in Stripe's fraud-detection primer using the public ULB/Zenodo credit-card fraud dataset. The arithmetic examples reproduce exactly: `$2.08` legitimate profit, `$38.92` fraud loss, `18.71x` fraud-to-profit ratio, and `5.07%` break-even precision. I then evaluated the article's illustrative `P(fraud) > 0.70` policy under the reconstructed setup. Under fixed Stripe-example costs, the cost-optimal threshold was `0.04`; under amount-scaled costs, it moved to `0.33`. I do not interpret this as a claim about Stripe Radar's production threshold. The result is that the published economics transfer cleanly, while the operating point is inseparable from the score distribution, calibration, dataset, and cost interpretation.

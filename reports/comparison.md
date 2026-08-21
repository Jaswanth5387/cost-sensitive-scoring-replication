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
| C5 | Block payments where `P(fraud) > 0.7` | Stripe illustrative policy example | Threshold sweep on synthetic fallback data | 0.70 | 0.07 | -0.63 | diverged |

## Implementation Notes

Implemented directly:

- Stripe's sale, margin, chargeback, fraud-loss, ratio, and break-even precision arithmetic.
- A block/allow threshold sweep over calibrated fraud probabilities.
- Cost evaluation using false-positive cost as lost legitimate profit and false-negative cost as fraud loss.

Inferred:

- The model, public dataset, feature set, calibration method, and threshold grid.
- Stripe does not publish Radar's production model, data, or universal threshold.

## Divergences

On the deterministic synthetic fallback run, the independently cost-optimal threshold is `0.07`, far below Stripe's illustrative `0.70` rule. This is the first claim that does not transfer cleanly.

This is not evidence that Stripe's threshold is wrong. Stripe presents `0.70` as an example policy threshold, not as a universal optimum. The result does show the core artifact point: once the economics are wired into an actual score distribution, the operating point becomes a property of the model, calibration, data distribution, and merchant cost assumptions together.

## Threats to Validity

- Data scale: Stripe uses private network-scale transaction data; the current checked-in run uses a synthetic fallback dataset.
- Feature mismatch: Stripe has proprietary payment, card, merchant, and network features.
- Cost assumption mismatch: The current run uses Stripe's single merchant economics example.
- Infrastructure mismatch: This is an offline reconstruction, not a real-time production hold system.
- Randomness and seed variance: Current scripts use a fixed seed; multi-seed runs still need to be added.

## Note to Original Authors

Draft the short comment/discussion note here before posting.

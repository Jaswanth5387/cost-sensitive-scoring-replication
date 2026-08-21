# Claims

Source: Stripe, "A primer on machine learning for fraud detection"  
URL: https://stripe.com/ae/guides/primer-on-machine-learning-for-fraud-protection

## Reproduced Economics

| ID | Claim | Source number | Status |
| --- | --- | ---: | --- |
| C1 | Average sale of `$26` at `8%` margin gives legitimate profit of `$2.08` | 2.08 | implemented |
| C2 | Product cost is `$26 - $2.08` | 23.92 | implemented |
| C3 | Fraud loss with a `$15` chargeback fee is `$23.92 + $15` | 38.92 | implemented |
| C4 | One fraud loss equals `38.92 / 2.08` legitimate sale profits | 18.71 | implemented |
| C5 | Break-even precision is `1 / (1 + 18.71)` | 5.07% | implemented |
| C6 | Stripe uses `P(fraud) > 0.7` as an illustrative block rule | 0.70 | comparison target |

## Not Claimed By Stripe

Stripe does not disclose a universal production threshold, model weights, training data, or a cost-optimal operating point. This repo compares the disclosed economics and illustrative threshold against an independent reconstruction.

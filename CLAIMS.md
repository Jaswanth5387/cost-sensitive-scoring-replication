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
| C6 | Stripe uses `P(fraud) > 0.7` as an illustrative block rule for precision/recall explanation | 0.70 | comparison target |
| C7 | Stripe's actual cost-optimal or production threshold | not published | not reproduced |

## Not Claimed By Stripe

Stripe does not disclose a universal production threshold, model weights, training data, or a cost-optimal operating point. This repo compares the disclosed economics and illustrative threshold against an independent reconstruction.

## Claim-Evidence-Reconstruction Table

| Stripe statement | Stripe value | Reconstruction | Result |
| --- | ---: | ---: | --- |
| Average sale | `$26.00` | `$26.00` | exact match |
| Margin | `8%` | `8%` | exact match |
| Legitimate profit | `$2.08` | `$2.08` | exact match |
| Product cost | `$23.92` | `$23.92` | exact match |
| Chargeback fee | `$15.00` | `$15.00` | exact match |
| Fraud loss | `$38.92` | `$38.92` | exact match |
| Cost ratio | `18.71x` | `18.71x` | exact match |
| Break-even precision | `5.07%` | `5.07%` | exact match |
| Example threshold | `0.70` | evaluated | comparison target |
| Cost-optimal threshold | not published | `0.04` fixed cost, `0.33` amount-scaled | reconstruction result |

# Cost Model

This repository separates Stripe's published arithmetic from the reconstruction assumptions used to evaluate a public fraud dataset.

## Published Stripe Arithmetic

Stripe's guide gives an approximate break-even precision example:

| Quantity | Value | Source status |
| --- | ---: | --- |
| Average sale | `$26.00` | published |
| Margin | `8%` | published |
| Chargeback fee | `$15.00` | published |
| Legitimate profit | `$26.00 * 0.08 = $2.08` | published derivation |
| Product cost | `$26.00 - $2.08 = $23.92` | published derivation |
| Fraud loss | `$23.92 + $15.00 = $38.92` | published derivation |
| Fraud-to-profit ratio | `$38.92 / $2.08 = 18.71` | published derivation |
| Break-even precision | `1 / (1 + 18.71) = 5.07%` | published derivation |

The source is Stripe's "A primer on machine learning for fraud detection":

https://stripe.com/guides/primer-on-machine-learning-for-fraud-protection

## Reconstruction Assumptions

The public ULB/Zenodo credit-card dataset is not Stripe data. It does not include merchant margin, product cost, chargeback fee, intervention cost, or Stripe Radar's production features.

For the main reconstruction, each false positive is assigned the lost legitimate profit from Stripe's example, and each false negative is assigned the fraud loss from Stripe's example:

| Error | Main cost used here | Status |
| --- | ---: | --- |
| False positive: legitimate transaction blocked | `$2.08` | Stripe-derived fixed assumption |
| False negative: fraudulent transaction allowed | `$38.92` | Stripe-derived fixed assumption |

This is not Stripe's production cost function. It is an independent reconstruction that applies Stripe's published example economics to a public score distribution.

## Amount-Scaled Sanity Check

As a robustness check, the repo also evaluates an amount-scaled variant using the dataset's `Amount` column:

| Error | Amount-scaled reconstruction |
| --- | --- |
| False positive | `Amount * 0.08` |
| False negative | `Amount * (1 - 0.08) + 15` |

At `Amount = $26`, this reduces to Stripe's published `$2.08` and `$38.92` example. On the real dataset, it lets larger transactions carry larger modeled losses.

## Why Both Are Reported

The fixed-cost model tests Stripe's exact break-even arithmetic against one independent score distribution.

The amount-scaled model tests whether the headline threshold is fragile to a plausible transaction-level extension. It is not claimed to be more faithful to Stripe. It is a sanity check on how much the result depends on treating every transaction as if it were the `$26` example transaction.

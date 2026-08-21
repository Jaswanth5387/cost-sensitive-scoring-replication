# Results Summary

Run date: 2026-08-21  
Data: Zenodo `creditcard.csv`, MD5 `e90efcb83d69faf99fcab8b0255024de`

## Stripe Economics

| Metric | Value |
| --- | ---: |
| Legitimate profit | `$2.08` |
| Fraud loss | `$38.92` |
| Fraud-to-profit ratio | `18.71x` |
| Break-even precision | `5.07%` |

## Threshold Sweep

| Metric | Value |
| --- | ---: |
| ROC AUC | `0.9874` |
| Average precision | `0.8378` |
| Stripe illustrative threshold | `0.70` |
| Cost-optimal threshold on this run | `0.04` |
| Minimum total cost | `$814.36` |

The first divergence is large: on this public dataset and model, the cheapest threshold is much lower than Stripe's illustrative `0.70` example. This should not be read as a claim about Stripe Radar. It shows that the operating threshold is highly dependent on score calibration, class prevalence, feature quality, and merchant economics.

## Policy Comparison

| Policy | Blocked | False positives | False negatives | Cost | Cost vs optimum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Always allow | `0` | `0` | `123` | `$4,787.16` | `+$3,972.80` |
| Always block | `71,202` | `71,079` | `0` | `$147,844.32` | `+$147,029.96` |
| Stripe example `0.70` | `86` | `8` | `45` | `$1,768.04` | `+$953.68` |
| Cost optimum `0.04` | `140` | `36` | `19` | `$814.36` | `$0.00` |

The Stripe example threshold is precise but too conservative for this score distribution under the example cost model. It avoids false positives, but the missed fraud dominates the cost.

## Calibration Check

| Metric | Value |
| --- | ---: |
| Brier score | `0.000504` |
| Highest-bin mean score | `0.0154` |
| Highest-bin observed fraud rate | `0.0166` |

The calibration curve is close in the highest populated score bin, which supports the main interpretation: the threshold gap is driven by the public score distribution and cost ratio, not only by a broken probability scale.

## Cost Model Sanity Check

| Cost model | Optimal threshold | Cost at optimum | Cost at `0.70` | Relative reduction |
| --- | ---: | ---: | ---: | ---: |
| Fixed Stripe example | `0.04` | `$814.36` | `$1,768.04` | `53.94%` |
| Amount-scaled reconstruction | `0.33` | `$3,167.77` | `$5,626.45` | `43.70%` |

The exact optimum is cost-model dependent. The amount-scaled reconstruction moves the threshold upward to `0.33`, but it remains below the illustrative `0.70` policy.

## Confusion Matrices

| Threshold | Action | Actual legitimate | Actual fraud |
| ---: | --- | ---: | ---: |
| `0.04` | allow | `71,043` | `19` |
| `0.04` | block | `36` | `104` |
| `0.70` | allow | `71,071` | `45` |
| `0.70` | block | `8` | `78` |

## Multi-Seed Check

| Metric | Mean | Std |
| --- | ---: | ---: |
| Best threshold | `0.1080` | `0.0785` |
| Best total cost | `$822.98` | `$186.03` |
| ROC AUC | `0.9751` | `0.0096` |
| Average precision | `0.8229` | `0.0422` |

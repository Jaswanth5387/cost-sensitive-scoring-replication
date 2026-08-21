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

## Multi-Seed Check

| Metric | Mean | Std |
| --- | ---: | ---: |
| Best threshold | `0.1080` | `0.0785` |
| Best total cost | `$822.98` | `$186.03` |
| ROC AUC | `0.9751` | `0.0096` |
| Average precision | `0.8229` | `0.0422` |

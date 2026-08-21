# Target Selection Log

This artifact needs a source write-up that can be contradicted by measurement. The selected target must include enough implementation detail to rebuild a cost-sensitive scoring or decision policy.

## Selection Criteria

Required:

- Public engineering write-up, paper, or technical post.
- Production or production-like scoring system.
- Asymmetric cost, expected-value decision policy, or named decision threshold.
- At least one quantitative claim to reproduce.
- Enough implementation detail to avoid inventing the method.

Reject if:

- The post only says a metric improved without explaining the scoring policy.
- The threshold or cost structure is not named or inferable.
- The data requirements are impossible to approximate and no smaller-scale proxy is honest.

## Candidate Table

| Candidate | Domain | Technical Specificity | Published Claim | Reproducibility Risk | Decision |
| --- | --- | --- | --- | --- | --- |
| Stripe: "A primer on machine learning for fraud detection" | Fraud | Strong for economics and threshold illustration; limited for model internals | `$2.08` profit, `$38.92` fraud loss, `18.71x` cost ratio, `5.07%` break-even precision, illustrative `P(fraud)>0.7` policy | Stripe does not disclose Radar data/model or a universal production threshold | selected |
| NIST: "Addressing misclassification costs in machine learning through asymmetric loss functions" | Industrial defect / imbalanced classification | Strong: asymmetric focal loss, cost ratio `C`, threshold `tau`, reported cost reduction ranges | AFL reduces total cost versus weighted BCE by 15%-40% for `0.2 < tau < 0.5`, `C > 64`; AFL reduces total cost at `0.1 <= tau < 0.5`, `C > 128` | It is a paper rather than an engineering blog; may still be acceptable if the artifact scope permits published technical write-ups | backup |
| Fraud Detection Handbook: cost-sensitive learning chapter | Credit-card fraud | Strong for method and open data, weaker as a "published production write-up" | Cost-matrix framing and reproducible fraud experiments | May not contain a company before/after production claim | backup substrate |
| Tableau: "Cost Sensitive Classifiers for Better Machine Learning Decision-Making" | General decision systems | Medium: explains design pattern | TBD | Likely too conceptual; may lack numeric claims | likely reject |
| Medium: "Fraud detection with cost-sensitive machine learning" | Fraud | Unknown | TBD | Platform and source details need verification; may be tutorial rather than production report | investigate |

## Final Target

Stripe's fraud-detection primer is selected for the first implementation pass.

Once chosen, record:

- Source URL: https://stripe.com/ae/guides/primer-on-machine-learning-for-fraud-protection
- Archived URL: TBD
- Date accessed: 2026-08-21
- System being reconstructed: cost-sensitive fraud probability thresholding
- Claims to test: C1-C6 in `CLAIMS.md`
- Known gaps: private data, private features, private model, production counterfactual evaluation
- Pre-declared tolerance: exact arithmetic claims must match to two decimals; threshold divergence is reported without treating `0.70` as a production optimum

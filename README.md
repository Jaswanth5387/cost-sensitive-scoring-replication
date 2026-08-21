# Cost-Sensitive Fraud Threshold Reconstruction

An independent reconstruction of the cost-sensitive decision example in Stripe's public guide, ["A primer on machine learning for fraud detection"](https://stripe.com/ae/guides/primer-on-machine-learning-for-fraud-protection).

This is not Stripe Radar. Stripe does not publish Radar's model, features, training data, or production threshold. This repo reconstructs the part Stripe does disclose: the economics that turn a fraud probability into a block/allow decision.

## Result

Stripe's arithmetic transfers exactly. The threshold does not.

| Claim | Stripe | This repo | Status |
| --- | ---: | ---: | --- |
| Legitimate profit on `$26` sale at `8%` margin | `$2.08` | `$2.08` | matched |
| Fraud loss with `$15` chargeback fee | `$38.92` | `$38.92` | matched |
| Fraud-to-profit ratio | `18.71x` | `18.71x` | matched |
| Break-even precision | `5.07%` | `5.07%` | matched |
| Example block rule | `P(fraud) > 0.70` | cost optimum `0.04` | diverged |

Across five train/test seeds, the cost-optimal threshold mean is `0.108` with standard deviation `0.079`. The single-seed threshold sweep gives `0.04`.

The gap is the artifact: once the economics are attached to a real score distribution, the operating point depends on model calibration, class prevalence, feature quality, and merchant cost assumptions.

## Figures

![Threshold vs cost](figures/threshold_cost.png)

![Sensitivity heatmap](figures/sensitivity_heatmap.png)

## Data

The run uses the Zenodo mirror of the European credit-card fraud dataset:

- Zenodo record: https://zenodo.org/records/7395559
- DOI: `10.5281/zenodo.7395559`
- File: `creditcard.csv`
- MD5: `e90efcb83d69faf99fcab8b0255024de`

The raw 150 MB CSV is not committed. See [data/README.md](data/README.md).

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/download_data.py
python experiments/threshold_sweep.py
python experiments/sensitivity_analysis.py
python experiments/multi_seed.py
python experiments/plots.py
pytest
ruff check .
```

If `data/raw/creditcard.csv` is missing, the experiment scripts fall back to a deterministic synthetic imbalanced dataset. The checked-in result uses the real Zenodo CSV.

## Files

| Path | Purpose |
| --- | --- |
| `CLAIMS.md` | Source claims being tested |
| `reports/comparison.md` | Main comparison report |
| `src/cost_sensitive_scoring/` | Cost model, threshold evaluation, model training |
| `experiments/` | Reproducible experiment scripts |
| `results/` | Saved result CSVs and summary |
| `figures/` | Generated plots |
| `data/README.md` | Dataset source and checksum |

## Current Limitations

- Stripe's private data and production features are unavailable.
- The public dataset is offline and historical, not a live payment stream.
- The model family and calibration method are fixed.
- The `0.70` value is Stripe's illustrative threshold, not a disclosed universal production optimum.

## Next Release Steps

- Create GitHub release `v0.1.0`.
- Archive the release on Zenodo.
- Add the Zenodo DOI to `CITATION.cff`.
- Post the short comparison note drafted in [reports/comparison.md](reports/comparison.md), if Stripe's platform allows it.

## License

MIT. Dataset rights are separate; see the Zenodo record and [data/README.md](data/README.md).

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from cost_sensitive_scoring.cost_model import StripeEconomics
from cost_sensitive_scoring.data import load_creditcard_or_synthetic
from cost_sensitive_scoring.evaluation import best_threshold, score_thresholds
from cost_sensitive_scoring.model import train_model

SEEDS = [1, 7, 13, 23, 42]


def main() -> None:
    economics = StripeEconomics()
    data = load_creditcard_or_synthetic(Path("data/raw/creditcard.csv"))
    thresholds = np.round(np.arange(0.01, 1.00, 0.01), 2)
    rows = []

    for seed in SEEDS:
        run = train_model(data, seed=seed)
        results = score_thresholds(
            run["y_test"],
            run["scores"],
            thresholds,
            false_positive_cost=economics.legitimate_profit,
            false_negative_cost=economics.fraud_loss,
        )
        best = best_threshold(results)
        rows.append(
            {
                "seed": seed,
                "roc_auc": run["roc_auc"],
                "average_precision": run["average_precision"],
                "best_threshold": best["threshold"],
                "best_total_cost": best["total_cost"],
                "false_positives": int(best["false_positives"]),
                "false_negatives": int(best["false_negatives"]),
                "precision": best["precision"],
                "recall": best["recall"],
            }
        )

    frame = pd.DataFrame(rows)
    summary = frame.drop(columns=["seed"]).agg(["mean", "std"]).reset_index(names="stat")

    Path("results").mkdir(exist_ok=True)
    frame.to_csv("results/multi_seed.csv", index=False)
    summary.to_csv("results/multi_seed_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

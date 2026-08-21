from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from cost_sensitive_scoring.data import load_creditcard_or_synthetic
from cost_sensitive_scoring.evaluation import best_threshold, score_thresholds
from cost_sensitive_scoring.model import train_model


def main() -> None:
    data = load_creditcard_or_synthetic(Path("data/raw/creditcard.csv"))
    run = train_model(data)
    thresholds = np.round(np.arange(0.01, 1.00, 0.01), 2)

    rows = []
    for fp_cost in [1, 2.08, 5, 10]:
        for fn_cost in [10, 20, 38.92, 50, 100]:
            results = score_thresholds(run["y_test"], run["scores"], thresholds, fp_cost, fn_cost)
            best = best_threshold(results)
            rows.append(
                {
                    "false_positive_cost": fp_cost,
                    "false_negative_cost": fn_cost,
                    "cost_ratio": fn_cost / fp_cost,
                    "best_threshold": best["threshold"],
                    "best_total_cost": best["total_cost"],
                }
            )

    Path("results").mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv("results/sensitivity_analysis.csv", index=False)


if __name__ == "__main__":
    main()

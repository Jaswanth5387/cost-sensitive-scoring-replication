from __future__ import annotations

from pathlib import Path

import numpy as np

from cost_sensitive_scoring.cost_model import StripeEconomics
from cost_sensitive_scoring.data import load_creditcard_or_synthetic
from cost_sensitive_scoring.evaluation import best_threshold, score_thresholds
from cost_sensitive_scoring.model import train_model


def main() -> None:
    economics = StripeEconomics()
    data = load_creditcard_or_synthetic(Path("data/raw/creditcard.csv"))
    run = train_model(data)

    thresholds = np.round(np.arange(0.01, 1.00, 0.01), 2)
    results = score_thresholds(
        run["y_test"],
        run["scores"],
        thresholds,
        false_positive_cost=economics.legitimate_profit,
        false_negative_cost=economics.fraud_loss,
    )
    best = best_threshold(results)

    Path("results").mkdir(exist_ok=True)
    results.to_csv("results/threshold_sweep.csv", index=False)

    print(f"roc_auc={run['roc_auc']:.4f}")
    print(f"average_precision={run['average_precision']:.4f}")
    print(f"stripe_break_even_precision={economics.break_even_precision:.4f}")
    print(f"best_threshold={best['threshold']:.2f}")
    print(f"best_total_cost={best['total_cost']:.2f}")


if __name__ == "__main__":
    main()

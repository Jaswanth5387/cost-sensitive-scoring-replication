from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss

from cost_sensitive_scoring.cost_model import StripeEconomics
from cost_sensitive_scoring.data import load_creditcard_or_synthetic
from cost_sensitive_scoring.evaluation import best_threshold, score_thresholds
from cost_sensitive_scoring.model import train_model


def policy_row(name: str, threshold: float, scored: pd.DataFrame) -> dict:
    row = scored.loc[np.isclose(scored["threshold"], threshold)].iloc[0]
    return {
        "policy": name,
        "threshold": threshold,
        "blocked": int(row["true_positives"] + row["false_positives"]),
        "false_positives": int(row["false_positives"]),
        "false_negatives": int(row["false_negatives"]),
        "true_positives": int(row["true_positives"]),
        "precision": row["precision"],
        "recall": row["recall"],
        "total_cost": row["total_cost"],
    }


def always_allow_row(y_true: np.ndarray, false_negative_cost: float) -> dict:
    fraud_count = int(np.sum(y_true == 1))
    return {
        "policy": "always_allow",
        "threshold": np.nan,
        "blocked": 0,
        "false_positives": 0,
        "false_negatives": fraud_count,
        "true_positives": 0,
        "precision": 0.0,
        "recall": 0.0,
        "total_cost": fraud_count * false_negative_cost,
    }


def calibration_bins(y_true: np.ndarray, scores: np.ndarray, n_bins: int = 10) -> pd.DataFrame:
    frame = pd.DataFrame({"y_true": y_true, "score": scores})
    frame["bin"] = pd.qcut(frame["score"], q=n_bins, duplicates="drop")
    return (
        frame.groupby("bin", observed=True)
        .agg(
            count=("y_true", "size"),
            mean_score=("score", "mean"),
            observed_fraud_rate=("y_true", "mean"),
        )
        .reset_index(drop=True)
    )


def main() -> None:
    economics = StripeEconomics()
    data = load_creditcard_or_synthetic(Path("data/raw/creditcard.csv"))
    run = train_model(data)

    thresholds = np.round(np.arange(0.00, 1.01, 0.01), 2)
    scored = score_thresholds(
        run["y_test"],
        run["scores"],
        thresholds,
        false_positive_cost=economics.legitimate_profit,
        false_negative_cost=economics.fraud_loss,
    )
    best = best_threshold(scored)

    rows = [
        always_allow_row(run["y_test"], economics.fraud_loss),
        policy_row("always_block", 0.0, scored),
        policy_row("stripe_example_0.70", 0.70, scored),
        policy_row("cost_optimal", float(best["threshold"]), scored),
    ]
    baseline = pd.DataFrame(rows)
    baseline["cost_vs_optimum"] = baseline["total_cost"] - float(best["total_cost"])

    calibration = calibration_bins(run["y_test"], run["scores"])
    calibration["brier_score"] = brier_score_loss(run["y_test"], run["scores"])

    Path("results").mkdir(exist_ok=True)
    baseline.to_csv("results/policy_comparison.csv", index=False)
    calibration.to_csv("results/calibration_bins.csv", index=False)

    print("policy_comparison=results/policy_comparison.csv")
    print("calibration_bins=results/calibration_bins.csv")
    print(f"brier_score={calibration['brier_score'].iloc[0]:.6f}")


if __name__ == "__main__":
    main()

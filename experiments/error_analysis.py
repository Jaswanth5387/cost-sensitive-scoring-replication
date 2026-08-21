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


def always_allow_row(y_true: np.ndarray, false_negative_cost: float | np.ndarray) -> dict:
    fraud_count = int(np.sum(y_true == 1))
    fraud = y_true == 1
    fn_cost = np.broadcast_to(false_negative_cost, y_true.shape)
    return {
        "policy": "always_allow",
        "threshold": np.nan,
        "blocked": 0,
        "false_positives": 0,
        "false_negatives": fraud_count,
        "true_positives": 0,
        "precision": 0.0,
        "recall": 0.0,
        "total_cost": float(np.sum(fn_cost[fraud])),
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


def score_distribution(y_true: np.ndarray, scores: np.ndarray) -> pd.DataFrame:
    rows = []
    for threshold in [0.04, 0.70]:
        fraud = y_true == 1
        above = scores >= threshold
        rows.append(
            {
                "threshold": threshold,
                "legit_at_or_above": int(np.sum(~fraud & above)),
                "fraud_at_or_above": int(np.sum(fraud & above)),
                "legit_below": int(np.sum(~fraud & ~above)),
                "fraud_below": int(np.sum(fraud & ~above)),
            }
        )
    return pd.DataFrame(rows)


def confusion_matrices(scored: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for threshold in [0.04, 0.70]:
        row = scored.loc[np.isclose(scored["threshold"], threshold)].iloc[0]
        rows.extend(
            [
                {
                    "threshold": threshold,
                    "action": "allow",
                    "actual_legit": int(row["true_negatives"]),
                    "actual_fraud": int(row["false_negatives"]),
                },
                {
                    "threshold": threshold,
                    "action": "block",
                    "actual_legit": int(row["false_positives"]),
                    "actual_fraud": int(row["true_positives"]),
                },
            ]
        )
    return pd.DataFrame(rows)


def compare_cost_models(economics: StripeEconomics, run: dict, thresholds: np.ndarray) -> pd.DataFrame:
    amount = run["x_test"]["Amount"].to_numpy()
    rows = []
    variants = [
        (
            "fixed_stripe_example",
            economics.legitimate_profit,
            economics.fraud_loss,
        ),
        (
            "amount_scaled",
            economics.amount_scaled_false_positive_cost(amount),
            economics.amount_scaled_false_negative_cost(amount),
        ),
    ]

    for name, fp_cost, fn_cost in variants:
        scored = score_thresholds(run["y_test"], run["scores"], thresholds, fp_cost, fn_cost)
        best = best_threshold(scored)
        stripe = scored.loc[np.isclose(scored["threshold"], 0.70)].iloc[0]
        rows.append(
            {
                "cost_model": name,
                "best_threshold": best["threshold"],
                "best_total_cost": best["total_cost"],
                "cost_at_0.70": stripe["total_cost"],
                "cost_reduction_vs_0.70": stripe["total_cost"] - best["total_cost"],
                "relative_cost_reduction_vs_0.70": (
                    (stripe["total_cost"] - best["total_cost"]) / stripe["total_cost"]
                ),
                "precision_at_best": best["precision"],
                "recall_at_best": best["recall"],
            }
        )
    return pd.DataFrame(rows)


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
    distribution = score_distribution(run["y_test"], run["scores"])
    matrices = confusion_matrices(scored)
    cost_models = compare_cost_models(economics, run, thresholds)

    Path("results").mkdir(exist_ok=True)
    baseline.to_csv("results/policy_comparison.csv", index=False)
    calibration.to_csv("results/calibration_bins.csv", index=False)
    distribution.to_csv("results/score_distribution.csv", index=False)
    matrices.to_csv("results/confusion_matrices.csv", index=False)
    cost_models.to_csv("results/cost_model_comparison.csv", index=False)

    print("policy_comparison=results/policy_comparison.csv")
    print("calibration_bins=results/calibration_bins.csv")
    print("score_distribution=results/score_distribution.csv")
    print("confusion_matrices=results/confusion_matrices.csv")
    print("cost_model_comparison=results/cost_model_comparison.csv")
    print(f"brier_score={calibration['brier_score'].iloc[0]:.6f}")


if __name__ == "__main__":
    main()

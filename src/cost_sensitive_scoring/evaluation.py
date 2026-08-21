from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ThresholdMetrics:
    threshold: float
    false_positives: int
    false_negatives: int
    true_positives: int
    true_negatives: int
    precision: float
    recall: float
    false_positive_rate: float
    total_cost: float


def score_thresholds(
    y_true: np.ndarray,
    y_score: np.ndarray,
    thresholds: np.ndarray,
    false_positive_cost: float | np.ndarray,
    false_negative_cost: float | np.ndarray,
) -> pd.DataFrame:
    rows = []
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score)
    fp_cost = np.broadcast_to(false_positive_cost, y_true.shape)
    fn_cost = np.broadcast_to(false_negative_cost, y_true.shape)

    for threshold in thresholds:
        blocked = y_score >= threshold
        fraud = y_true == 1

        tp = int(np.sum(blocked & fraud))
        fp = int(np.sum(blocked & ~fraud))
        fn = int(np.sum(~blocked & fraud))
        tn = int(np.sum(~blocked & ~fraud))

        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        fpr = fp / (fp + tn) if fp + tn else 0.0
        total_cost = float(np.sum(fp_cost[blocked & ~fraud]) + np.sum(fn_cost[~blocked & fraud]))

        rows.append(
            ThresholdMetrics(
                threshold=float(threshold),
                false_positives=fp,
                false_negatives=fn,
                true_positives=tp,
                true_negatives=tn,
                precision=precision,
                recall=recall,
                false_positive_rate=fpr,
                total_cost=total_cost,
            ).__dict__
        )

    return pd.DataFrame(rows)


def best_threshold(results: pd.DataFrame) -> pd.Series:
    return results.sort_values(["total_cost", "threshold"], ascending=[True, True]).iloc[0]

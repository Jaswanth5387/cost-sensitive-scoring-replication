import numpy as np

from cost_sensitive_scoring.evaluation import best_threshold, score_thresholds


def test_score_thresholds_counts_errors_and_costs() -> None:
    y_true = np.array([0, 0, 1, 1])
    y_score = np.array([0.1, 0.8, 0.4, 0.9])

    results = score_thresholds(
        y_true,
        y_score,
        thresholds=np.array([0.5]),
        false_positive_cost=2,
        false_negative_cost=10,
    )
    row = results.iloc[0]

    assert row["false_positives"] == 1
    assert row["false_negatives"] == 1
    assert row["true_positives"] == 1
    assert row["true_negatives"] == 1
    assert row["total_cost"] == 12


def test_score_thresholds_accepts_row_level_costs() -> None:
    y_true = np.array([0, 0, 1, 1])
    y_score = np.array([0.1, 0.8, 0.4, 0.9])

    results = score_thresholds(
        y_true,
        y_score,
        thresholds=np.array([0.5]),
        false_positive_cost=np.array([1, 20, 1, 1]),
        false_negative_cost=np.array([1, 1, 30, 1]),
    )
    row = results.iloc[0]

    assert row["false_positives"] == 1
    assert row["false_negatives"] == 1
    assert row["total_cost"] == 50


def test_best_threshold_picks_lowest_cost() -> None:
    y_true = np.array([0, 0, 1, 1])
    y_score = np.array([0.1, 0.8, 0.4, 0.9])

    results = score_thresholds(
        y_true,
        y_score,
        thresholds=np.array([0.3, 0.5, 0.95]),
        false_positive_cost=2,
        false_negative_cost=10,
    )

    assert best_threshold(results)["threshold"] == 0.3

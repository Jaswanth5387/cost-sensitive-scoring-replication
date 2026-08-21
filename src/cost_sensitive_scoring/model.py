from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split


def train_model(frame: pd.DataFrame, seed: int = 7) -> dict:
    x = frame.drop(columns=["Class"])
    y = frame["Class"].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        stratify=y,
        random_state=seed,
    )

    base = HistGradientBoostingClassifier(
        learning_rate=0.08,
        max_iter=120,
        l2_regularization=0.05,
        random_state=seed,
    )
    model = CalibratedClassifierCV(base, method="isotonic", cv=3)
    model.fit(x_train, y_train)

    scores = model.predict_proba(x_test)[:, 1]
    return {
        "model": model,
        "y_test": np.asarray(y_test),
        "scores": scores,
        "roc_auc": roc_auc_score(y_test, scores),
        "average_precision": average_precision_score(y_test, scores),
    }

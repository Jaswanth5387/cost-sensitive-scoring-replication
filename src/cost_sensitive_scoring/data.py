from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification


def load_creditcard_or_synthetic(path: Path, seed: int = 7) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)

    x, y = make_classification(
        n_samples=50000,
        n_features=30,
        n_informative=10,
        n_redundant=6,
        weights=[0.998, 0.002],
        flip_y=0.001,
        class_sep=2.0,
        random_state=seed,
    )
    frame = pd.DataFrame(x, columns=[f"V{i}" for i in range(1, 31)])
    frame["Amount"] = 26.0
    frame["Class"] = y
    return frame

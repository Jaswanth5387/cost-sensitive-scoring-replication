from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_threshold_cost(results_dir: Path, figures_dir: Path) -> None:
    frame = pd.read_csv(results_dir / "threshold_sweep.csv")
    best = frame.sort_values(["total_cost", "threshold"]).iloc[0]

    plt.figure(figsize=(8, 5))
    plt.plot(frame["threshold"], frame["total_cost"], linewidth=2)
    plt.axvline(0.70, color="tab:red", linestyle="--", label="Stripe example 0.70")
    plt.axvline(best["threshold"], color="tab:green", linestyle="--", label="Observed optimum")
    plt.xlabel("Threshold")
    plt.ylabel("Total cost")
    plt.title("Threshold vs cost")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "threshold_cost.png", dpi=180)
    plt.close()


def plot_sensitivity(results_dir: Path, figures_dir: Path) -> None:
    frame = pd.read_csv(results_dir / "sensitivity_analysis.csv")
    pivot = frame.pivot(
        index="false_negative_cost",
        columns="false_positive_cost",
        values="best_threshold",
    )

    plt.figure(figsize=(7, 5))
    image = plt.imshow(pivot.values, aspect="auto", origin="lower", cmap="viridis")
    plt.xticks(range(len(pivot.columns)), [str(x) for x in pivot.columns])
    plt.yticks(range(len(pivot.index)), [str(x) for x in pivot.index])
    plt.xlabel("False positive cost")
    plt.ylabel("False negative cost")
    plt.title("Cost-sensitive threshold by cost setting")
    plt.colorbar(image, label="Best threshold")
    plt.tight_layout()
    plt.savefig(figures_dir / "sensitivity_heatmap.png", dpi=180)
    plt.close()


def main() -> None:
    results_dir = Path("results")
    figures_dir = Path("figures")
    figures_dir.mkdir(exist_ok=True)
    plot_threshold_cost(results_dir, figures_dir)
    plot_sensitivity(results_dir, figures_dir)


if __name__ == "__main__":
    main()

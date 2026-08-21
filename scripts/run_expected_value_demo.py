from __future__ import annotations

from cost_sensitive_scoring import BinaryActionCosts, expected_value_gate


def main() -> None:
    costs = BinaryActionCosts(
        true_positive_value=100.0,
        false_positive_cost=25.0,
        action_cost=5.0,
    )
    probabilities = [0.05, 0.10, 0.20, 0.25, 0.40, 0.80]

    print("probability,expected_value,threshold,should_act")
    for probability in probabilities:
        result = expected_value_gate(probability, costs)
        print(
            f"{result.probability:.2f},"
            f"{result.expected_value:.2f},"
            f"{result.threshold:.2f},"
            f"{result.should_act}"
        )


if __name__ == "__main__":
    main()

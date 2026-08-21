from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BinaryActionCosts:
    true_positive_value: float
    false_positive_cost: float
    action_cost: float = 0.0

    def validate(self) -> None:
        if self.true_positive_value < 0:
            raise ValueError("true_positive_value must be non-negative")
        if self.false_positive_cost < 0:
            raise ValueError("false_positive_cost must be non-negative")
        if self.action_cost < 0:
            raise ValueError("action_cost must be non-negative")


@dataclass(frozen=True)
class DecisionResult:
    probability: float
    expected_value: float
    should_act: bool
    threshold: float


def action_threshold(costs: BinaryActionCosts) -> float:
    costs.validate()
    denominator = costs.true_positive_value + costs.false_positive_cost
    if denominator <= 0:
        raise ValueError("At least one of true_positive_value or false_positive_cost must be positive")
    return (costs.false_positive_cost + costs.action_cost) / denominator


def expected_value_gate(probability: float, costs: BinaryActionCosts) -> DecisionResult:
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between 0 and 1")

    threshold = action_threshold(costs)
    expected_value = (
        probability * costs.true_positive_value
        - (1 - probability) * costs.false_positive_cost
        - costs.action_cost
    )
    return DecisionResult(
        probability=probability,
        expected_value=expected_value,
        should_act=expected_value >= 0,
        threshold=threshold,
    )

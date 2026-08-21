import pytest

from cost_sensitive_scoring import BinaryActionCosts, expected_value_gate
from cost_sensitive_scoring.decision import action_threshold


def test_threshold_is_derived_from_costs() -> None:
    costs = BinaryActionCosts(true_positive_value=100, false_positive_cost=25, action_cost=0)

    assert action_threshold(costs) == pytest.approx(0.2)


def test_expected_value_gate_acts_when_ev_is_non_negative() -> None:
    costs = BinaryActionCosts(true_positive_value=100, false_positive_cost=25)

    below = expected_value_gate(0.19, costs)
    above = expected_value_gate(0.21, costs)

    assert below.should_act is False
    assert below.expected_value < 0
    assert above.should_act is True
    assert above.expected_value > 0


def test_action_cost_increases_threshold() -> None:
    no_action_cost = BinaryActionCosts(true_positive_value=100, false_positive_cost=25)
    with_action_cost = BinaryActionCosts(true_positive_value=100, false_positive_cost=25, action_cost=10)

    assert action_threshold(with_action_cost) > action_threshold(no_action_cost)


def test_probability_validation() -> None:
    costs = BinaryActionCosts(true_positive_value=100, false_positive_cost=25)

    with pytest.raises(ValueError, match="probability"):
        expected_value_gate(1.2, costs)

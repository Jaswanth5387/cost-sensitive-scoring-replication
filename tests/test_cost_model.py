import numpy as np

from cost_sensitive_scoring.cost_model import StripeEconomics


def test_stripe_economics_match_source_example() -> None:
    economics = StripeEconomics()

    assert round(economics.legitimate_profit, 2) == 2.08
    assert round(economics.product_cost, 2) == 23.92
    assert round(economics.fraud_loss, 2) == 38.92
    assert round(economics.fraud_to_legit_ratio, 2) == 18.71
    assert round(economics.break_even_precision, 4) == 0.0507


def test_amount_scaled_costs_match_source_at_average_sale() -> None:
    economics = StripeEconomics()
    amount = np.array([26.0])

    assert round(economics.amount_scaled_false_positive_cost(amount)[0], 2) == 2.08
    assert round(economics.amount_scaled_false_negative_cost(amount)[0], 2) == 38.92

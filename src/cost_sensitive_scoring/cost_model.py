from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StripeEconomics:
    average_sale: float = 26.0
    margin: float = 0.08
    chargeback_fee: float = 15.0

    @property
    def legitimate_profit(self) -> float:
        return self.average_sale * self.margin

    @property
    def product_cost(self) -> float:
        return self.average_sale - self.legitimate_profit

    @property
    def fraud_loss(self) -> float:
        return self.product_cost + self.chargeback_fee

    @property
    def fraud_to_legit_ratio(self) -> float:
        return self.fraud_loss / self.legitimate_profit

    @property
    def break_even_precision(self) -> float:
        return 1 / (1 + self.fraud_to_legit_ratio)

    def amount_scaled_false_positive_cost(self, amount: np.ndarray) -> np.ndarray:
        return np.asarray(amount) * self.margin

    def amount_scaled_false_negative_cost(self, amount: np.ndarray) -> np.ndarray:
        return np.asarray(amount) * (1 - self.margin) + self.chargeback_fee

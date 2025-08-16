from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class ModelTotals:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    total_tokens: int = 0
    cost_usd: Decimal = Decimal("0.0")


@dataclass
class Totals:
    per_model: Dict[str, ModelTotals] = field(default_factory=dict)

    @property
    def cost_usd(self) -> Decimal:
        return sum(m.cost_usd for m in self.per_model.values())

    @property
    def input_tokens(self) -> int:
        return sum(m.input_tokens for m in self.per_model.values())

    @property
    def cached_tokens(self) -> int:
        return sum(m.cached_tokens for m in self.per_model.values())

    @property
    def output_tokens(self) -> int:
        return sum(m.output_tokens for m in self.per_model.values())

    @property
    def total_tokens(self) -> int:
        return sum(m.total_tokens for m in self.per_model.values())



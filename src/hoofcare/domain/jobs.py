from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal, ROUND_HALF_UP


def _text(name: str, value: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be text")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} must be non-empty")
    return normalized


@dataclass(frozen=True)
class MaterialRate:
    code: str
    label: str
    unit: str
    unit_price_grosz: int
    quantity_scale: int
    job_local: bool = False
    active: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _text("material code", self.code))
        object.__setattr__(self, "label", _text("material label", self.label))
        object.__setattr__(self, "unit", _text("material unit", self.unit))
        if type(self.unit_price_grosz) is not int or self.unit_price_grosz < 0:
            raise ValueError("unit price must be non-negative integer grosze")
        if type(self.quantity_scale) is not int or self.quantity_scale not in range(4):
            raise ValueError("quantity scale must be between zero and three")
        if type(self.job_local) is not bool:
            raise ValueError("job_local must be boolean")
        if type(self.active) is not bool:
            raise ValueError("active must be boolean")

    def normalize_quantity(self, quantity: Decimal) -> Decimal:
        if (
            not isinstance(quantity, Decimal)
            or not quantity.is_finite()
            or quantity <= 0
        ):
            raise ValueError("quantity must be a positive finite Decimal")
        quantum = Decimal(1).scaleb(-self.quantity_scale)
        normalized = quantity.quantize(quantum)
        if normalized != quantity:
            raise ValueError("quantity exceeds material precision")
        return normalized

    def line_total_grosz(self, quantity: Decimal) -> int:
        normalized = self.normalize_quantity(quantity)
        amount = normalized * Decimal(self.unit_price_grosz)
        return int(amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class JobPricingSnapshot:
    cow_unit_price_grosz: int
    additional_materials: tuple[MaterialRate, ...]

    def __post_init__(self) -> None:
        if type(self.cow_unit_price_grosz) is not int or self.cow_unit_price_grosz < 0:
            raise ValueError("cow price must be non-negative integer grosze")
        if not isinstance(self.additional_materials, tuple):
            raise ValueError("additional materials must be an immutable tuple")
        if any(not isinstance(rate, MaterialRate) for rate in self.additional_materials):
            raise ValueError("additional materials must contain MaterialRate values")
        codes = tuple(rate.code for rate in self.additional_materials)
        if len(codes) != len(set(codes)):
            raise ValueError("material codes must be unique within job pricing")
        if any(not rate.active for rate in self.additional_materials):
            raise ValueError("job pricing accepts only active materials")

    def cow_subtotal_grosz(self, completed_cows: int) -> int:
        if type(completed_cows) is not int or completed_cows < 0:
            raise ValueError("completed cows must be a non-negative integer")
        return completed_cows * self.cow_unit_price_grosz

    def rate(self, code: str) -> MaterialRate:
        normalized_code = _text("material code", code)
        for item in self.additional_materials:
            if item.code == normalized_code:
                return item
        raise KeyError(normalized_code)

    def with_local_material(self, rate: MaterialRate) -> "JobPricingSnapshot":
        if not isinstance(rate, MaterialRate) or not rate.job_local or not rate.active:
            raise ValueError("job-local extension requires an active job_local material")
        return replace(
            self,
            additional_materials=self.additional_materials + (rate,),
        )

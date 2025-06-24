from decimal import Decimal

from dataclasses import dataclass
from enum import Enum

### # # ###

@dataclass(frozen=True)
class Principal:
    value: Decimal

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"Principal cannot be negative: {self.value}")

@dataclass(frozen=True)
class RatePercent:
    value: Decimal # 5.0 means 5%

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"RatePercent cannot be negative: {self.value}")

        if self.value > 100:
            raise ValueError(f"RatePercent cannot be more than 100: {self.value}")

@dataclass(frozen=True)
class Years:
    value: Decimal

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"Years cannot be negative: {self.value}")

class Compound(Enum):
    ANNUAL = 1
    SEMIANNUAL = 2
    QUARTERLY = 4
    MONTHLY = 12

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

### # # ###

from decimal import Decimal

from compbolt import (
    Principal,
    RatePercent,
    Years,
    Compound,

    calculate_compound_interest
)

### # # ###

result = calculate_compound_interest(
    principal=Principal(Decimal('1000')),
    rate_percent=RatePercent(Decimal('5.0')),
    years=Years(Decimal('2')),
    compound=Compound.ANNUAL
)

print(result)

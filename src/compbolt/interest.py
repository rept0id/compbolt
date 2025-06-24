from decimal import Decimal, getcontext
from .types import Principal, RatePercent, Years, Compound

### # # ###

def calculate_compound_interest(
    *,
    principal: Principal,
    rate_percent: RatePercent,
    years: Years,
    compound: Compound
) -> Decimal:
    if not isinstance(principal, Principal):
        raise TypeError(f"Expected Principal, got {type(principal).__name__}")
    if not isinstance(rate_percent, RatePercent):
        raise TypeError(f"Expected RatePercent, got {type(rate_percent).__name__}")
    if not isinstance(years, Years):
        raise TypeError(f"Expected Years, got {type(years).__name__}")
    if not isinstance(compound, Compound):
        raise TypeError(f"Expected Compound, got {type(compound).__name__}")

    ### # # ###

    rate_dec = rate_percent.value / Decimal('100')

    ### # # ###

    P = principal.value
    r = rate_dec
    t = years.value
    n = Decimal(compound.value)

    ### # # ###

    A = P * ((Decimal('1') + r/n) ** (n * t))

    ### # # ###

    return A

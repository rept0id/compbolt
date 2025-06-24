import pytest

from decimal import Decimal

from compbolt import (
    Principal,
    RatePercent,
    Years,
    Compound,

    calculate_compound_interest
)

### # # ###

DEF_PRINCIPAL = Principal(Decimal('1000'))
DEF_RATE_PERCENT = RatePercent(Decimal('5.0'))
DEF_YEARS = Years(Decimal('2'))
DEF_COMPOUND = Compound.ANNUAL

### # # ###

def test():
    result = calculate_compound_interest(
        principal=DEF_PRINCIPAL,
        rate_percent=DEF_RATE_PERCENT,
        years=DEF_YEARS,
        compound=DEF_COMPOUND
    )

    expected = Decimal('1102.5')

    assert round(result, 9) == round(expected, 9)

# principal

def test_principal_wrong_type():
    with pytest.raises(TypeError, match="Expected Principal"):
        calculate_compound_interest(
            principal=DEF_RATE_PERCENT, # intentional type mistake
            rate_percent=DEF_RATE_PERCENT,
            years=DEF_YEARS,
            compound=DEF_COMPOUND
        )

@pytest.mark.parametrize(
    "principal_dec",
    [
        Decimal("-774189"),
        Decimal("-1"),
        Decimal("-0.1"),
    ]
)

def test_principal_negative(principal_dec):
    with pytest.raises(ValueError, match="Principal cannot be negative"):
        calculate_compound_interest(
            principal=Principal(principal_dec),
            rate_percent=DEF_RATE_PERCENT,
            years=DEF_YEARS,
            compound=DEF_COMPOUND
        )

def test_principal_zero():
    result = calculate_compound_interest(
        principal=Principal(Decimal('0')),
        rate_percent=DEF_RATE_PERCENT,
        years=DEF_YEARS,
        compound=DEF_COMPOUND
    )

    expected = Decimal('0')

    assert round(result, 9) == round(expected, 9)

@pytest.mark.parametrize(
    "principal, expected",
    [
        (
            Principal(Decimal("0.1")),
            Decimal("0.11025")
        ),
        (
            Principal(Decimal("1")),
            Decimal("1.1025")
        ),
        (
            Principal(Decimal("376882")),
            Decimal("415512.405")
        )
    ]
)
def test_principal(principal, expected):
    result = calculate_compound_interest(
        principal=principal,
        rate_percent=DEF_RATE_PERCENT,
        years=DEF_YEARS,
        compound=DEF_COMPOUND
    )

    assert round(result, 9) == round(expected, 9)

# rate percent

def test_rate_percent_wrong_type():
    with pytest.raises(TypeError, match="Expected Principal"):
        calculate_compound_interest(
            principal=DEF_PRINCIPAL,
            rate_percent=DEF_PRINCIPAL, # intentional type mistake
            years=DEF_YEARS,
            compound=DEF_COMPOUND
        )

def test_rate_percent_negative():
    with pytest.raises(ValueError, match="RatePercent cannot be negative"):
        calculate_compound_interest(
            principal=DEF_PRINCIPAL,
            rate_percent=RatePercent(Decimal('-2.0')),
            years=DEF_YEARS,
            compound=DEF_COMPOUND
        )

def test_rate_percent_zero():
    result = calculate_compound_interest(
        principal=DEF_PRINCIPAL,
        rate_percent=RatePercent(Decimal('0.0')),
        years=DEF_YEARS,
        compound=DEF_COMPOUND
    )

    expected = DEF_PRINCIPAL.value

    assert round(result, 9) == round(expected, 9)

def test_rate_percent():
    result = calculate_compound_interest(
        principal=DEF_PRINCIPAL,
        rate_percent=RatePercent(Decimal('48.0')),
        years=DEF_YEARS,
        compound=DEF_COMPOUND
    )

    expected = Decimal('2190.4')

    assert round(result, 9) == round(expected, 9)

def test_rate_percent_100():
    result = calculate_compound_interest(
        principal=DEF_PRINCIPAL,
        rate_percent=RatePercent(Decimal('100.0')),
        years=DEF_YEARS,
        compound=DEF_COMPOUND
    )

    expected = Decimal('4000')

    assert round(result, 9) == round(expected, 9)

@pytest.mark.parametrize(
    "rate_percent_dec",
    [
        Decimal("100.1"),
        Decimal("101"),
        Decimal("570971")
    ]
)
def test_rate_percent_more_than_100(rate_percent_dec):
    with pytest.raises(ValueError, match="RatePercent cannot be more than 100"):
        calculate_compound_interest(
            principal=DEF_PRINCIPAL,
            rate_percent=RatePercent(rate_percent_dec),
            years=DEF_YEARS,
            compound=DEF_COMPOUND
        )

# years

def test_years_wrong_type():
    with pytest.raises(TypeError, match="Expected Principal"):
        calculate_compound_interest(
            principal=DEF_PRINCIPAL,
            rate_percent=DEF_PRINCIPAL, # intentional type mistake
            years=DEF_YEARS,
            compound=DEF_COMPOUND
        )

def test_years_negative():
    with pytest.raises(ValueError, match="Years cannot be negative"):
        calculate_compound_interest(
            principal=DEF_PRINCIPAL,
            rate_percent=DEF_RATE_PERCENT,
            years=Years(Decimal('-0.1')),
            compound=DEF_COMPOUND
        )

def test_years_zero():
    result = calculate_compound_interest(
        principal=DEF_PRINCIPAL,
        rate_percent=DEF_RATE_PERCENT,
        years=Years(Decimal('0')),
        compound=DEF_COMPOUND
    )

    expected = DEF_PRINCIPAL.value

    assert round(result, 9) == round(expected, 9)

def test_years():
    result = calculate_compound_interest(
        principal=DEF_PRINCIPAL,
        rate_percent=DEF_RATE_PERCENT,
        years=Years(Decimal('20')),
        compound=Compound.ANNUAL
    )

    expected = Decimal('2653.297705144')

    assert round(result, 9) == round(expected, 9)

# compound

@pytest.mark.parametrize(
    "compound, expected",
    [
        (
            Compound.ANNUAL,
            Decimal("1102.5")
        ),
        (
            Compound.SEMIANNUAL,
            Decimal("1103.812890625")
        ),
        (
            Compound.QUARTERLY,
            Decimal("1104.486101181")
        ),
        (
            Compound.MONTHLY,
            Decimal("1104.941335558")
        )
    ]
)
def test_compound(compound, expected):
    result = calculate_compound_interest(
        principal=DEF_PRINCIPAL,
        rate_percent=DEF_RATE_PERCENT,
        years=DEF_YEARS,
        compound=compound
    )

    assert round(result, 9) == round(expected, 9)

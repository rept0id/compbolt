import pytest

from decimal import Decimal

from compbolt import (
    Principal,
    RatePercent,
    Years
)

### # # ###

# principal

@pytest.mark.parametrize(
    "principal_dec",
    [
        Decimal("-768543"),
        Decimal("-1"),
        Decimal("-0.1")
    ]
)
def test_principal_negative(principal_dec):
    with pytest.raises(ValueError, match="Principal cannot be negative"):
        Principal(principal_dec)

def test_principal_zero():
    Principal(Decimal(0))

@pytest.mark.parametrize(
    "principal_dec",
    [
        Decimal("0.1"),
        Decimal("1"),
        Decimal("260337")
    ]
)
def test_principal(principal_dec):
    Principal(principal_dec)

# rate percent

@pytest.mark.parametrize(
    "rate_percent_dec",
    [
        Decimal("-838110"),
        Decimal("-1"),
        Decimal("-0.1")
    ]
)
def test_rate_percent_negative(rate_percent_dec):
    with pytest.raises(ValueError, match="RatePercent cannot be negative"):
        RatePercent(rate_percent_dec)

def test_rate_percent_zero():
    RatePercent(Decimal(0))

@pytest.mark.parametrize(
    "rate_percent_dec",
    [
        Decimal("0.1"),
        Decimal("1"),
        Decimal("42.42")
    ],
)
def test_rate_percent(rate_percent_dec):
    RatePercent(rate_percent_dec)

@pytest.mark.parametrize(
    "rate_precent_dec",
    [
        Decimal("100.1"),
        Decimal("101"),
        Decimal("426825")
    ]
)
def test_rate_percent_more_than_100(rate_precent_dec):
    with pytest.raises(ValueError, match="RatePercent cannot be more than 100"):
        RatePercent(rate_precent_dec)

# years

@pytest.mark.parametrize(
    "years_dec",
    [
        Decimal("-119122"),
        Decimal("-1"),
        Decimal("-0.1")
    ]
)
def test_years_negative(years_dec):
    with pytest.raises(ValueError, match="Years cannot be negative"):
        Years(years_dec)

def test_years_zero():
    Years(Decimal(0))

@pytest.mark.parametrize(
    "years_dec",
    [
        Decimal("0.1"),
        Decimal("1"),
        Decimal("758663")
    ]
)
def test_years(years_dec):
    Years(years_dec)

# compbolt

compbolt is an extremely stable and hard to misuse library. The functionality of this library is to calculate compounded interest, but the real purpose is to test Matt's Godbolt suggestions from "[Correct by Construction: APIs That Are Easy to Use and Hard to Misuse - Matt Godbolt - C++ on sea](https://www.youtube.com/watch?v=nLSm3Haxz0I)" on a higher level language.

Matt gives as an example a trading API, that is implemented in C++. In reality, many economical APIs are made in Python as well, so we picked Python as our high level language.

His ideas are :

1. Tinytypes enforce clarity (and protect the caller)

Tinytypes is a concept of making a distinct types even for simple -but important- values instead of doing only for complex structures. Simple but important values, meaning for example: `price`, `quantity`... values that are usually closeby as functions arguments and are easy to be flipped by mistake.

The main thing we try to avoid is :
```python
def buy(price, quantity):
  # ...

sell(1, 10000) # ooops ! We sold 10000 stocks for 1 buck !
sell(10000, 1) # Correct, we sold 1 stock for 10000 bucks
```

Before we go to a tinytypes example in Python, we need to mention that Python, in contrast to C++, does something to help to enforce clarity - but there is still potential into using tinytypes.

What Python does apart from tinytypes to address the issue, is that it allows for a function to enforce calling it with each parameters name. This happens if you put a '*' as first parameter.

```python
def buy(*, price, quantity):
  # ...

sell(1, 10000) # won't work, will throw TypeError - good, because it saved us from making a mistake
sell(price=10000, quantity=1) # will work, it's correct and it's harder to make a mistake
```

The problem with `*` is, that given a number of functions that the one passes to the other a fixed set of values, the number of functions that do use the `*` feature decreases and the possibilities of logical mistakes like flipping values by increases because of complexity, even if it's theoretically visible by the human eye that `sell(price=1, quantity=10000)` is wrong - let alone the case that high-order functions that pass data dynamically may do exist. 

Tinytypes enforce clarity through the whole data flow and the whole codebase and will throw errors in case of logical mistakes, in contrast to the `*` feature that does this per function and will fail silently in case of logical mistakes. Still, nothing stops the case of doing a mistake like `sell(price=Price(Decimal("10000"), quantity=Quantity(Decimal("1"))` (we assume that selling 10000 stocks for 1 buck is a mistake in all of our examples), but tinytypes can bring more safety from the statically-checked world to important APIs in dynamically typed languages.

Apart from this concept, in case of Python, tinytypes can also improve the domain-specific logic. For example, instead of checking in every function if `RatePercentage` is bigger than 100 (we assume it's mistake percentage to be bigger than 100), we just make a `RatePercentage` type that includes this check.

An example of tinytypes follows below: 

```python
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

### # # ###

def calculate_compound_interest_anually(
    *,
    principal: Principal,
    rate_percent: RatePercent,
    years: Years
) -> Decimal:
    if not isinstance(principal, Principal):
        raise TypeError(f"Expected Principal, got {type(principal).__name__}")
    if not isinstance(rate_percent, RatePercent):
        raise TypeError(f"Expected RatePercent, got {type(rate_percent).__name__}")
    if not isinstance(years, Years):
        raise TypeError(f"Expected Years, got {type(years).__name__}")

    ### # # ###

    rate_dec = rate_percent.value / Decimal('100')

    ### # # ###

    P = principal.value
    r = rate_dec
    t = years.value
    n = 1

    ### # # ###

    A = P * ((Decimal('1') + r/n) ** (n * t))

    ### # # ###

    return A

### # # ###

result = calculate_compound_interest_anually(
    principal=Principal(Decimal('1000')),
    rate_percent=RatePercent(Decimal('5.0')),
    years=Years(Decimal('2'))
)

print(result)
```

2. Enums everywhere
  

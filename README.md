# compbolt

Compbolt is library with a stable and hard to misuse API.

The functionality of this library is to calculate compounded interest... but the real purpose is to test Matt Godbolt's suggestions from "[Correct by Construction: APIs That Are Easy to Use and Hard to Misuse - Matt Godbolt - C++ on sea](https://www.youtube.com/watch?v=nLSm3Haxz0I)" on a high-level language.

Matt gives us the example of a stocks trading API that is implemented in C++. Because we wanted to test what we saw there on a high-level language, we picked Python.

## Concepts

### 1. Tinytypes enforce clarity (and protect the caller)

Tinytypes are a concept for creating distinct types even for simple -but important- values, instead of utilizing types only for complex structures. `Price` and `Quantity`, for example, are not values that you want to put the one in the place of the other, so the more hard is to do this, the better.

The main thing we try to avoid is :
```python
def sell(price, quantity):
  # ...

sell(1, 10000) # ooops ! We sold 10000 stocks for 1 buck !
sell(10000, 1) # Correct, we sold 1 stock for 10000 bucks
```

Before we go to a tinytypes example in Python, we need to mention that Python, in contrast to C++, does something to help to enforce clarity - but hold on after this, because there is still good potential into using tinytypes.

What Python does to address the exact issue, without tinytypes, is that it allows for a function to enforce calling it only with the names provided for each parameter.
For example :
```python
def sell(*, price, quantity):
  # ...

sell(1, 10000) # won't work, will throw TypeError - good, because it protects us
sell(price=10000, quantity=1) # will work, it's correct + it's harder to make a mistake
```

The problem with the `*` solution is that you don't get any error. Yes, it helps the programer to see better what he is doing, but still, if someone mistakes the one for the other, nothing will stop this from running. 

Given a complex data flow, a big number of functions and the existence of high-order functions, you need something that not only it makes it visible to your eyes that it's wrong but... that it will stop you as well if you make a mistake. With tinytypes, if you pass a value of type `Quantity` where `Price` is expected, you will get an error.

Tinytypes can also improve domain-specific logic. Instead of checking in each function that you expect a `Price` if the value is negative, tinytypes offer the option to centralize this and just make the tinytype check it's self. This way, wherever you expect a parameter of type `Price`, you can be sure that it won't be negative. (This could be called... tiny-OOP and it's just an extra, that's not the best of tinytypes.)

`Price` as a tinytype would simply look like this :
```
@dataclass(frozen=True)
class Price:
    value: Decimal

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"Price cannot be negative: {self.value}")
```

A full example of tinytypes follows below: 

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

### 2. Enums everywhere

Another clarity concept.

There are times that instead of waiting for a number, someone needs a specific set of numbers.

For example, for compound, only the numbers : 
 - 1 for annualy
 - 2 for semi-anually
 - 4 for quartely and
 - 12 for monthly

Anything else, in the context of our example, is a bad idea, specially 365 for daily or 52 for weekly, they both can be tricky, since they change according to the year.

Let's say now that we want to express this with code. One way is to make our function to check, once it's called, that the compound is one of the numbers that we like. But this way, the caller doesn't know this, and will get an error message (?) without knowning that it was not allowed to put 365 for compound but only 1,2,4 or 12.

With enums, we can express this in our code and exclude weekly and daily in a very cool way.

```python
class Compound(Enum):
    ANNUAL = 1
    SEMIANNUAL = 2
    QUARTERLY = 4
    MONTHLY = 12
```

Now, our function makes it clear what compound we are waiting for.
```python
def calculate_compound_interest(
    *,
    principal: Principal,
    rate_percent: RatePercent,
    years: Years,
    compound: Compound # <--- here
) -> Decimal:
    if not isinstance(principal, Principal):
        raise TypeError(f"Expected Principal, got {type(principal).__name__}")
    if not isinstance(rate_percent, RatePercent):
        raise TypeError(f"Expected RatePercent, got {type(rate_percent).__name__}")
    if not isinstance(years, Years):
        raise TypeError(f"Expected Years, got {type(years).__name__}")
    if not isinstance(compound, Compound): # <--- and here
        raise TypeError(f"Expected Compound, got {type(compound).__name__}")

    # ...
```

Now, our function makes it clear what are the options.
```python
calculate_compound_interest_anually(
    principal=Principal(Decimal('1000')),
    rate_percent=RatePercent(Decimal('5.0')),
    years=Years(Decimal('2')),
    compound=Compound.ANNUAL
)
```

Enums can also be used for better state management. Instead of states existing magically in our code, we can have an enum that specifies each state. This, not only makes our work more reliable, but adds to better readability and maintainability.


## Other concepts from Matt Godbolt

#### 1. RAII
RAII stands for "Resource Acquisition Is Initialization". 

In the context of higher level and garbage collected programing languages is not needed. 

Matt gives a more self-explanatory terms for this, "Constructor acquires, destructor releases". It's all about how you can free memory in a more streamlined way instead of throwing memory allocations everywhere and then based on your understanding of your code to free them. 

With this methodology, when you create an object (since he is talking about C++) you acquire memory and when you destroy it you free memory. 

A nice abstraction over memory management.

## How to test

```
pytest
```

## How to use 

```
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
```

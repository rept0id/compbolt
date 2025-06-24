# compbolt

compbolt is an extremely stable and hard to misuse library. The functionality of this library is to calculate compounded interest, but the real purpose is to test Matt's Godbolt suggestions from "[Correct by Construction: APIs That Are Easy to Use and Hard to Misuse - Matt Godbolt - C++ on sea](https://www.youtube.com/watch?v=nLSm3Haxz0I)" on a higher level language.

Matt gives as an example a trading API, that is implemented in C++. In reality, many economical APIs are made in Python as well, so we picked Python as our high level language.

His ideas are :

1. Tinytypes enforce clarity at the caller's side

Tinytypes is a concept of making a distinct type even simple but important values, for example: `price`, `quantity`. Values that are usually closeby as functions arguments and are easy to be flipped by mistake.

The main thing we try to avoid is :
```python
def buy(price, quantity):
  # ...

sell(1, 10000) # ooops ! We sold 10000 stocks for 1 buck !
sell(10000, 1) # Correct, we sold 1 stock for 10000 bucks
```

Before we go to a tinytypes example in Python, we need to mention that Python, in contrast to C++, does something to help to enforce clarity - but there is still potential into using tinytypes.

What Python does to address the issue, is that it allows for a function to enforce calling it with each parameters name. This happens if you put a '*' as first parameter.

```python
def buy(*, price, quantity):
  # ...

sell(1, 10000) # won't work, will throw TypeError - good, because it saved us from making a mistake
sell(price=10000, quantity=1) # will work, it's correct and it's harder to make a mistake
```

import pytest
from solutions.CHK import checkout_solution


@pytest.mark.parametrize("skus,price", [
    ("A", 50),
    ("B", 30),
    ("C", 20),
    ("", 0),
    ("AA", 100),
    ("ABC", 100),
    ("ABA", 130),
    ("AAA", 130),
    ("BB", 45),
    ("ABABA", 130 + 45),
    ("AACA", 130 + 20),
])
def test_checkout(skus, price):
    assert checkout_solution.checkout(skus) == price


@pytest.mark.parametrize("skus", [
    "Z",
    11,
])
def test_when_illegal_input_then_returns_minus_one(skus):
    assert checkout_solution.checkout(skus) == -1


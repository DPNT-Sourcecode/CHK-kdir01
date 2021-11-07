import pytest
from solutions.CHK import checkout_solution


@pytest.mark.parametrize("skus,price", [
    ("A", 50),
    ("B", 30),
    ("C", 20),
    ("", 0),
])
def test_checkout(skus, price):
    assert checkout_solution.checkout(skus) == price

import pytest
from solutions.CHK import checkout_solution


@pytest.mark.parametrize("skus,price", [
    ("A", 50),
    ("B", 30),
    ("C", 20),
    ("D", 15),
    ("E", 40),
    ("", 0),
    ("AA", 100),
    ("ABC", 100),
    ("ABA", 130),
    ("AAA", 130),
    ("BB", 45),
    ("ABABA", 130 + 45),
    ("AACA", 130 + 20),
    ("BBBB", 45 * 2),
    ("BBCBB", 45 * 2 + 20),
    ("AAAAA", 200)
])
def test_checkout(skus, price):
    assert checkout_solution.checkout(skus) == price


@pytest.mark.parametrize("skus", [
    "Z",
    11,
])
def test_when_illegal_input_then_returns_minus_one(skus):
    assert checkout_solution.checkout(skus) == -1


def test_offers_sorted_by_most_valuable():
    least_valuable = checkout_solution.PurchaseOption(sku="A", quantity=3, price=3 * 20)
    most_valuable = checkout_solution.PurchaseOption(sku="A", quantity=2, price=2 * 10)
    middle_valuable = checkout_solution.PurchaseOption(sku="A", quantity=4, price=4 * 15)

    checkout = checkout_solution.Checkout([
        checkout_solution.PurchaseOption(sku="A", quantity=1, price=100),
        least_valuable,
        most_valuable,
        middle_valuable,
    ])

    assert checkout.offers_by_sku["A"] == [most_valuable, middle_valuable, least_valuable]


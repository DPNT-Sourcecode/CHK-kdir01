import pytest
from solutions.CHK.checkout_solution import Checkout, PurchaseOption

TEST_PURCHASE_OPTIONS = [
    PurchaseOption(sku="A", quantity=1, price=50, freebies=()),
    PurchaseOption(sku="A", quantity=3, price=130, freebies=()),
    PurchaseOption(sku="A", quantity=5, price=200, freebies=()),
    PurchaseOption(sku="B", quantity=1, price=30, freebies=()),
    PurchaseOption(sku="B", quantity=2, price=45, freebies=()),
    PurchaseOption(sku="C", quantity=1, price=20, freebies=()),
    PurchaseOption(sku="D", quantity=1, price=15, freebies=()),
    PurchaseOption(sku="E", quantity=1, price=40, freebies=()),
    PurchaseOption(sku="E", quantity=2, price=80, freebies=tuple("B")),
    PurchaseOption(sku="F", quantity=1, price=10, freebies=()),
    PurchaseOption(sku="F", quantity=3, price=20, freebies=())
]


@pytest.fixture
def checkout():
    return Checkout(TEST_PURCHASE_OPTIONS)


@pytest.mark.parametrize("skus,price", [
    ("A", 50),
    ("B", 30),
    ("C", 20),
    ("D", 15),
    ("E", 40),
    ("F", 10),
    ("", 0),
    ("AA", 100),
    ("ABC", 100),
    ("ABA", 130),
    ("AAA", 130),
    ("BB", 45),
    ("FFF", 20),
    ("FF", 20),
    ("ABABA", 130 + 45),
    ("AACA", 130 + 20),
    ("BBBB", 45 * 2),
    ("BBCBB", 45 * 2 + 20),
    ("AAAAA", 200),
    ("AAA" + "AAAAA", 130 + 200),
    ("AAA" + "AAAAA" + "A", 130 + 200 + 50),
    ("EE", 80),
    ("EEB", 80),
    ("BEE", 80),
    ("EBE", 80),
    ("AAAAAEEAAABC", 200 + 80 + 130 + 20),
    ("AAAAAEEAAAC", 200 + 80 + 130 + 20),
])
def test_checkout(checkout, skus, price):
    assert checkout.checkout(skus) == price


@pytest.mark.parametrize("skus", [
    "Z*",
    11,
])
def test_when_illegal_input_then_returns_minus_one(checkout, skus):
    assert checkout.checkout(skus) == -1


def test_offers_sorted_by_most_valuable():
    least_valuable = PurchaseOption(sku="A", quantity=3, price=3 * 20, freebies=())
    most_valuable = PurchaseOption(sku="A", quantity=2, price=2 * 10, freebies=())
    middle_valuable = PurchaseOption(sku="A", quantity=4, price=4 * 15, freebies=())

    checkout = Checkout([
        PurchaseOption(sku="A", quantity=1, price=100, freebies=()),
        least_valuable,
        most_valuable,
        middle_valuable,
    ])

    assert checkout.offers_from_best_by_sku["A"] == [most_valuable, middle_valuable, least_valuable]


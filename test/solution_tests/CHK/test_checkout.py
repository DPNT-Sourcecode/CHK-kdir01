import pytest
from solutions.CHK.checkout_solution import Checkout, PurchaseOption

TEST_PURCHASE_OPTIONS = [
    PurchaseOption(sku="A", quantity=1, price=50),
    PurchaseOption(sku="A", quantity=3, price=130),
    PurchaseOption(sku="A", quantity=5, price=200),
    PurchaseOption(sku="B", quantity=1, price=30),
    PurchaseOption(sku="B", quantity=2, price=45),
    PurchaseOption(sku="C", quantity=1, price=20),
    PurchaseOption(sku="D", quantity=1, price=15),
    PurchaseOption(sku="E", quantity=1, price=40),
    PurchaseOption(sku="E", quantity=2, price=80, freebies="B"),
    PurchaseOption(sku="F", quantity=1, price=10),
    PurchaseOption(sku="F", quantity=3, price=20),
    PurchaseOption(sku="G", quantity=1, price=10),
    PurchaseOption(sku="G", quantity=2, price=20, freebies="BB"),
]


@pytest.fixture
def default_checkout():
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
    ("G", 10),
    ("GGBB", 20),
])
def test_checkout(default_checkout, skus, price):
    assert default_checkout.checkout(skus) == price


@pytest.mark.parametrize("skus", [
    "Z*",
    11,
])
def test_when_illegal_input_then_returns_minus_one(default_checkout, skus):
    assert default_checkout.checkout(skus) == -1


def test_offers_sorted_by_most_valuable():
    least_valuable = PurchaseOption(sku="A", quantity=3, price=3 * 20)
    most_valuable = PurchaseOption(sku="A", quantity=2, price=2 * 10)
    middle_valuable = PurchaseOption(sku="A", quantity=4, price=4 * 15)

    checkout = Checkout([
        PurchaseOption(sku="A", quantity=1, price=100),
        least_valuable,
        most_valuable,
        middle_valuable,
    ])

    assert checkout.offers_from_best_by_sku["A"] == [most_valuable, middle_valuable, least_valuable]


def test_creation_of_combi_purchase_options():
    skus = "XYZ"
    price = 100
    quantity = 4

    pos = PurchaseOption.create_combi_purchase_options(skus, quantity, price)

    assert len(pos) == 15  # One can check there are 15 options

    for po in pos:
        assert po.price == price
        assert po.sku in skus
        assert po.quantity + len(po.freebies) == quantity
        for freebie in po.freebies:
            assert freebie in skus



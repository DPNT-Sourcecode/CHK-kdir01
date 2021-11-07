from collections import Counter, namedtuple

SKU_PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}

OfferInfo = namedtuple("OfferInfo", ["sku", "quantity", "price"])

OFFERS = [
    OfferInfo(sku="A", quantity=3, price=130),
    OfferInfo(sku="B", quantity=2, price=45)
]


class Checkout:

    ERROR_RETURN_CODE = -1

    def __init__(self, prices, offers):
        self.prices = prices
        self.offers = offers

    def checkout(self, skus: str) -> int:
        if type(skus) != str:
            return self.ERROR_RETURN_CODE

        sku_count = Counter(skus)

        for sku in sku_count:
            if sku not in self.prices:
                return self.ERROR_RETURN_CODE

        prices = [self.prices[sku] * count for sku, count in sku_count.items()]

        return sum(prices)


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    return Checkout(SKU_PRICES, OFFERS).checkout(skus)



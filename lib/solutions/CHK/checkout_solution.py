from collections import Counter, namedtuple
from typing import Dict

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
        self.prices_by_sku: Dict[str, int] = prices
        self.offers_by_sku: Dict[str: OfferInfo] = {offer.sku: offer for offer in offers}

    def checkout(self, skus: str) -> int:
        try:
            sku_count = self._validate_and_get_counter(skus)
        except ValueError:
            return self.ERROR_RETURN_CODE

        prices = [self._get_price_for_sku(sku, count) for sku, count in sku_count.items()]

        return sum(prices)

    def _get_price_for_sku(self, sku: str, count: int) -> int:
        price = 0

        offer: OfferInfo = self.offers_by_sku.get(sku)

        if offer:
            instances_of_offer = count // offer.quantity
            price += instances_of_offer * offer.price
            count -= instances_of_offer * offer.quantity

        price += self.prices_by_sku[sku] * count

        return price

    def _validate_and_get_counter(self, skus) -> Counter:
        if type(skus) != str:
            raise ValueError

        sku_count = Counter(skus)

        for sku in sku_count:
            if sku not in self.prices_by_sku:
                raise ValueError

        return sku_count


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    return Checkout(SKU_PRICES, OFFERS).checkout(skus)







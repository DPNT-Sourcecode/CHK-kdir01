from collections import Counter, namedtuple
from typing import Dict, List

PurchaseOption = namedtuple("OfferInfo", ["sku", "quantity", "price"])

PURCHASE_OPTIONS = [
    PurchaseOption(sku="A", quantity=3, price=130),
    PurchaseOption(sku="B", quantity=2, price=45),
    PurchaseOption(sku="A", quantity=1, price=50),
    PurchaseOption(sku="B", quantity=1, price=30),
    PurchaseOption(sku="C", quantity=1, price=20),
    PurchaseOption(sku="D", quantity=1, price=15),
    PurchaseOption(sku="E", quantity=1, price=40),
]


class Checkout:

    ERROR_RETURN_CODE = -1

    def __init__(self, purchase_options: List[PurchaseOption]):
        self.prices_by_sku: Dict[str, int] = {
            po.sku: po.price for po in purchase_options
            if po.quantity == 1
        }
        self.purchase_option_by_sku: Dict[str: PurchaseOption] = {
            po.sku: po for po in purchase_options
            if po.quantity > 1
        }

    def checkout(self, skus: str) -> int:
        try:
            sku_count = self._validate_and_get_counter(skus)
        except ValueError:
            return self.ERROR_RETURN_CODE

        return self._get_price(sku_count)

    def _get_price(self, sku_count: Counter) -> int:
        price = 0

        for sku, count in sku_count.items():
            offer: PurchaseOption = self.purchase_option_by_sku.get(sku)

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
    return Checkout(PURCHASE_OPTIONS).checkout(skus)


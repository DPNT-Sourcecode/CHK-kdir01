from collections import Counter, defaultdict, namedtuple
from typing import Dict, List

PurchaseOption = namedtuple("OfferInfo", ["sku", "quantity", "price", "freebies"])

PURCHASE_OPTIONS = [
    PurchaseOption(sku="A", quantity=1, price=50, freebies=()),
    PurchaseOption(sku="B", quantity=1, price=30, freebies=()),
    PurchaseOption(sku="C", quantity=1, price=20, freebies=()),
    PurchaseOption(sku="D", quantity=1, price=15, freebies=()),
    PurchaseOption(sku="E", quantity=1, price=40, freebies=()),
    PurchaseOption(sku="A", quantity=3, price=130, freebies=()),
    PurchaseOption(sku="A", quantity=5, price=200, freebies=()),
    PurchaseOption(sku="B", quantity=2, price=45, freebies=()),
    PurchaseOption(sku="E", quantity=2, price=80, freebies=tuple("B")),
]


class Checkout:
    """
    Calculates the cost of items bought at checkout.

    We assume that:
     * the offers input are "well balanced" meaning you can take them in the order of savings per
       item and get the best result.
     * the input PurchaseOptions allow every item to be bought individually.
    """

    ERROR_RETURN_CODE = -1

    def __init__(self, purchase_options: List[PurchaseOption]):
        self.prices_by_sku: Dict[str, int] = {}
        self.offers_from_best_by_sku: Dict[str: PurchaseOption] = defaultdict(list)

        for po in purchase_options:
            if po.quantity == 1 and not po.freebies:
                self.prices_by_sku[po.sku] = po.price
            else:
                self.offers_from_best_by_sku[po.sku].append(po)

        self._sort_offers_by_most_valuable()

        # TODO: Maybe should validate the offers don't mention skus that can't be bought singly?
        # TODO: Other validation (quantity +ve etc.)
        # TODO: Decide if inputting all POs in the same format is the right way to go

    def checkout(self, skus: str) -> int:
        try:
            sku_count = self._validate_and_get_counter(skus)
        except ValueError:
            return self.ERROR_RETURN_CODE

        return self._get_price(sku_count)

    def _get_price(self, sku_count: Counter) -> int:
        price = 0

        for sku, count in sku_count.items():
            offers: List[PurchaseOption] = self.offers_from_best_by_sku.get(sku)

            if offers:
                for offer in offers:
                    instances_of_offer = count // offer.quantity
                    price += instances_of_offer * offer.price
                    count -= instances_of_offer * offer.quantity
                    # TODO: freebies not accounted for

            price += self.prices_by_sku[sku] * count

        return price

    def _calculate_po_saving_per_item(self, po: PurchaseOption):
        individual_cost = self.prices_by_sku[po.sku] * po.quantity
        for free_sku in po.freebies:
            individual_cost += self.prices_by_sku[free_sku]
        total_saving = individual_cost - po.price
        total_items = po.quantity + len(po.freebies)

        return total_saving / total_items

    def _sort_offers_by_most_valuable(self):
        for offers in self.offers_from_best_by_sku.values():
            offers.sort(key=self._calculate_po_saving_per_item, reverse=True)

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




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

        # This should make later sorting faster as the order will be more nearly correct.
        for offers in self.offers_from_best_by_sku.values():
            self._sort_offers_by_most_valuable(offers)

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
        offers_for_these_skus = []
        for sku in sku_count:
            offers_for_these_skus += self.offers_from_best_by_sku[sku]
        self._sort_offers_by_most_valuable(offers_for_these_skus)

        price = 0

        # Handle offers
        for offer in offers_for_these_skus:
            while self._is_offer_applicable(offer, sku_count):
                price += offer.price
                sku_count -= Counter({offer.sku: offer.quantity})
                for freebie in offer.freebies:
                    sku_count -= Counter({freebie: 1})

        # Handle non-offers
        for sku, count in sku_count.items():
            price += self.prices_by_sku[sku] * count

        return price

    @staticmethod
    def _is_offer_applicable(offer: PurchaseOption, sku_count):
        # TODO: would be nice not to have to construct this repeatedly, but not a big deal
        # TODO: here we assume that no offer has freebies of the main sku
        offer_count = Counter(offer.freebies)
        offer_count[offer.sku] = offer.quantity

        return all(sku in sku_count and sku_count[sku] >= offer_count[sku] for sku in offer_count)

    def _calculate_po_saving_per_item(self, po: PurchaseOption):
        individual_cost = self.prices_by_sku[po.sku] * po.quantity
        for free_sku in po.freebies:
            individual_cost += self.prices_by_sku[free_sku]
        total_saving = individual_cost - po.price
        total_items = po.quantity + len(po.freebies)

        return total_saving / total_items

    def _sort_offers_by_most_valuable(self, offers: List[PurchaseOption]):
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


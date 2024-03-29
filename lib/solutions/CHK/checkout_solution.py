from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import itertools
from typing import Dict, List


@dataclass
class PurchaseOption:
    """
    Represents a purchase option for customers in terms of a collection of skus for a given price.
    """

    sku: str
    quantity: int
    price: int
    freebies: str = ""

    @staticmethod
    def create_combi_purchase_options(skus: str, quantity: int, price: int) -> List[PurchaseOption]:
        """
        Creates a list of PurchaseOptions corresponding to: "buy any <quantity> of <skus> for <price>"
        """
        def create_po(sku_list):
            main_sku = sku_list[0]
            freebies = ""
            main_sku_count = 0

            for sku in sku_list:
                if sku != main_sku:
                    freebies += sku
                else:
                    main_sku_count += 1

            return PurchaseOption(sku=main_sku, quantity=main_sku_count, price=price, freebies=freebies)

        return [
            create_po(sku_list)
            for sku_list in itertools.combinations_with_replacement(skus, quantity)
        ]


# TODO: Add some way to read in input - talk to management about the format.
# TODO: Might help to be able to help with "3R get one Q free" also (as in you need to calculate the cost)
PURCHASE_OPTIONS = [
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
    PurchaseOption(sku="G", quantity=1, price=20),
    PurchaseOption(sku="H", quantity=1, price=10),
    PurchaseOption(sku="H", quantity=5, price=45),
    PurchaseOption(sku="H", quantity=10, price=80),
    PurchaseOption(sku="I", quantity=1, price=35),
    PurchaseOption(sku="J", quantity=1, price=60),
    PurchaseOption(sku="K", quantity=1, price=70),
    PurchaseOption(sku="K", quantity=2, price=120),
    PurchaseOption(sku="L", quantity=1, price=90),
    PurchaseOption(sku="M", quantity=1, price=15),
    PurchaseOption(sku="N", quantity=1, price=40),
    PurchaseOption(sku="N", quantity=3, price=120, freebies="M"),
    PurchaseOption(sku="O", quantity=1, price=10),
    PurchaseOption(sku="P", quantity=1, price=50),
    PurchaseOption(sku="P", quantity=5, price=200),
    PurchaseOption(sku="Q", quantity=1, price=30),
    PurchaseOption(sku="Q", quantity=3, price=80),
    PurchaseOption(sku="R", quantity=1, price=50),
    PurchaseOption(sku="R", quantity=3, price=150, freebies="Q"),
    PurchaseOption(sku="S", quantity=1, price=20),
    PurchaseOption(sku="T", quantity=1, price=20),
    PurchaseOption(sku="U", quantity=1, price=40),
    PurchaseOption(sku="U", quantity=4, price=120),
    PurchaseOption(sku="V", quantity=1, price=50),
    PurchaseOption(sku="V", quantity=2, price=90),
    PurchaseOption(sku="V", quantity=3, price=130),
    PurchaseOption(sku="W", quantity=1, price=20),
    PurchaseOption(sku="X", quantity=1, price=17),
    PurchaseOption(sku="Y", quantity=1, price=20),
    PurchaseOption(sku="Z", quantity=1, price=21),
]

PURCHASE_OPTIONS += PurchaseOption.create_combi_purchase_options("STXYZ", 3, 45)


class Checkout:
    """
    Calculates the cost of items bought at checkout.

    We assume that:
     * the offers input are "well balanced" meaning you can take them in the order of percentage saving
       and get the best result.
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

        # TODO: Maybe should validate that offers don't mention skus that can't be bought singly?
        # TODO: Other validation (quantity +ve etc.)

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
        # TODO: refactor PurchaseOption to not consider freebies and main sku separately
        # TODO: would be nice not to have to construct this Counter repeatedly, but not a big deal
        # TODO: here we assume that no offer has freebies of the main sku
        offer_count = Counter(offer.freebies)
        offer_count[offer.sku] = offer.quantity

        return all(sku in sku_count and sku_count[sku] >= offer_count[sku] for sku in offer_count)

    def _calculate_percentage_po_saving(self, po: PurchaseOption):
        individual_cost = self.prices_by_sku[po.sku] * po.quantity
        for free_sku in po.freebies:
            individual_cost += self.prices_by_sku[free_sku]
        total_saving = individual_cost - po.price

        return total_saving / individual_cost

    def _sort_offers_by_most_valuable(self, offers: List[PurchaseOption]):
        offers.sort(key=self._calculate_percentage_po_saving, reverse=True)

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




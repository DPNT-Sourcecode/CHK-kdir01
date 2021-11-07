from collections import Counter

SKU_PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    sku_count = Counter(skus)




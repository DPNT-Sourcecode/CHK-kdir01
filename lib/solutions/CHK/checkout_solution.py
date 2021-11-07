from collections import Counter

SKU_PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}

ERROR_RETURN_CODE = -1


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    if type(skus) != str:
        return ERROR_RETURN_CODE

    sku_count = Counter(skus)

    for sku in sku_count:
        if sku not in SKU_PRICES:
            return ERROR_RETURN_CODE

    prices = [SKU_PRICES[sku] * count for sku, count in sku_count.items()]

    return sum(prices)


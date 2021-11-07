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

    if SKU_PRICES.keys() 

    prices = [SKU_PRICES[sku] * count for sku, count in sku_count.items()]

    return sum(prices)

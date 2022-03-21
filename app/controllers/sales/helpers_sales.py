def helper_verify_quatity_product_stock(
    product: dict, product_variations: list[dict]
) -> bool:
    is_found = False
    for variation in product_variations:
        if variation.size == product["size"]:
            is_found = True
            if product["quantity"] > variation.quantity:
                is_found = False
    return is_found

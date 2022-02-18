def helper_verify_quatity_product_stock(
    product: dict, product_variations: list[dict]
) -> bool:
    is_found = False
    for variation in product_variations:
        product["color"] = product["color"].title()
        if variation.color == product["color"] and variation.size == product["size"]:
            is_found = True
            if product["quantity"] > variation.quantity:
                return False
    if not (is_found):
        return is_found

    return True

def help_normalize_variations(variations: list[dict]) -> list[dict]:
    list_normalized = []
    obj_normalized = {}
    list_obj_normalized = []
    last_color = ""
    count = 0
    for element in variations:
        if last_color == element.color or last_color == "":
            list_normalized.append(
                {
                    "size": element.size,
                    "quantity": element.quantity,
                }
            )
            obj_normalized["color_name"] = element.color
            obj_normalized["sizes_product"] = [*list_normalized]
            last_color = element.color
            if count == len(variations) - 1:
                list_obj_normalized.append(obj_normalized)
        else:
            list_obj_normalized.append(obj_normalized)
            obj_normalized = {}
            last_color = ""
            list_normalized = []
            list_normalized.append(
                {
                    "size": element.size,
                    "quantity": element.quantity,
                }
            )
        count += 1

    return list_obj_normalized

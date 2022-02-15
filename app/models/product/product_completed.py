from dataclasses import dataclass

from app.models.product.products_model import ProductModel


@dataclass
class ProductCompletedModel:
    nome: str
    age: int

    @classmethod
    def serializer_product(
        cls, product: ProductModel, sizes_product: dict
    ) -> "ProductCompletedModel":
        sizes = {}
        list_sizes_product = []
        for size in sizes_product:
            id_color = size.id_color
            # print("size=>", size)
            list_sizes_product.append(size.asdict())

    # print("list_sizes_product=>", list_sizes_product)
    #    if product["id_product"] == size.id_product:
    #        sizes[size.name] = {"name": size.name, "quantity": size.quantity}
    # product["sizes_product"] = sizes

    # return product

    @classmethod
    def separates_model(
        cls,
        list_keys_product: list[str],
        keys_colors: list[str],
        list_keys_sizes: list[str],
        data_json: dict,
    ) -> dict:
        product = {}
        list_colors_and_sizes = data_json["variations"]
        for key, value in data_json.items():
            if key in list_keys_product:
                product[key] = value

        list_variations = []
        for obj_color_sizes_product in list_colors_and_sizes:
            list_color_sizes_product: list = obj_color_sizes_product["sizes_product"]
            for size in list_color_sizes_product:
                size["color"] = obj_color_sizes_product["color_name"]
                list_variations.append(size)
        return {"product": product, "colors_sizes_product": list_variations}

    @classmethod
    def separates_model_for_update(
        cls,
        list_keys_product: list[str],
        keys_colors: list[str],
        list_keys_sizes: list[str],
        data_json: dict,
    ) -> dict:
        product = {}
        list_colors_and_sizes = None
        list_variations = []
        for key, value in data_json.items():
            if key in list_keys_product:
                product[key] = value

        if data_json.get("variations"):
            list_colors_and_sizes = data_json["variations"]

            for obj_color_sizes_product in list_colors_and_sizes:
                list_color_sizes_product: list = obj_color_sizes_product[
                    "sizes_product"
                ]
                for size in list_color_sizes_product:
                    size["color"] = obj_color_sizes_product["color_name"]
                    list_variations.append(size)
        return {"product": product, "variations": list_variations}

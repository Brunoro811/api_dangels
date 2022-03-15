from flask import Blueprint


from app.controllers.products import (
    update_product,
    get_one_product,
    delete_product,
    get_all_products_all_stores,
    create_product,
    get_image_product,
    create_update_images_product,
    get_groups_products,
    create_group_products,
)

bp = Blueprint("products", __name__, url_prefix="/products")

bp.get("/<int:id>")(get_one_product)
bp.get("/images/<name>")(get_image_product)
bp.get("/completed")(get_all_products_all_stores)
bp.get("/group")(get_groups_products)

bp.post("")(create_product)
bp.post("/images/<int:id>")(create_update_images_product)

bp.patch("<int:id>")(update_product)

bp.delete("<int:id>")(delete_product)

bp.post("/group")(create_group_products)

import datetime
from flask import current_app, jsonify
from http import HTTPStatus

from sqlalchemy.orm import Session

import werkzeug.exceptions
from app.controllers.sales.helpers_sales import (
    helper_verify_quatity_product_stock,
)

from app.models.product.products_model import ProductModel
from app.decorators import verify_payload

from app.models.orders_has_products.orders_has_products import OrdersHasProductsModel
from app.models.orders_sellers.orders_seller import OrdersModel
from app.models import ClientModel
from app.models.types_sales.type_sale import TypeSaleModel


@verify_payload(
    fields_and_types={
        "id_seller": int,
        "id_client": int,
        "id_store": int,
        "products": list,
        "id_type_sale": int,
    }
)
def create_sale(data: dict):
    try:
        session: Session = current_app.db.session

        orders_products = []
        date_now = datetime.date.today()
        list_products = data.pop("products")

        if not list_products:
            return {"erro": "list of products empty."}, HTTPStatus.BAD_REQUEST

        ClientModel.query.get_or_404(data["id_client"], description="client")

        type_sale: TypeSaleModel = TypeSaleModel.query.get_or_404(
            data["id_type_sale"], description="type sale"
        )
        sale_finish = (
            {"sale_finish": True}
            if type_sale.name == "Loja"
            else {"sale_finish": False}
        )

        new_order = OrdersModel(**{**data, **sale_finish})

        orders_products = []
        for product in list_products:
            if type(product["size"]) == str:
                product["size"] = product["size"].upper()

            product_stock: ProductModel = ProductModel.query.get_or_404(
                product["id_product"],
                description=f"id_product: {product['id_product']}",
            )

            if not (
                helper_verify_quatity_product_stock(product, product_stock.variations)
            ):
                return {
                    "erro": f"id_product:{product['id_product']} size:{product['size']} quantity greater than stock!"
                }, HTTPStatus.BAD_REQUEST

            product_stock.sale_product(product)

            date_start = product_stock.date_start
            date_end = product_stock.date_end

            sale_value = 0
            if date_now >= date_start and date_now <= date_end:
                sale_value = product_stock.sale_value_promotion
            elif date_now >= date_start and date_now <= date_end:
                sale_value = product_stock.sale_value_promotion
            else:
                sale_value = product_stock.sale_value_varejo

            orders_products.append(
                OrdersHasProductsModel(
                    **{
                        "sale_value": sale_value,
                        "quantity": product["quantity"],
                        "color": product["color"],
                        "size": product["size"],
                        "id_product": product["id_product"],
                        "id_order": new_order.id_order,
                    }
                )
            )
        new_order.orders_has_products = orders_products
        session.add(new_order)
        session.commit()

        return jsonify(new_order), HTTPStatus.CREATED
    except werkzeug.exceptions.NotFound as e:
        return {"erro": f"{e.description} Not found."}, HTTPStatus.NOT_FOUND
    except InterruptedError as e:
        return {"erro": f"{e.args[0]}"}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e

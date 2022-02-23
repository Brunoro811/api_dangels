import datetime
from operator import and_
from flask import current_app, jsonify, request
from http import HTTPStatus


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound

import werkzeug.exceptions
from app.controllers.sales_controllers.helpers_sales import (
    helper_verify_quatity_product_stock,
)

from app.models.product.products_model import ProductModel
from app.controllers.decorators import (
    verify_keys,
    verify_keys_list_interna_one,
    verify_types,
)
from app.models.users.orders_has_products import OrdersHasProductsModel
from app.models.users.orders_seller import OrdersModel


def verify_order_empty_and_delete(list_or_number_id_order: "int or list[int]") -> None:
    session: Session = current_app.db.session
    if type(list_or_number_id_order) == list:
        for id_order in list_or_number_id_order:
            order: OrdersModel = OrdersModel.query.get(id_order)
            session.delete(order)
    else:
        order: OrdersModel = OrdersModel.query.get(list_or_number_id_order)
        session.delete(order)
    session.commit()


@verify_keys(["id_seller", "id_client", "products", "id_store"])
@verify_types({"id_seller": int, "id_seller": int, "id_store": int, "products": list})
@verify_keys_list_interna_one("products", ["id_product", "color", "size", "quantity"])
def create_sale():
    try:
        session: Session = current_app.db.session
        orders_products = []
        data = request.get_json()
        date_now = datetime.date.today()
        list_products = data["products"]

        if not list_products:
            return {"erro": "list of products emepty."}, HTTPStatus.BAD_REQUEST

        new_order = OrdersModel(
            **{
                "id_seller": data["id_seller"],
                "id_client": data["id_client"],
                "id_store": data["id_store"],
            }
        )
        session.add(new_order)
        session.commit()

        for product in list_products:
            sale_value = None
            product_get: ProductModel = ProductModel.query.get_or_404(
                product["id_product"], description="product"
            )

            if not (
                helper_verify_quatity_product_stock(product, product_get.variations)
            ):
                return {
                    "erro": f"id_product:{product['id_product']} size:{product['size']} quantity greater than stock or product invalid!"
                }, HTTPStatus.BAD_REQUEST

            date_start = product_get.date_start
            date_end = product_get.date_end

            product_get.sale_product(product)

            if product["quantity"] >= product_get.quantity_atacado:
                sale_value = product_get.sale_value_atacado

            elif date_now >= date_start and date_now <= date_end:
                sale_value = product_get.sale_value_promotion

            else:
                sale_value = product_get.sale_value_varejo

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
        session.add_all(product_get.variations)
        session.add_all(orders_products)
        session.commit()

        return "", HTTPStatus.CREATED
    except werkzeug.exceptions.NotFound as e:
        return {"erro": f"{e.description} Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"erro": "Algum campo esta inválido"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def get_one_sale_for_id_order(id: int):
    try:
        order: OrdersModel = OrdersModel.query.get(id)
        if not order:
            raise NoResultFound
        data = {"order": order, "products": order.orders_has_products_seller}
        return data, HTTPStatus.OK
    except NoResultFound:
        return {"error": "Order not found."}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def get_all_sale_for_id_seller(id: int, month: "int or None" = None):
    try:
        list_orders_products_for_seller = []
        month = request.args.get("month", None)
        date = str(datetime.date.today())
        if month:
            if int(month) > 12 or int(month) < 1:
                return {"error": "Month invalid!"}, HTTPStatus.UNPROCESSABLE_ENTITY

            date_start = f"{date[:-5]}{month}-01"
            date_end = f"{date[:-5]}{month}-31"
        else:
            date_start = f"{date[:-2]}01"
            date_end = f"{date[:-2]}31"

        orders: OrdersModel = (
            OrdersModel.query.filter_by(id_seller=id)
            .filter(
                and_(
                    OrdersModel.date_creation >= date_start,
                    OrdersModel.date_creation <= date_end,
                )
            )
            .all()
        )
        if not orders:
            raise NoResultFound

        for order_product in orders:
            print("")
            print("=>", order_product)
            print("")
            if order_product.orders_has_products_seller:
                list_orders_products_for_seller.append(
                    {
                        "order": order_product,
                        "products": order_product.orders_has_products_seller,
                    }
                )
            if not order_product.orders_has_products_seller:
                verify_order_empty_and_delete([order_product.id_order])

        return jsonify(list_orders_products_for_seller), HTTPStatus.OK
    except ValueError as e:
        return {"error": f"Value {e.args[0]} incorret"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except NoResultFound:
        return {"error": "Order not found."}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def delete_sale(id: int):
    try:
        session: Session = current_app.db.session
        order: OrdersModel = OrdersModel.query.get(id)
        orders_products_seller = OrdersHasProductsModel.query.filter_by(id_order=id)
        orders_products_seller.delete()
        session.delete(order)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except UnmappedInstanceError:
        return {"erro": "Not found product."}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

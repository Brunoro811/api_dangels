from http import HTTPStatus
from flask import jsonify

from sqlalchemy.orm.exc import NoResultFound

from app.models.orders_sellers.orders_seller import OrdersModel


def get_orders_sale_for_store(id: int):
    try:
        list_found_orders_for_store = OrdersModel.query.filter_by(id_store=id)
        if not list_found_orders_for_store:
            return {"error": "store not found"}, HTTPStatus.NOT_FOUND
        list_orders = []
        for order in list_found_orders_for_store:
            if not order:
                raise NoResultFound
            order_completed = {
                "seller": order.sellers,
                "store": order.store,
                "client": order.client,
            }
            list_orders.append(order_completed)

        return jsonify(list_orders), HTTPStatus.OK
    except NoResultFound:
        return {"error": "Order not found."}, HTTPStatus.NOT_FOUND
    except AttributeError as e:
        return {"error": f" {e.args[0]}"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

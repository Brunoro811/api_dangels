from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound

from app.models.orders_sellers.orders_seller import OrdersModel


def get_one_sale_for_id_order(id: int):
    try:
        order: OrdersModel = OrdersModel.query.get(id)
        if not order:
            raise NoResultFound
        data = {"order": order}
        return data, HTTPStatus.OK

    except NoResultFound:
        return {"error": "Order not found."}, HTTPStatus.NOT_FOUND
    except AttributeError as e:
        return {"error": f" {e.args[0]}"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

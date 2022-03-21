from flask import current_app
from http import HTTPStatus


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.models.users.orders_has_products import OrdersHasProductsModel
from app.models.users.orders_seller import OrdersModel

from werkzeug.exceptions import NotFound


def delete_sale(id: int):
    try:
        session: Session = current_app.db.session
        order: OrdersModel = OrdersModel.query.get_or_404(id, description="order")

        orders_products_seller = OrdersHasProductsModel.query.filter_by(id_order=id)
        orders_products_seller.delete()
        session.delete(order)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except UnmappedInstanceError:
        return {"erro": "Not found product."}, HTTPStatus.NOT_FOUND
    except NotFound as e:
        return {"erro": f"{e.description} not found."}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

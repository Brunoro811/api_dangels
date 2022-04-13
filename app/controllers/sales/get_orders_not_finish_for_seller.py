from werkzeug import exceptions

from operator import and_
from flask import jsonify, request
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound
from app.helpers.range_date_of_month import range_date_of_month

from app.models.orders_sellers.orders_seller import OrdersModel
from app.models.sellers.seller_model import SellerModel


def get_all_sale_not_finish_for_id_seller(id: int, month: "int or bool" = False):
    try:
        SellerModel.query.get_or_404(id, description="Seller")

        month = request.args.get("month", False)

        dates_of_month = range_date_of_month(month) if month else range_date_of_month()
        date_start = dates_of_month.initial
        date_end = dates_of_month.the_end

        finish_orders: OrdersModel = (
            OrdersModel.query.filter_by(id_seller=id)
            .filter(
                and_(
                    OrdersModel.date_creation >= date_start,
                    OrdersModel.date_creation <= date_end,
                )
            )
            .filter_by(sale_finish=False)
            .all()
        )

        return jsonify(finish_orders), HTTPStatus.OK
    except exceptions.NotFound as e:
        return {"erro": f"{e.description} not found."}, HTTPStatus.NOT_FOUND
    except ValueError as e:
        return {"error": f"Value {e.args[0]} incorret"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except NoResultFound:
        return {"error": "Order not found."}, HTTPStatus.NOT_FOUND
    except AttributeError as e:
        return {"error": f"{e.args[0]}"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

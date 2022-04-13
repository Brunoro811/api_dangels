import datetime
from operator import and_
from flask import jsonify, request
from http import HTTPStatus


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from app.helpers.range_date_of_month import range_date_of_month

from app.models.orders_sellers.orders_seller import OrdersModel

from app.default import data_month


def get_all_sale_finish_for_id_seller(id: int, month: "int or None" = None):
    try:
        month = request.args.get("month", None)
        date = str(datetime.date.today())

        if month:
            if int(month) > 12 or int(month) < 1:
                return {"error": "Month invalid!"}, HTTPStatus.UNPROCESSABLE_ENTITY

            date_start = f"{date[:-5]}{month}-0{data_month[month][0]}"
            date_end = f"{date[:-5]}{month}-{data_month[month][1]}"
        else:
            dates_of_month = range_date_of_month(datetime.date.today())

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
            .filter_by(sale_finish=True)
            .all()
        )

        return jsonify(finish_orders), HTTPStatus.OK
    except ValueError as e:
        return {"error": f"Value {e.args[0]} incorret"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except NoResultFound:
        return {"error": "Order not found."}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

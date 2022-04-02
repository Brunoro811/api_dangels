from flask import current_app
from app.default.default_values import types_sales
from sqlalchemy.orm import Session
from app.models.users.type_sale import TypeSaleModel


def default_types_sales():
    try:
        session: Session = current_app.db.session
        types_sales_found = TypeSaleModel.query.all()
        if not types_sales_found:
            type_sales_list = []
            for type in types_sales:
                type_sales_list.append(TypeSaleModel(**type))
            session.add_all(type_sales_list)
            session.commit()
    except Exception as e:
        raise e

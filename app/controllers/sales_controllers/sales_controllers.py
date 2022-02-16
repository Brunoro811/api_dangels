from datetime import datetime
from flask import current_app, jsonify, request
from http import HTTPStatus


from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound
from app.models.product.products_model import ProductModel

from app.controllers.decorators import verify_keys, verify_optional_keys, verify_types
from app.models.users.orders_has_products import OrdersHasProductsModel
from app.models.users.orders_seller import OrdersModel


@verify_keys(["id_seller", "id_client", "products", "id_store"])
@verify_types({"id_seller": int, "id_seller": int, "id_store": int, "products": list})
def create_sale():
    try:
        session: Session = current_app.db.session
        data = request.get_json()
        date_now = datetime.date(datetime.utcnow())

        new_order = OrdersModel(
            **{
                "id_seller": data["id_seller"],
                "id_client": None,
                "id_store": data["id_store"],
            }
        )
        session.add(new_order)
        session.commit()

        list_products = data["products"]
        orders_products = []
        for product in list_products:
            sale_value = None
            product_get = ProductModel.query.get(product["id_product"])

            date_start = datetime.date(product_get.date_start)
            date_end = datetime.date(product_get.date_end)

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
        session.add_all(orders_products)
        session.commit()

        # print("=>", orders_products)

        return "", HTTPStatus.CREATED
    except AttributeError:
        return {"erro": "Algum campo esta inválido"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def get_one_sale(id: int):
    try:
        ...
        orders = OrdersModel.query.filter_by(date_creation="2022-02-12").all()
        print("ORDERS POR DATA => ", orders)

        return "", HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


"""

def get_sales():
    product_list = ProductModel.query.all()
    sizes_product = Query([SizeModel], current_app.db.session).all()

    new_lista_produtos = []
    for product in product_list:
        product: ProductModel
        new_product = product.asdict()
        arr = [
            size for size in sizes_product if (product.id_product == size.id_product)
        ]
        new_lista_produtos.append(
            ProductCompletedModel.serializer_product(new_product, arr)
        )

    return jsonify(new_lista_produtos), HTTPStatus.OK


@verify_optional_keys(["cost", "id_category", "name", "sizes_product"])
def update_sale(id: int):

    try:
        keys_product = ["name", "id_category", "cost"]
        keys_sizes_product = ["sizes_product"]
        data = request.get_json()

        product = ProductModel.query.get(id)
        if not (product):
            raise NoResultFound
        sizes_product = SizeModel.query.filter_by(id_product=id).all()

        obj_product_size = ProductCompletedModel.separates_model(
            keys_product, keys_sizes_product, data
        )

        if obj_product_size["product"]:
            update_product = dict(obj_product_size["product"])
            for key, value in update_product.items():
                setattr(product, key, value)
            current_app.db.session.add(product)
            current_app.db.session.commit()

        if obj_product_size["sizes_product"]:
            update_sizes_product = dict(obj_product_size["sizes_product"])
            for key, value in update_sizes_product.items():
                for element_sizeModel in sizes_product:
                    if element_sizeModel.name == key:
                        setattr(element_sizeModel, "quantity", value["quantity"])
                        current_app.db.session.add(element_sizeModel)

            current_app.db.session.commit()

        return "", HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def delete_sale(id: int):
    try:
        product = ProductModel.query.get(id)
        sizes_product = SizeModel.query.filter_by(id_product=id)

        sizes_product.delete()
        current_app.db.session.commit()
        current_app.db.session.delete(product)
        current_app.db.session.commit()

        return "", HTTPStatus.NO_CONTENT
    except UnmappedInstanceError:
        return {"erro": "Not found product."}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
"""

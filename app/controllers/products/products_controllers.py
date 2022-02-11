from flask import current_app, jsonify, request
from http import HTTPStatus


from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound


from app.models.category_products.category_model import CategoryModel
from app.models.product.product_completed import ProductCompletedModel
from app.models.product.products_model import ProductModel
from app.models.product.size_model import SizeModel

from app.controllers.products.decorators_products import verify_keys,verify_types, verify_optional_keys

@verify_keys(['cost', 'id_category', 'name', 'sizes_products'])
@verify_types({"cost": float, "id_category": int, 'name': str, 'sizes_products': list })
def create_product():
    try:
        keys_product = ['name','id_category','cost']
        keys_sizes_products = ['sizes_products']
        data: dict = request.get_json()

        obj_product_size = ProductCompletedModel.separates_model(keys_product,keys_sizes_products,data)
        product = dict(obj_product_size['product'])
        sizes_products = list(obj_product_size['sizes_product'])

        category = CategoryModel.query.get(int(product['id_category']))
        product.update({'id_category': category.id_category})
        new_product = ProductModel(**product)
        
        current_app.db.session.add(new_product)
        current_app.db.session.commit()
        
        list_new_sizes = [ SizeModel(**{**size,"id_product": new_product.id_product}) for size in sizes_products ]
        
        current_app.db.session.add_all(list_new_sizes)
        current_app.db.session.commit()
        product = new_product.asdict()
        data = ProductCompletedModel.serializer_product(product,list_new_sizes)

        return jsonify(data),HTTPStatus.CREATED
    except AttributeError:
        return {"erro": "Algum campo esta inválido"},HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def get_product():
    product_list = ProductModel.query.all()
    sizes_product = Query([SizeModel],current_app.db.session).all()

    new_lista_produtos= []
    for product in product_list :
        product: ProductModel
        new_product = product.asdict()
        arr = [ size for size in sizes_product if(product.id_product == size.id_product) ]
        new_lista_produtos.append(ProductCompletedModel.serializer_product(new_product,arr))

    return jsonify(new_lista_produtos),HTTPStatus.OK

def get_one_product(id_product:int):
    try:
        product = ProductModel.query.get(id_product)
        if not (product):
                raise NoResultFound

        sizes_product = Query([SizeModel],current_app.db.session).filter_by(id_product=id_product).all() 

        product: ProductModel
        new_product = product.asdict()
        arr = [ size for size in sizes_product if(product.id_product == size.id_product) ]
        new_produto = (ProductCompletedModel.serializer_product(new_product,arr))
        
        return jsonify(new_produto),HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

@verify_optional_keys(['cost', 'id_category', 'name', 'sizes_product'])
def update_product(id_product: int):
    
    try:
        keys_product = ['name','id_category','cost']
        keys_sizes_products = ['sizes_product']
        data = request.get_json()

        product = ProductModel.query.get(id_product)
        if not (product):
            raise NoResultFound
        sizes_product = SizeModel.query.filter_by(id_product=id_product).all()

        obj_product_size = ProductCompletedModel.separates_model(keys_product,keys_sizes_products,data)
        

        if(obj_product_size['product']):
            update_product = dict(obj_product_size['product'])
            for key,value in update_product.items():
                setattr(product,key,value)
            current_app.db.session.add(product)
            current_app.db.session.commit()

        if(obj_product_size['sizes_product']):
            update_sizes_products = dict(obj_product_size['sizes_product'])
            for key,value in update_sizes_products.items():
                for element_sizeModel in sizes_product:
                    if(element_sizeModel.name == key):
                        setattr(element_sizeModel,'quantity',value['quantity'])
                        current_app.db.session.add(element_sizeModel)

            current_app.db.session.commit()

        return "",HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except AttributeError:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def delete_product(id_product: int):
    try:
        product = ProductModel.query.get(id_product)
        sizes_product = SizeModel.query.filter_by(id_product=id_product)

        sizes_product.delete()
        current_app.db.session.commit()
        current_app.db.session.delete(product)
        current_app.db.session.commit()
        
        return "",HTTPStatus.NO_CONTENT
    except UnmappedInstanceError:
        return {"erro": "Not found product."},HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e
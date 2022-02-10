from flask import current_app, jsonify, request
from http import HTTPStatus as http

from app.models.category_products.category_model import CategoryModel
from app.models.products_model import ProductHaveSizeModel, ProductModel,SizeModel
from app.controllers.products.decorators_products import verify_keys,verify_types

@verify_keys(['cost', 'id_category', 'name', 'sizes_products'])
@verify_types({"cost": float, "id_category": int, 'name': str, 'sizes_products': list })
def create_product():
    try:
        keys_product = ['name','id_category','cost']
        keys_sizes_products = ['sizes_products']
        data: dict = request.get_json()
        product = {}
        sizes_products= None
        for key,value in data.items():
            if(key in keys_product):
                product[key] = value
            if(key in keys_sizes_products):
                sizes_products= value

        category = CategoryModel.query.get(int(product['id_category']))
        product.update({'id_category': category.id_category})
        new_product = ProductModel(**product)
        
        current_app.db.session.add(new_product)
        
        list_new_sizes = [ SizeModel(**size) for size in sizes_products ]
        
        current_app.db.session.add_all(list_new_sizes)
        current_app.db.session.commit()
        
        new_product_have_sizes = (
        [ ProductHaveSizeModel(**{"id_product": new_product.id_product ,"id_size": size_model.id_size})  for size_model in list_new_sizes]
            )

        current_app.db.session.add_all(new_product_have_sizes)
        current_app.db.session.commit()
        data : dict = {"product": new_product, "sizes_product": list_new_sizes}

        return jsonify(data),http.CREATED
    except Exception as e:
        raise e

def get_product():
    ...

    
def update_product():...
def delete_product():...
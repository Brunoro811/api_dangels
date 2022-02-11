from dataclasses import dataclass

from app.models.product.products_model import ProductModel
from app.models.product.size_model import SizeModel


@dataclass
class ProductCompletedModel:
    nome : str
    age: int
    
    @classmethod
    def serializer_product(cls,product: ProductModel, sizes_product: SizeModel)-> "ProductCompletedModel":
        sizes = {}
        for size in sizes_product:
            if(product['id_product'] == size.id_product):
                sizes[size.name] = {"name":size.name,"quantity": size.quantity}
        product['sizes_product'] = sizes    
            #product['sizes'] = [ {"name":size.name,"quantity": size.quantity} for size in sizes_product if(product['id_product'] == size.id_product) ]
            #product['sizes'] = [ {"name":size.name,"quantity": size.quantity} for size in sizes_product if(product['id_product'] == size.id_product) ]
        
        return product

    @classmethod
    def separates_model(cls,list_keys_product: list[str],list_keys_sizes: list[str],data_json: dict)-> dict:
        product = {}
        sizes_products= None
        for key,value in data_json.items():
            if(key in list_keys_product):
                product[key] = value
            if(key in list_keys_sizes):
                sizes_products= value
        return {"product": product, "sizes_product": sizes_products}
        
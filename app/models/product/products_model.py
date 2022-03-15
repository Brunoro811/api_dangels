from dataclasses import asdict, dataclass

from datetime import date
import os

from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import relationship, validates


@dataclass
class ProductModel(db.Model):
    id_product: int
    code_product: int
    name: str
    cost_value: float
    date_start: Date
    date_end: Date
    id_category: int
    date_creation: Date
    id_store: int
    image_name: str
    quantity_atacado: int
    sale_value_atacado: float
    sale_value_varejo: float
    sale_value_promotion: float

    """ Relacionamentos """
    store: dict
    category: dict
    """ Relacionamentos """

    sale_value: float = 0
    link_image: str = None
    is_promotion: bool = False

    __tablename__ = "products"
    id_product = Column(sql.Integer, autoincrement=True, primary_key=True)
    code_product = Column(sql.Integer, unique=True)
    name = Column(sql.String(50), nullable=False)
    date_creation = Column(sql.Date, default=date.today())
    cost_value = Column(sql.Float(2), nullable=False)
    sale_value_varejo = Column(sql.Float(2), nullable=False)
    sale_value_atacado = Column(sql.Float(2), nullable=False)
    quantity_atacado = Column(sql.Integer, nullable=False)
    sale_value_promotion = Column(sql.Float(2))
    date_start = Column(sql.Date, default=None)
    date_end = Column(sql.Date, default=None)
    id_category = Column(
        sql.Integer, ForeignKey("categorys.id_category"), nullable=False
    )
    id_store = Column(sql.Integer, ForeignKey("stores.id_store"), nullable=False)
    image = Column(sql.LargeBinary)
    image_name = Column(sql.Text)
    image_mimeType = Column(sql.Text)

    store = relationship("StoreModel", backref="product", uselist=False)
    category = relationship("CategoryModel", backref="category", uselist=False)

    variations = relationship("VariationModel", backref="product", uselist=True)

    orders_has_products_product = relationship(
        "OrdersHasProductsModel", backref="product", uselist=True
    )

    def asdict(self):
        return asdict(self)

    def sale_product(self, product_variation: dict):
        for color_size_stock in self.variations:
            if (
                color_size_stock.color == product_variation["color"]
                and color_size_stock.size == product_variation["size"]
            ):
                setattr(
                    color_size_stock,
                    "quantity",
                    (color_size_stock.quantity - product_variation["quantity"]),
                )

    @property
    def link_image(self):
        return self.link_image

    @link_image.getter
    def link_image(self, text: str = os.getenv("URL_PRODUCT_IMAGE")):
        text = f"{text}{self.image_name}"
        return text

    @property
    def sale_value(self):
        return self.sale_value

    @sale_value.getter
    def sale_value(self, value: str = 0):
        value = self.sale_value_varejo
        date_now = date.today()
        if self.date_start:
            if self.date_start and self.date_end:
                if date_now >= self.date_start and date_now <= self.date_end:
                    self.is_promotion = True
            value = self.sale_value_promotion

        return value

    @validates("sale_value_promotion")
    def validate_sale_value_promotion(self, key: str, value: str):
        if value == 0:
            return None
        return value

    @validates("date_start", "date_end")
    def valdiate_date(self, key: str, value: str):
        if value == "":
            return None
        return value

    @validates("name")
    def title(self, key: str, value: str):
        return value.title()

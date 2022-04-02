from dataclasses import asdict, dataclass

from datetime import date, datetime
import os

from app.configs.database import db

from sqlalchemy.sql import sqltypes as sql
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import relationship, validates

from re import match


@dataclass
class ProductModel(db.Model):
    id_product: int
    code_product: int
    name: str
    cost_value: float
    color: str
    id_category: int

    date_creation_product: Date

    id_store: int
    image_name: str
    quantity_atacado: int
    sale_value_atacado: float
    sale_value_varejo: float
    sale_value_promotion: float

    """ Relacionamentos """
    store: dict
    category: dict
    variations: dict
    """ Relacionamentos """
    date_start_promotion: Date = None
    date_end_promotion: Date = None
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
    color = Column(sql.String(50), nullable=False)
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
            if color_size_stock.size == product_variation["size"]:
                setattr(
                    color_size_stock,
                    "quantity",
                    (color_size_stock.quantity - product_variation["quantity"]),
                )

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

        if isinstance(self.date_start, date) and isinstance(self.date_end, date):
            if date_now >= self.date_start and date_now <= self.date_end:
                self.is_promotion = True
                value = self.sale_value_promotion

        return value

    """ format dates """

    @property
    def date_start_promotion(self):
        return self.date_start_promotion

    @date_start_promotion.getter
    def date_start_promotion(self, value: str = None):

        partern = "%d/%m/%Y"
        value = self.date_start

        if isinstance(
            self.date_start,
            date,
        ):
            value = datetime.strftime(self.date_start, partern)
        return value

    @property
    def date_end_promotion(self):
        return self.date_end_promotion

    @date_end_promotion.getter
    def date_end_promotion(self, value: str = None):
        partern = "%d/%m/%Y"
        value = self.date_end
        if isinstance(
            self.date_end,
            date,
        ):
            value = datetime.strftime(self.date_end, partern)
        return value

    @property
    def date_creation_product(self):
        return self.date_creation_product

    @date_creation_product.getter
    def date_creation_product(self, value: str = None):

        partern = "%d/%m/%Y"
        value = self.date_creation

        if isinstance(
            self.date_creation,
            date,
        ):
            value = datetime.strftime(self.date_creation, partern)
        return value

    """ format dates """

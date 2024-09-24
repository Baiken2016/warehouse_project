from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from app.models.orders import Order
from app.models.products import Product


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey(Order.id))
    product_id = Column(Integer, ForeignKey(Product.id))
    quantity = Column(Integer)

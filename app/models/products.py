from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from app.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


class ProductIn(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "name": "product name",
                "descriptiom": "product description",
                "price": 100.0,
                "quantity": 10
            }
        }


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None

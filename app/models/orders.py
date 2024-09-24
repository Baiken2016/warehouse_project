from sqlalchemy import Column, Integer, Enum
from app.database import Base
from app.models.common import TimestampMixin, Status
from pydantic import BaseModel
from datetime import datetime

class Order(TimestampMixin, Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(Status), nullable=False, default=Status.IN_PROCESS)
  

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
    

class OrderOut(BaseModel):
    id: int
    created_at: datetime
    status: Status
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: Status
    
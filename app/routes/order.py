from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.orders import OrderCreate, OrderOut, OrderStatusUpdate
from app.database import get_db
from app.services.order import order_service

router = APIRouter()


@router.post("/orders", response_model=OrderOut)
async def create_order(order_create: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await order_service.create_order(order_create=order_create, db=db)


@router.get("/orders", response_model=list[OrderOut])
async def get_orders_list(db: AsyncSession = Depends(get_db)):
    return await order_service.order_list(db=db)


@router.get("/orders/{id}")
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    return await order_service.get_order(order_id=order_id, db=db)


@router.patch("/orders/{id}/status", response_model=OrderOut)
async def update_order_status(order_id: int, order_update: OrderStatusUpdate, db: AsyncSession = Depends(get_db)):
    return await order_service.update_order_status(order_id=order_id, order_update=order_update, db=db)

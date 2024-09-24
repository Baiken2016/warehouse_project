from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order_item import OrderItem
from app.models.orders import Order, OrderCreate, OrderOut, OrderStatusUpdate
from app.database import get_db
from sqlalchemy.future import select

from app.models.products import Product


class OrderService:
    async def create_order(self, order_create: OrderCreate, db: AsyncSession = Depends(get_db)) -> OrderOut:
        new_order = Order()
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        order_out = OrderOut.from_orm(new_order)
        for item in order_create.items:
            product_query = await db.execute(select(Product).where(Product.id == item.product_id))
            product = product_query.scalars().first()
            if not product or product.quantity < item.quantity:
                raise HTTPException(status_code=404, detail=f"The product with id: {item.product_id} not enough")
            product.quantity -= item.quantity
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(order_item)
        await db.commit()
        return order_out

    async def order_list(self, db: AsyncSession = Depends(get_db)) -> list[OrderOut]:
        orders_out = [OrderOut.from_orm(order) for order in (await db.execute(select(Order))).scalars().all()]
        return orders_out

    async def get_order(self, order_id: int, db: AsyncSession = Depends(get_db)) -> OrderOut:
        order = await db.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return OrderOut.from_orm(order)

    async def update_order_status(self, order_id: int, order_update: OrderStatusUpdate,
                                  db: AsyncSession = Depends(get_db)) -> OrderOut:
        order = await db.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        for key, value in order_update.dict(exclude_unset=True).items():
            setattr(order, key, value)
        await db.commit()
        await db.refresh(order)
        return OrderOut.from_orm(order)


order_service = OrderService()

from app.models.products import ProductIn, ProductOut, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from app.database import get_db
from app.models.products import Product
from sqlalchemy.future import select


class ProductService:
    async def create_product(self, product: ProductIn, db: AsyncSession = Depends(get_db)) -> ProductOut:
        db_product = Product(**product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return ProductOut.from_orm(db_product)

    async def list_products(self, db: AsyncSession = Depends(get_db)) -> list[ProductOut]:
        products_out = [ProductOut.from_orm(product) for product in (await db.execute(select(Product))).scalars().all()]
        return products_out

    async def get_product(self, product_id: int, db: AsyncSession = Depends(get_db)):
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def update_product(self, product_id: int, product_update: ProductUpdate,
                             db: AsyncSession = Depends(get_db)) -> ProductOut:
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="product not found")
        for key, value in product_update.dict(exclude_unset=True).items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return ProductOut.from_orm(product)

    async def delete_product(self, product_id: int, db: AsyncSession = Depends(get_db)):
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="product not found")
        await db.delete(product)
        await db.commit()
        return {"message": f"Product deleted, id: {product_id}"}


product_service = ProductService()

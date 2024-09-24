from fastapi import APIRouter, Depends

from app.models.products import ProductOut, Product, ProductIn, ProductUpdate
from app.services.products import product_service
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/products", response_model=list[ProductOut])
async def get_list_products(db: AsyncSession = Depends(get_db)):
    return await product_service.list_products(db=db)


@router.get("/products/{id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await product_service.get_product(product_id=product_id, db=db)


@router.post("/products", response_model=ProductOut)
async def create_product(product: ProductIn, db: AsyncSession = Depends(get_db)):
    return await product_service.create_product(product=product, db=db)


@router.put("/products/{id}")
async def update_product(product_id: int, product_update: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await product_service.update_product(product_id=product_id, product_update=product_update, db=db)

@router.delete("/products/{id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await product_service.delete_product(product_id=product_id, db=db)
from fastapi import FastAPI, HTTPException
from app.database import create_tables
from app.routes.product import router as ProductRouter
from app.routes.order import router as OrderRouter

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    await create_tables()


app.include_router(ProductRouter, tags=["Product"], prefix="/api/v1")
app.include_router(OrderRouter, tags=["Order"], prefix="/api/v1")

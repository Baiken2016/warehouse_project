from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()
database_url = config("SQLALCHEMY_DATABASE_URL")
engine = create_async_engine(database_url, echo=True)

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
import asyncio

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config


engine = create_async_engine(config('PG_DSN_APG'), echo=True)
BaseModel = declarative_base()


class Character(BaseModel):

    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


async def get_async_session(
        drop: bool = False, create: bool = False
):
    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(BaseModel.metadata.drop_all)
        if create:
            await conn.run_sync(BaseModel.metadata.create_all)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session


async def main():
    await get_async_session(True, True)


if __name__ == "__main__":
    asyncio.run(main())

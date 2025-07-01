import asyncio

from app.db.session import AsyncSessionLocal, Base, engine
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization


async def init_db():
    # на случай чистой БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed():
    async with AsyncSessionLocal() as session:
        # здания
        b1 = Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173)
        b2 = Building(address="г. Санкт-Петербург, Невский проспект, 10", latitude=59.9343, longitude=30.3351)
        session.add_all([b1, b2])
        await session.commit()

        # виды деятельности (три уровня вложенности)
        food = Activity(name="Еда")
        meat = Activity(name="Мясная продукция", parent=food)
        dairy = Activity(name="Молочная продукция", parent=food)
        cars = Activity(name="Автомобили")
        trucks = Activity(name="Грузовые", parent=cars)
        parts = Activity(name="Запчасти", parent=cars)
        session.add_all([food, meat, dairy, cars, trucks, parts])
        await session.commit()

        # организации
        org1 = Organization(
            name="ООО Рога и Копыта",
            phone_numbers=["2-222-222", "8-923-666-13-13"],
            building=b1,
            activities=[meat, dairy]
        )
        org2 = Organization(
            name="ЗАО АвтоПлюс",
            phone_numbers=["3-333-333"],
            building=b2,
            activities=[trucks, parts]
        )
        session.add_all([org1, org2])
        await session.commit()

        print("Seed data inserted.")


async def main():
    await init_db()
    await seed()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from beanie import init_beanie
from models.user import User
from motor.motor_asyncio import AsyncIOMotorClient


async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.tarot_bot, document_models=[User])


async def example():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.tarot_bot, document_models=[User])
    user: User = await User.find_one({"telegram_id": 123})
    print(user)
    print(user.category)
    print(user.category.hello())


if __name__ == "__main__":
    asyncio.run(example())

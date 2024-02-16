from beanie import Document
from typing import Optional


class User(Document):
    telegram_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]

    @staticmethod
    async def get_or_create(*, telegram_id: int, **kwargs):
        user = await User.find_one({"telegram_id": telegram_id})

        if user:
            return user

        user = User(telegram_id=telegram_id, **kwargs)
        await user.insert()

        return user

    def __str__(self):
        return f"User<{self.telegram_id}>"

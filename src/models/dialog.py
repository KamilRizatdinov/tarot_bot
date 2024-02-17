from beanie import Document
from typing import Optional
from pydantic import BaseModel
import enum


class MessageRole(enum.Enum):
    SYSTEM = 0
    USER = 1


class DialogMessage(BaseModel):
    message_id: int
    role: MessageRole
    text: Optional[str]


class DialogType(enum.Enum):
    DAILY = 0
    BOOL = 1
    OTHER = 2


class Dialog(Document):
    telegram_id: int
    messages: list[DialogMessage]
    type: Optional[DialogType]

    @staticmethod
    async def get_or_create(*, telegram_id: int):
        dialog = await Dialog.find_one({"telegram_id": telegram_id})

        if dialog:
            return dialog

        dialog = Dialog(telegram_id=telegram_id, messages=[])
        await dialog.insert()

        return dialog

    async def add_message(self, *, telegram_id: int, message: DialogMessage):
        dialog = await Dialog.find_one({"telegram_id": telegram_id})

        if not dialog:
            return None

        dialog.update({"messages": [*dialog.messages, message]})

    def __str__(self):
        return f"Dialog<{self.telegram_id}>"

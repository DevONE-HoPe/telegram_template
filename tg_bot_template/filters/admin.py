from aiogram.filters import BaseFilter
from aiogram.types import Message

from tg_bot_template.core.config import settings

class AdminFilter(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False

        user_id = message.from_user.id

        creator_id = settings.CREATOR_ID

        if user_id == creator_id:
            return True

        return False
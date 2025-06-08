from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio import ConnectionPool, Redis

from tg_bot_template.core.config import settings

token = settings.BOT_TOKEN

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

if settings.IS_PRODUCTION:
    redis_client = Redis(
        connection_pool=ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASS,
            db=0,
        ),
    )

    storage = RedisStorage(
        redis=redis_client,
        key_builder=DefaultKeyBuilder(with_bot_id=True),
    )
else:
    redis_client = None
    storage = MemoryStorage()

dp = Dispatcher(storage=storage)

DEBUG = settings.DEBUG

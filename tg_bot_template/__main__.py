from __future__ import annotations

import asyncio
import uvloop
from loguru import logger
import aioschedule as schedule

from tg_bot_template.core.loader import bot, dp
from tg_bot_template.handlers import get_handlers_router
from tg_bot_template.keyboards.default_commands import (
    remove_default_commands,
    set_default_commands,
)
from tg_bot_template.middlewares import register_middlewares
from tg_bot_template.core.config import settings


async def send_daily_message():
    try:
        message_text = f"{settings.DAILY_MESSAGE_TEXT}"
        await bot.send_message(chat_id=settings.CREATOR_ID, text=message_text)
    except Exception as e:
        logger.error(f"Failed to send daily message: {e}")


async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def on_startup() -> None:
    logger.info("bot starting...")

    register_middlewares(dp)

    dp.include_router(get_handlers_router())

    await set_default_commands(bot)

    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")

    states: dict[bool | None, str] = {
        True: "Enabled",
        False: "Disabled",
        None: "Unknown (This's not a bot)",
    }

    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")

    if settings.DAILY_MESSAGE_ENABLED and settings.CREATOR_ID:
        schedule.every().day.at(settings.DAILY_MESSAGE_TIME).do(send_daily_message)
        asyncio.create_task(run_scheduler())
        logger.info(
            f"Daily message scheduler started ({settings.DAILY_MESSAGE_TIME} daily)"
        )

    logger.info("bot started")


async def on_shutdown() -> None:
    logger.info("bot stopping...")

    await remove_default_commands(bot)

    schedule.clear()

    await dp.storage.close()
    await dp.fsm.storage.close()

    await bot.delete_webhook()
    await bot.session.close()

    logger.info("bot stopped")


async def main() -> None:
    logger.add(
        "logs/TGbot_template.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="100 KB",
        compression="zip",
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    uvloop.run(main())

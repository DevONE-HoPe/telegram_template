from aiogram import Router


def get_handlers_router() -> Router:
    from . import (
        start,
        all_message,
        tap_handler,
        start_game,
        cancel,
        profile,
        help,
        top,
        admin,
    )

    router = Router()
    router.include_router(admin.router)

    router.include_router(start.router)

    router.include_router(help.router)

    router.include_router(cancel.router)

    router.include_router(profile.router)

    router.include_router(top.router)

    router.include_router(tap_handler.router)

    router.include_router(start_game.router)

    router.include_router(all_message.router)

    return router

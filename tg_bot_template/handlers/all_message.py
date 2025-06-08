from aiogram import Router, types

router = Router()


@router.message()
async def catch_all_messages(message: types.Message) -> None:
    pass
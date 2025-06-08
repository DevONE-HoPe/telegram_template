from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import func, select, update

from tg_bot_template.cache.redis import build_key, cached, clear_cache
from tg_bot_template.database.models import UserModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def add_user(
    session: AsyncSession,
    user_id: int,
    username: str | None,
) -> None:
    new_user = UserModel(
        id=user_id,
        username=username,
    )

    session.add(new_user)
    await session.commit()
    await clear_cache(user_exists, user_id)


@cached(key_builder=lambda session, user_id: build_key(user_id))
async def user_exists(session: AsyncSession, user_id: int) -> bool:
    query = select(UserModel.id).filter_by(id=user_id).limit(1)

    result = await session.execute(query)

    user = result.scalar_one_or_none()
    return bool(user)


async def update_user_profile(
    session: AsyncSession,
    user_id: int,
    name: str | None = None,
    info: str | None = None,
    photo: str | None = None,
) -> None:
    update_data = {}
    
    if name is not None:
        update_data['name'] = name
    if info is not None:
        update_data['info'] = info
    if photo is not None:
        update_data['photo'] = photo
    
    if update_data:
        stmt = update(UserModel).where(UserModel.id == user_id).values(**update_data)
        await session.execute(stmt)
        await session.commit()


async def increment_user_taps(
    session: AsyncSession,
    user_id: int,
) -> None:
    stmt = update(UserModel).where(UserModel.id == user_id).values(
        taps=UserModel.taps + 1
    )
    
    await session.execute(stmt)
    await session.commit()


async def get_top_users_by_taps(
    session: AsyncSession,
    limit: int = 1,
) -> list[UserModel]:
    query = (
        select(UserModel)
        .where(UserModel.taps > 0)
        .order_by(UserModel.taps.desc())
        .limit(limit)
    )
    
    result = await session.execute(query)
    users = result.scalars().all()
    
    return list(users)


@cached(key_builder=lambda session: build_key())
async def get_user_count(session: AsyncSession) -> int:
    query = select(func.count()).select_from(UserModel)

    result = await session.execute(query)

    count = result.scalar_one_or_none() or 0
    return int(count)

async def get_user_taps(session: AsyncSession, user_id: int) -> int:
    query = select(UserModel.taps).filter_by(id=user_id)
    
    result = await session.execute(query)
    taps = result.scalar_one_or_none()
    
    return taps or 0

async def get_total_taps(session: AsyncSession) -> int:
    query = select(func.sum(UserModel.taps))
    
    result = await session.execute(query)
    total_taps = result.scalar_one_or_none()
    
    return total_taps or 0
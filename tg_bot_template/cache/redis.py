from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar

from tg_bot_template.cache.serialization import AbstractSerializer, PickleSerializer
from tg_bot_template.core.loader import redis_client
from tg_bot_template.core.config import settings

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from datetime import timedelta

    from redis.asyncio import Redis


DEFAULT_TTL = 10

_Func = TypeVar("_Func")
Args = str | int  # basically only user_id is used as identifier
Kwargs = Any


def build_key(*args: Args, **kwargs: Kwargs) -> str:
    """Build a string key based on provided arguments and keyword arguments."""
    args_str = ":".join(map(str, args))
    kwargs_str = ":".join(f"{key}={value}" for key, value in sorted(kwargs.items()))
    return f"{args_str}:{kwargs_str}"


def _check_redis_availability() -> None:
    """Check if Redis is available. Raise error in production if not."""
    if redis_client is None and settings.IS_PRODUCTION:
        raise RuntimeError(
            "Redis client is not available in production mode. Please configure Redis connection."
        )


async def set_redis_value(
    key: bytes | str,
    value: bytes | str,
    ttl: int | timedelta | None = DEFAULT_TTL,
    is_transaction: bool = False,
) -> None:
    """Set a value in Redis with an optional time-to-live (TTL)."""
    _check_redis_availability()

    if redis_client is None:
        return

    async with redis_client.pipeline(transaction=is_transaction) as pipeline:
        await pipeline.set(key, value)
        if ttl:
            await pipeline.expire(key, ttl)

        await pipeline.execute()


def cached(
    ttl: int | timedelta = DEFAULT_TTL,
    namespace: str = "main",
    cache: Redis = redis_client,
    key_builder: Callable[..., str] = build_key,
    serializer: AbstractSerializer | None = None,
) -> Callable[[Callable[..., Awaitable[_Func]]], Callable[..., Awaitable[_Func]]]:
    """Caches the function's return value into a key generated with module_name, function_name, and args.

    Args:
        ttl (int | timedelta): Time-to-live for the cached value.
        namespace (str): Namespace for cache keys.
        cache (Redis): Redis instance for storing cached data.
        key_builder (Callable[..., str]): Function to build cache keys.
        serializer (AbstractSerializer | None): Serializer for cache data.

    Returns:
        Callable: A decorator that wraps the original function with caching logic.

    """
    if serializer is None:
        serializer = PickleSerializer()

    def decorator(
        func: Callable[..., Awaitable[_Func]],
    ) -> Callable[..., Awaitable[_Func]]:
        @wraps(func)
        async def wrapper(*args: Args, **kwargs: Kwargs) -> Any:
            _check_redis_availability()

            if cache is None:
                return await func(*args, **kwargs)

            key = key_builder(*args, **kwargs)
            key = f"{namespace}:{func.__module__}:{func.__name__}:{key}"

            # Check if the key is in the cache
            cached_value = await cache.get(key)
            if cached_value is not None:
                return serializer.deserialize(cached_value)

            # If not in cache, call the original function
            result = await func(*args, **kwargs)

            # Store the result in Redis
            await set_redis_value(
                key=key,
                value=serializer.serialize(result),
                ttl=ttl,
            )

            return result

        return wrapper

    return decorator


async def clear_cache(
    func: Callable[..., Awaitable[Any]],
    *args: Args,
    **kwargs: Kwargs,
) -> None:
    """Clear the cache for a specific function and arguments.

    Parameters
    ----------
    - func (Callable): The target function for which the cache needs to be cleared.
    - args (Args): Positional arguments passed to the function.
    - kwargs (Kwargs): Keyword arguments passed to the function.

    Keyword Arguments:
    - namespace (str, optional): A string indicating the namespace for the cache. Defaults to "main".

    """
    _check_redis_availability()

    if redis_client is None:
        return

    namespace = kwargs.get("namespace", "main")

    key = build_key(*args, **kwargs)
    key = f"{namespace}:{func.__module__}:{func.__name__}:{key}"

    await redis_client.delete(key)

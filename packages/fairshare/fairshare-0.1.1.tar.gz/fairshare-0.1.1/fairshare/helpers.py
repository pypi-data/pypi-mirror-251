import asyncio
from typing import Type, AsyncGenerator
from uuid import uuid4

from redis._parsers.base import AsyncBaseParser
from redis.asyncio import Redis, BlockingConnectionPool

from .patches import PatchedAsyncHiredisParser


def get_id() -> str:
    try:
        from xxhash import xxh3_64_hexdigest
        return xxh3_64_hexdigest(str(uuid4()))
    except ImportError:
        return str(uuid4())


def init_redis(
        url: str,
        timeout: int | None = 300,
        encoding: str = "utf-8",
        parser_class: Type[AsyncBaseParser] = PatchedAsyncHiredisParser,
        max_connections: int = 100,
        decode_responses: bool = True,
) -> Redis:
    pool = BlockingConnectionPool.from_url(
        url,
        timeout=timeout,
        encoding=encoding,
        parser_class=parser_class,
        max_connections=max_connections,
        decode_responses=decode_responses,
    )
    return Redis(connection_pool=pool)


async def poll_limiter(step: float = 0.5) -> AsyncGenerator[float, None]:
    loop = asyncio.get_event_loop()
    start = loop.time()
    while True:
        before = loop.time()
        yield before - start
        after = loop.time()
        wait = max([0, step - after + before])
        await asyncio.sleep(wait)

from datetime import timedelta
from pathlib import Path
from typing import AsyncGenerator, Type, List

from redis.asyncio import Redis

from .base import BaseMessage, BaseSerializer
from .helpers import poll_limiter
from .patches import PatchedAsyncScript
from .serializers import JSONSerializer

SCRIPTS_DIR = Path(__file__).parent / "scripts"


class FairQueue:
    PREFIX: str = "fair"
    SHARES_SUFFIX: str = "shares"
    MESSAGES_SUFFIX: str = "messages"
    READY_SHARES_SUFFIX: str = ":".join([SHARES_SUFFIX, "ready"])
    RANGED_SHARES_SUFFIX: str = ":".join([SHARES_SUFFIX, "ranged"])
    UNACKED_SHARES_SUFFIX: str = ":".join([SHARES_SUFFIX, "unacked"])
    PENDING_SHARES_SUFFIX: str = ":".join([SHARES_SUFFIX, "pending"])
    PENDING_MESSAGES_SUFFIX: str = ":".join([MESSAGES_SUFFIX, "pending"])

    def __init__(
            self,
            name: str,
            client: Redis,
            acks_auto: bool = True,
            acks_late: bool = False,
            acks_timeout: timedelta = timedelta(minutes=15),
            serializer_class: Type[BaseSerializer] = JSONSerializer,
    ):
        self._name = name
        self._client = client
        self._acks_auto = acks_auto
        self._acks_late = acks_late
        self._acks_timeout = acks_timeout
        self._serializer_class = serializer_class
        with open(SCRIPTS_DIR / "get.lua", "rb") as file:
            self._script = PatchedAsyncScript(client, file.read())
        with open(SCRIPTS_DIR / "put.lua", "rb") as file:
            self._put_script = PatchedAsyncScript(client, file.read())
        with open(SCRIPTS_DIR / "ack.lua", "rb") as file:
            self._ack_script = PatchedAsyncScript(client, file.read())

    async def get(self, count: int = 1) -> List[BaseMessage]:
        messages = []

        response = await self._script(
            keys=(
                self._ready_shares_key,
                self._ranged_shares_key,
                self._unacked_shares_key,
                self._pending_shares_key,
            ),
            args=(
                count,
                self._acks_timeout.total_seconds(),
                self._messages_prefix,
                self._pending_messages_prefix,
            ),
        )

        for record in response:
            messages.append(
                self._serializer_class().deserialize(
                    record
                )
            )

        return messages

    async def put(
            self,
            message: BaseMessage,
            _limit: int = -1,
            _defer_by: timedelta = timedelta(seconds=0),
            _expire_in: timedelta = timedelta(hours=24 * 7),
    ) -> bool:
        response = await self._put_script(
            keys=(
                self._get_message_key(
                    message.id
                ),
                self._pending_shares_key,
                self._get_pending_messages_key(message.share_id),
            ),
            args=(
                message.share_id, message.id,
                self._serializer_class().serialize(message),
                _limit, _defer_by.total_seconds(), _expire_in.total_seconds()
            ),
        )
        return bool(response)

    async def ack(self, message: BaseMessage) -> None:
        await self._ack_script(
            keys=(
                self._get_message_key(
                    message.id
                ),
                self._pending_shares_key,
                self._unacked_shares_key,
                self._get_pending_messages_key(message.share_id),
            ),
            args=(
                message.share_id,
                message.id,
            ),
        )

    async def poll(self, prefetch_count: int = 10) -> AsyncGenerator[BaseMessage, None]:
        async for _ in poll_limiter(1.0):
            for message in await self.get(prefetch_count):
                if self._acks_auto and not self._acks_late:
                    await self.ack(message)
                yield message
                if self._acks_auto and self._acks_late:
                    await self.ack(message)

    async def flush(self, count: int = 1000) -> None:
        """
            Remove all keys associated with this queue
        :return:
        """
        cursor = 0
        pattern = f"{self.PREFIX}:{self._name}*"

        while True:
            cursor, keys = await self._client.scan(
                cursor, match=pattern, count=count
            )
            if keys:
                await self._client.delete(*keys)
            if cursor == 0:
                break

    @property
    def _messages_prefix(self) -> str:
        return self._get_redis_key(
            self.MESSAGES_SUFFIX
        )

    @property
    def _ready_shares_key(self) -> str:
        return self._get_redis_key(
            self.READY_SHARES_SUFFIX,
        )

    @property
    def _ranged_shares_key(self) -> str:
        return self._get_redis_key(
            self.RANGED_SHARES_SUFFIX,
        )

    @property
    def _unacked_shares_key(self) -> str:
        return self._get_redis_key(
            self.UNACKED_SHARES_SUFFIX,
        )

    @property
    def _pending_shares_key(self) -> str:
        return self._get_redis_key(
            self.PENDING_SHARES_SUFFIX,
        )

    @property
    def _pending_messages_prefix(self) -> str:
        return self._get_redis_key(
            self.PENDING_MESSAGES_SUFFIX
        )

    def _get_redis_key(self, *parts: str) -> str:
        return ":".join([self.PREFIX, self._name, *parts])

    def _get_message_key(self, message_id: str) -> str:
        return ":".join([self._messages_prefix, message_id])

    def _get_pending_messages_key(self, share_id: str) -> str:
        return ":".join([self._pending_messages_prefix, share_id])

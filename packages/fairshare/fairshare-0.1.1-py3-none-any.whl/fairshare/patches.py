from typing import Iterable, Sequence
from typing import Union, List

from redis._parsers import _AsyncHiredisParser
from redis._parsers.socket import SERVER_CLOSED_CONNECTION_ERROR
from redis.asyncio import Redis
from redis.client import NEVER_DECODE
from redis.commands.core import AsyncScript
from redis.exceptions import NoScriptError
from redis.typing import EncodableT
from redis.typing import KeyT


class PatchedAsyncScript(AsyncScript):

    async def __call__(
            self,
            keys: Union[Sequence[KeyT], None] = None,
            args: Union[Iterable[EncodableT], None] = None,
            client: Union["Redis", None] = None,
    ):
        """Execute the script, passing any required ``args``"""
        keys = keys or []
        args = args or []
        if client is None:
            client = self.registered_client
        args = tuple(keys) + tuple(args)
        # make sure the Redis server knows about the script
        from redis.asyncio.client import Pipeline

        if isinstance(client, Pipeline):
            # Make sure the pipeline can register the script before executing.
            client.scripts.add(self)
        try:
            return await client.execute_command(
                "EVALSHA", self.sha, len(keys), *args, **{NEVER_DECODE: 1}
            )
        except NoScriptError:
            # Maybe the client is pointed to a different server than the client
            # that created this instance?
            # Overwrite the sha just in case there was a discrepancy.
            self.sha = await client.script_load(self.script)
            return await client.execute_command(
                "EVALSHA", self.sha, len(keys), *args, **{NEVER_DECODE: 1}
            )


class PatchedAsyncHiredisParser(_AsyncHiredisParser):
    async def read_response(
            self, disable_decoding: bool = False
    ) -> Union[EncodableT, List[EncodableT]]:
        # If `on_disconnect()` has been called, prohibit any more reads
        # even if they could happen because data might be present.
        # We still allow reads in progress to finish
        if not self._connected:
            raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR) from None

        if disable_decoding:
            response = self._reader.gets(False)
        else:
            response = self._reader.gets()

        while response is False:
            await self.read_from_socket()
            if disable_decoding:
                response = self._reader.gets(False)
            else:
                response = self._reader.gets()

        # if the response is a ConnectionError or the response is a list and
        # the first item is a ConnectionError, raise it as something bad
        # happened
        if isinstance(response, ConnectionError):
            raise response
        elif (
                isinstance(response, list)
                and response
                and isinstance(response[0], ConnectionError)
        ):
            raise response[0]
        return response

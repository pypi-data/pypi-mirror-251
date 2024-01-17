from __future__ import annotations

from base64 import b64decode
from functools import cached_property
from ssl import SSLContext, create_default_context
from tempfile import NamedTemporaryFile
from types import TracebackType
from typing import Literal, Type
from urllib.parse import urljoin

from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager
from structlog import get_logger

from kludge.konfig import Konfig

logger = get_logger()


class Klient:
    def __init__(self, konfig: Konfig):
        self.konfig = konfig

        self._session: ClientSession | None = None

    async def session(self) -> ClientSession:
        if self._session is not None:
            return self._session

        self._session = ClientSession()
        return self._session

    async def __aenter__(self) -> Klient:
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await (await self.session()).close()

    @cached_property
    def sslcontext(self) -> SSLContext:
        cluster = self.konfig.clusters[0].cluster
        user = self.konfig.users[0].user

        context = create_default_context(
            cafile=cluster.certificate_authority,
            cadata=b64decode(cluster.certificate_authority_data).decode("utf-8")
            if cluster.certificate_authority_data
            else None,
        )

        # Work around Python's ssl lib not support client certs as data instead of files
        # https://github.com/encode/httpx/discussions/2037#discussioncomment-2006795
        if user.client_certificate_data and user.client_key_data:
            with NamedTemporaryFile(mode="w+b") as certfile, NamedTemporaryFile() as keyfile:
                certfile.write(b64decode(user.client_certificate_data))
                certfile.seek(0)

                keyfile.write(b64decode(user.client_key_data))
                keyfile.seek(0)

                context.load_cert_chain(
                    certfile=certfile.name,
                    keyfile=keyfile.name,
                )
        elif user.client_certificate is not None and user.client_key is not None:
            context.load_cert_chain(
                certfile=user.client_certificate,
                keyfile=user.client_key,
            )
        else:
            raise Exception("No client certificate or key provided")

        return context

    def url(self, path: str) -> str:
        return urljoin(self.konfig.clusters[0].cluster.server, path)

    async def request(self, method: Literal["get"], path: str) -> _RequestContextManager:
        return (await self.session()).request(
            method=method,
            url=self.url(path),
            ssl=self.sslcontext,
        )

from asyncio import sleep

from counterweight.components import component
from counterweight.elements import Div, Text
from counterweight.hooks import use_effect, use_state
from counterweight.styles.utilities import *
from structlog import get_logger

from kludge.klient import Klient
from kludge.konfig import Konfig

logger = get_logger()


@component
def root() -> Div:
    pods, set_pods = use_state([])  # type: ignore[var-annotated]

    async def fetch() -> None:
        async with Klient(Konfig.build()) as klient:
            while True:
                logger.info("fetching")

                async with await klient.request(
                    method="get",
                    path="/api/v1/namespaces/ping-pong/pods",
                ) as response:
                    j = await response.json()

                set_pods(j["items"])
                logger.info("fetched", j=j)

                await sleep(2)

    use_effect(fetch, ())

    return Div(
        style=col | border_lightrounded | pad_x_1,
        children=[
            Text(
                style=weight_none,
                content=pod["metadata"]["name"],
            )
            for pod in pods
        ],
    )

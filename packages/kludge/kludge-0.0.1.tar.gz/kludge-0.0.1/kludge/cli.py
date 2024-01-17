from asyncio import run
from textwrap import dedent

from counterweight.app import app
from typer import Typer

from kludge.app import root
from kludge.constants import PACKAGE_NAME

cli = Typer(
    name=PACKAGE_NAME,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help=dedent(
        """\
        """
    ),
)


@cli.command()
def kludge() -> None:
    async def _() -> None:
        await app(root)

    run(_())

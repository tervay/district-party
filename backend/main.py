import asyncio
from asyncio import TaskGroup, run, sleep
from functools import wraps
from typing import Any, Dict, List

import click
from aiohttp import ClientSession, TCPConnector
from tbapy import TBA

from getters import get_all_teams
from impls import RealDistricts

from api import app


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@coro
async def team_events():
    # print(len(await get_all_teams(2024)))
    # print(await fim.get_team_keys(2024))
    # print(RealDistricts.ALL)
    await RealDistricts.generate_annual_infos()


@cli.command()
def api():
    app.run(debug=True)


if __name__ == "__main__":
    cli()

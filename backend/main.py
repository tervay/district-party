import asyncio
import json
import os
from asyncio import TaskGroup, run, sleep
from functools import wraps
from typing import Any, Dict, List

import click
from aiohttp import ClientSession, TCPConnector
from api import app
from api_types import DistrictInfo
from getters import get_all_teams
from impls import RealDistricts
from tbapy import TBA
from tqdm import tqdm

import processors


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
def process_data():
    process_fns = [
        processors.process_district_index,
    ]

    root_dir = "data/out/"
    for subdir in (pbar := tqdm(os.listdir(root_dir))):
        # if subdir != "ne":
        #     continue

        subdir_path = os.path.join(root_dir, subdir)
        pbar.set_description(f"{subdir}")

        if os.path.isdir(subdir_path):
            annual_infos_path = os.path.join(subdir_path, "annual_info.json")
            if os.path.exists(annual_infos_path):
                with open(annual_infos_path, "r") as file:
                    annual_data: DistrictInfo = DistrictInfo.from_dict(json.load(file))

                    for fn in tqdm(process_fns, position=1, leave=False):
                        fn(annual_data)


@cli.command()
def api():
    app.run(debug=True)


if __name__ == "__main__":
    cli()

import dataclasses
import json
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

from api_types import (
    AnnualInfo,
    AnnualSlots,
    DistrictInfo,
    DistrictSummary,
    SimpleTeam,
    DistrictRanking,
)
from getters import get_all_teams_by_keys, get_team_events, tba, get_district_rankings
from numpyencoder import NumpyEncoder
from tqdm import tqdm
from yaml import Loader, load
from util import us_state_to_abbrev, can_province_abbrev

CURRENT_YEAR = 2024


class District(ABC):
    district_key: str
    first_year: int
    slots: Dict[int, AnnualSlots]
    name: str

    def __init__(
        self,
        district_key: str,
        first_year: int,
        slots: Dict[int, AnnualSlots],
        name: str,
    ) -> None:
        self.district_key = district_key
        self.first_year = first_year
        self.slots = slots
        self.name = name

    @abstractmethod
    async def get_team_keys(self, year: int) -> List[str]:
        pass

    @abstractmethod
    async def get_event_keys(self, year: int) -> List[str]:
        pass


class RealDistrict(District):
    def __init__(
        self,
        district_key: str,
        first_year: int,
        slots: Dict[int, AnnualSlots],
        name: str,
    ) -> None:
        super().__init__(district_key, first_year, slots, name)

    async def get_event_keys(self, year: int) -> List[str]:
        return [
            e["key"]
            for e in tba.events(year=year)
            if (
                e["district"] is not None
                and e["district"]["abbreviation"] == self.district_key
            )
        ]

    async def get_team_keys(self, year: int) -> List[str]:
        return sorted(
            [
                r["team_key"]
                for r in tba.district_rankings(district=f"{year}{self.district_key}")
            ],
            key=lambda k: int(k[3:]),
        )


class FakeDistrict(District):
    def __init__(
        self,
        district_key: str,
        first_year: int,
        slots: Dict[int, AnnualSlots],
        name: str,
    ) -> None:
        super().__init__(district_key, first_year, slots, name)


class RealDistricts:
    ALL: List[RealDistrict] = []

    @classmethod
    def load(cls):
        with open("data/config/real_districts.yml", "r") as f:
            data = load(f, Loader=Loader)
            for rd in data:
                cls.ALL.append(
                    RealDistrict(
                        district_key=rd["key"],
                        first_year=rd["first_year"],
                        slots={
                            year: AnnualSlots(
                                total=slot_breakdown["total"],
                                impact=slot_breakdown["impact"],
                                ei=slot_breakdown["ei"],
                                ras=slot_breakdown["ras"],
                                dlf=slot_breakdown["dlf"],
                                wffa=slot_breakdown["wffa"],
                            )
                            for year, slot_breakdown in rd["slots"].items()
                        },
                        name=rd["name"],
                    )
                )

    @classmethod
    async def generate_annual_infos(cls):
        district_infos: Dict[str, DistrictInfo] = {}

        for rd in (pb1 := tqdm(cls.ALL, position=0, leave=False)):
            all_teams: Set[str] = set()
            annual_infos: Dict[int, AnnualInfo] = {}
            active_years = defaultdict(list)

            pb1.set_description(rd.district_key.rjust(3))
            for year in (
                pb2 := tqdm(
                    [
                        y
                        for y in range(rd.first_year, CURRENT_YEAR + 1)
                        if y not in [2020, 2021]
                    ],
                    position=1,
                    leave=False,
                )
            ):
                pb2.set_description(str(year))
                tks = await rd.get_team_keys(year=year)
                eks = await rd.get_event_keys(year=year)

                team_events, events = await get_team_events(
                    team_keys=tks,
                    event_keys=eks,
                    pbar_maker=lambda l: tqdm(l, position=2, leave=False),
                )

                all_teams.update(team_events.keys())
                for k in team_events.keys():
                    active_years[k].append(year)

                ai = AnnualInfo(
                    year=year,
                    team_keys=list(team_events.keys()),
                    team_events=team_events,
                    slots=rd.slots.get(
                        year, AnnualSlots(total=0, impact=0, ei=0, ras=0, dlf=0, wffa=0)
                    ),
                    events=events,
                    rankings=[
                        DistrictRanking(
                            qualifying_points_individual=[
                                e["total"]
                                for e in r["event_points"]
                                if not e["district_cmp"]
                            ],
                            qualifying_points_total=sum(
                                e["total"]
                                for e in r["event_points"]
                                if not e["district_cmp"]
                            ),
                            dcmp_points=sum(
                                e["total"]
                                for e in r["event_points"]
                                if e["district_cmp"]
                            ),
                            rank=r["rank"],
                            age_bonus=r["rookie_bonus"],
                            team_key=r["team_key"],
                        )
                        for r in (
                            await get_district_rankings(
                                district_key=rd.district_key, year=year
                            )
                        )
                        if (r["point_total"] - r["rookie_bonus"]) > 0
                    ],
                )
                annual_infos[year] = ai

            team_infos = await get_all_teams_by_keys(list(all_teams))

            district_infos[rd.district_key] = DistrictInfo(
                annual_info=annual_infos,
                summary=DistrictSummary(
                    all_teams={
                        k: SimpleTeam(
                            key=k,
                            number=int(k[3:]),
                            city=t["city"],
                            state_prov={
                                "USA": us_state_to_abbrev,
                                "Canada": can_province_abbrev,
                            }
                            .get(t["country"], {})
                            .get(t["state_prov"], t["state_prov"]),
                            country=t["country"],
                            name=t["nickname"],
                            rookie_year=t["rookie_year"],
                            active_years=active_years[k],
                        )
                        for k, t in team_infos.items()
                    },
                    first_year=rd.first_year,
                    key=rd.district_key,
                    name=rd.name,
                ),
            )

            Path(f"data/out/{rd.district_key}/").mkdir(parents=True, exist_ok=True)
            with open(f"data/out/{rd.district_key}/annual_info.json", "w+") as f:
                json.dump(
                    dataclasses.asdict(district_infos[rd.district_key]),
                    f,
                    indent=2,
                    sort_keys=True,
                    cls=NumpyEncoder,
                )


RealDistricts.load()

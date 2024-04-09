import asyncio
import csv
import itertools
from collections import defaultdict
from typing import Any, Dict, List, Tuple, TypedDict, Union

from aiohttp import ClientSession, TCPConnector
from tbapy import TBA

from api_types import (
    Alliance,
    Award,
    Event,
    EventType,
    Record,
    TeamEvent,
    TeamEventEPA,
    PlayoffType,
    DoubleElimRound,
    AlliancePlacement,
)

KEY = "1EhUOwczJi4vDUXza94fAo7s4UFrKgBrTJ6A3MTeYR0WrgzlyGR0Tzyl1TN2P6Tu"
tba = TBA(KEY)
TBA_HEADERS: Dict[str, str] = {"X-TBA-Auth-Key": KEY}


class TBATeam(TypedDict):
    address: None
    city: str
    country: str
    gmaps_place_id: None
    gmaps_url: None
    key: str
    lat: None
    lng: None
    location_name: None
    motto: None
    name: str
    nickname: str
    postal_code: Union[str, None]
    rookie_year: int
    school_name: str
    state_prov: str
    team_number: int
    website: Union[str, None]


async def fetch_json(session: ClientSession, url: str) -> Any:
    async with session.get(url, headers=TBA_HEADERS) as response:
        return await response.json()


async def fetch_all(urls: List[str]) -> List[Any]:
    connector = TCPConnector(limit=32)
    async with ClientSession(connector=connector) as session:
        tasks = [fetch_json(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def flatten(l: List[List]) -> List:
    return [x for xs in l for x in xs]


def tba_url(endpoint: str) -> str:
    return f"https://www.thebluealliance.com/api/v3/{endpoint}"


async def get_all_teams(year: int) -> List[TBATeam]:
    return flatten(
        await fetch_all([tba_url(f"teams/{year}/{x}") for x in range(0, 20)])
    )


async def get_event_teams_keys(keys: List[str]) -> Dict[str, List[str]]:
    l = await fetch_all([tba_url(f"event/{k}/teams/keys") for k in keys])
    return dict(zip(keys, l))


async def get_all_teams_by_keys(keys: List[str]) -> Dict[str, TBATeam]:
    return dict(zip(keys, await fetch_all([tba_url(f"team/{k}") for k in keys])))


async def get_team_events(
    team_keys: List[str], event_keys: List[str], pbar_maker=None
) -> Tuple[Dict[str, List[TeamEvent]], List[Event]]:

    statbotics_team_events = []
    with open("data/statbotics/team_events.csv", "r") as f:
        reader = csv.DictReader(f)
        statbotics_team_events = list(reader)

    team_events = defaultdict(list)

    event_infos = dict(
        zip(event_keys, await fetch_all([tba_url(f"event/{k}") for k in event_keys]))
    )
    event_statuses = dict(
        zip(
            event_keys,
            await fetch_all([tba_url(f"event/{k}/teams/statuses") for k in event_keys]),
        )
    )
    event_dpts = dict(
        zip(
            event_keys,
            await fetch_all(
                [tba_url(f"event/{k}/district_points") for k in event_keys]
            ),
        )
    )
    event_matches = dict(
        zip(
            event_keys,
            await fetch_all([tba_url(f"event/{k}/matches/simple") for k in event_keys]),
        )
    )
    event_awards = dict(
        zip(
            event_keys,
            await fetch_all([tba_url(f"event/{k}/awards") for k in event_keys]),
        )
    )
    event_rankings = dict(
        zip(
            event_keys,
            await fetch_all([tba_url(f"event/{k}/rankings") for k in event_keys]),
        )
    )
    event_alliances = dict(
        zip(
            event_keys,
            await fetch_all([tba_url(f"event/{k}/alliances") for k in event_keys]),
        )
    )

    team_event_combos = itertools.product(team_keys, event_keys)
    iterable = (
        team_event_combos if pbar_maker is None else pbar_maker(list(team_event_combos))
    )
    for tk, ek in iterable:
        if pbar_maker is not None:
            iterable.set_description(f"{tk[3:].rjust(4)} @ {ek.ljust(10)}")

        if tk not in event_statuses[ek] or tk not in event_dpts[ek]["points"]:
            continue

        award_only = event_statuses[ek][tk]["last_match_key"] is None

        epa_data = None
        if not award_only:
            maybe_sb_data = list(
                filter(
                    lambda r: r["event"] == ek and r["team"] == tk[3:],
                    statbotics_team_events,
                )
            )

            if len(maybe_sb_data) > 0:
                epa_data = maybe_sb_data[0]

        if epa_data is None and not award_only:
            continue

        qual_record = (
            None
            if (
                award_only
                or event_infos[ek]["year"] == 2015
                or len(event_infos[ek]["division_keys"]) > 0
            )
            else Record(
                won=int(epa_data["qual_wins"]),
                lost=int(epa_data["qual_losses"]),
                tied=int(epa_data["qual_ties"]),
            )
        )

        elim_record = (
            None
            if (
                award_only
                or event_infos[ek]["year"] == 2015
                or event_statuses[ek][tk]["playoff"] is None
            )
            else Record(
                won=int(epa_data["wins"]) - int(epa_data["qual_wins"]),
                lost=int(epa_data["losses"]) - int(epa_data["qual_losses"]),
                tied=int(epa_data["ties"]) - int(epa_data["qual_ties"]),
            )
        )

        total_record = (
            None
            if (qual_record is None and elim_record is None)
            else [qual_record, elim_record][qual_record is None].add(
                [elim_record, qual_record][qual_record is None]
            )
        )

        team_events[tk].append(
            TeamEvent(
                team_key=tk,
                event_key=ek,
                event_type=event_infos[ek]["event_type"],
                award_only_appearance=award_only,
                qual_pts=event_dpts[ek]["points"][tk]["qual_points"],
                alliance_pts=event_dpts[ek]["points"][tk]["alliance_points"],
                elim_pts=event_dpts[ek]["points"][tk]["elim_points"],
                award_pts=event_dpts[ek]["points"][tk]["award_points"],
                total_pts=event_dpts[ek]["points"][tk]["total"],
                awards_received=[
                    award["award_type"]
                    for award in event_awards[ek]
                    if any(
                        recipient["team_key"] == tk
                        for recipient in award["recipient_list"]
                    )
                ],
                qual_record=qual_record,
                elim_record=elim_record,
                total_record=total_record,
                match_keys=[
                    m["key"]
                    for m in event_matches[ek]
                    if (
                        tk in m["alliances"]["blue"]["team_keys"]
                        or tk in m["alliances"]["red"]["team_keys"]
                    )
                ],
                epa=(
                    None
                    if epa_data is None
                    else TeamEventEPA(
                        mean=epa_data["epa_mean"],
                        sd=epa_data["epa_sd"],
                        start=epa_data["epa_start"],
                        normalized=epa_data["norm_epa"],
                    )
                ),
            )
        )

    events: List[Event] = []
    for ek in event_keys:
        alliances = []
        for tba_alliance in event_alliances[ek] or []:
            placement = AlliancePlacement.NOT_YET_IMPLEMENTED

            if event_infos[ek]["playoff_type"] == PlayoffType.DOUBLE_ELIM_8_TEAM:
                if (
                    tba_alliance["status"]["double_elim_round"]
                    == DoubleElimRound.FINALS
                ):
                    placement = {
                        "eliminated": AlliancePlacement.FINALIST,
                        "won": AlliancePlacement.WINNER,
                    }[tba_alliance["status"]["status"]]
                else:
                    placement = {
                        DoubleElimRound.ROUND5: AlliancePlacement.DE_THIRD,
                        DoubleElimRound.ROUND4: AlliancePlacement.DE_FOURTH,
                        DoubleElimRound.ROUND3: AlliancePlacement.DE_FIFTH_SIXTH,
                        DoubleElimRound.ROUND2: AlliancePlacement.DE_SEVENTH_EIGHTH,
                    }[tba_alliance["status"]["double_elim_round"]]

            elif event_infos[ek]["playoff_type"] in [
                PlayoffType.BRACKET_8_TEAM,
                PlayoffType.BRACKET_16_TEAM,
            ]:
                if tba_alliance["status"]["status"] == "won":
                    placement = AlliancePlacement.WINNER
                else:
                    placement = {
                        "f": AlliancePlacement.FINALIST,
                        "sf": AlliancePlacement.SE_SEMIS,
                        "qf": AlliancePlacement.SE_QUARTERS,
                        "ef": AlliancePlacement.SE_EIGHTHS,
                    }[tba_alliance["status"]["level"]]

            alliances.append(
                Alliance(
                    teams=tba_alliance["picks"],
                    captain=tba_alliance["picks"][0],
                    first_pick=tba_alliance["picks"][1],
                    second_pick=tba_alliance["picks"][2],
                    backup=(
                        None
                        if len(tba_alliance["picks"]) <= 3
                        else tba_alliance["picks"][3]
                    ),
                    placement=placement,
                )
            )

        events.append(
            Event(
                key=ek,
                start_date=event_infos[ek]["start_date"],
                end_date=event_infos[ek]["end_date"],
                code=event_infos[ek]["event_code"],
                name=event_infos[ek]["name"],
                short_name=event_infos[ek]["short_name"],
                city=event_infos[ek]["city"],
                state_prov=event_infos[ek]["state_prov"],
                country=event_infos[ek]["country"],
                week=event_infos[ek]["week"],
                year=event_infos[ek]["year"],
                event_type=event_infos[ek]["event_type"],
                awards=flatten(
                    [
                        Award(
                            award_type=a["award_type"],
                            recipient_team=recipient["team_key"],
                        )
                        for recipient in a["recipient_list"]
                        if recipient["team_key"] is not None
                    ]
                    for a in event_awards[ek]
                ),
                district_pts=event_dpts[ek]["points"],
                matches=event_matches[ek],
                alliances=alliances,
                rankings=event_rankings[ek]["rankings"],
            )
        )

    return dict(team_events), events

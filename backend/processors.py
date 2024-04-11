import dataclasses
import json
from collections import Counter, defaultdict
from typing import Dict, List

from api_types import DistrictInfo, DistrictRanking, EventType, AlliancePlacement
from util import Averager, avg, district_years, write_district_data


def avg_nth_event(qualifying_points_individual: List[List[int]], n: int) -> int:
    a = Averager()

    for year in qualifying_points_individual:
        if n < len(year):
            a.feed(year[n])

    return a.get()


def process_district_index(info: DistrictInfo):
    team_data = []
    for tk, t in info.summary.all_teams.items():
        obj = {
            "team": dataclasses.asdict(t),
            "record": {"wins": 0, "losses": 0, "ties": 0},
            "dcmps": 0,
            "epa": info.annual_info[t.active_years[-1]]
            .team_events[t.key][-1]
            .epa.normalized,
            "avg_dpts": 0,
        }

        dpts_averager = Averager()
        for y in t.active_years:
            team_events = info.annual_info[y].team_events[t.key]
            for te in team_events:
                if te.total_record is not None:
                    obj["record"]["wins"] += te.total_record.won
                    obj["record"]["losses"] += te.total_record.lost
                    obj["record"]["ties"] += te.total_record.tied

            first_two_plays = [
                te
                for te in sorted(team_events, key=lambda x: x.event_week)
                if te.event_type == EventType.DISTRICT
            ][:2]

            dpts_averager.feed_many([x.total_pts for x in first_two_plays])

            if (
                dcmp := next(
                    filter(
                        lambda te: te.event_type
                        in [EventType.DISTRICT_CMP, EventType.DISTRICT_CMP_DIVISION],
                        team_events,
                    ),
                    None,
                )
            ) is not None:
                obj["dcmps"] += 1

        obj["avg_dpts"] = dpts_averager.get()
        team_data.append(obj)

    rankings = {}
    team_rankings: Dict[List[DistrictRanking]] = defaultdict(list)
    for y in district_years(info.summary.first_year):
        rankings[str(y)] = sorted(
            info.annual_info[y].rankings,
            key=lambda r: r.rank,
        )[:25]

        for r in info.annual_info[y].rankings:
            team_rankings[r.team_key].append(r)

    avged_ranks: List[DistrictRanking] = []
    for tk, team_ranks in team_rankings.items():
        if len(team_ranks) < 2:
            continue

        avged_ranks.append(
            DistrictRanking(
                qualifying_points_individual=[
                    avg_nth_event(
                        [
                            r.qualifying_points_individual
                            for r in team_ranks
                            if r.qualifying_points_total > 0
                        ],
                        0,
                    ),
                    avg_nth_event(
                        [
                            r.qualifying_points_individual
                            for r in team_ranks
                            if r.qualifying_points_total > 0
                        ],
                        1,
                    ),
                ],
                qualifying_points_total=avg(
                    [
                        r.qualifying_points_total
                        for r in team_ranks
                        if r.qualifying_points_total > 0
                    ]
                ),
                dcmp_points=avg(
                    [r.dcmp_points for r in team_ranks if r.dcmp_points > 0]
                ),
                rank=avg(
                    [
                        r.rank
                        for r in team_ranks
                        if r.qualifying_points_total > 0 and r.rank > 0
                    ]
                ),
                age_bonus=0,
                team_key=tk,
            )
        )

    winners = []
    for y in district_years(info.summary.first_year):
        dcmps = [
            e
            for e in info.annual_info[y].events
            if e.event_type in [EventType.DISTRICT_CMP, EventType.DISTRICT_CMP_DIVISION]
        ]

        final_event = None
        if len(dcmps) == 1:
            final_event = dcmps[0]
        else:
            final_event = next(
                filter(
                    lambda dcmp: len(dcmp.child_keys) > 0,
                    dcmps,
                ),
                None,
            )

        if final_event is None:
            winners.append({"year": y, "teams": []})
            continue

        winning_alliance = next(
            filter(
                lambda a: a.placement == AlliancePlacement.WINNER, final_event.alliances
            ),
            None,
        )

        if winning_alliance is None:
            winners.append({"year": y, "teams": []})
            continue

        winners.append({"year": y, "teams": winning_alliance.teams})

    data = {
        "summary": info.summary.to_dict(),
        # "team_data": team_data,
        "teams_per_year": {
            y: Counter(
                [
                    t.state_prov
                    for t in info.summary.all_teams.values()
                    if y in t.active_years
                ]
            )
            for y in district_years(info.summary.first_year)
        },
        "rankings": {
            "overall": [
                x.to_dict()
                for x in sorted(
                    [r for r in avged_ranks if r.rank > 0],
                    key=lambda r: (r.dcmp_points + r.qualifying_points_total),
                    reverse=True,
                )[:25]
            ],
            "by_year": {k: [x.to_dict() for x in v] for k, v in rankings.items()},
        },
        "events": {
            "total": sum([len(ai.events) for ai in info.annual_info.values()]),
            "recent": len(info.annual_info[2024].events),
        },
        "winners": winners,
    }

    write_district_data(
        info.summary.key,
        "district/index.json",
        json.dumps(data, indent=2, sort_keys=True),
    )

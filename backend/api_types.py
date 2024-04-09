import enum
from dataclasses import dataclass
from typing import Dict, List, Optional


@enum.unique
class AwardType(enum.IntEnum):
    CHAIRMANS = 0
    WINNER = 1
    FINALIST = 2

    WOODIE_FLOWERS = 3
    DEANS_LIST = 4
    VOLUNTEER = 5
    FOUNDERS = 6
    BART_KAMEN_MEMORIAL = 7
    MAKE_IT_LOUD = 8

    ENGINEERING_INSPIRATION = 9
    ROOKIE_ALL_STAR = 10
    GRACIOUS_PROFESSIONALISM = 11
    COOPERTITION = 12
    JUDGES = 13
    HIGHEST_ROOKIE_SEED = 14
    ROOKIE_INSPIRATION = 15
    INDUSTRIAL_DESIGN = 16
    QUALITY = 17
    SAFETY = 18
    SPORTSMANSHIP = 19
    CREATIVITY = 20
    ENGINEERING_EXCELLENCE = 21
    ENTREPRENEURSHIP = 22
    EXCELLENCE_IN_DESIGN = 23
    EXCELLENCE_IN_DESIGN_CAD = 24
    EXCELLENCE_IN_DESIGN_ANIMATION = 25
    DRIVING_TOMORROWS_TECHNOLOGY = 26
    IMAGERY = 27
    MEDIA_AND_TECHNOLOGY = 28
    INNOVATION_IN_CONTROL = 29
    SPIRIT = 30
    WEBSITE = 31
    VISUALIZATION = 32
    AUTODESK_INVENTOR = 33
    FUTURE_INNOVATOR = 34
    RECOGNITION_OF_EXTRAORDINARY_SERVICE = 35
    OUTSTANDING_CART = 36
    WSU_AIM_HIGHER = 37
    LEADERSHIP_IN_CONTROL = 38
    NUM_1_SEED = 39
    INCREDIBLE_PLAY = 40
    PEOPLES_CHOICE_ANIMATION = 41
    VISUALIZATION_RISING_STAR = 42
    BEST_OFFENSIVE_ROUND = 43
    BEST_PLAY_OF_THE_DAY = 44
    FEATHERWEIGHT_IN_THE_FINALS = 45
    MOST_PHOTOGENIC = 46
    OUTSTANDING_DEFENSE = 47
    POWER_TO_SIMPLIFY = 48
    AGAINST_ALL_ODDS = 49
    RISING_STAR = 50
    CHAIRMANS_HONORABLE_MENTION = 51
    CONTENT_COMMUNICATION_HONORABLE_MENTION = 52
    TECHNICAL_EXECUTION_HONORABLE_MENTION = 53
    REALIZATION = 54
    REALIZATION_HONORABLE_MENTION = 55
    DESIGN_YOUR_FUTURE = 56
    DESIGN_YOUR_FUTURE_HONORABLE_MENTION = 57
    SPECIAL_RECOGNITION_CHARACTER_ANIMATION = 58
    HIGH_SCORE = 59
    TEACHER_PIONEER = 60
    BEST_CRAFTSMANSHIP = 61
    BEST_DEFENSIVE_MATCH = 62
    PLAY_OF_THE_DAY = 63
    PROGRAMMING = 64
    PROFESSIONALISM = 65
    GOLDEN_CORNDOG = 66
    MOST_IMPROVED_TEAM = 67
    WILDCARD = 68
    CHAIRMANS_FINALIST = 69
    OTHER = 70
    AUTONOMOUS = 71
    INNOVATION_CHALLENGE_SEMI_FINALIST = 72
    ROOKIE_GAME_CHANGER = 73
    SKILLS_COMPETITION_WINNER = 74
    SKILLS_COMPETITION_FINALIST = 75
    ROOKIE_DESIGN = 76
    ENGINEERING_DESIGN = 77
    DESIGNERS = 78
    CONCEPT = 79
    GAME_DESIGN_CHALLENGE_WINNER = 80
    GAME_DESIGN_CHALLENGE_FINALIST = 81
    SUSTAINABILITY = 82


@enum.unique
class EventType(enum.IntEnum):
    REGIONAL = 0
    DISTRICT = 1
    DISTRICT_CMP = 2
    CMP_DIVISION = 3
    CMP_FINALS = 4
    DISTRICT_CMP_DIVISION = 5
    FOC = 6
    REMOTE = 7

    OFFSEASON = 99
    PRESEASON = 100
    UNLABLED = -1


@enum.unique
class PlayoffType(enum.IntEnum):
    # Standard Brackets
    BRACKET_16_TEAM = 1
    BRACKET_8_TEAM = 0
    BRACKET_4_TEAM = 2
    BRACKET_2_TEAM = 9

    # 2015 is special
    AVG_SCORE_8_TEAM = 3

    # Round Robin
    ROUND_ROBIN_6_TEAM = 4

    # Double Elimination Bracket
    # The legacy style is just a basic internet bracket
    # https://www.printyourbrackets.com/fillable-brackets/8-seeded-double-fillable.pdf
    LEGACY_DOUBLE_ELIM_8_TEAM = 5
    # The "regular" style is the one that FIRST plans to trial for the 2023 season
    # https://www.firstinspires.org/robotics/frc/blog/2022-timeout-and-playoff-tournament-updates
    DOUBLE_ELIM_8_TEAM = 10
    # The bracket used for districts with four divisions
    DOUBLE_ELIM_4_TEAM = 11

    # Festival of Champions
    BO5_FINALS = 6
    BO3_FINALS = 7

    # Custom
    CUSTOM = 8


@enum.unique
class DoubleElimRound(enum.StrEnum):
    ROUND1 = "Round 1"
    ROUND2 = "Round 2"
    ROUND3 = "Round 3"
    ROUND4 = "Round 4"
    ROUND5 = "Round 5"
    FINALS = "Finals"


@enum.unique
class AlliancePlacement(enum.IntEnum):
    WINNER = 0
    FINALIST = 1

    DE_THIRD = 2
    DE_FOURTH = 3
    DE_FIFTH_SIXTH = 4
    DE_SEVENTH_EIGHTH = 5

    SE_SEMIS = 6
    SE_QUARTERS = 7
    SE_EIGHTHS = 8

    NOT_YET_IMPLEMENTED = -1


@dataclass
class Record:
    won: int
    lost: int
    tied: int

    def add(self, record: "Record") -> "Record":
        if record is None:
            return self

        return Record(
            won=self.won + record.won,
            lost=self.lost + record.lost,
            tied=self.tied + record.tied,
        )


@dataclass
class SimpleTeam:
    key: str
    number: int
    name: str
    city: str
    state_prov: str
    country: str
    rookie_year: int
    active_years: List[int]


@dataclass
class TeamEventEPA:
    mean: float
    sd: float
    start: float
    normalized: int


@dataclass
class TeamEvent:
    team_key: str
    event_key: str
    event_type: EventType
    award_only_appearance: bool

    qual_pts: Optional[int]
    alliance_pts: Optional[int]
    elim_pts: Optional[int]
    award_pts: int
    total_pts: int

    awards_received: List[AwardType]
    qual_record: Optional[Record]
    elim_record: Optional[Record]
    total_record: Optional[Record]
    match_keys: List[str]

    epa: Optional[TeamEventEPA]


@dataclass
class AnnualSlots:
    total: int
    impact: int
    ei: int
    ras: int
    dlf: int
    wffa: int


@dataclass
class Award:
    award_type: AwardType
    recipient_team: str


@dataclass
class Alliance:
    teams: List[str]
    captain: str
    first_pick: str
    second_pick: str
    backup: Optional[str]
    placement: AlliancePlacement


@dataclass
class Event:
    key: str
    start_date: str
    end_date: str
    code: str
    name: str
    short_name: str
    city: str
    state_prov: str
    country: str
    week: int
    year: int
    event_type: EventType

    awards: List[Award]
    district_pts: Dict
    matches: List[Dict]
    alliances: List[Alliance]
    rankings: List[Dict]


@dataclass
class AnnualInfo:
    year: int
    team_keys: List[str]
    team_events: Dict[str, List[TeamEvent]]
    slots: AnnualSlots
    events: List[Event]


@dataclass
class DistrictSummary:
    all_teams: Dict[str, SimpleTeam]
    key: str
    name: str
    first_year: int


@dataclass
class DistrictInfo:
    summary: DistrictSummary
    annual_info: Dict[int, AnnualInfo]

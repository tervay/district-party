from pathlib import Path
from typing import List, Union
import json

CURRENT_YEAR = 2024

can_province_abbrev = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Northwest Territories": "NT",
    "Nova Scotia": "NS",
    "Nunavut": "NU",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Yukon": "YT",
}

abbrev_to_can_province = dict(map(reversed, can_province_abbrev.items()))

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))


def write_district_data(district_key: str, relative_path: str, data):
    excluded_filename = "/".join(relative_path.split("/")[:-1])
    path_without_filename = f"data/out/{district_key}/{excluded_filename}"
    path = f"data/out/{district_key}/{relative_path}"

    Path(path_without_filename).mkdir(parents=True, exist_ok=True)
    with open(path, "w+") as f:
        f.write(data)


def read_district_data(district_key: str, relative_path: str):
    with open(f"data/out/{district_key}/{relative_path}", "r") as f:
        return json.load(f)


def district_years(first_year: int) -> List[int]:
    return [y for y in range(first_year, CURRENT_YEAR + 1) if y not in [2020, 2021]]


class Averager:
    total: Union[int, float]
    count: int

    def __init__(self) -> None:
        self.total = 0
        self.count = 0

    def feed(self, value: Union[int, float]):
        self.total += value
        self.count += 1

    def feed_many(self, values: List[Union[int, float]]):
        self.total += sum(values)
        self.count += len(values)

    def get(self):
        if self.count == 0:
            return 0

        return self.total / self.count


def avg(vals) -> float:
    if len(vals) == 0:
        return 0

    return sum(vals) / len(vals)

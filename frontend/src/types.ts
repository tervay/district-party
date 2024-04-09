export type DistrictInfoMap = { [key: string]: DistrictInfo };

export type AnnualInfoMap = { [key: string]: AnnualInfo };

export interface DistrictInfo {
  summary: Summary;
  annual_info: AnnualInfoMap;
}

export interface AnnualInfo {
  year: number;
  team_keys: string[];
  team_events: { [key: string]: TeamEvent[] };
  slots: Slots;
  events: Event[];
}

export interface Event {
  key: string;
  start_date: string;
  end_date: string;
  code: string;
  name: string;
  short_name: string;
  city: string;
  state_prov: string;
  country: string;
  week: number;
  year: number;
  event_type: number;
  awards: Award[];
  district_pts: { [key: string]: DistrictPt };
  matches: Match[];
  alliances: Alliance[];
  rankings: Ranking[];
}

export interface Alliance {
  teams: string[];
  captain: string;
  first_pick: string;
  second_pick: string;
  backup: null | string;
  placement: number;
}

export interface Award {
  award_type: number;
  recipient_team: string;
}

export interface DistrictPt {
  alliance_points: number;
  award_points: number;
  elim_points: number;
  qual_points: number;
  total: number;
}

export interface Match {
  actual_time: number | null;
  alliances: Alliances;
  comp_level: string;
  event_key: string;
  key: string;
  match_number: number;
  predicted_time: number | null;
  set_number: number;
  time: number;
  winning_alliance: string;
}

export interface Alliances {
  blue: Blue;
  red: Blue;
}

export interface Blue {
  dq_team_keys: string[];
  score: number;
  surrogate_team_keys: any[];
  team_keys: string[];
}

export interface Ranking {
  dq: number;
  extra_stats: number[];
  matches_played: number;
  qual_average: null;
  rank: number;
  record: Record;
  sort_orders: number[];
  team_key: string;
}

export interface Record {
  losses: number;
  ties: number;
  wins: number;
}

export interface Slots {
  total: number;
  impact: number;
  ei: number;
  ras: number;
  dlf: number;
  wffa: number;
}

export interface TeamEvent {
  team_key: string;
  event_key: string;
  event_type: number;
  award_only_appearance: boolean;
  qual_pts: number;
  alliance_pts: number;
  elim_pts: number;
  award_pts: number;
  total_pts: number;
  awards_received: number[];
  qual_record: QualRecordClass | null;
  elim_record: QualRecordClass | null;
  total_record: QualRecordClass | null;
  match_keys: string[];
  epa: Epa;
}

export interface QualRecordClass {
  won: number;
  lost: number;
  tied: number;
}

export interface Epa {
  mean: string;
  sd: string;
  start: string;
  normalized: string;
}

export interface Summary {
  all_teams: { [key: string]: SimpleTeam };
  key: string;
  name: string;
  first_year: number;
}

export interface SimpleTeam {
  key: string;
  number: number;
  name: string;
  city: string;
  state_prov: string;
  country: string;
  rookie_year: number;
  active_years: number[];
}

export enum EventType {
  REGIONAL = 0,
  DISTRICT = 1,
  DISTRICT_CMP = 2,
  CMP_DIVISION = 3,
  CMP_FINALS = 4,
  DISTRICT_CMP_DIVISION = 5,
  FOC = 6,
  REMOTE = 7,
  OFFSEASON = 99,
  PRESEASON = 100,
  UNLABELED = -1,
}

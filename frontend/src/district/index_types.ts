export interface DistrictIndexData {
  summary: Summary;
  // team_data: TeamDatum[];
  teams_per_year: { [year: string]: TeamsPerYear };
  rankings: Rankings;
  events: Events;
  winners: Winner[];
}

export interface Rankings {
  by_year: { [key: string]: Rank[] };
  overall: Rank[];
}

export interface Events {
  recent: number;
  total: number;
}

export interface Rank {
  age_bonus: number;
  dcmp_points: number;
  qualifying_points_individual: number[];
  qualifying_points_total: number;
  rank: number;
  team_key: string;
}

export interface Summary {
  all_teams: { [key: string]: Team };
  first_year: number;
  key: string;
  name: string;
}

export interface Team {
  active_years: number[];
  city: string;
  country: string;
  key: string;
  name: string;
  number: number;
  rookie_year: number;
  state_prov: string;
}

export interface TeamDatum {
  dcmps: number;
  epa: number;
  record: Record;
  team: Team;
}

export interface Record {
  losses: number;
  ties: number;
  wins: number;
}

export interface Winner {
  teams: string[];
  year: number;
}

export type TeamsPerYear = { [state: string]: number };

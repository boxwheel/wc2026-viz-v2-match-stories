"""Tidy frame loaders rooted at the fetched ~/research/fifa_data."""
from __future__ import annotations
import os
import pandas as pd

ROOT = os.path.expanduser("~/research/fifa_data")

def matches(completed_only: bool = True) -> pd.DataFrame:
    m = pd.read_csv(os.path.join(ROOT, "matches.csv"))
    md = pd.read_csv(os.path.join(ROOT, "matches_detailed.csv"))
    df = m.merge(md[["match_id", "home_team_name", "away_team_name",
                     "home_fifa_code", "away_fifa_code", "stage_name",
                     "stadium_name", "city"]], on="match_id", how="left")
    if completed_only:
        df = df[df["status"] == "Completed"].copy()
    df["home_residual"] = df["home_score"] - df["home_xg"]
    df["away_residual"] = df["away_score"] - df["away_xg"]
    return df.reset_index(drop=True)

def events() -> pd.DataFrame:
    return pd.read_csv(os.path.join(ROOT, "match_events.csv"))

def team_stats() -> pd.DataFrame:
    return pd.read_csv(os.path.join(ROOT, "match_team_stats.csv"))

def teams() -> pd.DataFrame:
    return pd.read_csv(os.path.join(ROOT, "teams.csv"))

def long_team_match() -> pd.DataFrame:
    """One row per (team, match) — handy for ranking / atlas plots."""
    m = matches(completed_only=True)
    home = m.assign(team="home")[["match_id", "date", "home_team_name", "home_fifa_code",
                                  "away_team_name", "away_fifa_code",
                                  "home_score", "away_score", "home_xg", "away_xg",
                                  "home_residual", "stage_name"]].rename(columns={
        "home_team_name": "team", "home_fifa_code": "fifa_code",
        "away_team_name": "opp",   "away_fifa_code": "opp_code",
        "home_score": "gf", "away_score": "ga",
        "home_xg": "xg", "away_xg": "xg_against",
        "home_residual": "residual",
    })
    away = m[["match_id", "date", "home_team_name", "home_fifa_code",
              "away_team_name", "away_fifa_code", "home_score", "away_score",
              "home_xg", "away_xg", "away_residual", "stage_name"]].rename(columns={
        "away_team_name": "team", "away_fifa_code": "fifa_code",
        "home_team_name": "opp",   "home_fifa_code": "opp_code",
        "away_score": "gf", "home_score": "ga",
        "away_xg": "xg", "home_xg": "xg_against",
        "away_residual": "residual",
    })
    return pd.concat([home, away], ignore_index=True)

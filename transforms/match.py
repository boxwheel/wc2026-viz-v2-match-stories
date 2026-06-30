from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def read_csv(name: str) -> list[dict[str, str]]:
    with (RAW / name).open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def num(value: str | None, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def load_context() -> dict[str, object]:
    matches = read_csv("matches.csv")
    detailed = {int(r["match_id"]): r for r in read_csv("matches_detailed.csv")}
    events = read_csv("match_events.csv")
    stats = read_csv("match_team_stats.csv")
    teams = {r["team_id"]: r for r in read_csv("teams.csv")}
    id_to_name = {tid: r["team_name"] for tid, r in teams.items()}
    return {
        "matches": matches,
        "detailed": detailed,
        "events": events,
        "stats": stats,
        "teams": teams,
        "id_to_name": id_to_name,
    }


def match_events(ctx: dict[str, object], match_id: int, event_type: str | None = None) -> list[dict[str, str]]:
    rows = [r for r in ctx["events"] if int(r["match_id"]) == match_id]
    if event_type:
        rows = [r for r in rows if r["event_type"] == event_type]
    return sorted(rows, key=lambda r: (int(r["minute"]), int(r["event_id"])))


def match_stats(ctx: dict[str, object], match_id: int) -> list[dict[str, str]]:
    return [r for r in ctx["stats"] if int(r["match_id"]) == match_id]


def fixture(ctx: dict[str, object], match_id: int) -> dict[str, str]:
    return ctx["detailed"][match_id]


def completed_team_rows(ctx: dict[str, object]) -> list[dict[str, object]]:
    out = []
    for r in ctx["matches"]:
        if r["status"] != "Completed":
            continue
        d = ctx["detailed"][int(r["match_id"])]
        pairs = [
            ("home", d["home_team_name"], int(r["home_score"]), num(r["home_xg"])),
            ("away", d["away_team_name"], int(r["away_score"]), num(r["away_xg"])),
        ]
        for side, team, goals, xg in pairs:
            out.append(
                {
                    "match_id": int(r["match_id"]),
                    "side": side,
                    "team": team,
                    "opponent": d["away_team_name"] if side == "home" else d["home_team_name"],
                    "goals": goals,
                    "xg": xg,
                    "resid": goals - xg,
                    "label": f"{team} {goals} ({xg:.2f} xG)",
                }
            )
    return out


def running_score(ctx: dict[str, object], match_id: int) -> list[dict[str, object]]:
    d = fixture(ctx, match_id)
    home_id = next(r["home_team_id"] for r in ctx["matches"] if int(r["match_id"]) == match_id)
    away_id = next(r["away_team_id"] for r in ctx["matches"] if int(r["match_id"]) == match_id)
    h = a = 0
    rows = [{"minute": 0, "home": h, "away": a, "team": "", "score": "0-0"}]
    for e in match_events(ctx, match_id, "Goal"):
        if e["team_id"] == home_id:
            h += 1
            team = d["home_team_name"]
        else:
            a += 1
            team = d["away_team_name"]
        rows.append({"minute": int(e["minute"]), "home": h, "away": a, "team": team, "score": f"{h}-{a}"})
    rows.append({"minute": 95, "home": h, "away": a, "team": "", "score": f"{h}-{a}"})
    return rows


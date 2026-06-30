"""House style for the WC-2026 viz gallery (v2)."""
from __future__ import annotations

import matplotlib as mpl

BG = "#101418"
PANEL = "#151b21"
FG = "#E6EDF3"
TEXT = "#f1f5f2"
MUTED = "#9da8ae"
GRID = "#2a333c"
GOOD = "#3FB950"
BAD = "#F85149"
ACCENT = "#F2A65A"
HILIGHT = "#FFD166"
GOLD = "#d2a32f"
BLUE = "#4aa3df"
AMBER = "#f0b44f"
GREEN = "#5cc37b"
RED = "#e05a5a"
PURPLE = "#9b7de3"

CONFED_COLORS = {
    "UEFA": "#4FA3F7",
    "CONMEBOL": "#FFC857",
    "CONCACAF": "#3FB950",
    "CAF": "#F2784B",
    "AFC": "#E83A82",
    "OFC": "#9D7CE0",
}

TEAM_COLORS = {
    "Germany": "#d1d5db",
    "Curaçao": "#38bdf8",
    "Switzerland": "#ef4444",
    "Bosnia and Herzegovina": "#fbbf24",
    "Bosnia & Herzegovina": "#fbbf24",
    "Algeria": "#10b981",
    "Austria": "#f97316",
    "Senegal": "#22c55e",
    "Iraq": "#f59e0b",
    "France": "#3b82f6",
    "Norway": "#ef4444",
    "Mexico": "#16a34a",
    "South Africa": "#facc15",
    "Netherlands": "#FF8E1A",
    "Sweden": "#FFD166",
}


def apply_style() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "axes.edgecolor": GRID,
            "axes.labelcolor": FG,
            "axes.titlecolor": FG,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": FG,
            "grid.color": GRID,
            "grid.alpha": 0.6,
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 15,
            "axes.labelsize": 12,
            "figure.dpi": 140,
            "legend.frameon": False,
            "legend.labelcolor": FG,
        }
    )


def caption_stamp(fig, text: str, y: float = 0.02) -> None:
    fig.text(0.012, y, text, color=MUTED, fontsize=8.5, ha="left", va="bottom")


def team_color(name: str, fallback: str = ACCENT) -> str:
    return TEAM_COLORS.get(name, fallback)


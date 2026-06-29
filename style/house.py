"""House style for the WC-2026 viz gallery (v2)."""
from __future__ import annotations
import matplotlib as mpl
import matplotlib.pyplot as plt

BG       = "#0E1117"
PANEL    = "#161B22"
FG       = "#E6EDF3"
MUTED    = "#7D8590"
GRID     = "#262C36"
GOOD     = "#3FB950"
BAD      = "#F85149"
ACCENT   = "#F2A65A"
HILIGHT  = "#FFD166"
LIGHT_RED = "#FF8E8A"
LIGHT_GREEN = "#5FE07A"

CONFED_COLORS = {
    "UEFA":     "#4FA3F7",
    "CONMEBOL": "#FFC857",
    "CONCACAF": "#3FB950",
    "CAF":      "#F2784B",
    "AFC":      "#E83A82",
    "OFC":      "#9D7CE0",
}

# Team kit-ish colors for the eight features matches
TEAM_COLORS = {
    "Germany":     "#FFD166",
    "Curaçao":     "#1E5BA8",
    "Switzerland": "#F85149",
    "Bosnia & Herzegovina": "#1F77B4",
    "Algeria":     "#3FB950",
    "Austria":     "#F85149",
    "Senegal":     "#3FB950",
    "Iraq":        "#F2A65A",
    "France":      "#4FA3F7",
    "Norway":      "#F85149",
    "Mexico":      "#3FB950",
    "South Africa": "#F2A65A",
    "Netherlands": "#FF8E1A",
    "Sweden":      "#FFD166",
}

def apply_style():
    mpl.rcParams.update({
        "figure.facecolor":  BG,
        "axes.facecolor":    BG,
        "savefig.facecolor": BG,
        "axes.edgecolor":    MUTED,
        "axes.labelcolor":   FG,
        "axes.titlecolor":   FG,
        "axes.titleweight":  "bold",
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "xtick.color":  MUTED,
        "ytick.color":  MUTED,
        "text.color":    FG,
        "grid.color":    GRID,
        "grid.alpha":    0.6,
        "font.family":   "DejaVu Sans",
        "font.size":     11,
        "axes.titlesize":18,
        "axes.labelsize":12,
        "legend.frameon":False,
        "legend.labelcolor": FG,
        "lines.linewidth":  2.0,
    })

def caption_stamp(fig, text, y=0.02):
    fig.text(0.012, y, text, color=MUTED, fontsize=8.5, ha="left", va="bottom")

def team_color(name, default=ACCENT):
    return TEAM_COLORS.get(name, default)

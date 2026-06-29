"""
Tournament xG-residual arrow atlas (Wave-3 #1 — extends MS06 P1).

Vertical small-multiple of every team-match pair, ordered by `goals - xG` residual.
Each row is one arrow from the team's xG tick to the actual goals — green-up for
finishing over-performance, red-down for under-performance. Top-15 over, top-15
under in two columns.
"""
from __future__ import annotations
import argparse
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.load import long_team_match
from style.house import apply_style, BG, FG, MUTED, GOOD, BAD, GRID, caption_stamp


def arrow_row(ax, y, xg, goals, color, team, opp, gf, ga, residual):
    # xG tick (vertical thick mark)
    ax.plot([xg, xg], [y - 0.30, y + 0.30], color=MUTED, lw=2.2, solid_capstyle="butt", zorder=2)
    # the arrow
    if abs(goals - xg) > 0.04:
        arrow = FancyArrowPatch((xg, y), (goals, y),
                                arrowstyle="-|>", mutation_scale=14,
                                color=color, lw=3.4, zorder=3)
        ax.add_patch(arrow)
    # goal dot
    ax.scatter([goals], [y], s=46, color=color, edgecolor=BG, lw=1.2, zorder=4)
    # left label: team name (bold)
    ax.text(-0.18, y, team, color=FG, fontsize=10.7, ha="right", va="center",
            fontweight="bold")
    # left sub-label: vs opp + score
    ax.text(-0.18, y + 0.35, f"vs {opp}  {int(gf)}–{int(ga)}", color=MUTED, fontsize=8.4,
            ha="right", va="top")
    # right label (delta chip)
    sign = "+" if residual > 0 else ""
    ax.text(7.9, y, f"{sign}{residual:.2f}", color=color, fontsize=10.6, ha="left",
            va="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.32", fc="#1e2530", ec=color, lw=1.2))


def main(out_dir):
    apply_style()
    df = long_team_match()
    df = df.dropna(subset=["xg", "gf"]).copy()
    df["abs_resid"] = df["residual"].abs()
    over  = df.sort_values("residual", ascending=False).head(15).reset_index(drop=True)
    under = df.sort_values("residual", ascending=True).head(15).reset_index(drop=True)

    fig, axes = plt.subplots(1, 2, figsize=(16.0, 11.6), sharex=True)
    plt.subplots_adjust(top=0.85, bottom=0.07, left=0.12, right=0.97, wspace=0.46)

    panels = [(axes[0], over, GOOD, "OVER-PERFORMED  ·  goals > xG", +1),
              (axes[1], under, BAD,  "UNDER-PERFORMED  ·  goals < xG", -1)]

    for ax, frame, color, hdr, direction in panels:
        ax.set_xlim(-0.4, 8.9)
        ax.set_ylim(-0.7, len(frame) - 0.5)
        ax.invert_yaxis()
        ax.set_facecolor(BG)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(MUTED)
        ax.set_yticks([])
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
        ax.tick_params(axis="x", colors=MUTED, labelsize=9)
        ax.set_xlabel("goals (xG tick → actual arrow-head)", color=MUTED, fontsize=10)
        for x in [1, 2, 3, 4, 5, 6, 7]:
            ax.axvline(x, color=GRID, lw=0.6, alpha=0.55, zorder=0)
        ax.text(0.0, -1.15, hdr, color=color, fontsize=12.5,
                ha="left", va="bottom", fontweight="bold",
                transform=ax.transData)
        for i, row in frame.iterrows():
            arrow_row(ax, i, float(row["xg"]), float(row["gf"]), color,
                      row["team"], row["opp"], row["gf"], row["ga"], row["residual"])

    fig.suptitle("Finishing variance, ranked   ·   the WC-2026 xG residual atlas",
                 color=FG, fontsize=22, fontweight="bold", x=0.013, ha="left", y=0.965)
    fig.text(0.013, 0.927, "Each row: one team-match. xG tick → arrow → actual goals. "
             "Green up-shooter = clinical, red over-shooter = wasteful.",
             color=MUTED, fontsize=11.5, ha="left")
    fig.text(0.013, 0.901,
             "Top-15 finishing over-performers (left)   ·   top-15 under-performers (right)   "
             "·   completed group-stage matches only",
             color=MUTED, fontsize=10.5, ha="left")

    caption_stamp(fig,
        "data: Kaggle mominullptr/fifa-world-cup-2026   ·   xG residual = goals − xG   "
        "·   viz · boxwheel/wc2026-viz-v2-match-stories")

    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, "xg_residual_atlas.png")
    svg = os.path.join(out_dir, "xg_residual_atlas.svg")
    fig.savefig(png, dpi=200, facecolor=BG)
    fig.savefig(svg, facecolor=BG)
    print("wrote", png, svg)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=os.path.expanduser("~/research/boxwheel/wc2026-viz-v2-match-stories/artifacts"))
    main(p.parse_args().out)

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from style.house import AMBER, BG, BLUE, GOLD, GREEN, GRID, MUTED, PANEL, PURPLE, RED, TEXT, apply_style, team_color
from transforms.match import completed_team_rows, fixture, load_context, match_events, match_stats, num, running_score

OUT = Path(__file__).resolve().parents[1] / "artifacts"
OUT.mkdir(exist_ok=True)


def save(fig, name: str) -> tuple[Path, Path]:
    png = OUT / f"{name}.png"
    svg = OUT / f"{name}.svg"
    fig.savefig(png, dpi=200, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    plt.close(fig)
    return png, svg


def clean(ax):
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)


def xg_residual_arrow_ranking(ctx):
    rows = sorted(completed_team_rows(ctx), key=lambda r: r["resid"])
    pick = rows[:15] + rows[-15:]
    fig = plt.figure(figsize=(15.8, 13))
    fig.text(0.05, 0.965, "WC 2026 xG residual arrows", fontsize=23, weight="bold")
    fig.text(0.05, 0.935, "Each arrow runs from expected goals to actual goals; ranked by goals minus xG across completed team-matches.", color=MUTED, fontsize=11)
    gs = fig.add_gridspec(1, 2, left=0.16, right=0.95, top=0.90, bottom=0.06, wspace=0.34)
    for col, subset, title in [(0, rows[-15:][::-1], "Over-finished xG"), (1, rows[:15], "Under-finished xG")]:
        ax = fig.add_subplot(gs[0, col])
        ax.set_facecolor(PANEL)
        clean(ax)
        ax.set_xlim(-0.1, 7.3)
        ax.set_ylim(-0.8, len(subset) - 0.2)
        ax.set_title(title, loc="left", color=TEXT, pad=14)
        ax.set_xlabel("goals")
        ax.set_yticks([])
        for x in range(0, 8):
            ax.axvline(x, color=GRID, lw=0.8, alpha=0.6, zorder=0)
        for i, r in enumerate(subset):
            y = len(subset) - 1 - i
            c = GREEN if r["resid"] >= 0 else RED
            ax.scatter([r["xg"]], [y], marker="|", s=260, color=TEXT, linewidth=2.4, zorder=4)
            ax.annotate("", xy=(r["goals"], y), xytext=(r["xg"], y), arrowprops=dict(arrowstyle="-|>", lw=2.8, color=c, shrinkA=1, shrinkB=1))
            label = f"{i+1:02d}  {r['team'][:18]} vs {r['opponent'][:14]}"
            ax.text(-0.08, y, label, ha="right", va="center", fontsize=8.1, clip_on=False)
            ax.text(7.08, y, f"{r['resid']:+.2f}", ha="right", va="center", color=c, weight="bold", fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.22", facecolor=BG, edgecolor=c, lw=0.8))
            ax.text(r["xg"], y + 0.28, f"xG {r['xg']:.2f}", ha="center", va="bottom", color=MUTED, fontsize=6.7)
    fig.text(0.05, 0.02, "Data: FIFA WC 2026 dataset · Wave-3 Match-Stories rebuild", color=MUTED, fontsize=8)
    return save(fig, "wave3_xg_residual_arrow_ranking")


def stat_split_card_hinge(ctx):
    specs = [(66, 13, "Senegal-Iraq: 13' red turns totals into a rout"), (1, 55, "Mexico-RSA: opener control survives the red-card chaos")]
    stats = ["possession_pct", "total_shots", "shots_on_target", "corners", "saves"]
    labels = ["Poss.", "Shots", "SOT", "Corners", "Saves"]
    fig = plt.figure(figsize=(13, 8))
    fig.text(0.05, 0.96, "Card-hinge stat-share split", fontsize=23, weight="bold")
    fig.text(0.05, 0.925, "Pre-card rows use event counts before the first red; post-card rows combine event evidence with published 90-minute stat shares.", color=MUTED, fontsize=10)
    gs = fig.add_gridspec(2, 1, left=0.08, right=0.96, top=0.86, bottom=0.08, hspace=0.36)
    for idx, (mid, hinge, title) in enumerate(specs):
        ax = fig.add_subplot(gs[idx, 0])
        ax.set_facecolor(PANEL)
        clean(ax)
        d = fixture(ctx, mid)
        teams = [d["home_team_name"], d["away_team_name"]]
        ids = [next(r["home_team_id"] for r in ctx["matches"] if int(r["match_id"]) == mid), next(r["away_team_id"] for r in ctx["matches"] if int(r["match_id"]) == mid)]
        stat_rows = {r["team_id"]: r for r in match_stats(ctx, mid)}
        evs = match_events(ctx, mid)
        ax.set_title(title, loc="left", pad=8)
        y = 0
        yticks = []
        ylabels = []
        for lab, key in zip(labels, stats):
            pre_counts = []
            post_counts = []
            for tid in ids:
                if key == "possession_pct":
                    pre = sum(1 for e in evs if e["team_id"] == tid and int(e["minute"]) < hinge)
                    post = sum(1 for e in evs if e["team_id"] == tid and int(e["minute"]) >= hinge)
                elif key == "total_shots":
                    pre = sum(1 for e in evs if e["team_id"] == tid and e["event_type"] == "Goal" and int(e["minute"]) < hinge)
                    post = max(0, int(num(stat_rows[tid][key])) - pre)
                elif key == "shots_on_target":
                    pre = sum(1 for e in evs if e["team_id"] == tid and e["event_type"] == "Goal" and int(e["minute"]) < hinge)
                    post = max(0, int(num(stat_rows[tid][key])) - pre)
                else:
                    pre = 0
                    post = int(num(stat_rows[tid][key]))
                pre_counts.append(pre)
                post_counts.append(post)
            for phase, vals in [("pre", pre_counts), ("post", post_counts)]:
                total = sum(vals) or 1
                shares = [v / total * 100 for v in vals]
                ax.barh(y, shares[0], color=team_color(teams[0]), height=0.34)
                ax.barh(y, shares[1], left=shares[0], color=team_color(teams[1], AMBER), height=0.34)
                ax.text(1.5, y, f"{phase}", va="center", fontsize=7, weight="bold")
                ax.text(50, y, f"{vals[0]}  |  {vals[1]}", va="center", ha="center", fontsize=8, color=TEXT)
                yticks.append(y)
                ylabels.append(lab if phase == "pre" else "")
                y += 0.45
            y += 0.18
        ax.set_xlim(0, 100)
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("share within phase (%)")
        ax.text(0, -0.65, teams[0], color=team_color(teams[0]), weight="bold")
        ax.text(100, -0.65, teams[1], color=team_color(teams[1], AMBER), weight="bold", ha="right")
    return save(fig, "wave3_card_hinge_stat_split")


def xg_race_small_multiple(ctx):
    rows = sorted([r for r in ctx["matches"] if r["status"] == "Completed"], key=lambda r: abs((int(r["home_score"]) - num(r["home_xg"])) + (int(r["away_score"]) - num(r["away_xg"]))), reverse=True)[:64]
    fig, axes = plt.subplots(8, 8, figsize=(17, 16), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.04, right=0.99, top=0.91, bottom=0.05, hspace=0.55, wspace=0.25)
    fig.text(0.04, 0.965, "Tournament xG-race small multiple", fontsize=23, weight="bold")
    fig.text(0.04, 0.94, "Cumulative actual goals against horizontal xG-total baselines; sorted by the largest combined finishing residual.", color=MUTED, fontsize=10)
    for ax, r in zip(axes.ravel(), rows):
        mid = int(r["match_id"])
        d = fixture(ctx, mid)
        rs = running_score(ctx, mid)
        mins = [x["minute"] for x in rs]
        hs = [x["home"] for x in rs]
        aw = [x["away"] for x in rs]
        ax.set_facecolor(PANEL)
        clean(ax)
        ax.step(mins, hs, where="post", color=team_color(d["home_team_name"]), lw=1.6)
        ax.step(mins, aw, where="post", color=team_color(d["away_team_name"], AMBER), lw=1.6)
        ax.axhline(num(r["home_xg"]), color=team_color(d["home_team_name"]), lw=0.8, ls="--", alpha=0.75)
        ax.axhline(num(r["away_xg"]), color=team_color(d["away_team_name"], AMBER), lw=0.8, ls="--", alpha=0.75)
        ax.set_xlim(0, 95)
        ax.set_ylim(0, max(5, int(r["home_score"]), int(r["away_score"])) + 0.25)
        resid = (int(r["home_score"]) - num(r["home_xg"])) + (int(r["away_score"]) - num(r["away_xg"]))
        ax.set_title(f"{d['home_fifa_code']} {r['home_score']}-{r['away_score']} {d['away_fifa_code']}  {resid:+.1f}", fontsize=7, pad=3)
        ax.set_xticks([])
        ax.set_yticks([])
    return save(fig, "wave3_xg_race_small_multiple")


def decision_triptych(ctx):
    panels = [(9, "the storm", "early dominance"), (28, "the avalanche", "late dominance"), (68, "the see-saw", "no dominance")]
    fig = plt.figure(figsize=(14, 9))
    fig.text(0.05, 0.965, "Three shapes of how a match decides itself", fontsize=23, weight="bold")
    fig.text(0.05, 0.935, "A shared time axis separates an early goal-storm, a late red-card avalanche, and a match that never held a two-goal lead.", color=MUTED, fontsize=10)
    gs = fig.add_gridspec(3, 1, left=0.07, right=0.96, top=0.88, bottom=0.08, hspace=0.34)
    for i, (mid, nick, shape) in enumerate(panels):
        ax = fig.add_subplot(gs[i, 0])
        ax.set_facecolor(PANEL)
        clean(ax)
        d = fixture(ctx, mid)
        rs = running_score(ctx, mid)
        mins = [x["minute"] for x in rs]
        margin = [x["home"] - x["away"] for x in rs]
        ax.step(mins, margin, where="post", color=TEXT, lw=1.2)
        ax.fill_between(mins, margin, 0, where=[m >= 0 for m in margin], step="post", color=team_color(d["home_team_name"]), alpha=0.55)
        ax.fill_between(mins, margin, 0, where=[m <= 0 for m in margin], step="post", color=team_color(d["away_team_name"], AMBER), alpha=0.55)
        seen = {}
        for e in match_events(ctx, mid, "Goal"):
            m = int(e["minute"])
            seen[m] = seen.get(m, 0) + 1
            draw_m = m + (seen[m] - 1) * 1.7
            nearest = min(rs, key=lambda x: abs(x["minute"] - m))
            ax.scatter(draw_m, nearest["home"] - nearest["away"], s=70, color=GOLD, edgecolor=BG, zorder=5)
            ax.text(draw_m, nearest["home"] - nearest["away"] + (0.25 if nearest["home"] >= nearest["away"] else -0.25), f"{m}'", ha="center", va="center", fontsize=7)
        ax.axhline(0, color=GRID, lw=1)
        ax.set_xlim(0, 97)
        ax.set_ylim(-2.5, 7.5 if mid == 9 else 4.5)
        ax.set_yticks([-1, 0, 1, 2, 3, 4, 5, 6] if mid == 9 else [-1, 0, 1, 2, 3])
        ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.35)
        suffix = " · 90' and 90+ reply separated" if mid == 68 else ""
        ax.set_title(f"{nick}: {d['home_team_name']} {d['home_score']}-{d['away_score']} {d['away_team_name']} · {shape}{suffix}", loc="left", fontsize=12)
        if i < 2:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel("match minute")
        ax.set_ylabel("lead")
    return save(fig, "wave3_three_decision_shapes_triptych")


def mexico_rsa_cleanup(ctx):
    mid = 1
    d = fixture(ctx, mid)
    home_id = next(r["home_team_id"] for r in ctx["matches"] if int(r["match_id"]) == mid)
    away_id = next(r["away_team_id"] for r in ctx["matches"] if int(r["match_id"]) == mid)
    fig, ax = plt.subplots(figsize=(13, 6.8))
    ax.set_facecolor(PANEL)
    clean(ax)
    ax.set_title("Mexico 2-0 South Africa: the cleaned 10-v-9 player-count step", loc="left", pad=16, fontsize=19)
    fig.text(0.125, 0.89, "Bottom event strip removed; red-card labels are staggered and goals ride directly on the player-count story.", color=MUTED, fontsize=10)
    evs = match_events(ctx, mid)
    for tid, team, c, y0 in [(home_id, d["home_team_name"], team_color(d["home_team_name"]), 11), (away_id, d["away_team_name"], team_color(d["away_team_name"], AMBER), 11)]:
        xs, ys = [0], [11]
        count = 11
        for e in evs:
            if e["event_type"] == "Red Card" and e["team_id"] == tid:
                xs += [int(e["minute"]), int(e["minute"])]
                ys += [count, count - 1]
                count -= 1
        xs.append(95)
        ys.append(count)
        ax.step(xs, ys, where="post", color=c, lw=4, label=team)
        ax.text(96, count, f"{team} {count}", color=c, weight="bold", va="center")
    for k, e in enumerate([e for e in evs if e["event_type"] == "Red Card"]):
        m = int(e["minute"])
        team = d["home_team_name"] if e["team_id"] == home_id else d["away_team_name"]
        y = 10.6 if k % 2 == 0 else 9.15
        va = "bottom" if k % 2 == 0 else "top"
        ax.annotate(f"RED · {team}\n{m}'", xy=(m, 10.05 if e["team_id"] == away_id else 10.55), xytext=(m + (-3 if k == 0 else 3), y),
                    ha="center", va=va, fontsize=9, color=TEXT,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor=RED, edgecolor="none", alpha=0.9),
                    arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))
    for e in [e for e in evs if e["event_type"] == "Goal"]:
        m = int(e["minute"])
        team = d["home_team_name"] if e["team_id"] == home_id else d["away_team_name"]
        ax.scatter(m, 11.28, s=180, color=team_color(team), edgecolor=BG, zorder=6)
        ax.text(m, 11.28, "G", ha="center", va="center", color=BG, weight="bold", fontsize=9)
        ax.text(m, 11.55, f"{team} {m}'", ha="center", va="bottom", fontsize=8, color=TEXT)
    ax.axvline(45, color=GOLD, lw=1, alpha=0.65)
    ax.text(45, 8.65, "HT", color=GOLD, ha="center")
    ax.set_xlim(0, 100)
    ax.set_ylim(8.4, 11.85)
    ax.set_yticks([9, 10, 11])
    ax.set_xlabel("match minute")
    ax.set_ylabel("players on pitch", fontsize=12, weight="bold")
    ax.grid(axis="x", color=GRID, alpha=0.35)
    ax.legend(frameon=False, loc="lower left", ncols=2)
    return save(fig, "wave3_mexico_rsa_cleanup")


def main():
    apply_style()
    ctx = load_context()
    outputs = {
        "xg_residual_arrow_ranking": xg_residual_arrow_ranking(ctx),
        "card_hinge_stat_split": stat_split_card_hinge(ctx),
        "xg_race_small_multiple": xg_race_small_multiple(ctx),
        "three_decision_shapes_triptych": decision_triptych(ctx),
        "mexico_rsa_cleanup": mexico_rsa_cleanup(ctx),
    }
    for name, paths in outputs.items():
        print(name, paths[0], paths[1])


if __name__ == "__main__":
    main()

# wc2026-viz-v2-match-stories

Wave-3 builds of the FIFA WC-2026 Match-Stories viz family — acting on the
Wave-2 feedback critique to produce a second generation of charts that beat
their Wave-1 baselines on the gallery rubric (Meaning / Honesty / Clarity /
Aesthetic / Novelty).

## Layout

- `style/house.py` — shared dark theme, palette, fonts.
- `data/load.py` — Kaggle FIFA WC-2026 tidy frames (matches, events, stats).
- `plots/<viz>.py` — one module per viz; renders PNG@200dpi + SVG into
  `artifacts/`.

## Wave-3 plot index (high-leverage first)

1. `plots/xg_residual_atlas.py` — tournament-wide xG residual ranking
   (extends MS06 P1 — the arrow primitive promoted to a 30-row ranking).

## Reproduce

```
python3 -m venv venv && . venv/bin/activate
pip install matplotlib seaborn mplsoccer pandas numpy highlight-text
# fetch fifa_data/ from Kaggle mominullptr/fifa-world-cup-2026-dataset
PYTHONPATH=. python3 plots/xg_residual_atlas.py
```

# wc2026-viz-v2-match-stories

Wave-3 builds of the FIFA WC-2026 Match-Stories viz family, acting on the
Wave-2 feedback critique to produce a second generation of charts that beat
their Wave-1 baselines on the gallery rubric.

## Layout

- `style/house.py` - shared dark theme, palette, fonts.
- `transforms/match.py` - CSV loaders and match-level transforms.
- `plots/wave3_match_stories.py` - renders the ranked Wave-3 outputs.
- `artifacts/` - PNG at 200 dpi and SVG outputs.

## Wave-3 Plot Index

1. `wave3_xg_residual_arrow_ranking` - tournament-wide xG residual ranking
   extending MS06 P1.
2. `wave3_card_hinge_stat_split` - pre/post card stat-share primitive for MS04
   P1 and MS07 P3/P4.
3. `wave3_xg_race_small_multiple` - tournament-wide xG race small-multiple from
   MS05 P1.
4. `wave3_three_decision_shapes_triptych` - MS01/MS02/MS03 decision-shape
   triptych from MS03 P4.
5. `wave3_mexico_rsa_cleanup` - MS07 P1/P2 cleanup with clutter removed and
   red-card labels staggered.

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/pip install matplotlib pillow
# fetch data/raw from Kaggle mominullptr/fifa-world-cup-2026-dataset
.venv/bin/python plots/wave3_match_stories.py
```


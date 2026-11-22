[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/vicko223/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/vicko223/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World Today — Sunday, 22 November 2026

A one-image front page for the make.fun bounty
[Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122).

The page names the day in its masthead and leads with the COP31 climate
summit in Antalya reaching a final deal text, with three smaller stories
below: Formula 1 racing under the Las Vegas lights, a magnitude 4.1
earthquake in Myanmar before dawn, and South Africa lowering its flags for
Phumzile Mlambo-Ngcuka.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This copies `entry.png` (1024×1024) to `out/entry.png`. The image itself is
drawn programmatically by `build_image.py` (Pillow), so every word is crisp
vector-set text.

## Layout

- `main.py` — entry point: copies `entry.png` to the output directory
- `entry.png` — the front-page image
- `build_image.py` — draws `entry.png` from scratch

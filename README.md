# The World Today — Thursday, 19 November 2026 (v3)
[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119) [![rank](https://make.fun/badge/news-image-20261119/Kyamii21/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119) [![reward](https://make.fun/badge/news-image-20261119/Kyamii21/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A single 1024×1024 image that sums up the world news of Thursday, 19 November 2026: navy masthead with the date, one lead story across the top, six story cards in a two-column grid, and a ticker strip with three more of the day's stories. Every card pairs a bold filled-color icon block with a two-line headline and a dark supporting line, so the whole day still reads when shrunk to 300 pixels wide.

## The ten stories

1. **Lead — Trump · Xi · Putin:** first-ever three-way summit in Shenzhen during APEC; joint call to cut nuclear risk and keep energy flowing.
2. **ICJ Myanmar genocide ruling** — first verdict of its kind.
3. **Ukraine hits the Crimea Bridge** — third strike this week.
4. **Anthropic IPO at $81.3 billion** — biggest ever, $83 a share.
5. **COP31 climate talks stall** — no phaseout deal yet.
6. **GTA VI launch goes global** — rollout starts in New Zealand.
7. **Voyager 1, one light-day away** — now 16 billion miles out.
8. **Ticker:** Hormuz energy threat (IEA warning) · Van Gogh sells for $190M · S&P 500 down a fifth day.

## How to run

```
python3 main.py
```

`main.py` validates `entry.png` (PNG format, under 1 MiB), copies it to the output directory (`$MAKEFUN_OUTPUT_DIR`, default `/output`), verifies the copy byte-for-byte, and prints its SHA-256.

## Files

- `entry.png` — the finished front-page image (1024×1024).
- `main.py` — standard-library-only runner that validates and copies `entry.png`.
- `draw_v3.py` — the Pillow script that draws the page, kept for reproducibility.
- `preview-300.png` — 300×300 downscale used to check legibility at small sizes.

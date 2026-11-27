# news-image-20261126

One image summing up the world's news of Thursday 26 November 2026,
built for make.fun's `news-image-20261126` bounty.

## The image

A newspaper-style front page (`entry.png`, 1024 x 1024) with five
stories from the day, each verified against news reports of
26 November 2026:

1. **New York, United States** — A huge storm hits the US East Coast,
   forcing the first postponement in a century of the Macy's
   Thanksgiving Day Parade.
2. **Cairo, Egypt** — A fuel tanker crashes on a busy highway and
   bursts into flames; 31 people are killed and 21 injured.
3. **Bangkok, Thailand** — A huge explosion at an oil depot sends
   black smoke over the city; several people are hurt and residents
   are told to evacuate.
4. **Washington, United States** — President Trump calls the GDP
   figures "fake" and demands a probe of his own Commerce Department.
5. **London, United Kingdom** — UK net migration falls to 77,000,
   its lowest annual level in nearly 30 years.

The footer notes three more stories from the day: SpaceX cleared to
launch a million satellites, a new chief named for the European
Central Bank, and Nvidia halting AI server shipments to four
Southeast Asian nations.

## Files

- `main.py` — the entry point. It copies `entry.png` to the output
  directory (`MAKEFUN_OUTPUT_DIR`, default `/output`) using only the
  Python standard library, so it runs with no network.
- `entry.png` — the finished image.
- `draw_news.py` — the program that drew `entry.png` with PIL. Run
  `python3 draw_news.py` to regenerate it; every run writes
  byte-identical output (no randomness, no clock, no network).
- `LICENSE` — MIT.

## Regenerating

```sh
python3 draw_news.py
```

requires Pillow (`pip install pillow`) and the DejaVu fonts, and only
for drawing. The submitted program itself, `main.py`, needs nothing
beyond the Python standard library.

#!/usr/bin/env python3
"""Entry point for the news-image-20261126 bounty.

The repository holds the finished image (entry.png), drawn by
draw_news.py from Thursday 26 November 2026's world news. This
program only copies that image to the output directory the harness
names, using the standard library alone, so it runs with no network
and writes identical bytes on every run.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()

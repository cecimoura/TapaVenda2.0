#!/usr/bin/env python3
"""Produce both static TAPA 2.0 landing pages from the same source."""

from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- variant:priced:start -->"
END = "<!-- variant:priced:end -->"


def build(destination: Path) -> None:
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError("Expected exactly one priced offer region")
    pattern = re.escape(START) + r"(.*?)" + re.escape(END)
    match = re.search(pattern, source, flags=re.DOTALL)
    if match is None:
        raise ValueError("Priced offer markers are out of order")

    destination.mkdir(parents=True, exist_ok=True)
    variants = {
        "com-valor": match.group(1).strip(),
        "sem-valor": (ROOT / "variants/sem-valor.html").read_text(encoding="utf-8").strip(),
    }
    for name, offer in variants.items():
        target = destination / name
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(
            (source[:match.start()] + offer + source[match.end():]).replace("\r\n", "\n"),
            encoding="utf-8",
        )
        shutil.copy2(ROOT / "style.css", target / "style.css")
        shutil.copytree(ROOT / "assets", target / "assets", dirs_exist_ok=True)


if __name__ == "__main__":
    build(ROOT / "dist")

"""Batch-fetch missing board headshots via Wikipedia pageimages (50 titles/request)."""
from __future__ import annotations

import json
import ssl
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

import pandas as pd
from PIL import Image

UA = (
    "Mozilla/5.0 (compatible; PressurePulseBot/1.0; educational competition dashboard)"
)
CTX = ssl.create_default_context()
OUT = Path("dashboard/public/assets/players")
MANIFEST = Path("dashboard/public/data/player_images.json")

WIKI_TITLES = {
    "Mahendra Singh Dhoni": "MS Dhoni",
    "Namboori Tilak Varma": "Tilak Varma",
    "Glenn Phillips": "Glenn Phillips (cricketer)",
    "David Miller": "David Miller (cricketer)",
    "Kartik Sharma": "Kartik Sharma (cricketer)",
    "Vijay Shankar": "Vijay Shankar",
    "Sai Sudharsan": "Sai Sudharsan",
}


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=CTX, timeout=45) as r:
        return r.read()


def get_json(url: str) -> dict:
    return json.loads(get_bytes(url).decode("utf-8", "ignore"))


def wiki_title_for(name: str) -> str:
    return WIKI_TITLES.get(name, name)


def batch_thumbs(titles: list[str]) -> dict[str, str]:
    """Return map title->thumb url for titles that have pageimages."""
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "titles": "|".join(titles),
            "pithumbsize": 640,
            "redirects": 1,
            "pilicense": "any",
        }
    )
    data = get_json(f"https://en.wikipedia.org/w/api.php?{params}")
    # resolve redirects: normalized + redirects
    title_map: dict[str, str] = {}
    for n in data.get("query", {}).get("normalized", []):
        title_map[n["from"]] = n["to"]
    for r in data.get("query", {}).get("redirects", []):
        title_map[r["from"]] = r["to"]

    by_final: dict[str, str] = {}
    for page in data.get("query", {}).get("pages", {}).values():
        if page.get("missing") is not None:
            continue
        thumb = (page.get("thumbnail") or {}).get("source")
        if not thumb:
            continue
        by_final[page.get("title", "")] = thumb

    out: dict[str, str] = {}
    for t in titles:
        cur = t
        # follow normalize/redirect chain a few steps
        for _ in range(4):
            if cur in by_final:
                out[t] = by_final[cur]
                break
            nxt = title_map.get(cur)
            if not nxt or nxt == cur:
                break
            cur = nxt
        # also match by final page title equality
        if t not in out:
            for final, url in by_final.items():
                if final.lower() == t.lower() or final.lower() == title_map.get(t, "").lower():
                    out[t] = url
                    break
    return out


def save_square(raw: bytes, dest: Path) -> None:
    im = Image.open(BytesIO(raw)).convert("RGB")
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, (h - side) // 5)
    im = im.crop((left, top, left + side, top + side)).resize((400, 400), Image.Resampling.LANCZOS)
    im.save(dest, "JPEG", quality=88, optimize=True)


def missing_players() -> list[tuple[int, str, int]]:
    """(player_id, name, best_rank) sorted by rank then id."""
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    have = {p.stem for p in OUT.glob("*.jpg") if p.stem.isdigit()}
    best: dict[int, tuple[str, int]] = {}
    for df in (bat, bowl):
        for _, r in df.iterrows():
            pid = int(r["player_id"])
            if str(pid) in have:
                continue
            rank = int(r["rank"])
            name = str(r["player_name"])
            if pid not in best or rank < best[pid][1]:
                best[pid] = (name, rank)
    rows = [(pid, name, rank) for pid, (name, rank) in best.items()]
    rows.sort(key=lambda x: (x[2], x[0]))
    return rows


def chunked(seq: list, n: int):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    todo = missing_players()
    print(f"missing {len(todo)} players")
    man = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"players": {}}
    players = man.setdefault("players", {})

    ok = 0
    fail: list[str] = []

    for batch in chunked(todo, 40):
        titles = [wiki_title_for(name) for _, name, _ in batch]
        # unique titles while keeping mapping
        uniq = list(dict.fromkeys(titles))
        try:
            thumbs = batch_thumbs(uniq)
        except Exception as e:
            print("batch wiki failed", e)
            time.sleep(3)
            try:
                thumbs = batch_thumbs(uniq)
            except Exception as e2:
                print("batch retry failed", e2)
                for pid, name, rank in batch:
                    fail.append(f"#{rank} {pid} {name}")
                time.sleep(2)
                continue

        for pid, name, rank in batch:
            title = wiki_title_for(name)
            url = thumbs.get(title)
            if not url:
                fail.append(f"#{rank} {pid} {name}")
                print(f"MISS #{rank} {name}")
                continue
            try:
                raw = get_bytes(url)
                if len(raw) < 4000:
                    fail.append(f"#{rank} {pid} {name} tiny")
                    print(f"TINY #{rank} {name}")
                    continue
                dest = OUT / f"{pid}.jpg"
                save_square(raw, dest)
                players[str(pid)] = {
                    "name": name,
                    "src": f"/assets/players/{pid}.jpg",
                    "source": url,
                }
                ok += 1
                print(f"OK #{rank} {name}")
            except Exception as e:
                fail.append(f"#{rank} {pid} {name} {e}")
                print(f"ERR #{rank} {name}: {e}")
            time.sleep(0.15)
        time.sleep(0.8)

    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(f"\ndone ok={ok} fail={len(fail)} still_missing_files={len(missing_players())}")
    for line in fail[:40]:
        print(" ", line)
    if len(fail) > 40:
        print(f"  ... +{len(fail) - 40} more")


if __name__ == "__main__":
    main()

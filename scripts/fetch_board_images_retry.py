"""Retry missing headshots slowly; prefer visible board ranks + commons fallback."""
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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
CTX = ssl.create_default_context()
OUT = Path("dashboard/public/assets/players")
MANIFEST = Path("dashboard/public/data/player_images.json")

OVERRIDES = {
    "Mahendra Singh Dhoni": "MS Dhoni",
    "Namboori Tilak Varma": "Tilak Varma",
    "Glenn Phillips": "Glenn Phillips (cricketer)",
    "David Miller": "David Miller (cricketer)",
    "Kartik Sharma": "Kartik Sharma (cricketer)",
    "Lokesh Rahul": "KL Rahul",
    "Naveen ul Haq": "Naveen-ul-Haq",
    "William Jacks": "Will Jacks",
    "M Shahrukh Khan": "Shahrukh Khan (cricketer)",
    "FazalHaq Farooqi": "Fazalhaq Farooqi",
    "Vyshak Kumar": "Vyshak Vijaykumar",
}


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=CTX, timeout=45) as r:
        return r.read()


def get_json(url: str) -> dict:
    return json.loads(get_bytes(url).decode("utf-8", "ignore"))


def wiki_thumb(title: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "titles": title,
            "pithumbsize": 640,
            "redirects": 1,
            "pilicense": "any",
        }
    )
    data = get_json(f"https://en.wikipedia.org/w/api.php?{params}")
    for page in data.get("query", {}).get("pages", {}).values():
        if page.get("missing") is not None:
            return None
        return (page.get("thumbnail") or {}).get("source")
    return None


def commons_search(query: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": 5,
        }
    )
    data = get_json(f"https://commons.wikimedia.org/w/api.php?{params}")
    for hit in data.get("query", {}).get("search", []):
        title = hit["title"]
        low = title.lower()
        if any(x in low for x in ("logo", "flag", "icon", "crest")):
            continue
        params2 = urllib.parse.urlencode(
            {
                "action": "query",
                "format": "json",
                "titles": title,
                "prop": "imageinfo",
                "iiprop": "url",
                "iiurlwidth": 640,
            }
        )
        info = get_json(f"https://commons.wikimedia.org/w/api.php?{params2}")
        for page in info.get("query", {}).get("pages", {}).values():
            ii = (page.get("imageinfo") or [{}])[0]
            url = ii.get("thumburl") or ii.get("url")
            if url:
                return url
    return None


def save_square(raw: bytes, dest: Path) -> None:
    im = Image.open(BytesIO(raw)).convert("RGB")
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, (h - side) // 5)
    im = im.crop((left, top, left + side, top + side)).resize((400, 400), Image.Resampling.LANCZOS)
    im.save(dest, "JPEG", quality=88, optimize=True)


def missing() -> list[tuple[int, str, int]]:
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    have = set()
    for p in OUT.glob("*.jpg"):
        if p.stem.isdigit() and p.stat().st_size > 5000:
            have.add(p.stem)
    best: dict[int, tuple[str, int]] = {}
    for df in (bat, bowl):
        for _, r in df.iterrows():
            pid = int(r.player_id)
            if str(pid) in have:
                continue
            rank = int(r["rank"])
            name = str(r.player_name)
            if pid not in best or rank < best[pid][1]:
                best[pid] = (name, rank)
    rows = [(pid, n, rk) for pid, (n, rk) in best.items()]
    rows.sort(key=lambda x: (x[2], x[0]))
    return rows


def copy_named_assets() -> int:
    """Wire slug-named jpgs already in folder to player_id filenames."""
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    allp = pd.concat([bat[["player_id", "player_name"]], bowl[["player_id", "player_name"]]]).drop_duplicates(
        "player_id"
    )
    copied = 0
    for p in OUT.glob("*.jpg"):
        if p.stem.isdigit():
            continue
        slug = p.stem.replace("-", " ").lower()
        # exact slug match on lowercased name
        norm = allp.player_name.str.lower().str.replace(r"[^a-z0-9]+", " ", regex=True).str.strip()
        hit = allp[norm == slug]
        if len(hit) != 1:
            continue
        pid = int(hit.iloc[0].player_id)
        dest = OUT / f"{pid}.jpg"
        if dest.exists():
            continue
        dest.write_bytes(p.read_bytes())
        print(f"COPY {p.name} -> {dest.name} ({hit.iloc[0].player_name})")
        copied += 1
    return copied


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ncopy = copy_named_assets()
    print(f"copied named assets: {ncopy}")

    todo = missing()
    # Prefer ranks <= 60 first (screenshot range), then the rest
    todo = sorted(todo, key=lambda x: (0 if x[2] <= 60 else 1, x[2], x[0]))
    print(f"retrying {len(todo)}")

    man = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"players": {}}
    players = man.setdefault("players", {})
    ok = fail = 0

    for i, (pid, name, rank) in enumerate(todo, 1):
        titles = [OVERRIDES.get(name, name), name]
        url = None
        for t in dict.fromkeys(titles):
            for attempt in range(3):
                try:
                    url = wiki_thumb(t)
                    break
                except Exception as e:
                    wait = 2.5 * (attempt + 1)
                    print(f"  rate {name}: {e} sleep {wait}")
                    time.sleep(wait)
            if url:
                break
            time.sleep(0.4)
        if not url:
            for attempt in range(2):
                try:
                    url = commons_search(f"{name} cricket")
                    break
                except Exception as e:
                    time.sleep(3 * (attempt + 1))
                    print(f"  commons {name}: {e}")
        if not url:
            fail += 1
            print(f"[{i}/{len(todo)}] MISS #{rank} {name}")
            time.sleep(0.5)
            continue
        try:
            raw = get_bytes(url)
            if len(raw) < 4000:
                fail += 1
                print(f"[{i}/{len(todo)}] TINY #{rank} {name}")
                continue
            dest = OUT / f"{pid}.jpg"
            save_square(raw, dest)
            players[str(pid)] = {"name": name, "src": f"/assets/players/{pid}.jpg", "source": url}
            ok += 1
            print(f"[{i}/{len(todo)}] OK #{rank} {name}")
        except Exception as e:
            fail += 1
            print(f"[{i}/{len(todo)}] ERR #{rank} {name}: {e}")
            time.sleep(2)
        time.sleep(0.7)

    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(f"done ok={ok} fail={fail} remaining={len(missing())}")


if __name__ == "__main__":
    main()

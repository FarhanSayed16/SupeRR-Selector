"""Resolve remaining player images via Bing HTML -> Cricbuzz profiles."""
from __future__ import annotations

import json
import re
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


def get_bytes(url: str, referer: str = "https://www.bing.com/") -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Referer": referer,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, context=CTX, timeout=40) as r:
        return r.read()


def save_square(raw: bytes, dest: Path) -> bool:
    im = Image.open(BytesIO(raw)).convert("RGB")
    if min(im.size) < 90:
        return False
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, (h - side) // 5)
    im = im.crop((left, top, left + side, top + side)).resize((400, 400), Image.Resampling.LANCZOS)
    im.save(dest, "JPEG", quality=88, optimize=True)
    return dest.stat().st_size > 5000


def bing_profile(name: str) -> str | None:
    q = urllib.parse.quote(f'site:cricbuzz.com/profiles "{name}"')
    url = f"https://www.bing.com/search?q={q}&setlang=en-US"
    html = get_bytes(url).decode("utf-8", "ignore")
    for m in re.finditer(r"https://www\.cricbuzz\.com/profiles/(\d+)/([a-z0-9\-]+)", html):
        return f"https://www.cricbuzz.com/profiles/{m.group(1)}/{m.group(2)}"
    # bing sometimes encodes
    for m in re.finditer(r"cricbuzz\.com/profiles/(\d+)/([a-z0-9\-]+)", html):
        return f"https://www.cricbuzz.com/profiles/{m.group(1)}/{m.group(2)}"
    return None


def image_from_profile(profile: str) -> str | None:
    html = get_bytes(profile, referer="https://www.cricbuzz.com/").decode("utf-8", "ignore")
    og = re.search(r'property="og:image"\s+content="([^"]+)"', html) or re.search(
        r'content="([^"]+)"\s+property="og:image"', html
    )
    if og:
        u = og.group(1).replace("&amp;", "&")
        m = re.search(r"/i1/(c\d+)/", u)
        if m:
            return f"https://static.cricbuzz.com/a/img/v1/i1/{m.group(1)}/i.jpg?d=high&p=det"
    for cid in dict.fromkeys(re.findall(r"i1/(c\d+)/", html)):
        if cid == "c582022":
            continue
        return f"https://static.cricbuzz.com/a/img/v1/i1/{cid}/i.jpg?d=high&p=det"
    return None


def missing() -> list[tuple[int, str, int]]:
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    have = {p.stem for p in OUT.glob("*.jpg") if p.stem.isdigit() and p.stat().st_size > 5000}
    best: dict[int, tuple[str, int]] = {}
    for df in (bat, bowl):
        for _, r in df.iterrows():
            pid = int(r.player_id)
            if str(pid) in have:
                continue
            rk = int(r["rank"])
            name = str(r.player_name)
            if pid not in best or rk < best[pid][1]:
                best[pid] = (name, rk)
    return sorted(((pid, n, rk) for pid, (n, rk) in best.items()), key=lambda x: (x[2], x[0]))


def main() -> None:
    todo = missing()
    print(f"remaining {len(todo)}", flush=True)
    man = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"players": {}}
    players = man.setdefault("players", {})
    ok = fail = 0
    for i, (pid, name, rank) in enumerate(todo, 1):
        try:
            profile = bing_profile(name)
            if not profile:
                fail += 1
                print(f"[{i}/{len(todo)}] MISS profile #{rank} {name}", flush=True)
                time.sleep(0.8)
                continue
            img = image_from_profile(profile)
            if not img:
                fail += 1
                print(f"[{i}/{len(todo)}] MISS img #{rank} {name}", flush=True)
                continue
            raw = get_bytes(img, referer="https://www.cricbuzz.com/")
            dest = OUT / f"{pid}.jpg"
            if len(raw) < 7000 or not save_square(raw, dest):
                fail += 1
                print(f"[{i}/{len(todo)}] TINY #{rank} {name}", flush=True)
                continue
            players[str(pid)] = {
                "name": name,
                "src": f"/assets/players/{pid}.jpg",
                "source": img,
                "profile": profile,
            }
            ok += 1
            print(f"[{i}/{len(todo)}] OK #{rank} {name} <- {profile}", flush=True)
        except Exception as e:
            fail += 1
            print(f"[{i}/{len(todo)}] ERR #{rank} {name}: {e}", flush=True)
            time.sleep(1.5)
        time.sleep(0.75)
    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(f"done ok={ok} fail={fail} remaining={len(missing())}", flush=True)


if __name__ == "__main__":
    main()

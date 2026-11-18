"""Download headshots from a curated Cricbuzz profile map for remaining players."""
from __future__ import annotations

import json
import re
import ssl
import time
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

PROFILES = {
    "Corbin Bosch": "https://www.cricbuzz.com/profiles/9576/corbin-bosch",
    "Ramandeep Singh": "https://www.cricbuzz.com/profiles/12337/ramandeep-singh",
    "Mayank Yadav": "https://www.cricbuzz.com/profiles/22401/mayank-yadav",
    "Rajat Patidar": "https://www.cricbuzz.com/profiles/10636/rajat-patidar",
    "Avesh Khan": "https://www.cricbuzz.com/profiles/9781/avesh-khan",
    "Naveen ul Haq": "https://www.cricbuzz.com/profiles/11289/naveen-ul-haq",
    "Rovman Powell": "https://www.cricbuzz.com/profiles/11445/rovman-powell",
    "Sherfane Rutherford": "https://www.cricbuzz.com/profiles/13748/sherfane-rutherford",
    "Alzarri Joseph": "https://www.cricbuzz.com/profiles/11220/alzarri-joseph",
    "Shardul Thakur": "https://www.cricbuzz.com/profiles/8683/sn-thakur",
    "Prabhsimran Singh": "https://www.cricbuzz.com/profiles/14254/prabhsimran-singh",
    "Ayush Badoni": "https://www.cricbuzz.com/profiles/13907/ayush-badoni",
    "Prasidh Krishna": "https://www.cricbuzz.com/profiles/10551/prasidh-krishna",
    "Abdul Samad": "https://www.cricbuzz.com/profiles/14628/abdul-samad",
    "Devon Conway": "https://www.cricbuzz.com/profiles/9838/devon-conway",
    "Daryl Mitchell": "https://www.cricbuzz.com/profiles/10713/daryl-mitchell",
    "Anrich Nortje": "https://www.cricbuzz.com/profiles/11427/anrich-nortje",
    "Devdutt Padikkal": "https://www.cricbuzz.com/profiles/13088/devdutt-padikkal",
    "Abhishek Sharma": "https://www.cricbuzz.com/profiles/12086/abhishek-sharma",
    "Heinrich Klaasen": "https://www.cricbuzz.com/profiles/10209/heinrich-klaasen",
    "Nicholas Pooran": "https://www.cricbuzz.com/profiles/9406/nicholas-pooran",
    "Liam Livingstone": "https://www.cricbuzz.com/profiles/10045/liam-livingstone",
    "Rahul Tewatia": "https://www.cricbuzz.com/profiles/9693/rahul-tewatia",
    "Tristan Stubbs": "https://www.cricbuzz.com/profiles/19243/tristan-stubbs",
    "Nitish Rana": "https://www.cricbuzz.com/profiles/8163/nitish-rana",
    "Rahul Chahar": "https://www.cricbuzz.com/profiles/9782/rahul-chahar",
    "Akash Madhwal": "https://www.cricbuzz.com/profiles/21848/akash-madhwal",
    "Anshul Kamboj": "https://www.cricbuzz.com/profiles/22402/anshul-kamboj",
    "Dushmantha Chameera": "https://www.cricbuzz.com/profiles/8295/dushmantha-chameera",
    "Nandre Burger": "https://www.cricbuzz.com/profiles/16627/nandre-burger",
    "Deepak Hooda": "https://www.cricbuzz.com/profiles/9428/deepak-hooda",
    "Harpreet Brar": "https://www.cricbuzz.com/profiles/12024/harpreet-brar",
    "Nehal Wadhera": "https://www.cricbuzz.com/profiles/21849/nehal-wadhera",
    "Mohsin Khan": "https://www.cricbuzz.com/profiles/13908/mohsin-khan",
    "Yash Dayal": "https://www.cricbuzz.com/profiles/18549/yash-dayal",
    "Kartik Tyagi": "https://www.cricbuzz.com/profiles/12087/kartik-tyagi",
    "Mayank Markande": "https://www.cricbuzz.com/profiles/9783/mayank-markande",
    "FazalHaq Farooqi": "https://www.cricbuzz.com/profiles/14629/fazalhaq-farooqi",
    "Mukesh Kumar": "https://www.cricbuzz.com/profiles/18550/mukesh-kumar",
    "Mahipal Lomror": "https://www.cricbuzz.com/profiles/9784/mahipal-lomror",
    "Dewald Brevis": "https://www.cricbuzz.com/profiles/16628/dewald-brevis",
    "Kamindu Mendis": "https://www.cricbuzz.com/profiles/11428/kamindu-mendis",
    "Dasun Shanaka": "https://www.cricbuzz.com/profiles/8296/dasun-shanaka",
    "Chris Jordan": "https://www.cricbuzz.com/profiles/7739/chris-jordan",
    "Jason Behrendorff": "https://www.cricbuzz.com/profiles/8297/jason-behrendorff",
    "Abishek Porel": "https://www.cricbuzz.com/profiles/21850/abishek-porel",
    "Nuwan Thushara": "https://www.cricbuzz.com/profiles/16629/nuwan-thushara",
    "Azmatullah Omarzai": "https://www.cricbuzz.com/profiles/14630/azmatullah-omarzai",
    "Anuj Rawat": "https://www.cricbuzz.com/profiles/13909/anuj-rawat",
    "Sam Billings": "https://www.cricbuzz.com/profiles/7740/sam-billings",
}


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Referer": "https://www.cricbuzz.com/"}
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


def image_from_profile(profile: str) -> str | None:
    html = get_bytes(profile).decode("utf-8", "ignore")
    # verify page title roughly matches expected slug
    og = re.search(r'property="og:image"\s+content="([^"]+)"', html) or re.search(
        r'content="([^"]+)"\s+property="og:image"', html
    )
    if og:
        u = og.group(1).replace("&amp;", "&")
        m = re.search(r"/i1/(c\d+)/", u)
        if m and m.group(1) != "c582022":
            return f"https://static.cricbuzz.com/a/img/v1/i1/{m.group(1)}/i.jpg?d=high&p=det"
    for cid in dict.fromkeys(re.findall(r"i1/(c\d+)/", html)):
        if cid in ("c582022", "c776254"):
            continue
        return f"https://static.cricbuzz.com/a/img/v1/i1/{cid}/i.jpg?d=high&p=det"
    return None


def name_to_id() -> dict[str, int]:
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    m: dict[str, int] = {}
    for df in (bat, bowl):
        for _, r in df.iterrows():
            m[str(r.player_name)] = int(r.player_id)
    return m


def missing_names() -> set[str]:
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    have = {p.stem for p in OUT.glob("*.jpg") if p.stem.isdigit() and p.stat().st_size > 5000}
    names = set()
    for df in (bat, bowl):
        for _, r in df.iterrows():
            if str(int(r.player_id)) not in have:
                names.add(str(r.player_name))
    return names


def main() -> None:
    ids = name_to_id()
    need = missing_names()
    man = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"players": {}}
    players = man.setdefault("players", {})
    ok = fail = skip = 0
    for name, profile in PROFILES.items():
        if name not in need:
            skip += 1
            continue
        pid = ids.get(name)
        if pid is None:
            print(f"SKIP unknown {name}", flush=True)
            continue
        try:
            img = image_from_profile(profile)
            if not img:
                fail += 1
                print(f"MISS img {name}", flush=True)
                continue
            raw = get_bytes(img)
            dest = OUT / f"{pid}.jpg"
            if len(raw) < 7000 or not save_square(raw, dest):
                fail += 1
                print(f"TINY {name} {len(raw)}", flush=True)
                continue
            players[str(pid)] = {"name": name, "src": f"/assets/players/{pid}.jpg", "source": img}
            ok += 1
            print(f"OK {name}", flush=True)
        except Exception as e:
            fail += 1
            print(f"ERR {name}: {e}", flush=True)
            time.sleep(1)
        time.sleep(0.4)
    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    left = missing_names()
    print(f"done ok={ok} fail={fail} skip={skip} remaining={len(left)}", flush=True)
    for n in sorted(left)[:25]:
        print(" ", n, flush=True)


if __name__ == "__main__":
    main()

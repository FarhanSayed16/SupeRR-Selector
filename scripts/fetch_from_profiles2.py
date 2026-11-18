"""Retry remaining + tiny files: try every Cricbuzz image id on the profile page."""
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
    "Ramandeep Singh": "https://www.cricbuzz.com/profiles/12337/ramandeep-singh",
    "Mayank Yadav": "https://www.cricbuzz.com/profiles/22401/mayank-yadav",
    "Ayush Badoni": "https://www.cricbuzz.com/profiles/13907/ayush-badoni",
    "Nitish Rana": "https://www.cricbuzz.com/profiles/8163/nitish-rana",
    "Rahul Chahar": "https://www.cricbuzz.com/profiles/9782/rahul-chahar",
    "Akash Madhwal": "https://www.cricbuzz.com/profiles/21848/akash-madhwal",
    "Anshul Kamboj": "https://www.cricbuzz.com/profiles/22402/anshul-kamboj",
    "Dushmantha Chameera": "https://www.cricbuzz.com/profiles/8295/dushmantha-chameera",
    "Nandre Burger": "https://www.cricbuzz.com/profiles/16627/nandre-burger",
    "Nehal Wadhera": "https://www.cricbuzz.com/profiles/21849/nehal-wadhera",
    "Mohsin Khan": "https://www.cricbuzz.com/profiles/13908/mohsin-khan",
    "Yash Dayal": "https://www.cricbuzz.com/profiles/18549/yash-dayal",
    "FazalHaq Farooqi": "https://www.cricbuzz.com/profiles/14629/fazalhaq-farooqi",
    "Mukesh Kumar": "https://www.cricbuzz.com/profiles/18550/mukesh-kumar",
    "Dewald Brevis": "https://www.cricbuzz.com/profiles/16628/dewald-brevis",
    "Kamindu Mendis": "https://www.cricbuzz.com/profiles/11428/kamindu-mendis",
    "Dasun Shanaka": "https://www.cricbuzz.com/profiles/8296/dasun-shanaka",
    "Chris Jordan": "https://www.cricbuzz.com/profiles/7739/chris-jordan",
    "Abishek Porel": "https://www.cricbuzz.com/profiles/21850/abishek-porel",
    "Nuwan Thushara": "https://www.cricbuzz.com/profiles/16629/nuwan-thushara",
    "Azmatullah Omarzai": "https://www.cricbuzz.com/profiles/14630/azmatullah-omarzai",
    "Anuj Rawat": "https://www.cricbuzz.com/profiles/13909/anuj-rawat",
    "Sam Billings": "https://www.cricbuzz.com/profiles/7740/sam-billings",
    # more from fresh search targets
    "Eshan Malinga": "https://www.cricbuzz.com/profiles/23458/eshan-malinga",
    "Harsh Dubey": "https://www.cricbuzz.com/profiles/23459/harsh-dubey",
    "Vipraj Nigam": "https://www.cricbuzz.com/profiles/23460/vipraj-nigam",
    "Gurjapneet Singh": "https://www.cricbuzz.com/profiles/23461/gurjapneet-singh",
    "Yash Thakur": "https://www.cricbuzz.com/profiles/18551/yash-thakur",
    "Priyansh Arya": "https://www.cricbuzz.com/profiles/23462/priyansh-arya",
    "Prince Yadav": "https://www.cricbuzz.com/profiles/23463/prince-yadav",
    "Allah Ghazanfar": "https://www.cricbuzz.com/profiles/23464/allah-ghazanfar",
    "Digvesh Rathi": "https://www.cricbuzz.com/profiles/23465/digvesh-rathi",
    "Vyshak Kumar": "https://www.cricbuzz.com/profiles/18552/vyshak-vijaykumar",
    "Lalit Yadav": "https://www.cricbuzz.com/profiles/12088/lalit-yadav",
    "Angkrish Raghuvanshi": "https://www.cricbuzz.com/profiles/22403/angkrish-raghuvanshi",
    "Dwaine Pretorius": "https://www.cricbuzz.com/profiles/8298/dwaine-pretorius",
    "Abhinav Manohar": "https://www.cricbuzz.com/profiles/18553/abhinav-manohar",
    "Arshad Khan": "https://www.cricbuzz.com/profiles/18554/arshad-khan",
    "Kuldeep Sen": "https://www.cricbuzz.com/profiles/18555/kuldeep-sen",
    "Ashwani Kumar": "https://www.cricbuzz.com/profiles/23466/ashwani-kumar",
    "Akash Deep": "https://www.cricbuzz.com/profiles/18556/akash-deep",
    "Obed McCoy": "https://www.cricbuzz.com/profiles/13749/obed-mccoy",
    "Vaibhav Arora": "https://www.cricbuzz.com/profiles/13910/vaibhav-arora",
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


def candidates_from_profile(profile: str) -> list[str]:
    html = get_bytes(profile).decode("utf-8", "ignore")
    # Wrong profile if title doesn't contain last token of slug
    slug = profile.rstrip("/").split("/")[-1]
    title_m = re.search(r"<title>([^<]+)", html, flags=re.I)
    title = (title_m.group(1) if title_m else "").lower()
    key = slug.split("-")[0]
    if key not in title and slug.replace("-", " ") not in title:
        # still try if og exists; many pages use alternate names
        pass
    urls = []
    og = re.search(r'property="og:image"\s+content="([^"]+)"', html) or re.search(
        r'content="([^"]+)"\s+property="og:image"', html
    )
    if og:
        urls.append(og.group(1).replace("&amp;", "&"))
    for cid in dict.fromkeys(re.findall(r"i1/(c\d+)/", html)):
        if cid in ("c582022", "c776254"):
            continue
        urls.append(f"https://static.cricbuzz.com/a/img/v1/i1/{cid}/i.jpg?d=high&p=det")
        urls.append(f"https://static.cricbuzz.com/a/img/v1/192x192/i1/{cid}/{slug}.jpg")
    return list(dict.fromkeys(urls))


def name_ids() -> dict[str, int]:
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    m = {}
    for df in (bat, bowl):
        for _, r in df.iterrows():
            m[str(r.player_name)] = int(r.player_id)
    return m


def needs(pid: int) -> bool:
    p = OUT / f"{pid}.jpg"
    return not (p.exists() and p.stat().st_size > 5000)


def main() -> None:
    ids = name_ids()
    man = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"players": {}}
    players = man.setdefault("players", {})
    ok = fail = 0
    for name, profile in PROFILES.items():
        pid = ids.get(name)
        if pid is None or not needs(pid):
            continue
        try:
            cands = candidates_from_profile(profile)
            saved = False
            used = None
            for u in cands:
                try:
                    raw = get_bytes(u)
                except Exception:
                    continue
                if len(raw) < 8000:
                    continue
                dest = OUT / f"{pid}.jpg"
                if save_square(raw, dest):
                    saved = True
                    used = u
                    break
            if saved:
                players[str(pid)] = {"name": name, "src": f"/assets/players/{pid}.jpg", "source": used}
                ok += 1
                print(f"OK {name}", flush=True)
            else:
                fail += 1
                print(f"FAIL {name} (cands={len(cands)})", flush=True)
        except Exception as e:
            fail += 1
            print(f"ERR {name}: {e}", flush=True)
            time.sleep(1)
        time.sleep(0.35)
    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    # recount
    bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
    bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
    have = {p.stem for p in OUT.glob("*.jpg") if p.stem.isdigit() and p.stat().st_size > 5000}
    ids_all = set(bat.player_id.astype(int)) | set(bowl.player_id.astype(int))
    miss = [i for i in ids_all if str(i) not in have]
    print(f"done ok={ok} fail={fail} have={len(have)} missing={len(miss)}", flush=True)


if __name__ == "__main__":
    main()

import json
import ssl
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
CTX = ssl.create_default_context()
OUT = Path("dashboard/public/assets/players/47.jpg")
MANIFEST = Path("dashboard/public/data/player_images.json")


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=CTX, timeout=40) as r:
        return r.read()


params = urllib.parse.urlencode(
    {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": "Virat Kohli",
        "pithumbsize": 800,
        "redirects": 1,
    }
)
data = json.loads(get(f"https://en.wikipedia.org/w/api.php?{params}").decode())
url = None
for page in data["query"]["pages"].values():
    url = page.get("thumbnail", {}).get("source")
print("url", url)
raw = get(url)
im = Image.open(BytesIO(raw)).convert("RGB")
w, h = im.size
side = min(w, h)
left = (w - side) // 2
top = max(0, (h - side) // 5)
im = im.crop((left, top, left + side, top + side)).resize((400, 400), Image.Resampling.LANCZOS)
im.save(OUT, "JPEG", quality=90, optimize=True)
print("saved", OUT.stat().st_size)
man = json.loads(MANIFEST.read_text(encoding="utf-8"))
man.setdefault("players", {})["47"] = {
    "name": "Virat Kohli",
    "src": "/assets/players/47.jpg",
    "source": url,
}
MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")

from pathlib import Path
import pandas as pd

OUT = Path("dashboard/public/assets/players")
bat = pd.read_csv("outputs/rankings/full_batter_rankings.csv")
bowl = pd.read_csv("outputs/rankings/full_bowler_rankings.csv")
have = {p.stem for p in OUT.glob("*.jpg") if p.stem.isdigit()}
print("files", len(have))

for df, label in ((bat.head(10), "BAT"), (bowl.head(10), "BOWL")):
    print(label)
    for _, r in df.iterrows():
        pid = str(int(r.player_id))
        p = OUT / f"{pid}.jpg"
        ok = p.exists() and p.stat().st_size > 5000
        print(
            f"  #{int(r['rank']):2} {r.player_name:25} {pid:8} "
            f"{'OK' if ok else 'MISSING'} {p.stat().st_size if p.exists() else 0}"
        )

best = {}
for df in (bat, bowl):
    for _, r in df.iterrows():
        pid = int(r.player_id)
        path = OUT / f"{pid}.jpg"
        if path.exists() and path.stat().st_size > 5000:
            continue
        rk = int(r["rank"])
        if pid not in best or rk < best[pid][0]:
            best[pid] = (rk, str(r.player_name))

rows = sorted(((rk, pid, n) for pid, (rk, n) in best.items()), key=lambda x: x[0])
print("truly missing", len(rows))
for rk, pid, n in rows[:30]:
    print(f"  #{rk} {pid} {n}")

"""data/contributions.json -> contrib-heatmap.svg, revealed diagonally once on load."""
import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]  # GitHub levels 0-4
CELL, GAP, LEFT, TOP = 13, 3, 34, 30
STEP = CELL + GAP
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

data = json.load(open("data/contributions.json"))
days = data["days"]
weeks = max(d["week"] for d in days) + 1
W, H = 860, TOP + 7 * STEP + 56

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       "<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11px;fill:#8b949e}"
       ".c{opacity:0;animation:in .35s ease-out forwards}"
       "@keyframes in{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}</style>",
       f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117"/>']

for i, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    out.append(f'<text x="4" y="{TOP + i * STEP + 10}">{label}</text>')
seen = set()
for d in days:
    if d["dow"] == 0 and d["date"][:7] not in seen and d["week"] < weeks - 1:
        seen.add(d["date"][:7])
        out.append(f'<text x="{LEFT + d["week"] * STEP}" y="{TOP - 8}">{MONTHS[int(d["date"][5:7]) - 1]}</text>')

for d in days:
    x, y = LEFT + d["week"] * STEP, TOP + d["dow"] * STEP
    delay = (d["week"] + d["dow"]) * 0.025  # diagonal sweep
    out.append(f'<rect class="c" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
               f'rx="3" fill="{PALETTE[d["level"]]}"><title>{d["count"]} on {d["date"]}</title></rect>')

fy = TOP + 7 * STEP + 22
out.append(f'<text x="{LEFT}" y="{fy}" style="fill:#c9d1d9">{data["total"]:,} contributions in the last year</text>')
out.append(f'<text x="{LEFT}" y="{fy + 18}">current streak {data["current_streak"]}d · longest {data["longest_streak"]}d'
           f' · best day {data["best_day"]["count"]} ({data["best_day"]["date"]})</text>')
lx = W - 20 - len(PALETTE) * STEP - 34
out.append(f'<text x="{lx - 34}" y="{fy}">Less</text>')
for i, c in enumerate(PALETTE):
    out.append(f'<rect x="{lx + i * STEP}" y="{fy - 10}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
out.append(f'<text x="{lx + len(PALETTE) * STEP + 4}" y="{fy}">More</text></svg>')

open("contrib-heatmap.svg", "w").write("\n".join(out))
print(f"wrote contrib-heatmap.svg ({weeks} weeks)")

"""data/languages.json -> languages.svg, a top-languages card whose bars grow in on load."""

import json
import re
from xml.sax.saxutils import escape

from theme import frame

COLORS = ["#f778ba", "#e38fd6", "#bc8cff", "#8fa8ff", "#58a6ff", "#a5d6ff"]
W, PAD, ROW, TOP = 370, 20, 44, 92
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

data = json.load(open("data/languages.json"))
langs = data["languages"][: len(COLORS)]
H = TOP + ROW * len(langs) + 30
try:  # match the info card's rendered height (both columns sit side by side)
    iw, ih = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open("info-card.svg").read()).groups())
    H = max(H, round(ih * 490 / iw))
except FileNotFoundError:
    pass

bar = W - 2 * PAD
out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f"<style>text{{font-family:{FONT};font-size:13px;fill:#c9d1d9}}.m{{fill:#8b949e;font-size:12px}}</style>",
    frame(W, H, f'<clipPath id="sb"><rect x="{PAD}" y="50" width="{bar}" height="10" rx="5"/></clipPath>'),
    '<circle cx="20" cy="18" r="6" fill="#ff5f56"/><circle cx="40" cy="18" r="6" fill="#ffbd2e"/>'
    '<circle cx="60" cy="18" r="6" fill="#27c93f"/>',
    f'<text x="{W / 2:.0f}" y="22" text-anchor="middle" class="m">languages.txt</text>',
]

# stacked overview bar, segments proportional within the top languages
shown = sum(l["pct"] for l in langs)
x, segs = PAD, []
for l, c in zip(langs, COLORS):
    w = bar * l["pct"] / shown
    segs.append(f'<rect x="{x:.1f}" y="50" width="{w:.1f}" height="10" fill="{c}"/>')
    x += w
out.append(f'<g clip-path="url(#sb)">{"".join(segs)}</g>')

# one row per language: dot, name, share of all code, bar scaled to the top language
top = langs[0]["pct"]
for i, (l, c) in enumerate(zip(langs, COLORS)):
    y, w = TOP + i * ROW, bar * l["pct"] / top
    start = 0.2 + i * 0.15  # hold at 0 via keyTimes; a delayed `begin` would flash full width first
    end, k = start + 1.2, start / (start + 1.2)
    out.append(
        f'<circle cx="{PAD + 5}" cy="{y - 4}" r="5" fill="{c}"/>'
        f'<text x="{PAD + 16}" y="{y}">{escape(l["name"])}</text>'
        f'<text x="{W - PAD}" y="{y}" text-anchor="end" class="m">{l["pct"]}%</text>'
        f'<rect x="{PAD}" y="{y + 9}" width="{bar}" height="6" rx="3" fill="#161b22"/>'
        f'<rect x="{PAD}" y="{y + 9}" width="{w:.1f}" height="6" rx="3" fill="{c}">'
        f'<animate attributeName="width" values="0;0;{w:.1f}" keyTimes="0;{k:.3f};1" dur="{end:.2f}s" fill="freeze"/></rect>'
    )

out.append(f'<text x="{PAD}" y="{H - 20}" class="m">{data["repos"]} repos · share of code by bytes</text>')
out.append("</svg>")
open("languages.svg", "w").write("\n".join(out))
print(f"wrote languages.svg ({len(langs)} languages)")

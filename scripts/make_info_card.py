"""Write info-card.svg, a neofetch-style panel. STATIC=1 emits a frozen frame for previews."""

import os
import re
import textwrap
from xml.sax.saxutils import escape

TITLE = "yosia@github"
ROWS = [
    ("Name", "Yosia Sipahutar"),
    ("Now", "CS Student"),
    ("Location", "DKI Jakarta, Indonesia"),
    ("Stack", "Python · JavaScript · TypeScript · PHP"),
    ("Focus", "Machine learning, AI, Data Science, Web Development"),
    ("Tools", "VS Code · Cursor · Claude Code · ChatGPT"),
    ("Motto", "Still Learning."),
    ("Contact", "github.com/YosiaCoKR"),
]
COLORS = ["#58a6ff", "#3fb950", "#d29922", "#f778ba", "#a5d6ff", "#ff7b72"]
STATIC = os.environ.get("STATIC") == "1"

W, LH, TOP = 490, 26, 70
# long values wrap onto continuation lines instead of running off the card
LINES = [(i, key if j == 0 else "", part)
         for i, (key, val) in enumerate(ROWS)
         for j, part in enumerate(textwrap.wrap(val, 40) or [""])]
H = TOP + LH * len(LINES) + 64
if os.path.exists("ascii.svg"):  # stretch to the portrait's rendered height (370px column)
    aw, ah = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open("ascii.svg").read()).groups())
    H = max(H, round(370 * ah / aw * W / 490))
anim = (
    ""
    if STATIC
    else """
.l{animation:in .4s ease-out both}
@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"""
)

out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f"<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px}}{anim}</style>",
    f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="#0d1117" stroke="#30363d"/>',
    '<circle cx="20" cy="20" r="6" fill="#ff5f56"/><circle cx="40" cy="20" r="6" fill="#ffbd2e"/>'
    '<circle cx="60" cy="20" r="6" fill="#27c93f"/>',
    f'<text x="20" y="56" fill="#3fb950" font-weight="bold">{TITLE}</text>',
    f'<line x1="20" y1="64" x2="{W - 20}" y2="64" stroke="#30363d"/>',
]
for n, (i, key, val) in enumerate(LINES):
    delay = "" if STATIC else f' style="animation-delay:{0.3 + n * 0.15:.2f}s"'
    out.append(
        f'<g class="l"{delay}><text x="20" y="{TOP + 20 + n * LH}">'
        f'<tspan fill="{COLORS[i % len(COLORS)]}" font-weight="bold">{escape(key + ":" if key else "")}</tspan>'
        f'<tspan x="130" fill="#c9d1d9">{escape(val)}</tspan></text></g>'
    )
delay = "" if STATIC else f' style="animation-delay:{0.3 + len(LINES) * 0.15:.2f}s"'
blocks = ["#484f58", "#ff7b72", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]
out.append(f'<g class="l"{delay}>' + "".join(
    f'<rect x="{20 + k * 26}" y="{H - 40}" width="22" height="16" rx="3" fill="{c}"/>' for k, c in enumerate(blocks)) + "</g>")
out.append("</svg>")
open("info-card.svg", "w").write("\n".join(out))
print("wrote info-card.svg")

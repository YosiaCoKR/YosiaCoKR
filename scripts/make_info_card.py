"""Write info-card.svg, a neofetch-style panel. STATIC=1 emits a frozen frame for previews."""
import os
from xml.sax.saxutils import escape

TITLE = "yosia@github"
ROWS = [  # TODO: isi pakai data kamu sendiri
    ("Name", "Yosia Sipahutar"),
    ("Now", "<role / tempat sekarang>"),
    ("Prev", "<pengalaman sebelumnya>"),
    ("Stack", "<Python, TypeScript, ...>"),
    ("Focus", "<lagi ngulik apa>"),
    ("Highlights", "<pencapaian 1>"),
    ("", "<pencapaian 2>"),
    ("Contact", "github.com/YosiaCoKR"),
]
COLORS = ["#58a6ff", "#3fb950", "#d29922", "#f778ba", "#a5d6ff", "#ff7b72"]
STATIC = os.environ.get("STATIC") == "1"

W, LH, TOP = 490, 26, 70
H = TOP + LH * len(ROWS) + 30
anim = "" if STATIC else """
.l{opacity:0;animation:in .4s ease-out forwards}
@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"""

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       f"<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px}}{anim}</style>",
       f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
       '<circle cx="20" cy="20" r="6" fill="#ff5f56"/><circle cx="40" cy="20" r="6" fill="#ffbd2e"/>'
       '<circle cx="60" cy="20" r="6" fill="#27c93f"/>',
       f'<text x="20" y="56" fill="#3fb950" font-weight="bold">{TITLE}</text>',
       f'<line x1="20" y1="64" x2="{W - 20}" y2="64" stroke="#30363d"/>']
for i, (key, val) in enumerate(ROWS):
    delay = "" if STATIC else f' style="animation-delay:{0.3 + i * 0.15:.2f}s"'
    out.append(f'<g class="l"{delay}><text x="20" y="{TOP + 20 + i * LH}">'
               f'<tspan fill="{COLORS[i % len(COLORS)]}" font-weight="bold">{escape(key + ":" if key else "")}</tspan>'
               f'<tspan x="130" fill="#c9d1d9">{escape(val)}</tspan></text></g>')
out.append("</svg>")
open("info-card.svg", "w").write("\n".join(out))
print("wrote info-card.svg")

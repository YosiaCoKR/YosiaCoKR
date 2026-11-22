"""data/contributions.json -> activity.svg, a monthly contributions curve that draws itself in."""

import json

from theme import GRAD, frame, sparkle

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
W, H = 860, 190
L, R, T, B = 50, 30, 52, 44  # chart padding: left, right, top, bottom

months = json.load(open("data/contributions.json"))["months"]
keys, vals = list(months), list(months.values())
peak = max(vals) or 1
cw, ch = W - L - R, H - T - B
pts = [(L + i * cw / (len(vals) - 1), T + ch - v / peak * ch) for i, v in enumerate(vals)]

# smooth curve through every point (Catmull-Rom -> cubic Bézier); control points
# are clamped to the baseline so a 0 next to a spike never dips below zero
base = T + ch
d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
for i in range(len(pts) - 1):
    (ax, ay), (bx, by), (cx, cy), (ex, ey) = (pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)])
    c1y, c2y = min(by + (cy - ay) / 6, base), min(cy - (ey - by) / 6, base)
    d += f"C{bx + (cx - ax) / 6:.1f} {c1y:.1f} {cx - (ex - bx) / 6:.1f} {c2y:.1f} {cx:.1f} {cy:.1f}"
area = f"{d}L{pts[-1][0]:.1f} {base}L{L} {base}Z"

fade = (
    f'<linearGradient id="ar" x1="0" y1="{T}" x2="0" y2="{T + ch}" gradientUnits="userSpaceOnUse">'
    f'<stop offset="0" stop-color="{GRAD[0]}" stop-opacity=".35"/>'
    f'<stop offset="1" stop-color="{GRAD[2]}" stop-opacity="0"/></linearGradient>'
)
out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    "<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11px;fill:#8b949e}"
    ".ln{stroke-dasharray:1;animation:draw 2.4s ease-out both}"
    ".ar{animation:fade 1s 1.6s ease-out both}"
    "@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
    "@keyframes fade{from{opacity:0}to{opacity:1}}</style>",
    frame(W, H, fade),
    f'<text x="{L}" y="28" style="fill:#c9d1d9">contributions per month</text>',
    sparkle(W - 40, 24, 7, 0),
]
for f in (0.5, 1):  # faint guide lines at half and full peak
    y = T + ch - f * ch
    out.append(
        f'<line x1="{L}" y1="{y:.1f}" x2="{W - R}" y2="{y:.1f}" stroke="#21262d" stroke-dasharray="3 4"/>'
        f'<text x="{L - 8}" y="{y + 4:.1f}" text-anchor="end">{round(f * peak)}</text>'
    )
out.append(f'<path class="ar" d="{area}" fill="url(#ar)"/>')
out.append(
    f'<path class="ln" d="{d}" pathLength="1" fill="none" stroke="url(#tx)" stroke-width="2.5" stroke-linecap="round"/>'
)
for (x, y), k, v in zip(pts, keys, vals):
    big = v == peak
    out.append(
        f'<circle class="ar" cx="{x:.1f}" cy="{y:.1f}" r="{4.5 if big else 2.5}" fill="{GRAD[0] if big else "#d2b8ff"}">'
        f"<title>{v} in {k}</title></circle>"
        f'<text x="{x:.1f}" y="{H - 20}" text-anchor="middle">{MONTHS[int(k[5:]) - 1]}</text>'
    )
    if big:
        out.append(f'<text class="ar" x="{x:.1f}" y="{y - 10:.1f}" text-anchor="middle" style="fill:{GRAD[0]}">{v}</text>')
out.append("</svg>")
open("activity.svg", "w").write("\n".join(out))
print(f"wrote activity.svg ({len(vals)} months, peak {peak})")

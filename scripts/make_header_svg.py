"""Write header.svg: intro lines that type themselves out, then a blinking cursor."""
from xml.sax.saxutils import escape

LINES = [  # (text, font size, color)
    ("Hi, I'm Yosia Sipahutar", 30, "#3fb950"),
    ("Student @ Tarumanagara University · Jakarta", 16, "#c9d1d9"),
    ("Machine learning · forecasting · dev tooling", 16, "#8b949e"),
]
W, CPS = 860, 28  # width, typed characters per second

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 130" width="{W}" height="130">',
       f'<rect width="{W}" height="130" rx="8" fill="#0d1117"/>',
       '<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" text-anchor="start">']
t, y = 0.3, 0
for i, (text, size, color) in enumerate(LINES):
    y += size + 14
    wide, dur = len(text) * size * 0.6, len(text) / CPS
    x, end, k = (W - wide) / 2, t + dur, t / (t + dur)
    # base value = full width, so viewers without SMIL still show the text
    out.append(
        f'<clipPath id="h{i}"><rect x="{x:.1f}" y="{y - size}" height="{size * 1.4}" width="{wide:.1f}">'
        f'<animate attributeName="width" values="0;0;{wide:.1f}" keyTimes="0;{k:.3f};1" dur="{end:.2f}s" fill="freeze"/>'
        f'</rect></clipPath>'
        f'<text x="{x:.1f}" y="{y}" font-size="{size}" fill="{color}" textLength="{wide:.1f}" '
        f'clip-path="url(#h{i})">{escape(text)}</text>')
    t = end + 0.25
# blinking cursor after the last line
out.append(f'<rect x="{x + wide + 4:.1f}" y="{y - size + 2}" width="{size * 0.6:.1f}" height="{size}" fill="#3fb950">'
           f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
out.append("</g></svg>")
open("header.svg", "w").write("\n".join(out))
print("wrote header.svg")

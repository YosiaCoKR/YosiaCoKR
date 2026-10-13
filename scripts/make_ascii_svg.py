"""source-prepped.png -> ascii.svg, a monochrome portrait that types itself in row by row."""
from xml.sax.saxutils import escape

from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense); leading space clears the bg
COLS = 100
FONT, CW, LH = 7, 4.2, 8  # font size, char width, line height
ROW_DUR, ROW_GAP = 0.35, 0.06  # seconds per row wipe, stagger between rows
BAR = 34  # title bar height

img = Image.open("source-prepped.png").convert("L")
rows = round(COLS * img.height / img.width * CW / LH)
img = img.resize((COLS, rows))
# stretch the subject's tones over the full ramp; the white background stays blank
subj = sorted(v for v in img.tobytes() if v < 250) or [0, 249]
lo, hi = subj[len(subj) // 50], subj[-len(subj) // 50 - 1]
img = img.point(lambda v: 255 if v >= 250 else max(0, min(249, (v - lo) * 249 // max(1, hi - lo))))
px = img.load()

lines = []
for y in range(rows):
    line = "".join(RAMP[(255 - px[x, y]) * (len(RAMP) - 1) // 255] for x in range(COLS))
    lines.append(line.rstrip())

W, H = COLS * CW + 20, rows * LH + 20 + BAR
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H}" width="{W:.0f}" height="{H}">',
       f'<rect x=".5" y=".5" width="{W - 1:.0f}" height="{H - 1}" rx="8" fill="#0d1117" stroke="#30363d"/>',
       '<circle cx="20" cy="18" r="6" fill="#ff5f56"/><circle cx="40" cy="18" r="6" fill="#ffbd2e"/>'
       '<circle cx="60" cy="18" r="6" fill="#27c93f"/>',
       f'<text x="{W / 2:.0f}" y="22" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
       f'font-size="12" fill="#8b949e">portrait.txt</text>',
       f'<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="{FONT}" fill="#c9d1d9" xml:space="preserve">']
for y, line in enumerate(lines):
    if not line:
        continue
    begin, ty, wide = y * ROW_GAP, 10 + BAR + y * LH, len(line) * CW
    end, k = begin + ROW_DUR, begin / (begin + ROW_DUR)
    out.append(
        f'<clipPath id="r{y}"><rect x="10" y="{ty}" height="{LH}" width="{wide}">'
        f'<animate attributeName="width" values="0;0;{wide}" keyTimes="0;{k:.3f};1" dur="{end:.2f}s" fill="freeze"/></rect></clipPath>'
        f'<text x="10" y="{ty + FONT}" textLength="{wide:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#r{y})">{escape(line)}</text>'
        f'<rect y="{ty}" width="{CW}" height="{LH}" fill="#c9d1d9" opacity="0">'
        f'<animate attributeName="x" from="10" to="{10 + wide}" begin="{begin:.2f}s" dur="{ROW_DUR}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="1" begin="{begin:.2f}s" dur="{ROW_DUR}s"/></rect>'
    )
out.append("</g></svg>")
open("ascii.svg", "w").write("\n".join(out))
print(f"wrote ascii.svg ({COLS}x{rows})")

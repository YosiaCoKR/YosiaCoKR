"""Write fortune.svg: an ASCII cat with a speech bubble holding today's quote (rotates daily in CI)."""

import datetime
import textwrap
from xml.sax.saxutils import escape

from theme import GRAD, PASTEL, frame, gradient

QUOTES = [
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("All models are wrong, but some are useful.", "George E. P. Box"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    (
        "Programs must be written for people to read, and only incidentally for machines to execute.",
        "Harold Abelson",
    ),
    (
        "Any fool can write code that a computer can understand. "
        "Good programmers write code that humans can understand.",
        "Martin Fowler",
    ),
    ("Simple things should be simple, complex things should be possible.", "Alan Kay"),
]
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
W, LH, CAT_W = 860, 24, 150  # width, quote line height, space reserved for the cat

text, who = QUOTES[datetime.date.today().toordinal() % len(QUOTES)]
lines = textwrap.wrap(text, 62)
bx, by, bw = CAT_W + 20, 24, W - CAT_W - 44  # speech bubble box
bh = 34 + LH * len(lines) + 26
H = by + bh + 34

out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f"<style>text{{font-family:{FONT}}}"
    ".q{animation:in .6s ease-out both}"
    "@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}</style>",
    frame(W, H, gradient("ct", 0, 1, colors=PASTEL)),
    # bubble with a little tail pointing at the cat
    f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="#161b22" stroke="url(#tx)" stroke-width="1.2"/>',
    f'<path d="M{bx} {by + bh - 30} L{bx - 18} {by + bh - 14} L{bx} {by + bh - 16}Z" fill="#161b22"/>'
    f'<path d="M{bx} {by + bh - 30} L{bx - 18} {by + bh - 14} L{bx} {by + bh - 16}" fill="none" stroke="{GRAD[0]}" stroke-width="1.2"/>',
]
for i, line in enumerate(lines):
    out.append(
        f'<text class="q" style="animation-delay:{0.2 + i * 0.25:.2f}s" x="{bx + 24}" y="{by + 34 + i * LH}" '
        f'font-size="15" fill="#e6edf3">{"“" if i == 0 else ""}{escape(line)}{"”" if i == len(lines) - 1 else ""}</text>'
    )
out.append(
    f'<text class="q" style="animation-delay:{0.2 + len(lines) * 0.25:.2f}s" x="{bx + bw - 24}" '
    f'y="{by + bh - 16}" text-anchor="end" font-size="13" fill="{GRAD[0]}">— {escape(who)}</text>'
)

# the cat: eyes open most of the time, a quick blink every 4s
cx, cy = 34, by + bh - 26
cat = '<text x="{x}" y="{y}" font-size="17" fill="url(#ct)" xml:space="preserve">{t}{a}</text>'
blink = '<animate attributeName="opacity" values="{v}" keyTimes="0;.9;.95;1" dur="4s" repeatCount="indefinite"/>'
out += [
    cat.format(x=cx, y=cy, t=" /\\_/\\", a=""),
    cat.format(x=cx, y=cy + 22, t="( o.o )", a=blink.format(v="1;1;0;1")),
    # closed eyes hidden by default, so viewers without SMIL see one open face
    cat.format(x=cx, y=cy + 22, t="( -.- )", a=blink.format(v="0;0;1;0")).replace("<text ", '<text opacity="0" ', 1),
    cat.format(x=cx, y=cy + 44, t=" &gt; ^ &lt;", a=""),
    "</svg>",
]
open("fortune.svg", "w").write("\n".join(out))
print(f"wrote fortune.svg ({who})")

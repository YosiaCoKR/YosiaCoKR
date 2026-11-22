"""Shared card look: dark panel, pink -> purple -> blue gradient border and text accents."""

GRAD = ("#f778ba", "#bc8cff", "#58a6ff")
PASTEL = ("#ffb3d9", "#d2b8ff", "#a5d6ff")  # lighter, for large text areas


def gradient(gid, x2=1, y2=1, user=False, colors=GRAD):
    """Linear gradient from (0,0) to (x2,y2): bbox fractions, or pixels when user=True."""
    units = ' gradientUnits="userSpaceOnUse"' if user else ""
    stops = "".join(f'<stop offset="{i / 2}" stop-color="{c}"/>' for i, c in enumerate(colors))
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"{units}>{stops}</linearGradient>'


def frame(w, h, extra_defs=""):
    """Card background; also defines #tx, a left-to-right gradient for text fills."""
    return (
        f'<defs>{gradient("bd")}{gradient("tx", 1, 0)}{extra_defs}</defs>'
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="#0d1117" '
        f'stroke="url(#bd)" stroke-width="1.5"/>'
    )


def sparkle(cx, cy, s, delay):
    """Four-point twinkling star (a path, so no font glyph needed)."""
    return (
        f'<path transform="translate({cx} {cy})" fill="#f778ba" '
        f'd="M0 {-s}Q0 0 {s} 0Q0 0 0 {s}Q0 0 {-s} 0Q0 0 0 {-s}Z">'
        f'<animate attributeName="opacity" values=".15;1;.15" dur="2.4s" begin="{delay}s" '
        f'repeatCount="indefinite"/></path>'
    )

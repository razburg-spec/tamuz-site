# Cover order (Raz, 2026-11-27, same rule as razburg.com): his featured artists first, in his order,
# then everything else, and never two covers by the same artist next to each other
# (side by side, or above/below in the 7- and 4-column grids, or across the marquee's wrap).
import re

FEATURED_TITLES = ["Hour After Hour", "Out In The Dark", "Backwash", "Life Factory", "Love Happening", "Cracks",
    "The Opposite Way Around", "A Life Invisible", "Hard Sense Of War", "Modern Phase", "Borderlines", "In Bloom",
    "Home", "All In", "Voca Dance", "Uptown Funk (Vocal Cover)", "Like The Tide", "Rockets On The Balcony",
    "Remedies", "Lost In Time", "Cloud Nine", "Where Are You Going", "Any Human Heart", "Independent", "Drug",
    "27/04", "Cities", "The Magister", "Friday", "The Kid Collection Vol. 4 & 5", "Sinking Ship"]
OWN = "רז בורג"
GRID_COLS = (7, 4)

def people(artist):
    """'שרלוט ומגון' -> {שרלוט, מגון}; 'נועם רותם ואיתמר רוטשילד' -> {נועם רותם, איתמר רוטשילד}."""
    parts = re.split(r",\s*|\s+ו(?=\S)|\s*&\s*", artist)
    return {p.strip().lower() for p in parts if p.strip()}

def arrange(items, cols=GRID_COLS):
    """items: (path, artist, title). Featured first in Raz's order; then Raz's own releases interleaved
    with the rest; greedy placement so the same artist never touches."""
    feat = sorted([c for c in items if c[2] in FEATURED_TITLES], key=lambda c: FEATURED_TITLES.index(c[2]))
    own = [c for c in items if c not in feat and c[1].startswith(OWN)]
    other = [c for c in items if c not in feat and c not in own]
    mixed, oi, ri = [], 0, 0
    while oi < len(other) or ri < len(own):   # spread own releases evenly among the others
        if ri >= len(own) or (oi < len(other) and oi * len(own) <= ri * len(other)):
            mixed.append(other[oi]); oi += 1
        else:
            mixed.append(own[ri]); ri += 1
    prio = feat + mixed
    out, left = [], list(range(len(prio)))
    g = [people(c[1]) for c in prio]
    def clash(i, pos):
        near = ([pos - 1] if pos else []) + [pos - k for k in cols if pos - k >= 0]
        return sum(1 for p in near if g[out[p]] & g[i])
    while left:
        pos = len(out)
        window = left[:12] if cols else left[:3]
        best = min(window, key=lambda i: (clash(i, pos), window.index(i)))
        left.remove(best)
        out.append(best)
    return [prio[i] for i in out]

def conflicts(items):
    g = [people(c[1]) for c in items]
    n = len(items)
    bad = [i for i in range(1, n) if g[i] & g[i - 1]]
    bad += [i for k in GRID_COLS for i in range(k, n) if g[i] & g[i - k]]
    return len(bad)

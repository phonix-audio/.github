#!/usr/bin/env python3
"""Draw the Phonix Audio mark: a Lissajous figure at the ratio 1:2.

A Lissajous plots one frequency against another, so the ratio names a musical
interval; 1:2 is the octave, and it closes into a single crossing loop. The
mark is therefore an audio object rather than a picture of one, and the same
generator gives every repository in the catalogue its own figure by changing
one pair of integers.

The band's width is the inverse of the beam's speed. On a scope the trace
lingers where the curve turns, so it reads brightest and heaviest there; here
the width follows the same law, which is what gives the loop its calligraphic
swell without a single width being placed by hand.

Two things the geometry demands, both found the hard way:

- The figure is closed, so the band is an annulus: two loops wound against
  each other under the non-zero rule. Walking out along one edge and back
  along the other leaves a blunt tab at the seam, and the even-odd rule
  cancels any figure that crosses itself more than twice.
- Phase matters. At zero, ratios such as 1:3 retrace themselves instead of
  closing; a quarter turn on x opens them.

One source, two outputs. Cairo writes the SVG and the PNG from the same calls,
so the vector and the raster cannot disagree.
"""
import cairo, math, re, sys

S = 512.0                      # design space; both outputs scale from it
CX = CY = S / 2
TAU = math.tau

RATIO = (1, 2)                 # the octave; a repository may take its own
PHASE = 0.0                    # a quarter turn opens the degenerate ratios
AMP = 0.330                    # of the design space, corner to corner
WIDTH = 0.030                  # the band at its widest, where the beam turns

INK = (0.055, 0.058, 0.086)
STOPS = ((0.42, 0.24, 0.82), (0.26, 0.36, 0.88),
         (0.24, 0.78, 0.92), (0.46, 0.94, 0.86))


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def ramp(t):
    t = max(0.0, min(1.0, t)) * (len(STOPS) - 1)
    i = min(int(t), len(STOPS) - 2)
    return lerp(STOPS[i], STOPS[i + 1], t - i)


def curve(n=900):
    """The figure, sampled at equal time. Equal time is the point: it is what
    makes the samples crowd where the beam is slow."""
    a, b = RATIO
    return [(0.5 + AMP * math.sin(TAU * a * k / n + PHASE),
             0.5 + AMP * math.sin(TAU * b * k / n))
            for k in range(n)]


def band(pts):
    """The two edges of the ribbon, thick where the beam lingers."""
    n = len(pts)
    speed = []
    for k in range(n):
        x0, y0 = pts[(k - 1) % n]
        x1, y1 = pts[(k + 1) % n]
        speed.append(math.hypot(x1 - x0, y1 - y0))
    fastest = max(speed)

    left, right = [], []
    for k, (x, y) in enumerate(pts):
        x0, y0 = pts[(k - 1) % n]
        x1, y1 = pts[(k + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        m = math.hypot(dx, dy) or 1e-9
        w = WIDTH * (0.34 + 1.5 * (1.0 - speed[k] / fastest) ** 1.4)
        left.append((x - dy / m * w, y + dx / m * w))
        right.append((x + dy / m * w, y - dx / m * w))
    return left, right


def draw(cr):
    # Nothing outside the disc: the mark is the circle, so it sits on any page
    # and survives the round crop an avatar is put through.
    cr.arc(CX, CY, S * 0.480, 0, TAU)
    cr.set_source_rgb(*INK)
    cr.fill()

    left, right = band(curve())
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    for loop in (left, right[::-1]):
        cr.move_to(S * loop[0][0], S * loop[0][1])
        for x, y in loop[1:]:
            cr.line_to(S * x, S * y)
        cr.close_path()

    g = cairo.LinearGradient(S * 0.17, S * 0.83, S * 0.83, S * 0.17)
    for k in range(len(STOPS)):
        g.add_color_stop_rgb(k / (len(STOPS) - 1), *ramp(k / (len(STOPS) - 1)))
    cr.set_source(g)
    cr.fill()


def render(target, px=None):
    """Write one output. A raster takes its size from the name, logo-512.png."""
    if target.endswith(".svg"):
        surf = cairo.SVGSurface(target, S, S)
        cr = cairo.Context(surf)
    else:
        px = px or int(re.search(r"(\d+)", target).group(1))
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, px, px)
        cr = cairo.Context(surf)
        cr.scale(px / S, px / S)
    cr.set_antialias(cairo.ANTIALIAS_BEST)
    draw(cr)
    if not target.endswith(".svg"):
        surf.write_to_png(target)
    surf.finish()


for p in sys.argv[1:]:
    render(p)
    print("wrote", p)

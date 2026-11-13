"""Render the rotating "Now shipping" chip as an animated GIF (drawn at 2x)."""
from PIL import Image, ImageDraw, ImageFont
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site', 'img', 'now-shipping.gif')

K = 2                      # render scale (retina)
H = 28 * K                 # chip height
PAD_L, PAD_R = 6 * K, 12 * K
ICON = 18 * K
GAP = 8 * K
RADIUS = 6 * K
BG = (244, 241, 234)       # warm paper, the "bookplate"
INK = (26, 26, 26)
MUTED = (104, 100, 94)

NAME_FONT = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 13 * K)
DESC_FONT = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 13 * K)

PRODUCTS = [
    ('remi_icon_72.png', 'Remi for Mac', 'a little bird that remembers for you'),
    ('pr_icon_288.png', 'PR Tracker', 'gym progress and personal records'),
    ('solace_icon_72.png', 'Solace', 'private therapy with verified psychologists'),
]

HOLD_MS = 2600
STEPS = 4                  # frames per half-transition
STEP_MS = 55
SHIFT = 7 * K              # vertical travel during transition


def text_w(font, s):
    return font.getbbox(s)[2]


def content(icon_file, name, desc):
    icon = Image.open(os.path.join(HERE, icon_file)).convert('RGBA').resize((ICON, ICON), Image.LANCZOS)
    nw, dw = text_w(NAME_FONT, name), text_w(DESC_FONT, desc)
    w = ICON + GAP + nw + GAP + dw
    layer = Image.new('RGBA', (w, H), (0, 0, 0, 0))
    layer.alpha_composite(icon, (0, (H - ICON) // 2))
    d = ImageDraw.Draw(layer)
    # vertically centre on cap height
    asc = NAME_FONT.getmetrics()[0]
    cap = NAME_FONT.getbbox('H')
    y = (H - (cap[3] - cap[1])) // 2 - cap[1]
    d.text((ICON + GAP, y), name, font=NAME_FONT, fill=INK)
    d.text((ICON + GAP + nw + GAP, y), desc, font=DESC_FONT, fill=MUTED)
    return layer


layers = [content(*p) for p in PRODUCTS]
W = PAD_L + max(l.width for l in layers) + PAD_R
W += W % 2  # even, so the 1x size is exact


def chip():
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(base).rounded_rectangle([0, 0, W - 1, H - 1], RADIUS, fill=BG + (255,))
    return base


def place(layer, dy, alpha):
    frame = chip()
    mask = frame.getchannel('A')
    lay = layer.copy()
    if alpha < 1:
        a = lay.getchannel('A').point(lambda v: int(v * alpha))
        lay.putalpha(a)
    tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tmp.alpha_composite(lay, (PAD_L, int(round(dy))))
    # clip to the chip
    clipped = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    clipped.paste(tmp, (0, 0), mask)
    frame.alpha_composite(clipped)
    return frame


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)


frames, durations = [], []
n = len(layers)
for i, layer in enumerate(layers):
    frames.append(place(layer, 0, 1)); durations.append(HOLD_MS)
    nxt = layers[(i + 1) % n]
    for s in range(1, STEPS + 1):          # current slides up and out
        t = ease(s / STEPS)
        frames.append(place(layer, -SHIFT * t, 1 - t)); durations.append(STEP_MS)
    for s in range(1, STEPS):              # next slides up and in
        t = ease(s / STEPS)
        frames.append(place(nxt, SHIFT * (1 - t), t)); durations.append(STEP_MS)


def to_p(frame):
    rgb = Image.new('RGB', frame.size, (255, 255, 255))
    rgb.paste(frame, mask=frame.getchannel('A'))
    p = rgb.quantize(colors=255, method=Image.MEDIANCUT, dither=Image.NONE)
    pal = p.getpalette()[:255 * 3] + [255, 255, 255]
    p.putpalette(pal)
    transparent = frame.getchannel('A').point(lambda v: 255 if v < 128 else 0)
    p.paste(255, mask=transparent)
    p.info['transparency'] = 255
    return p


def build(scale_div, path):
    fs = []
    for f in frames:
        if scale_div != 1:
            f = f.resize((f.width // scale_div, f.height // scale_div), Image.LANCZOS)
        fs.append(to_p(f))
    fs[0].save(path, save_all=True, append_images=fs[1:], duration=durations, loop=0,
               transparency=255, disposal=2, optimize=True)
    return os.path.getsize(path), fs[0].size


size, dims = build(1, OUT)
print('gif', OUT, dims, f'{size/1024:.0f}KB', 'display', (dims[0] // K, dims[1] // K), 'frames', len(frames),
      'loop ms', sum(durations))
# first frame as a still, for previews and the products page
frames[0].save(os.path.join(os.path.dirname(OUT), 'now-shipping-frame1.png'))

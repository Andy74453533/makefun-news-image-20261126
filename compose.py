#!/usr/bin/env python3
"""Compose the news-image-20261126 front page (1024x1024) with PIL.
Masthead + lead photo (Cairo tanker fire) + 3 story columns (tariffs, Kuwait drone, Macy's parade).
All text is drawn by PIL from DejaVu fonts, so no garbled text."""
from PIL import Image, ImageDraw, ImageFont

IMG = '/home/hatch/workspace/imagine_media/'
OUT = '/home/hatch/workspace/makefun/news-image-20261126/entry.png'
W, H = 1024, 1024
BG = (247, 243, 232)
INK = (20, 20, 20)
RED = (178, 0, 0)
GRAY = (105, 100, 90)


def font(name, size):
    return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/{name}', size)


F_TITLE = font('DejaVuSerif-Bold.ttf', 62)
F_DATE = font('DejaVuSans-Bold.ttf', 22)
F_HEAD = font('DejaVuSerif-Bold.ttf', 50)
F_STAND = font('DejaVuSerif.ttf', 21)
F_CAP = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf', 17)
F_KICK = font('DejaVuSans-Bold.ttf', 15)
F_COLHEAD = font('DejaVuSerif-Bold.ttf', 23)
F_COLSUM = font('DejaVuSerif.ttf', 17)
F_FOOT = font('DejaVuSans.ttf', 13)


def crop_to(im, tw, th, y_bias=0.5):
    sw, sh = im.size
    target = tw / th
    if sw / sh > target:
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, sh))
    else:
        nh = int(sw / target)
        y0 = int((sh - nh) * y_bias)
        im = im.crop((0, y0, sw, y0 + nh))
    return im.resize((tw, th), Image.LANCZOS)


def wrap(draw, text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


page = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(page)

# ---- masthead ----
d.text(((W - d.textlength('THE WORLD TODAY', font=F_TITLE)) / 2, 12),
       'THE WORLD TODAY', font=F_TITLE, fill=INK)
d.text(((W - d.textlength('THURSDAY, 26 NOVEMBER 2026', font=F_DATE)) / 2, 88),
       'THURSDAY, 26 NOVEMBER 2026', font=F_DATE, fill=INK)
d.line([(24, 122), (1000, 122)], fill=INK, width=3)
d.line([(24, 128), (1000, 128)], fill=INK, width=1)

# ---- lead photo ----
lead = crop_to(Image.open(IMG + 'media-generation-news-26nov-cairo-fire-0-bd90a331-1f0e-480b-9590-2cc56ea194e8.webp').convert('RGB'),
               976, 370, y_bias=0.45)
page.paste(lead, (24, 138))
d.text((24, 514),
       "A fuel tanker burns on Cairo's Ring Road in Giza. The crash killed 31 people and injured 21; 27 vehicles were destroyed.",
       font=F_CAP, fill=GRAY)

# ---- lead headline (two lines, shrink until it fits) ----
head_lines = ['31 KILLED AS FUEL TANKER', 'EXPLODES ON CAIRO RING ROAD']
size = 50
while size > 30:
    f = font('DejaVuSerif-Bold.ttf', size)
    if max(d.textlength(t, font=f) for t in head_lines) <= 976:
        break
    size -= 2
F_HEAD = f
y = 542
for t in head_lines:
    d.text((24, y), t, font=F_HEAD, fill=INK)
    y += size + 8

# ---- standfirst ----
stand = ('A car struck the tanker at speed and it overturned, setting off a blaze that engulfed '
         'the highway in the Warraq district. Egypt mourns its deadliest road disaster in years.')
for i, line in enumerate(wrap(d, stand, F_STAND, 976)):
    d.text((24, 648 + i * 27), line, font=F_STAND, fill=INK)
d.line([(24, 712), (1000, 712)], fill=INK, width=2)

# ---- three story columns ----
cols = [
    ('TRADE  •  WASHINGTON',
     IMG + 'media-generation-news-26nov-tariffs-port-0-5752892c-f647-49bf-8631-d1e1248f7061.webp',
     'U.S. HITS 14 NATIONS WITH NEW TARIFFS',
     'China faces up to 20% — or 40% if the trade truce collapses.'),
    ('GULF  •  KUWAIT CITY',
     IMG + 'media-generation-news-26nov-kuwait-drone-0-4ae66193-b83f-4d3e-bc06-dbcbedcf7a06.webp',
     'DRONE ATTACK KILLS TWO IN KUWAIT',
     'Italy blames Iran for the strike; Tehran denies any role.'),
    ('NEW YORK  •  THANKSGIVING',
     IMG + 'media-generation-news-26nov-macys-parade-0-a9407138-8de4-469c-a9e4-d2827ac23104.webp',
     "STORM POSTPONES MACY'S PARADE",
     'Thanksgiving parade delayed for the first time in 100 years.'),
]
bias = [0.5, 0.15, 0.0]
for i, (kick, path, head, summ) in enumerate(cols):
    x = 24 + i * (312 + 20)
    thumb = crop_to(Image.open(path).convert('RGB'), 312, 168, y_bias=bias[i])
    page.paste(thumb, (x, 726))
    d.text((x, 902), kick, font=F_KICK, fill=RED)
    y = 926
    for line in wrap(d, head, F_COLHEAD, 312):
        d.text((x, y), line, font=F_COLHEAD, fill=INK)
        y += 29
    for line in wrap(d, summ, F_COLSUM, 312):
        d.text((x, y), line, font=F_COLSUM, fill=INK)
        y += 22

# (no footer — the columns run to the foot of the page)

page.save(OUT, 'PNG', optimize=True)
import os
n = os.path.getsize(OUT)
print('PNG bytes:', n)
if n > 1048576:
    page.save(OUT, 'JPEG', quality=90)
    print('saved as JPEG bytes:', os.path.getsize(OUT))
print('size:', page.size)

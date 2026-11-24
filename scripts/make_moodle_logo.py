from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('/home/iful/.hermes/cache/scratch/moodle-logo')
OUT.mkdir(parents=True, exist_ok=True)
S = 4
IPA = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
DEJA = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def gradient(size, c1, c2):
    img = Image.new('RGBA', size)
    d = ImageDraw.Draw(img)
    h = size[1]
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)
        d.line([(0, y), (size[0], y)], fill=color)
    return img


def make_icon(px):
    p = px * S
    grad = gradient((p, p), (18, 105, 178), (12, 166, 160))
    mask = Image.new('L', (p, p), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, p - 1, p - 1], radius=int(p * 0.22), fill=255)
    icon = Image.new('RGBA', (p, p), (0, 0, 0, 0))
    icon.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(icon)

    font = ImageFont.truetype(IPA, int(p * 0.54))
    bbox = d.textbbox((0, 0), 'あ', font=font)
    x = (p - (bbox[2] - bbox[0])) / 2 - bbox[0]
    y = (p - (bbox[3] - bbox[1])) / 2 - bbox[1] + p * 0.02
    d.text((x, y), 'あ', font=font, fill=(255, 255, 255, 255))

    r = int(p * 0.085)
    cx, cy = int(p * 0.80), int(p * 0.78)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(231, 76, 60, 255))
    return icon.resize((px, px), Image.LANCZOS)


icon512 = make_icon(512)
icon512.save(OUT / 'moodle-logo-compact.png')
icon512.resize((64, 64), Image.LANCZOS).save(OUT / 'favicon.png')
icon512.resize((180, 180), Image.LANCZOS).save(OUT / 'icon-180.png')

# Full header logo — 3 baris, lebih ramah navbar
W, H = 900, 180
pW, pH = W * S, H * S
full = Image.new('RGBA', (pW, pH), (0, 0, 0, 0))
icon = make_icon(150)
full.paste(icon, (15 * S, 15 * S), icon)

d = ImageDraw.Draw(full)
x = 190 * S
f_small = ImageFont.truetype(DEJA, 28 * S)
f_big = ImageFont.truetype(DEJA, 54 * S)
f_tag = ImageFont.truetype(DEJA, 19 * S)

d.text((x, 34 * S), 'E-LEARNING', font=f_small, fill=(12, 166, 160, 255))
d.text((x, 68 * S), 'Anaksepaku', font=f_big, fill=(23, 42, 69, 255))
d.text((x, 132 * S), 'Bahasa Jepang · Bulan Pertama', font=f_tag, fill=(92, 105, 120, 255))

full.resize((W, H), Image.LANCZOS).save(OUT / 'moodle-logo.png')
print('written:', ', '.join(p.name for p in sorted(OUT.glob('*.png'))))

# SVG source for future edits
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="180" viewBox="0 0 900 180">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1269b2"/>
      <stop offset="1" stop-color="#0ca6a0"/>
    </linearGradient>
  </defs>
  <g transform="translate(15,15)">
    <rect width="150" height="150" rx="33" fill="url(#g)"/>
    <text x="75" y="99" text-anchor="middle" font-family="'Noto Sans JP','IPA Gothic',sans-serif" font-size="81" fill="#fff">あ</text>
    <circle cx="120" cy="117" r="13" fill="#e74c3c"/>
  </g>
  <text x="190" y="60" font-family="DejaVu Sans,Arial,sans-serif" font-size="28" font-weight="bold" fill="#0ca6a0">E-LEARNING</text>
  <text x="190" y="115" font-family="DejaVu Sans,Arial,sans-serif" font-size="54" font-weight="bold" fill="#172a45">Anaksepaku</text>
  <text x="190" y="151" font-family="DejaVu Sans,Arial,sans-serif" font-size="19" fill="#5c6978">Bahasa Jepang · Bulan Pertama</text>
</svg>
'''
(OUT / 'moodle-logo.svg').write_text(svg, encoding='utf-8')

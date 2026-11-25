from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('/home/iful/.hermes/cache/scratch/moodle-logo')
OUT.mkdir(parents=True, exist_ok=True)
S = 4
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
    grad = gradient((p, p), (18, 105, 178), (14, 130, 190))
    mask = Image.new('L', (p, p), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, p - 1, p - 1], radius=int(p * 0.22), fill=255)
    icon = Image.new('RGBA', (p, p), (0, 0, 0, 0))
    icon.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(icon)

    # Komunitas: tiga titik manusia yang terhubung
    nodes = [(0.36, 0.27), (0.50, 0.20), (0.64, 0.27)]
    r = int(p * 0.055)
    pts = [(int(x * p), int(y * p)) for x, y in nodes]
    d.line([pts[0], pts[1], pts[2]], fill=(255, 255, 255, 210), width=max(2, int(p * 0.018)))
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 255))

    # Buku terbuka = pembelajaran umum
    left = [(int(p * 0.18), int(p * 0.42)), (int(p * 0.48), int(p * 0.47)),
            (int(p * 0.48), int(p * 0.80)), (int(p * 0.18), int(p * 0.72))]
    right = [(int(p * 0.52), int(p * 0.47)), (int(p * 0.82), int(p * 0.42)),
             (int(p * 0.82), int(p * 0.72)), (int(p * 0.52), int(p * 0.80))]
    d.polygon(left, fill=(255, 255, 255, 255))
    d.polygon(right, fill=(255, 255, 255, 255))
    d.line([(int(p * 0.50), int(p * 0.47)), (int(p * 0.50), int(p * 0.80))],
           fill=(18, 105, 178, 255), width=max(2, int(p * 0.014)))
    return icon.resize((px, px), Image.LANCZOS)


icon512 = make_icon(512)
icon512.save(OUT / 'moodle-logo-compact.png')
icon512.resize((64, 64), Image.LANCZOS).save(OUT / 'favicon.png')
icon512.resize((180, 180), Image.LANCZOS).save(OUT / 'icon-180.png')

# Full header logo
W, H = 1000, 180
pW, pH = W * S, H * S
full = Image.new('RGBA', (pW, pH), (0, 0, 0, 0))
icon = make_icon(150)
full.paste(icon, (15 * S, 15 * S), icon)

d = ImageDraw.Draw(full)
x = 190 * S
f_small = ImageFont.truetype(DEJA, 28 * S)
f_big = ImageFont.truetype(DEJA, 46 * S)
f_tag = ImageFont.truetype(DEJA, 18 * S)

d.text((x, 30 * S), 'E-LEARNING', font=f_small, fill=(14, 130, 190, 255))
d.text((x, 66 * S), 'Komunitas Anak Sepaku', font=f_big, fill=(23, 42, 69, 255))
d.text((x, 130 * S), 'Belajar bareng · Materi swadaya komunitas', font=f_tag, fill=(92, 105, 120, 255))

full.resize((W, H), Image.LANCZOS).save(OUT / 'moodle-logo.png')
print('written:', ', '.join(p.name for p in sorted(OUT.glob('*.png'))))

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="180" viewBox="0 0 1000 180">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1269b2"/>
      <stop offset="1" stop-color="#0e82be"/>
    </linearGradient>
  </defs>
  <g transform="translate(15,15)">
    <rect width="150" height="150" rx="33" fill="url(#g)"/>
    <path d="M27 63 L72 70 L72 120 L27 108 Z" fill="#fff"/>
    <path d="M78 70 L123 63 L123 108 L78 120 Z" fill="#fff"/>
    <line x1="75" y1="70" x2="75" y2="120" stroke="#1269b2" stroke-width="3"/>
    <g fill="#fff">
      <circle cx="54" cy="41" r="8"/><circle cx="75" cy="30" r="8"/><circle cx="96" cy="41" r="8"/>
    </g>
    <path d="M54 41 L75 30 L96 41" stroke="#fff" stroke-width="3" fill="none" opacity="0.85"/>
  </g>
  <text x="190" y="58" font-family="DejaVu Sans,Arial,sans-serif" font-size="28" font-weight="bold" fill="#0e82be">E-LEARNING</text>
  <text x="190" y="112" font-family="DejaVu Sans,Arial,sans-serif" font-size="46" font-weight="bold" fill="#172a45">Komunitas Anak Sepaku</text>
  <text x="190" y="151" font-family="DejaVu Sans,Arial,sans-serif" font-size="18" fill="#5c6978">Belajar bareng · Materi swadaya komunitas</text>
</svg>
'''
(OUT / 'moodle-logo.svg').write_text(svg, encoding='utf-8')

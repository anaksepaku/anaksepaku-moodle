from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('/home/iful/.hermes/cache/scratch/moodle-slides')
OUT.mkdir(parents=True, exist_ok=True)
ICON = Path('/home/iful/.hermes/cache/scratch/moodle-logo/moodle-logo-compact.png')
DEJA = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
W, H = 1400, 418
S = 2


def gradient(size, c1, c2):
    img = Image.new('RGBA', size)
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / max(size[1] - 1, 1)
        color = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)
        d.line([(0, y), (size[0], y)], fill=color)
    return img


slides = [
    ('BELAJAR BARENG', 'Ilmu dibagikan, bukan ditimbun.', 'Materi umum dan swadaya dari komunitas Anak Sepaku.'),
    ('SWADAYA KOMUNITAS', 'Dari komunitas, untuk komunitas.', 'Belajar bisa dimulai dari siapa saja, di mana saja.'),
    ('AKSES TERBUKA', 'Moodle untuk belajar bersama.', 'Kursus, latihan, dan materi bisa diakses kapan saja.'),
]

icon = Image.open(ICON).convert('RGBA').resize((280, 280), Image.LANCZOS)

for idx, (small, big, desc) in enumerate(slides, 1):
    img = gradient((W * S, H * S), (16, 86, 150), (12, 150, 122))
    d = ImageDraw.Draw(img, 'RGBA')

    # dekorasi lingkaran halus
    for cx, cy, r, a in [(1180, 60, 190, 28), (1310, 330, 150, 22), (980, 390, 120, 18)]:
        d.ellipse([cx*S-r*S, cy*S-r*S, cx*S+r*S, cy*S+r*S], outline=(255,255,255,a), width=3*S)

    # ikon samar di kanan sebagai tekstur; teks di-overlay oleh theme
    ic = icon.resize((280*S, 280*S), Image.LANCZOS)
    faint = ic.copy()
    faint.putalpha(faint.getchannel('A').point(lambda a: int(a * 0.22)))
    img.paste(faint, ((W - 360) * S, 29 * S), faint)

    img.resize((W, H), Image.LANCZOS).save(OUT / f'slide{idx}.png')
    print(f'slide{idx}.png')

from pathlib import Path
from PIL import Image, ImageFilter

OUT = Path('/home/iful/.hermes/cache/scratch/moodle-slides')
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1400, 418

SRC1 = Path('/home/iful/.hermes/cache/documents/native-inputs/81500c9e070a89e13faa97b134e219b3cdb1c42161afb2b46bb1b96db829a2cc/img_6a55fe1eb8a5.jpg')
SRC2 = Path('/home/iful/.hermes/cache/documents/native-inputs/222c386596fb04c1afa8d65485f02d25eb6624246d553b166da3437cdb91f57a/img_cc89c07a87a3.jpg')


def cover(path, mirror=False):
    im = Image.open(path).convert('RGB')
    if mirror:
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    ratio = W / H
    w, h = im.size
    ch = int(w / ratio)
    if ch <= h:
        y = (h - ch) // 2
        im = im.crop((0, y, w, y + ch))
    else:
        cw = int(h * ratio)
        x = (w - cw) // 2
        im = im.crop((x, 0, x + cw, h))
    return im.resize((W, H), Image.LANCZOS).convert('RGBA')


def right_fade(img, start=0.52, max_alpha=190, color=(8, 30, 55), blur=False, hotspot=None):
    if blur:
        blurred = img.filter(ImageFilter.GaussianBlur(12 if blur is True else blur))
        mask = Image.new('L', img.size, 0)
        md = ImageDraw.Draw(mask)
        for x in range(img.width):
            t = max(0.0, (x / img.width - (start - 0.12)) / (1 - (start - 0.12)))
            a = int(255 * min(1.0, t ** 1.1))
            md.line([(x, 0), (x, img.height)], fill=a)
        img = Image.composite(blurred, img, mask)
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(img.width):
        t = max(0.0, (x / img.width - start) / (1 - start))
        a = int(max_alpha * min(1.0, t ** 1.25))
        od.line([(x, 0), (x, img.height)], fill=color + (a,))
    img = Image.alpha_composite(img, overlay)
    if hotspot:
        cx, cy, rx, ry, strength = hotspot
        hm = Image.new('L', img.size, 0)
        hd = ImageDraw.Draw(hm)
        hd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=strength)
        hm = hm.filter(ImageFilter.GaussianBlur(60))
        ho = Image.new('RGBA', img.size, color + (0,))
        ho.putalpha(hm)
        img = Image.alpha_composite(img, ho)
    return img.convert('RGB')

from PIL import ImageDraw

s1 = right_fade(cover(SRC1), start=0.38, max_alpha=205, blur=True,
                hotspot=(int(W * 0.60), H // 2, 260, 180, 150))
s2 = right_fade(cover(SRC2, mirror=True), start=0.55, max_alpha=220)
s1.save(OUT / 'slide1.png', quality=92)
s2.save(OUT / 'slide2.png', quality=92)
print('slide1.png', s1.size)
print('slide2.png', s2.size)

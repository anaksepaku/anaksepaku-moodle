from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

OUT = Path('/home/iful/.hermes/cache/scratch/moodle-slides')
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1400, 418
NAVY = (8, 30, 55)

S1 = Path('/home/iful/.hermes/cache/documents/native-inputs/81500c9e070a89e13faa97b134e219b3cdb1c42161afb2b46bb1b96db829a2cc/img_6a55fe1eb8a5.jpg')
S2 = Path('/home/iful/.hermes/cache/documents/native-inputs/222c386596fb04c1afa8d65485f02d25eb6624246d553b166da3437cdb91f57a/img_cc89c07a87a3.jpg')


def cover(path):
    im = Image.open(path).convert('RGB')
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
    return im.resize((W, H), Image.LANCZOS)


def background(path):
    bg = cover(path).filter(ImageFilter.GaussianBlur(26)).convert('RGBA')
    veil = Image.new('RGBA', (W, H), NAVY + (165,))
    return Image.alpha_composite(bg, veil)


def foreground(path, crop_ratio=None, max_w=900):
    im = Image.open(path).convert('RGB')
    if crop_ratio:
        ch = int(im.width / crop_ratio)
        y = (im.height - ch) // 2
        im = im.crop((0, y, im.width, y + ch))
    box_h = H - 18
    scale = min(max_w / im.width, box_h / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.LANCZOS).convert('RGBA')

    # integrasikan dengan latar: veil tipis + feather di sisi kanan
    veil = Image.new('RGBA', (nw, nh), NAVY + (42,))
    im = Image.alpha_composite(im, veil)
    mask = Image.new('L', (nw, nh), 255)
    md = ImageDraw.Draw(mask)
    fade_from = int(nw * 0.70)
    for x in range(fade_from, nw):
        t = (x - fade_from) / max(1, nw - fade_from)
        md.line([(x, 0), (x, nh)], fill=int(255 * (1 - t) ** 1.25))
    for y in range(0, 12):
        a = int(255 * y / 12)
        md.line([(0, y), (nw, y)], fill=min(mask.getpixel((0, y)), a))
        md.line([(0, nh - 1 - y), (nw, nh - 1 - y)], fill=min(mask.getpixel((0, nh - 1 - y)), a))
    return im, mask, nw, nh


def right_gradient(canvas, start=0.56, max_alpha=205):
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(W):
        t = max(0.0, (x / W - start) / (1 - start))
        a = int(max_alpha * min(1.0, t ** 1.2))
        od.line([(x, 0), (x, H)], fill=NAVY + (a,))
    return Image.alpha_composite(canvas, overlay).convert('RGB')


def build(src, out, crop_ratio=None):
    canvas = background(src)
    fg, mask, nw, nh = foreground(src, crop_ratio=crop_ratio)
    canvas.paste(fg, (20, (H - nh) // 2), mask)
    right_gradient(canvas).save(out, quality=92)
    print(out.name, 'fg', nw, 'x', nh)


build(S1, OUT / 'slide1.png')
build(S2, OUT / 'slide2.png', crop_ratio=2.0)

from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, PageBreak,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT = 'IPA'
pdfmetrics.registerFont(TTFont(FONT, '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
pdfmetrics.registerFontFamily(FONT, normal=FONT, bold=FONT, italic=FONT, boldItalic=FONT)

SRC = Path(__import__('sys').argv[1]) if len(__import__('sys').argv) > 1 else Path('course/v2/html')
OUT = Path(__import__('sys').argv[2]) if len(__import__('sys').argv) > 2 else Path('course/pdf')
OUT.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
h1 = ParagraphStyle('H1', parent=styles['Title'], fontName=FONT, fontSize=20, leading=26, spaceAfter=8)
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName=FONT, fontSize=14, leading=18, spaceBefore=10, spaceAfter=5)
body = ParagraphStyle('Body', parent=styles['BodyText'], fontName=FONT, fontSize=10, leading=15, spaceAfter=5)
small = ParagraphStyle('Small', parent=body, fontSize=8.5, leading=12)

def esc(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def inline(node):
    parts = []
    if isinstance(node, NavigableString):
        parts.append(esc(str(node)))
        return ''.join(parts)
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(esc(str(child)))
        elif isinstance(child, Tag):
            inner = inline(child)
            if child.name in ('b', 'strong'):
                parts.append(f'<b>{inner}</b>')
            elif child.name in ('i', 'em'):
                parts.append(f'<i>{inner}</i>')
            elif child.name == 'code':
                parts.append(f'<font face="Courier">{inner}</font>')
            elif child.name == 'br':
                parts.append('<br/>')
            else:
                parts.append(inner)
    return ''.join(parts)

def build_story(files, chapter_title=None):
    story = []
    if chapter_title:
        story.append(Paragraph(chapter_title, h1))
        story.append(Spacer(1, 4*mm))
    for idx, path in enumerate(files):
        soup = BeautifulSoup(path.read_text(errors='replace'), 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else path.stem
        body_tag = soup.body or soup
        story.append(Paragraph(f'{idx+1}. {esc(title)}', h2))
        for el in body_tag.children:
            if not isinstance(el, Tag):
                continue
            if el.name in ('h1','h2','h3','h4','h5'):
                story.append(Paragraph(esc(el.get_text(' ', strip=True)), h2))
            elif el.name == 'p':
                t = inline(el).strip()
                if t: story.append(Paragraph(t, body))
            elif el.name in ('ol','ul'):
                items = []
                for li in el.find_all('li', recursive=False):
                    items.append(ListItem(Paragraph(inline(li).strip(), body)))
                if items:
                    story.append(ListFlowable(items, bulletType='1' if el.name=='ol' else 'bullet', start='1', leftIndent=12))
            elif el.name == 'table':
                data = []
                for tr in el.find_all('tr'):
                    row = [Paragraph(inline(cell).strip(), small) for cell in tr.find_all(['th','td'])]
                    if row: data.append(row)
                if data:
                    t = Table(data, repeatRows=1, hAlign='LEFT')
                    t.setStyle(TableStyle([
                        ('GRID',(0,0),(-1,-1),0.4,colors.grey),
                        ('BACKGROUND',(0,0),(-1,0),colors.whitesmoke),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('FONTNAME',(0,0),(-1,-1),FONT),
                        ('FONTSIZE',(0,0),(-1,-1),8),
                        ('LEFTPADDING',(0,0),(-1,-1),4),
                        ('RIGHTPADDING',(0,0),(-1,-1),4),
                        ('TOPPADDING',(0,0),(-1,-1),3),
                        ('BOTTOMPADDING',(0,0),(-1,-1),3),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 3*mm))
        story.append(Spacer(1, 4*mm))
        if idx < len(files)-1:
            story.append(PageBreak())
    return story

def write_pdf(name, files, title):
    doc = SimpleDocTemplate(
        str(OUT/name), pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=title,
    )
    doc.build(build_story(files, title))
    print(name, (OUT/name).stat().st_size)

all_files = sorted(SRC.glob('*.html'))
by_name = {p.name: p for p in all_files}

write_pdf('Bahasa-Jepang-Bulan-Pertama-v2.pdf', all_files, 'Bahasa Jepang Bulan Pertama — Versi 2')

sessions = {
    'Sesi-1-Hiragana.pdf': (['01-pengantar-dan-rencana.html','02-hiragana.html','02a-cara-berlatih-menulis-kana.html'], 'Minggu 1 — Hiragana'),
    'Sesi-2-Katakana.pdf': (['03-katakana.html'], 'Minggu 2 — Katakana'),
    'Sesi-3-Kanji-Partikel.pdf': (['04-kanji.html','06-partikel.html','08-kata-tanya-dan-penunjuk.html'], 'Minggu 3 — Kanji & Partikel'),
    'Sesi-4-Pola-Kalimat.pdf': (['05-sapaan-dan-perkenalan.html','07-pola-kalimat.html','09-angka-dan-waktu.html','10-kata-kerja-langkah-demi-langkah.html','11-kata-sifat.html','12-dialog-mini.html'], 'Minggu 4 — Pola Kalimat & Listening'),
    'Latihan-Sumber-Belajar.pdf': (['13-sumber-belajar.html'], 'Latihan & Sumber Belajar'),
}
for name, (names, title) in sessions.items():
    write_pdf(name, [by_name[n] for n in names], title)

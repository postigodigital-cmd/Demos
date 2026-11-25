# GIF da demo dentro de um telemóvel: pausa 1,2 s no topo, desce a página toda, volta ao topo, em loop.
# Uso: python3 gif.py pasta-da-demo saida.gif [pasta-com-fotos-locais]
import sys, io, math
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

slug, out = sys.argv[1], sys.argv[2]
W, H = 390, 844            # proporções atuais do telemóvel (ecrã)
SB = 44                    # barra de estado (hora, rede, Wi-Fi, bateria)
PH = H - SB                # altura visível da página
CREME = (246, 240, 230)
ESC = 0.68
FRACAO = 0.5               # até onde desce (metade da página)
CORES = int(sys.argv[3]) if len(sys.argv) > 3 else 96
DITHER = False                 # escala final do ecrã dentro do GIF

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": PH}, device_scale_factor=1, color_scheme="light")
    pg.goto(f"file:///home/claude/demos/{slug}/index.html")
    pg.add_style_tag(content=".aviso{display:none!important}html{scroll-behavior:auto!important}")
    pg.wait_for_timeout(500)
    total = pg.evaluate("document.documentElement.scrollHeight") - PH
    total = min(total, int(total * FRACAO))     # de propósito: só até meio da página
    nome = pg.evaluate("document.title.split(' · ')[0]")
    passos = max(24, int(total / 17))           # ~45 px por frame a descer
    posicoes = [0] * 1                             # topo (pausa feita pela duração)
    descer = [round(total * (1 - math.cos(math.pi * i / passos)) / 2) for i in range(1, passos + 1)]
    subir = [round(total * (1 + math.cos(math.pi * i / 11)) / 2) for i in range(1, 12)]
    seq = [(0, 1200)] + [(y, 50) for y in descer] + [(total, 900)] + [(y, 45) for y in subir]
    shots = {}
    for y, _ in seq:
        if y not in shots:
            pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(40)
            shots[y] = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
    b.close()

def desenha_estado(img):
    d = ImageDraw.Draw(img); cor = (20, 20, 20)
    try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except Exception: f = ImageFont.load_default()
    d.text((34, 13), "9:41", font=f, fill=cor)
    x = 286
    for i, h in enumerate([5, 8, 11, 14]):            # rede
        d.rectangle([x + i * 5, 29 - h, x + i * 5 + 3, 29], fill=cor)
    cx, cy = 320, 30                                  # Wi-Fi
    for r in (13, 9, 5):
        d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=cor, width=2)
    d.ellipse([cx - 2, cy - 3, cx + 2, cy + 1], fill=cor)
    d.rounded_rectangle([336, 16, 362, 29], 3, outline=cor, width=2)   # bateria
    d.rectangle([339, 19, 355, 26], fill=cor); d.rectangle([363, 20, 365, 25], fill=cor)

# moldura
sw, sh = int(W * ESC), int(H * ESC)
borda, raio = 12, 44
fw, fh = sw + 2 * borda, sh + 2 * borda
CW, CH = fw + 80, fh + 110
try:
    fonte = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 15)
    fonte2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except Exception:
    fonte = fonte2 = ImageFont.load_default()
mask = Image.new("L", (sw, sh), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, sh - 1], raio - borda, fill=255)
base = Image.new("RGB", (CW, CH), CREME); d = ImageDraw.Draw(base)
x0, y0 = 40, 24
d.rounded_rectangle([x0 + 4, y0 + 8, x0 + fw + 4, y0 + fh + 8], raio, fill=(225, 218, 205))
d.rounded_rectangle([x0, y0, x0 + fw, y0 + fh], raio, fill=(17, 17, 17))
t1 = f"Esboço de demonstração para {nome}"; t2 = "preparado pela Postigo Digital · não é o site oficial"
for t, f, yy, cor in [(t1, fonte, y0 + fh + 30, (40, 40, 40)), (t2, fonte2, y0 + fh + 56, (110, 110, 100))]:
    tw = d.textlength(t, font=f); d.text(((CW - tw) / 2, yy), t, font=f, fill=cor)

rgb, durs = [], []
for y, dur in seq:
    fr = base.copy()
    tela = Image.new("RGB", (W, H), (251, 248, 242))
    tela.paste(shots[y], (0, SB))
    desenha_estado(tela)
    ecra = tela.resize((sw, sh), Image.LANCZOS)
    fr.paste(ecra, (x0 + borda, y0 + borda), mask)
    rgb.append(fr); durs.append(dur)
# paleta única para todo o GIF (mais leve e sem tremer)
amostra = Image.new("RGB", (CW, CH * 4))
for i, k in enumerate([0, len(rgb) // 3, 2 * len(rgb) // 3, len(rgb) - 1]):
    amostra.paste(rgb[k], (0, CH * i))
pal = amostra.quantize(colors=CORES, method=Image.MEDIANCUT)
frames = [f.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG if DITHER else Image.Dither.NONE) for f in rgb]
frames[0].save(out, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True, disposal=1)
import os; print(out, round(os.path.getsize(out) / 1e6, 2), "MB", len(frames), "frames")

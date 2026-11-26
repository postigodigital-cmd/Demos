# Gerador de demos Postigo Digital: python3 gerar.py dados.json pasta
import json,sys,html
d=json.load(open(sys.argv[1],encoding='utf-8')); out=sys.argv[2]
e=html.escape
c=d.get("cor","#1F3A2B"); a=d.get("acento","#B8323F")
units="".join(f'''<div class="u"><div class="foto" style="background-image:url('{u["img"]}')"></div><div class="ut"><b>{e(u["nome"])}</b><span>{e(u["desc"])}</span></div></div>''' for u in d["unidades"])
chips="".join(f"<li>{e(x)}</li>" for x in d["destaques"])
extra=f'<div class="cupao">{e(d["promo"])}</div>' if d.get("promo") else ""
page=f'''<!DOCTYPE html><html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="color-scheme" content="only light">
<title>{e(d["nome"])} · Esboço · Postigo Digital</title><style>
:root{{color-scheme:only light;--c:{c};--a:{a};--papel:#FBF8F2;--creme:#F4EEE3;--tinta:#22261F;--suave:#6B6F62}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{font-family:Georgia,serif;background:var(--papel);color:var(--tinta);line-height:1.55;padding-bottom:100px}}
.s{{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
.aviso{{background:#000;color:#ddd;font:12px/1.4 -apple-system,Roboto,sans-serif;text-align:center;padding:7px 12px}}.aviso b{{color:#fff}}
header{{position:sticky;top:0;z-index:5;background:rgba(251,248,242,.95);border-bottom:1px solid #e7e0d3;display:flex;align-items:center;justify-content:space-between;padding:14px 18px}}
.marca{{font-size:23px;color:var(--c);text-decoration:none}}.lang{{font:600 15px -apple-system,Roboto,sans-serif;color:var(--c)}}
.hero{{min-height:560px;color:#fff;padding:60px 22px 40px;display:flex;flex-direction:column;justify-content:flex-end;background:linear-gradient(180deg,rgba(0,0,0,.15) 0,rgba(0,0,0,.55) 55%,rgba(0,0,0,.82) 100%),url('{d["hero"]}') center/cover,var(--c)}}
.k{{font:600 11px -apple-system,Roboto,sans-serif;letter-spacing:.18em;text-transform:uppercase;opacity:.9}}
.hero h1{{font-weight:400;font-size:38px;line-height:1.08;margin:12px 0}}.hero p{{font-size:17px;opacity:.92;max-width:34ch}}
.ctas{{display:grid;gap:10px;margin-top:24px}}
.btn{{display:flex;justify-content:center;align-items:center;text-decoration:none;font:600 16px -apple-system,Roboto,sans-serif;padding:15px;border-radius:12px}}
.p{{background:var(--a);color:#fff}}.o{{border:1.5px solid rgba(255,255,255,.6);color:#fff}}
section{{padding:42px 22px}}h2{{font-weight:400;font-size:29px;color:var(--c);margin:6px 0 16px;line-height:1.15}}
.u{{background:#fff;border:1px solid #ebe3d4;border-radius:16px;overflow:hidden;margin-bottom:14px}}
.u .foto{{aspect-ratio:16/10;background:var(--creme) center/cover}}.ut{{padding:14px 16px;font:15px -apple-system,Roboto,sans-serif}}.ut b{{display:block;font:400 20px Georgia,serif;color:var(--c)}}.ut span{{color:var(--suave)}}
.preco{{background:var(--creme);border-radius:16px;padding:18px;margin:6px 0 16px}}.preco b{{font-size:30px;font-weight:400;color:var(--c)}}
.nota{{font:12px -apple-system,Roboto,sans-serif;color:var(--suave)}}
ul.ch{{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:8px;font:14px -apple-system,Roboto,sans-serif}}ul.ch li{{background:var(--creme);border-radius:10px;padding:10px}}
.cupao{{margin-top:14px;border:2px dashed var(--a);border-radius:12px;padding:12px;text-align:center;font:600 15px -apple-system,Roboto,sans-serif;color:var(--a)}}
.xt{{display:grid;gap:10px}}.xt div{{background:#fff;border:1px solid #ebe3d4;border-radius:14px;padding:14px 16px;font:15px -apple-system,Roboto,sans-serif}}.xt b{{display:block;font:400 19px Georgia,serif;color:var(--c)}}.min{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}}.min div{{border-radius:14px;padding:16px 12px;color:#fff;font:400 18px Georgia,serif;text-align:center}}.dir{{background:var(--c);color:#fff}}.dir h2{{color:#fff}}.dir p{{opacity:.88;margin-bottom:10px}}
footer{{padding:28px 22px;font:13px -apple-system,Roboto,sans-serif;color:var(--suave);text-align:center}}
.barra{{position:fixed;left:0;right:0;bottom:0;display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px 18px 24px;background:rgba(251,248,242,.98);border-top:1px solid #e3dbcc}}
.barra .btn{{padding:13px 8px;font-size:15px}}.barra .w{{border:1.5px solid var(--c);color:var(--c)}}
@media(min-width:760px){{body{{max-width:760px;margin:0 auto}}}}
</style></head><body>
<div class="aviso"><b>Esboço de demonstração</b> preparado pela Postigo Digital para {e(d["nome"])} · não é o site oficial</div>
<header><a class="marca" href="#">{e(d["nome"])}</a><span class="lang">PT · EN · FR · ES</span></header>
<div class="hero"><div class="k">{e(d["kicker"])}</div><h1>{e(d["titulo"])}</h1><p>{e(d["sub"])}</p>
<div class="ctas"><a class="btn p" href="#reservar">Ver datas e reservar →</a><a class="btn o" href="#">Falar por WhatsApp</a></div></div>
<section id="reservar"><div class="k" style="color:var(--a)">{e(d["k_unid"])}</div><h2>{e(d["t_unid"])}</h2>{units}
<div class="preco"><span class="s" style="font-size:14px">desde </span><b>{e(d["preco"])}</b><span class="s" style="font-size:14px"> /noite</span><div class="nota">* Preço ilustrativo, só para o esboço.</div></div>
<a class="btn p" href="#">Ver disponibilidade</a>{extra}</section>
{d.get("extra","")}<section style="padding-top:0"><div class="k" style="color:var(--a)">Porquê ficar aqui</div><h2>{e(d["t_dest"])}</h2><ul class="ch">{chips}</ul></section>
<section class="dir"><h2>Reserve diretamente connosco</h2><p>Melhor preço, sem intermediários e resposta direta de quem vos recebe.</p><p class="s" style="font-size:14px">WhatsApp · Email · Calendário online</p></section><section style="padding:26px 22px;text-align:center"><p class="nota" style="font-size:13px">Este esboço é só um ponto de partida: cores, textos, secções e fotografias escolhem-se convosco, ao vosso gosto.</p></section>
<footer>{e(d["nome"])} · {e(d["local"])}<br><span style="font-size:12px">Esboço preparado pela Postigo Digital · postigodigital.pt</span></footer>
<div class="barra"><a class="btn p" href="#reservar">Reservar</a><a class="btn w" href="#">WhatsApp</a></div>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "a3b89414fee64e46a75b1ccb7246c2ec"}}'></script><!-- End Cloudflare Web Analytics --></body></html>'''
import os; os.makedirs(out,exist_ok=True); open(os.path.join(out,"index.html"),"w",encoding="utf-8").write(page); print("ok",out)

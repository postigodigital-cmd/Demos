# Lê a página pública de um site de prospeto e guarda o essencial em _testes/resultados/<slug>-pagina.json
import sys, re, json, html, urllib.request, urllib.parse, os
slug, url = sys.argv[1], sys.argv[2]
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36"}
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25)
        return r.status, r.geturl(), r.read(2_000_000).decode("utf-8", "replace")
    except Exception as e:
        return None, u, str(e)
def cfemail(h):
    k = int(h[:2], 16); return "".join(chr(int(h[i:i+2], 16) ^ k) for i in range(2, len(h), 2))
out = {"site": url, "abre": False}
st, final, txt = get(url)
out["estado_http"] = st; out["url_final"] = final
if st is None:
    out["erro"] = txt[:200]
else:
    out["abre"] = True
    paginas = [txt]
    base = final if final.endswith("/") else final.rsplit("/", 1)[0] + "/"
    links = set(re.findall(r'href=["\']([^"\'#]+)', txt, re.I))
    for l in list(links):
        if re.search(r"contact", l, re.I):
            s2, _, t2 = get(urllib.parse.urljoin(base, l))
            if s2: paginas.append(t2); links |= set(re.findall(r'href=["\']([^"\'#]+)', t2, re.I))
            break
    tudo = "\n".join(paginas)
    emails = set(e.lower() for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", html.unescape(tudo)) if not re.search(r"\.(png|jpg|webp|gif|svg)$|sentry|wixpress|example", e, re.I))
    emails |= {cfemail(h) for h in re.findall(r'data-cfemail="([0-9a-f]+)"', tudo)}
    emails |= {cfemail(h) for h in re.findall(r"/cdn-cgi/l/email-protection#([0-9a-f]+)", tudo)}
    out["emails"] = sorted(emails)
    out["telefones"] = sorted(set(re.sub(r"\s+", " ", t).strip() for t in re.findall(r"(?:\+351[\s.]?)?(?:2\d|9[1236])\d[\s.]?\d{3}[\s.]?\d{3}", re.sub(r"<[^>]+>", " ", tudo))))[:6]
    def tem(p): return sorted({l for l in links if re.search(p, l, re.I)})[:3]
    out["instagram"] = tem(r"instagram\.com/"); out["facebook"] = tem(r"facebook\.com/")
    out["booking"] = tem(r"booking\.com"); out["airbnb"] = tem(r"airbnb\."); out["thefork"] = tem(r"thefork|lafourchette")
    out["whatsapp"] = tem(r"wa\.me|whatsapp"); 
    out["botao_reserva"] = bool(re.search(r">\s*(reservar|reserve|book now|booking|reservas)\s*<", tudo, re.I))
    out["linguas"] = sorted(set(re.findall(r'hreflang=["\']([\w-]+)', tudo)))
    anos = [int(a) for a in re.findall(r"(?:©|&copy;|copyright)\D{0,20}((?:19|20)\d\d)", tudo, re.I)]
    out["ano_rodape"] = max(anos) if anos else None
    m = re.search(r"<title[^>]*>(.*?)</title>", txt, re.I | re.S); out["titulo"] = html.unescape(m.group(1).strip())[:120] if m else None
    m = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)', txt, re.I); out["feito_com"] = m.group(1)[:60] if m else None
    out["viewport_telemovel"] = bool(re.search(r'name=["\']viewport', txt, re.I))
os.makedirs("_testes/resultados", exist_ok=True)
json.dump(out, open(f"_testes/resultados/{slug}-pagina.json", "w"), ensure_ascii=False, indent=1)
print(out)

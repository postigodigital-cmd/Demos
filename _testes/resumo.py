import json, sys, base64, os
src, slug, url = sys.argv[1], sys.argv[2], sys.argv[3]
r = json.load(open(src))
c = r.get("categories", {}); a = r.get("audits", {})
def sc(k): v = c.get(k, {}).get("score"); return None if v is None else round(v*100)
def dv(k): return a.get(k, {}).get("displayValue")
out = {"site": url, "data": r.get("fetchTime"), "modo": "telemóvel",
 "velocidade": sc("performance"), "acessibilidade": sc("accessibility"),
 "boas_praticas": sc("best-practices"), "seo": sc("seo"),
 "primeiro_conteudo": dv("first-contentful-paint"), "maior_conteudo": dv("largest-contentful-paint"),
 "tempo_total_bloqueio": dv("total-blocking-time"), "estabilidade_cls": dv("cumulative-layout-shift"),
 "https": a.get("is-on-https", {}).get("score") == 1,
 "adaptado_telemovel": a.get("viewport", {}).get("score") == 1,
 "erro": r.get("runtimeError", {}).get("message")}
os.makedirs("_testes/resultados", exist_ok=True)
json.dump(out, open(f"_testes/resultados/{slug}.json", "w"), ensure_ascii=False, indent=1)
shot = a.get("final-screenshot", {}).get("details", {}).get("data", "")
if shot.startswith("data:image"):
    open(f"_testes/resultados/{slug}.jpg", "wb").write(base64.b64decode(shot.split(",", 1)[1]))
print(out)

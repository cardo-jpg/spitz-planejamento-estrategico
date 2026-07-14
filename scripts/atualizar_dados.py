# -*- coding: utf-8 -*-
"""
Atualiza os dados da dashboard Spitz a partir da planilha publica do Drive.
Uso:  python scripts/atualizar_dados.py
Regenera:  data.js (bloco METAD) e meta_granular.js (CAMPD/PUBD/CRIAD/CRIA_URL)

A planilha [SP] Fonte de dados Ecom e' PUBLICA (link view) -> da' pra ler aba por aba
via gviz CSV sem depender de conector:
  https://docs.google.com/spreadsheets/d/{ID}/gviz/tq?tqx=out:csv&sheet={AbaURLencoded}
Listar abas reais:  curl .../htmlview | grep -oE 'items.push\\(\\{name: "[^"]+"'
Abas: Somatorio, GG Search - Campanhas/Palavras-chave/Localizacoes, GG Display,
      YT, YT - Criativos, GA4, Meta Ads, Meta Ads - Publico, Meta Ads - Criativos.
As abas 'Meta Ads*' tem dado DIARIO granular + coluna URL (permalink Instagram do anuncio).
ATENCAO: a aba Criativos tem datas historicas -> filtrar pelas datas validas do periodo
(senao dias iguais de anos diferentes somam e inflam ~18x).
"""
import csv, io, json, re, os, urllib.parse, urllib.request

SHEET_ID = "1s7JWfFTVcZT7l_Z9sDPaqmxDqSspZs-0xvkTV7qf1k0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fetch(tab):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(tab)}"
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read().decode("utf-8")
    return list(csv.reader(io.StringIO(data)))

def num(s):
    if s is None: return 0.0
    s = s.replace("R$", "").replace("\xa0", "").strip()
    if not s or s in ("-", "—"): return 0.0
    s = s.replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

def dm(d):
    p = d.split("/"); return p[0] + "/" + p[1] if len(p) >= 2 else d

# ATENCAO: a aba 'Somatorio' agora SOMA Meta+Google -> faturamento/vendas double-count
# (atribuicao se sobrepoe). Por isso METAD e' derivado da aba 'Meta Ads' (Meta puro), abaixo.

# ---------- Granular (abas Meta Ads*) ----------
camp = fetch("Meta Ads")[1:]
VALID = set(r[0] for r in camp if r and r[0] and r[0].endswith("/2026"))

def agg(rows, name_idx, cols):  # cols = (inv,imp,clk,add,chk,vd,fat) indices
    m = {}
    for r in rows:
        if not r or not r[0] or r[0] not in VALID or len(r) <= max(name_idx, *cols): continue
        nm = r[name_idx].strip()
        if not nm: continue
        a = m.setdefault((dm(r[0]), nm), [0.0]*7)
        for i, ci in enumerate(cols): a[i] += num(r[ci])
    return [[k[0], k[1], round(v[0],2), int(v[1]), int(v[2]), int(v[3]), int(v[4]), int(v[5]), round(v[6],2)]
            for k, v in m.items()]

# Meta Ads: 0Data 1Camp 2Inv 3Imp 4Clk 5Vis 6Add 7vAdd 8Chk 9Vd 10Fat 11Criativo 12URL
CAMPD = agg(camp, 1, (2,3,4,6,8,9,10))
cria_url = {}
for r in camp:
    if len(r) > 12 and r[0] in VALID and r[11].strip() and r[12].strip().startswith("http"):
        cria_url.setdefault(r[11].strip(), r[12].strip())

# Meta Ads - Publico: 0Data 1Camp 2Pub 3Inv 4Imp 5Clk 6Vis 7Add 8vAdd 9Chk 10vChk 11Vd 12Fat
PUBD = agg(fetch("Meta Ads - Público")[1:], 2, (3,4,5,7,9,11,12))

# Meta Ads - Criativos: 0Data 1Camp 2Pub 3Cria 4Inv 5Imp 6Clk 7Vis 8Add 9vAdd 10Chk 11vChk 12Vd 13Fat
CRIAD = agg(fetch("Meta Ads - Criativos")[1:], 3, (4,5,6,8,10,12,13))
crioms = set(r[1] for r in CRIAD)
CRIA_URL = {k: v for k, v in cria_url.items() if k in crioms}

# ---------- METAD = aba 'Meta Ads' agregada por DIA (Meta puro, funil completo) ----------
# Meta Ads: 0Data 1Camp 2Inv 3Imp 4Clk 5Vis 6Add 7vAdd 8Chk 9Vd 10Fat
mday = {}
for r in camp:
    if not r or not r[0] or r[0] not in VALID or len(r) < 11: continue
    a = mday.setdefault(dm(r[0]), [0.0]*8)
    for i, ci in enumerate((2,3,4,5,6,8,9,10)): a[i] += num(r[ci])
METAD = [[k, round(v[0],2), int(v[1]), int(v[2]), int(v[3]), int(v[4]), int(v[5]), int(v[6]), round(v[7],2)]
         for k, v in sorted(mday.items(), key=lambda x: (x[0][3:5], x[0][:2]))]

# ---------- Google Search (abas GG Search *) ----------
gcamp = fetch("GG Search - Campanhas")[1:]
GVALID = set(r[0] for r in gcamp if r and r[0] and r[0].endswith("/2026"))

def gagg(rows, name_idx, cols):  # cols = (inv,imp,clk,vd,fat) indices -> [data,nome,inv,imp,clk,vd,fat]
    m = {}
    for r in rows:
        if not r or not r[0] or r[0] not in GVALID or len(r) <= max(name_idx, *cols): continue
        nm = r[name_idx].strip()
        if not nm: continue
        a = m.setdefault((dm(r[0]), nm), [0.0]*5)
        for i, ci in enumerate(cols): a[i] += num(r[ci])
    return [[k[0], k[1], round(v[0],2), int(v[1]), int(v[2]), int(v[3]), round(v[4],2)] for k, v in m.items()]

# GG camp: 0Data 1Camp 2Inv 3Imp 4Clk 5Vd 6Fat ; kw: 0Data 1Palavra 2Inv 3Imp 4Clk 5Vd 6Fat ; loc: +7Estado
GCAMPD = gagg(gcamp, 1, (2,3,4,5,6))
GKWD = gagg(fetch("GG Search - Palavras-chave")[1:], 1, (2,3,4,5,6))
GLOCD = gagg(fetch("GG Search - Localizações")[1:], 7, (2,3,4,5,6))

outg = "// ===== Google Search diario (fonte: [SP] Fonte de dados Ecom, abas GG Search *) =====\n"
outg += "// [data, nome, inv, imp, clk, vendas, faturamento]\n"
outg += "const GCAMPD=" + json.dumps(GCAMPD, ensure_ascii=False) + ";\n"
outg += "const GKWD=" + json.dumps(GKWD, ensure_ascii=False) + ";\n"
outg += "const GLOCD=" + json.dumps(GLOCD, ensure_ascii=False) + ";\n"
open(os.path.join(ROOT, "google_granular.js"), "w", encoding="utf-8", newline="\n").write(outg)
ginv = sum(x[2] for x in GCAMPD); gfat = sum(x[6] for x in GCAMPD); gvd = sum(x[5] for x in GCAMPD)
print(f"GOOGLE camp {len(GCAMPD)} | kw {len(GKWD)} | loc {len(GLOCD)} | inv R${ginv:,.2f} | fat R${gfat:,.2f} | vendas {gvd} | ROAS {gfat/ginv if ginv else 0:.2f}")

# ---------- grava data.js (so' o bloco METAD) ----------
dj = open(os.path.join(ROOT, "data.js"), encoding="utf-8").read()
metad_js = "const METAD=[\n" + ",\n".join(json.dumps(x, ensure_ascii=False) for x in METAD) + "\n];"
dj = re.sub(r"const METAD=\[.*?\];", metad_js, dj, count=1, flags=re.S)
open(os.path.join(ROOT, "data.js"), "w", encoding="utf-8", newline="\n").write(dj)

# ---------- grava meta_granular.js ----------
out = "// ===== Granular diario (fonte: [SP] Fonte de dados Ecom, abas Meta Ads*) =====\n"
out += "// [data, nome, inv, imp, clk, add_carrinho, checkout, vendas, faturamento]\n"
out += "const CAMPD=" + json.dumps(CAMPD, ensure_ascii=False) + ";\n"
out += "const PUBD=" + json.dumps(PUBD, ensure_ascii=False) + ";\n"
out += "const CRIAD=" + json.dumps(CRIAD, ensure_ascii=False) + ";\n"
out += "const CRIA_URL=" + json.dumps(CRIA_URL, ensure_ascii=False) + ";\n"
open(os.path.join(ROOT, "meta_granular.js"), "w", encoding="utf-8", newline="\n").write(out)

inv = sum(x[1] for x in METAD); fat = sum(x[8] for x in METAD); vd = sum(x[7] for x in METAD)
print(f"METAD: {len(METAD)} dias | inv R${inv:,.2f} | fat R${fat:,.2f} | vendas {vd} | ROAS {fat/inv if inv else 0:.2f}")
print(f"CAMPD {len(CAMPD)} | PUBD {len(PUBD)} | CRIAD {len(CRIAD)} | URLs {len(CRIA_URL)}")
print("OK -> lembre de dar bump no ?v= das tags <script> no index.html e commitar.")

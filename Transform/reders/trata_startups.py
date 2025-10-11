import json, csv, os

folder = '../Extract/reders/jsons_startups'

# nomes dos ecossistemas
ecos = [
    "Central",
    "Fronteira Oeste e Campanha",
    "Metropolitana e Litoral Norte",
    "Noroeste e Missoes",
    "Producao e Norte",
    "Serra Gaucha",
    "Sul",
    "Vales"
]

def busca_dict(v, dic):
    # Se é numero tem q buscar no dict o valor
    if isinstance(v, int) and v < len(dic):
        return dic[v]
    # Se é texto só retorna o valor
    if isinstance(v, str):
        return v
    return ""

with open("startups.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Ecossistema","Nome","Cidade","Link"])

    for eco_nome in ecos:
        arq = eco_nome.replace(" ", "_") + ".json"
        path = os.path.join(folder, arq)
        eco = os.path.splitext(arq)[0].replace("_", " ")

        d = json.load(open(path, encoding="utf-8"))
        ds = d["results"][0]["result"]["data"]["dsr"]["DS"][0]
        vd, regs = ds["ValueDicts"], ds["PH"][0]["DM0"]

        cids, links, nomes = vd.get("D0", []), vd.get("D1", []), vd.get("D2", [])

        for r in regs:
            c, r_, o = r.get("C", []), r.get("R"), r.get("Ø")
            cidade, link, nome = "", "", ""

            if len(c) == 3:     # Tem todas infos no C
                cidade, link, nome = c
            elif len(c) == 2 and r_ is not None :   # Nome e link no C
                link, nome = c
                cidade = busca_dict(r_, cids)
            elif len(c) == 2 and  o is not None :   # Nome e cidade no C
                cidade, nome = c
                link = "" if o == 2 else link
            elif len(c) == 1:   # Só o nome no C
                nome = c[0]
                cidade = busca_dict(r_, cids)
                link = "" if o == 2 else link

            # Busca no dict o nome, cidade e link (se necessário, se não retorna os valores de texto)
            nb = busca_dict(nome, nomes)
            cb = busca_dict(cidade, cids)
            lb = busca_dict(link, links)
            
            w.writerow([eco, nb, cb, lb])

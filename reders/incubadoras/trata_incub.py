import os
import csv
import json

folder = "jsons_incubadoras"

ecossistemas = [
    "Central",
    "Fronteira Oeste e Campanha",
    "Metropolitana e Litoral Norte",
    "Noroeste e Missões",
    "Produção e Norte",
    "Serra Gaúcha",
    "Sul",
    "Vales"
]

files = [
    "Central",
    "Campanha_e_Fronteira_Oeste",
    "Metropolitana_e_Litoral_Norte",
    "Noroeste_e_Missoes",
    "Producao_e_Norte",
    "Serra_Gaucha",
    "Sul",
    "Regiao_dos_Vales"
]

def extrai_incubadoras():
    all_incubadoras = []
    for idx, eco in enumerate(ecossistemas):
        path = os.path.join(folder, f"{files[idx]}.json")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            ds = data["results"][0]["result"]["data"]["dsr"]["DS"][0]
            dm = ds["PH"][0]["DM0"]
            dicts = ds["ValueDicts"]

            for reg in dm:
                c = reg.get("C", [])
                r = reg.get("R")
                if len(c) > 2:
                    cid, link, nome = c[0], c[1], c[2]
                elif r is not None and r == 1:
                    link, nome = c[0], c[1]
                else:
                    cid, nome = c[0], c[1]

                cid_dict = dicts["D0"][cid]
                link_dict = dicts["D1"][link]
                nome_dict = dicts["D2"][nome]

                all_incubadoras.append([eco, nome_dict, cid_dict, link_dict])
                
    return all_incubadoras

incubadoras = extrai_incubadoras()
with open("incubadoras.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Ecossistema", "Nome", "Cidade", "Link"])
    w.writerows(incubadoras)
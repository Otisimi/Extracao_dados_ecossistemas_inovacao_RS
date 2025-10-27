import os
import csv
import json

folder = "jsons_aceleradoras"

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
    "Vales"
]

def extrai_aceleradoras():
    all_aceleradoras = []
    for idx, eco in enumerate(ecossistemas):
        path = os.path.join(folder, f"{files[idx]}.json")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            dm = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
            
            for dm_reg in dm:
                dm1 = dm_reg["M"][0]["DM1"]

                for reg in dm1:
                    c = reg.get("C", [])
                    sigla = c[2] 
                    nome = c[3]
                    link = c[4]
                    cid = c[7]
                            
                    all_aceleradoras.append([eco, sigla, nome, cid, link])
                
    return all_aceleradoras

aceleradoras = extrai_aceleradoras()
with open("aceleradoras.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Ecossistema", "Sigla", "Nome", "Cidade", "Link"])
    w.writerows(aceleradoras)
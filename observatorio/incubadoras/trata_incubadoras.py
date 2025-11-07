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
    "Vales"
]

# Casos possíveis de valores em cada registro de DM1
CASOS = {
    # Sigla, Nome, Link, Cidade
    (None, None): [0, 1, 3, 6],
    (32, None): [0, 1, 3, 5],
    (36, None): [0, 1, 2, 4],
    (44, None): [0, 1, 99, 3],
    (46, None): [0, 99, 99, 2],
    (100, None): [0, 1, 2, 99],
    (172, None): [0, 1, 99, 3],
    (180, None): [0, 1, 2, 3],
    (190, None): [0, 99, 99, 1],
    (252, None): [0, 1, 99, 99],
    (None, 4): [0, 1, 2, 5],
    (None, 136): [0, 1, None, 5],
    (None, 156): [0, 1, 2, 3],
    (32, 4): [0, 1, 2, 4],
    (36, 152): [0, 1, None, 2],   
    (36, 154): [0, None, None, 1],
    (44, 16): [0, 1, 99, 2],
    (100, 136): [0, 1, None, 99],
    (172, 16): [0, 1, 99, 2],
}

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
                o = reg.get("Ø")
                
                indices = CASOS.get((r, o))
                
                if indices:
                    # Pega o indice dos campos no registro (se é 99 é o mesmo anterior, se é nulo é nulo mesmo kk)
                    sigla = None if indices[0] is None else (sigla if indices[0] == 99 else c[indices[0]])
                    nome  = None if indices[1] is None else (nome  if indices[1] == 99 else c[indices[1]])
                    link  = None if indices[2] is None else (link  if indices[2] == 99 else c[indices[2]])
                    cid   = None if indices[3] is None else (cid   if indices[3] == 99 else c[indices[3]])
                    # Busca o valor no dict
                    sigla_dict = None if sigla is None else dicts["D0"][sigla]
                    nome_dict = None if nome is None else dicts["D1"][nome]
                    link_dict = None if link is None else dicts["D3"][link]
                    cid_dict = None if cid is None else dicts["D6"][cid]
                    
                    all_incubadoras.append([eco, sigla_dict, nome_dict, cid_dict, link_dict])
                
    return all_incubadoras

incubadoras = extrai_incubadoras()
with open("incubadoras.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Ecossistema", "Sigla", "Nome", "Cidade", "Link"])
    w.writerows(incubadoras)
import os
import csv
import json

folder = "jsons_instituicoes"

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
    (36, None): [0, 1, 2, 4],
    (48, None): [0, 1, 3, 4],
    (52, None): [0, 1, 2, 3],
    (53, None): [99, 0, 1, 2],
    (61, None): [99, 0, 99, 1],
    (116, None): [0, 1, 2, 99],
    (117, None): [99, 0, 1, 99],
    (181, None): [99, 0, 1, 2],
    (None, 4): [0, 1, 2, 5],
    (None, 16): [0, 1, 3, 5],
    (None, 20): [0, 1, 2, 4],
    (32, 20): [0, 1, 2, 3],
    (36, 16): [0, 1, 2, 3],
    (48, 4): [0, 1, 2, 3],
    (52, 128): [0, 1, 2, 3],
    (53, 128): [99, 0, 1, 2],
}

def extrai_instituicoes():
    all_instituicoes = []
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
                    try:
                    # Pega o indice dos campos no registro (se é 99 é o mesmo anterior, se é nulo é nulo mesmo kk)
                        sigla = None if indices[0] is None else (sigla if indices[0] == 99 else c[indices[0]])
                        nome  = None if indices[1] is None else (nome  if indices[1] == 99 else c[indices[1]])
                        link  = None if indices[2] is None else (link  if indices[2] == 99 else c[indices[2]])
                        cid   = None if indices[3] is None else (cid   if indices[3] == 99 else c[indices[3]])
                    except:
                        print(f"{eco} - {indices} - {nome} - {cid} - {c}")
                    # Busca o valor no dict
                    sigla_dict = None if sigla is None else dicts["D0"][sigla]
                    nome_dict = None if nome is None else dicts["D1"][nome]
                    link_dict = None if link is None else dicts["D3"][link]
                    cid_dict = None if cid is None else dicts["D6"][cid]
                    
                    all_instituicoes.append([eco, sigla_dict, nome_dict, cid_dict, link_dict])
                
    return all_instituicoes

instituicoes = extrai_instituicoes()
with open("instituicoes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Ecossistema", "Sigla", "Nome", "Cidade", "Link"])
    w.writerows(instituicoes)
import os
import csv
import json

def extrai_instituicoes():
    all_instituicoes = []
    with open("instituicoes_sucup.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
        for reg in data:
            nome = reg.get("nome")
            sigla = reg.get("sigla")
            cid = reg.get("municipio")

            all_instituicoes.append([sigla, nome, cid])
                
    return all_instituicoes

instituicoes = extrai_instituicoes()
with open("instituicoes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Sigla", "Nome", "Município"])
    w.writerows(instituicoes)
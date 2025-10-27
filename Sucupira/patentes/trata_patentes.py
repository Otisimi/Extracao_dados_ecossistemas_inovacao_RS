import os
import csv
import json

def extrai_patentes():
    all_patentes = []
    with open("patentes_sucup.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
        for reg in data:
            nome = reg.get("nomeProducao")
            sigla = reg.get("siglaIes")
            
            aut = reg.get("autores")
            autores = []
            for na in aut:
                autores.append(na.get("nomePessoa"))

            all_patentes.append([sigla, nome, autores])
                
    return all_patentes

patentes = extrai_patentes()
with open("patentes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Sigla IES", "Nome", "Autores"])
    w.writerows(patentes)
import os
import csv
import json

def extrai_projetos():
    all_projetos = []
    with open("projetos_sucup.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
        for reg in data:
            nome = reg.get("nomeProjeto")
            sigla = reg.get("siglaIes")
            responsavel = reg.get("membroResponsavel")
            resp = None
            if responsavel is not None:
                resp = responsavel.get("nomePessoa")
                

            all_projetos.append([sigla, nome, resp])
                
    return all_projetos

projetos = extrai_projetos()
with open("projetos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Sigla", "Nome", "Responsável"])
    w.writerows(projetos)
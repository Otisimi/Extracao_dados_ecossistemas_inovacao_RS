import os
import csv
import json

def extrai_publicacoes():
    all_publicacoes = []
    with open("publicacoes_sucup.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
        for reg in data:
            nome = reg.get("nomeProducao")
            sigla = reg.get("siglaIes")
            tipo = reg.get("nomeSubTipoProducao")
            
            aut = reg.get("autores")
            autores = []
            for na in aut:
                autores.append(na.get("nomePessoa"))
                

            all_publicacoes.append([sigla, nome, tipo, autores])
                
    return all_publicacoes

publicacoes = extrai_publicacoes()
with open("publicacoes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Sigla", "Nome", "Tipo Produção", "Autores"])
    w.writerows(publicacoes)
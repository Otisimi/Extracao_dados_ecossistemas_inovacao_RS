import pandas as pd

arq_instituicoes = "instituicoes/instituicoes.csv"
arq_projetos = "projetos/projetos.csv"
arq_saida = "projetos_instituicoes.csv"

instituicoes = pd.read_csv(arq_instituicoes, sep=';', encoding='utf-8')
projetos = pd.read_csv(arq_projetos, sep=';', encoding='utf-8')

combinado = pd.merge(
    projetos,
    instituicoes,
    left_on="Sigla",   
    right_on="Sigla",      
    how='inner',
    suffixes=("_projeto", "_instituicao")
)

combinado = combinado[
    [
        "Sigla", 
        "Nome_instituicao",
        "Nome_projeto", 
        "Responsável"
    ]
]

combinado = combinado.rename(columns={
    "Sigla": "Sigla da IES",
    "Nome_instituicao": "Instituição",
    "Nome_projeto": "Projeto"
})

combinado.to_csv(arq_saida, sep=';', index=False, encoding='utf-8')

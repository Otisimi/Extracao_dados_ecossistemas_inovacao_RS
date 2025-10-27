import pandas as pd

arq_instituicoes = "instituicoes/instituicoes.csv"
arq_publicacoes = "publicacoes/publicacoes.csv"
arq_saida = "publicacoes_instituicoes.csv"

instituicoes = pd.read_csv(arq_instituicoes, sep=';', encoding='utf-8')
publicacoes = pd.read_csv(arq_publicacoes, sep=';', encoding='utf-8')

combinado = pd.merge(
    publicacoes,
    instituicoes,
    left_on="Sigla",   
    right_on="Sigla",      
    how='inner',
    suffixes=("_publicacao", "_instituicao")
)

combinado = combinado[
    [
        "Sigla", 
        "Nome_instituicao",
        "Nome_publicacao", 
        "Tipo Produção",
        "Autores"
    ]
]

combinado = combinado.rename(columns={
    "Sigla": "Sigla da IES",
    "Nome_instituicao": "Instituição",
    "Nome_publicacao": "Publicação",
    "Tipo Produção": "Tipo de produção"
})

combinado.to_csv(arq_saida, sep=';', index=False, encoding='utf-8')

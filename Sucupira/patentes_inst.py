import pandas as pd

# Caminhos dos arquivos
arq_instituicoes = "instituicoes/instituicoes.csv"
arq_patentes = "patentes/patentes.csv"
arq_saida = "patentes_instituicoes.csv"

# Lê os dois arquivos CSV
instituicoes = pd.read_csv(arq_instituicoes, sep=';', encoding='utf-8')
patentes = pd.read_csv(arq_patentes, sep=';', encoding='utf-8')

# Verifica os nomes das colunas (útil para confirmar correspondência)
print("Colunas instituições:", instituicoes.columns)
print("Colunas patentes:", patentes.columns)

# Faz o merge (junção) pela coluna 'siglaIes'
combinado = pd.merge(
    patentes,
    instituicoes,
    left_on="Sigla IES",   
    right_on="Sigla",      
    how='inner',
    suffixes=("_patente", "_instituicao")
)

combinado = combinado[
    [
        "Sigla", 
        "Nome_instituicao",
        "Nome_patente", 
        "Autores"
    ]
]

combinado = combinado.rename(columns={
    "Sigla": "Sigla da IES",
    "Nome_instituicao": "Instituição",
    "Nome_patente": "Patente"
})

# Salva o resultado em um novo CSV
combinado.to_csv(arq_saida, sep=';', index=False, encoding='utf-8')

print(f"Arquivo combinado gerado com sucesso: {arq_saida}")

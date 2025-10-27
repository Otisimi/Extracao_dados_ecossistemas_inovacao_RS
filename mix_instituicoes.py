import pandas as pd
import re
from difflib import SequenceMatcher
import json

# Função pra normalizar as strings
def norm(s):
    if pd.isna(s): 
        return ""
    s = str(s).lower() # Minúsculo
    s = re.sub(r'\s*-\s*.*$', '', s) # Remove tudo depois do primeiro hífen
    s = re.sub(r'[^\w\s]', '', s) # Remove acentos e caracteres especiais
    return s           

# Função que verifica se as strings são similares (ratio 95%)
def similar(a, b, nome_min=0.95):
    return SequenceMatcher(None, norm(a), norm(b)).ratio() >= nome_min

# Função principal pra junção dos arquivos
def merge_instituicoes(arq_json, arq_csv, arq_saida):
    # Le o json
    with open(arq_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df_json = pd.DataFrame(data)
    df_csv = pd.read_csv(arq_csv, sep=';', encoding='utf-8')
    df_csv.columns = df_csv.columns.str.strip()

    # Adiciona só a coluna de matriculas (dps de Sigla) no novo arquivo
    cols = df_csv.columns.tolist()
    sigla_idx = cols.index('Sigla')
    cols.insert(sigla_idx + 1, 'Matriculas')
    
    # Reordena com a nova coluna
    df_csv['Matriculas'] = None
    df_csv = df_csv[cols]

    resultado = []

    # Loop no CSV
    for idx, r_csv in df_csv.iterrows():
        # Vê se tem um registro parecido no json
        match = next(
            (i for i, r_json in df_json.iterrows() 
             if similar(r_json['Instiuição'], r_csv['Nome'])),
            None
        )

        # Se tem, salva a quantidade de matriculas no novo arquivo
        if match is not None:
            r_json = df_json.loc[match]
            # Str só pra tirar o decimal
            r_csv['Matriculas'] = str(r_json.get('QtIngresso', None))
        
        
        resultado.append(r_csv.to_dict())

    pd.DataFrame(resultado).to_csv(arq_saida, sep=';', index=False, encoding='utf-8')

if __name__ == "__main__":
    merge_instituicoes(
        'INEP_Bi/json_matriculas.json',
        'observatorio/instituicoes/instituicoes.csv',
        'instituicoes_merged.csv'
    )
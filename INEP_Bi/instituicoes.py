import requests
import json

url = "https://wabi-brazil-south-api.analysis.windows.net/public/reports/querydata?synchronous=true"

headers = {
    "ActivityId": "10050467-b51c-4be2-9a4e-96dc00cef203",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://app.powerbi.com",
    "Referer": "https://app.powerbi.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-PowerBI-ResourceKey": "0bb2cb50-9658-4f53-868e-203c3ba09b9b"
}

def montar_json(restart_token=None, datavolume=5000):
    # Separa o data_reduction
    data_reduction = {
        "DataVolume": datavolume,
        "Primary": {"Window": {}}
    }
    # Seta o restar token para as próximas buscas
    if restart_token:
        data_reduction["Primary"]["Window"]["RestartTokens"] = restart_token

    return {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [
                                        {"Name": "i", "Entity": "DIM_NOME_IES", "Type": 0}
                                    ],
                                    "Select": [
                                        {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "i"}},
                                                "Property": "NO_IES"
                                            },
                                            "Name": "IES.NO_IES"
                                        }
                                    ]
                                },
                                "Binding": {
                                    "Primary": {"Groupings": [{"Projections": [0]}]},
                                    "DataReduction": data_reduction, # Coloca o DR com o restart novo
                                    "Version": 1
                                }
                            }
                        }
                    ]
                }
            }
        ],
        "cancelQueries": [],
        "modelId": 6380715
    }

def get_instituicoes():
    all_rows = []
    restart_token = None

    while True:
        # Monta o json com o restart token da vez
        payload = montar_json(restart_token=restart_token, datavolume=5000)
        resp = requests.post(url, headers=headers, json=payload)
        data = resp.json()

        # Busca os valores dentro do json
        rows = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
        # Pega os nomes das instituicoes e guarda no vetor
        all_rows.extend([r["G0"] for r in rows if "G0" in r])

        # Pega o novo restart token
        ds_obj = data["results"][0]["result"]["data"]["dsr"]["DS"][0]
        restart_token = ds_obj.get("RT")

        # Não tem entao acabou
        if not restart_token:
            break 

    return all_rows

instituicoes = get_instituicoes()

# Grava no arquivo
with open("json_instituicoes.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(instituicoes, ensure_ascii=False, indent=2))

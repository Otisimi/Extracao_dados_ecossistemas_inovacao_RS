import requests
import json
import csv
import os

url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "ActivityId": "81eeca96-3fce-4691-9fa6-a49e7f039954",
    "X-PowerBI-ResourceKey": "dabce6b5-0a57-4827-bfdf-39f731e5ee5d",
    "Origin": "https://app.powerbi.com",
    "Referer": "https://app.powerbi.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

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

def montar_json(eco):
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
                                        {"Name": "s", "Entity": "Startups", "Type": 0}
                                    ],
                                    "Select": [
                                        {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "s"}},
                                                "Property": "Startup"
                                            },
                                            "Name": "Startups.Startup"
                                        }
                                    ],
                                    "Where": [
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {"SourceRef": {"Source": "s"}},
                                                                "Property": "Ecossistema Regional de Inovação"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [{"Literal": {"Value": f"'{eco}'"}}]
                                                    ]
                                                }
                                            }
                                        }
                                    ]
                                },
                                "Binding": {
                                    "Primary": {"Groupings": [{"Projections": [0]}]},
                                    "IncludeEmptyGroups": True,
                                    "Version": 1
                                },
                                "ExecutionMetricsKind": 1
                            }
                        }
                    ]
                },
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "9cddff5b-a4d3-4c98-8788-aaaaddf2e780",
                    "Sources": [
                        {
                            "ReportId": "32183f8c-af1e-4fe8-8c98-9b2602aa1dfa",
                            "VisualId": "397ee2644d79c08406d0"
                        }
                    ]
                }
            }
        ],
        "cancelQueries": [],
        "modelId": 3574567
    }


with open('nomes_startups.csv', "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Ecossistema", "Startup"])

    for eco in ecossistemas:
        payload = montar_json(eco)
        resp = requests.post(url, headers=headers, json=payload)

        data = resp.json()

        registros = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
        nomes = [r["G0"] for r in registros if "G0" in r]
            
        folder = "jsons_startups/nomes"
        os.makedirs(folder, exist_ok=True)
            
        file_name = eco.replace(" ", "_").replace("ã", "a").replace("ç", "c").replace("õ", "o").replace("ú", "u").replace("í", "i")
            
        complete_path = os.path.join(folder, file_name + ".csv")
        for nome in nomes:
            w.writerow([eco, nome])

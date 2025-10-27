import requests
import json
import re
import os

url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "ActivityId": "b93b3151-b6df-46dd-8e9f-50a160310ad1",
    "Connection": "keep-alive",
    "Content-Length": "2987",
    "Content-Type": "application/json;charset=UTF-8",
    "Host": "wabi-brazil-south-b-primary-api.analysis.windows.net",
    "Origin": "https//app.powerbi.com",
    "Referer": "https//app.powerbi.com/",
    "RequestId": "94c40d2c-2723-7ca5-2134-396c93e9d955",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "X-PowerBI-ResourceKey": "378eee44-bfb1-4892-bc8c-db3634c9ffce",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

ecossistemas = [
    "Central",
    "Campanha e Fronteira Oeste",
    "Metropolitana e Litoral Norte",
    "Noroeste e Missões",
    "Produção e Norte",
    "Serra Gaúcha",
    "Sul",
    "Vales"
]

# Método pra substituir os char especial dos nomes dos ecossistemas
def repl(match):
    data = {"ã": "a", "ú": "u", "õ": "o", "ç": "c"}
    return data.get(match.group(0))

def get_aceleradoras_by_eco(url, headers, ecossistemas):
    for eco in ecossistemas:
        json_model = {
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
                            { "Name": "a", "Entity": "AMBIENTES - Tabela", "Type": 0 },
                            { "Name": "m", "Entity": "GERAL - Municípios", "Type": 0 }
                            ],
                            "Select": [
                            {
                                "Column": {
                                "Expression": { "SourceRef": { "Source": "a" } },
                                "Property": "Latitude"
                                },
                                "Name": "Min(AMBIENTES - Tabela.Latitude)",
                                "NativeReferenceName": "Latitude"
                            },
                            {
                                "Column": {
                                "Expression": { "SourceRef": { "Source": "a" } },
                                "Property": "Longitude"
                                },
                                "Name": "Min(AMBIENTES - Tabela.Longitude)",
                                "NativeReferenceName": "Longitude"
                            },
                            {
                                "Column": {
                                "Expression": { "SourceRef": { "Source": "a" } },
                                "Property": "Tipo de Ambiente"
                                },
                                "Name": "AMBIENTES - Tabela.Tipo de Ambiente",
                                "NativeReferenceName": "Tipo de Ambiente"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "Sigla/Nome Fantasia"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.Sigla/Nome Fantasia)",
                                "NativeReferenceName": "Primeiro Sigla/Nome Fantasia"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "Nome Completo"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.Nome Completo)",
                                "NativeReferenceName": "Primeiro Nome Completo"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "Site"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.Site)",
                                "NativeReferenceName": "Primeiro Site"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "E-mail"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.E-mail)",
                                "NativeReferenceName": "Primeiro E-mail"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "Áreas de Atuação"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.Áreas de Atuação)",
                                "NativeReferenceName": "Primeiro Áreas de Atuação"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "Município"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.Município)",
                                "NativeReferenceName": "Primeiro Município"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "ERI"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.ERI)",
                                "NativeReferenceName": "Primeiro ERI"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": { "SourceRef": { "Source": "a" } },
                                    "Property": "Telefone"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(AMBIENTES - Tabela.Telefone)",
                                "NativeReferenceName": "Primeiro Telefone"
                            }
                            ],
                            "Where": [
                            {
                                "Condition": {
                                "In": {
                                    "Expressions": [
                                    {
                                        "Column": {
                                        "Expression": { "SourceRef": { "Source": "a" } },
                                        "Property": "ERI"
                                        }
                                    },
                                    {
                                        "Column": {
                                        "Expression": { "SourceRef": { "Source": "a" } },
                                        "Property": "Tipo de Ambiente"
                                        }
                                    }
                                    ],
                                    "Values": [
                                    [
                                        {
                                        "Literal": { "Value": f"'{eco}'" }
                                        },
                                        { "Literal": { "Value": "'Aceleradora'" } }
                                    ]
                                    ]
                                }
                                }
                            },
                            {
                                "Condition": {
                                "Not": {
                                    "Expression": {
                                    "In": {
                                        "Expressions": [
                                        {
                                            "Column": {
                                            "Expression": {
                                                "SourceRef": { "Source": "m" }
                                            },
                                            "Property": "ERI"
                                            }
                                        }
                                        ],
                                        "Values": [[{ "Literal": { "Value": "null" } }]]
                                    }
                                    }
                                }
                                }
                            },
                            {
                                "Condition": {
                                "In": {
                                    "Expressions": [
                                    {
                                        "Column": {
                                        "Expression": { "SourceRef": { "Source": "a" } },
                                        "Property": "Tipo de Ambiente"
                                        }
                                    }
                                    ],
                                    "Values": [
                                    [{ "Literal": { "Value": "'Aceleradora'" } }]
                                    ]
                                }
                                }
                            }
                            ]
                        },
                        "Binding": {
                            "Primary": {
                            "Groupings": [
                                { "Projections": [2] },
                                { "Projections": [0, 1, 3, 4, 5, 6, 7, 8, 9, 10] }
                            ]
                            },
                            "DataReduction": {
                            "DataVolume": 6,
                            "Primary": {
                                "OverlappingPointsSample": {
                                "X": { "Index": 1 },
                                "Y": { "Index": 0 }
                                }
                            }
                            },
                            "SuppressedJoinPredicates": [3, 4, 5, 6, 7, 8, 9, 10],
                            "Version": 1
                        },
                        "ExecutionMetricsKind": 1
                        }
                    }
                    ]
                },
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "43ae77f6-e15b-4975-aba8-121f809c8513",
                    "Sources": [
                    {
                        "ReportId": "9ef11196-4f9b-4929-b1e9-25c7afdacbfe",
                        "VisualId": "4c169f0d1b808e0ba264"
                    }
                    ]
                }
                }
            ],
            "cancelQueries": [],
            "modelId": 2466596
            }

        # Faz request e passa pra UTF-8
        req = requests.post(url, headers=headers, json=json_model)
        req.encoding = req.apparent_encoding
        
        # Colocar pra salvar o arquivo na pasta própria
        folder = "jsons_aceleradoras"
        os.makedirs(folder, exist_ok=True)
        
        # Nome do arquivo é o nome do ecossistema
        file_name = eco.replace(" ", "_").replace("ã", "a").replace("ç", "c").replace("õ", "o").replace("ú", "u").replace("í", "i")
        
        complete_path = os.path.join(folder, file_name + ".json")
        
        with open(complete_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(req.json(), ensure_ascii=False, indent=2))

get_aceleradoras_by_eco(url, headers, ecossistemas)
            
            
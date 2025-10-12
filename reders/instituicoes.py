import requests
import json
import re
import os

url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"

headers = {
    "ActivityId": "04b65c5e-5d6b-4b4c-b458-15063b35ba09",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://app.powerbi.com",
    "Referer": "https://app.powerbi.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-PowerBI-ResourceKey": "dabce6b5-0a57-4827-bfdf-39f731e5ee5d"
}

ecossistemas = [
    "Central",
    "Campanha e Fronteira Oeste",
    "Metropolitana e Litoral Norte",
    "Noroeste e Missões",
    "Produção e Norte",
    "Serra Gaúcha",
    "Sul",
    "Região dos Vales"
]

def get_instituicoes_by_eco(url, headers, ecossistemas):
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
                            {
                                "Name": "p",
                                "Entity": "Ambientes",
                                "Type": 0
                            }
                            ],
                            "Select": [
                            {
                                "Column": {
                                "Expression": {
                                    "SourceRef": {
                                    "Source": "p"
                                    }
                                },
                                "Property": "Cidade"
                                },
                                "Name": "Planilha1.Cidade",
                                "NativeReferenceName": "Cidade"
                            },
                            {
                                "Column": {
                                "Expression": {
                                    "SourceRef": {
                                    "Source": "p"
                                    }
                                },
                                "Property": "Link"
                                },
                                "Name": "Planilha1.Site",
                                "NativeReferenceName": "Link"
                            },
                            {
                                "Column": {
                                "Expression": {
                                    "SourceRef": {
                                    "Source": "p"
                                    }
                                },
                                "Property": "Ambiente de Inovação"
                                },
                                "Name": "Ambientes.Ambiente de Inovação",
                                "NativeReferenceName": "Ambiente de Inovação"
                            }
                            ],
                            "Where": [
                            {
                                "Condition": {
                                "In": {
                                    "Expressions": [
                                    {
                                        "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                            "Source": "p"
                                            }
                                        },
                                        "Property": "Tipo de Ambiente"
                                        }
                                    }
                                    ],
                                    "Values": [
                                    [
                                        {
                                        "Literal": {
                                            "Value": "'ICTs'"
                                        }
                                        }
                                    ]
                                    ]
                                }
                                }
                            },
                            {
                                "Condition": {
                                "In": {
                                    "Expressions": [
                                    {
                                        "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                            "Source": "p"
                                            }
                                        },
                                        "Property": "Ecossistema Regional de Inovação"
                                        }
                                    }
                                    ],
                                    "Values": [
                                    [
                                        {
                                        "Literal": {
                                            "Value": F"'{eco}'"
                                        }
                                        }
                                    ]
                                    ]
                                }
                                }
                            }
                            ],
                            "OrderBy": [
                            {
                                "Direction": 1,
                                "Expression": {
                                "Column": {
                                    "Expression": {
                                    "SourceRef": {
                                        "Source": "p"
                                    }
                                    },
                                    "Property": "Ambiente de Inovação"
                                }
                                }
                            }
                            ]
                        },
                        "Binding": {
                            "Primary": {
                            "Groupings": [
                                {
                                "Projections": [0, 1, 2],
                                "Subtotal": 1
                                }
                            ]
                            },
                            "DataReduction": {
                            "DataVolume": 3,
                            "Primary": {
                                "Window": {
                                "Count": 500
                                }
                            }
                            },
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
                        "VisualId": "7acb0ea4c0103040e496"
                    }
                    ]
                }
                }
            ],
            "cancelQueries": [],
            "modelId": 3574567
            }

        # Faz request e passa pra UTF-8
        req = requests.post(url, headers=headers, json=json_model)
        req.encoding = req.apparent_encoding
        
        # Colocar pra salvar o arquivo na pasta própria
        folder = "jsons_instituicoes"
        os.makedirs(folder, exist_ok=True)
        # Nome do arquivo é o nome do ecossistema
        file_name = eco.replace(" ", "_").replace("ã", "a").replace("ç", "c").replace("õ", "o").replace("ú", "u").replace("í", "i")
        
        complete_path = os.path.join(folder, file_name + ".json")
        
        with open(complete_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(req.json(), ensure_ascii=False, indent=2))

get_instituicoes_by_eco(url, headers, ecossistemas)
            
            
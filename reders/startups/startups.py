import requests
import json
import csv
import os

folder = 'jsons_startups/nomes'

# nomes dos ecossistemas
ecos = [
    "Central",
    "Fronteira_Oeste_e_Campanha",
    "Metropolitana_e_Litoral_Norte",
    "Noroeste_e_Missoes",
    "Producao_e_Norte",
    "Serra_Gaucha",
    "Sul",
    "Vales"
]

url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "ActivityId": "04b65c5e-5d6b-4b4c-b458-15063b35ba09",
    "X-PowerBI-ResourceKey": "dabce6b5-0a57-4827-bfdf-39f731e5ee5d",
    "Origin": "https://app.powerbi.com",
    "Referer": "https://app.powerbi.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def monta_json(name_start, eco):
    safe_name = name_start.replace("'", "''")
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
                        {
                            "Name": "s",
                            "Entity": "Startups",
                            "Type": 0
                        }
                        ],
                        "Select": [
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Cidade"
                            },
                            "Name": "Startups.Cidade",
                            "NativeReferenceName": "Cidade"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Link"
                            },
                            "Name": "Startups.Link",
                            "NativeReferenceName": "Link"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Estágio de Maturidade"
                            },
                            "Name": "Startups.Estágio de Maturidade",
                            "NativeReferenceName": "Estágio de Maturidade"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Modelo de Negócio"
                            },
                            "Name": "Startups.Modelo de Negócio",
                            "NativeReferenceName": "Modelo de Negócio"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Segmento"
                            },
                            "Name": "Startups.Segmento",
                            "NativeReferenceName": "Segmento"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Vertical"
                            },
                            "Name": "Startups.Vertical",
                            "NativeReferenceName": "Vertical"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Público-alvo"
                            },
                            "Name": "Startups.Público-alvo",
                            "NativeReferenceName": "Público-alvo"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Startup"
                            },
                            "Name": "Startups.Startup",
                            "NativeReferenceName": "Startup"
                        },
                        {
                            "Column": {
                            "Expression": {
                                "SourceRef": {
                                "Source": "s"
                                }
                            },
                            "Property": "Ambiente de Inovação"
                            },
                            "Name": "Startups.Ambiente de Inovação",
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
                                        "Source": "s"
                                        }
                                    },
                                    "Property": "Startup"
                                    }
                                }
                                ],
                                "Values": [
                                    [{"Literal": {"Value": f"'{safe_name}'"}}]
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
                                        "Source": "s"
                                        }
                                    },
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
                        ],
                        "OrderBy": [
                        {
                            "Direction": 1,
                            "Expression": {
                            "Column": {
                                "Expression": {
                                "SourceRef": {
                                    "Source": "s"
                                }
                                },
                                "Property": "Startup"
                            }
                            }
                        }
                        ]
                    },
                    "Binding": {
                        "Primary": {
                        "Groupings": [
                            {
                            "Projections": [0, 1, 2, 3, 4, 5, 6, 7, 8],
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
                    "VisualId": "65b3db00870d89a99773"
                }
                ]
            }
            }
        ],
        "cancelQueries": [],
        "modelId": 3574567
        }

def busca_startups():
    all_rows =[]
    with open('nomes_startups.csv', 'r', encoding='utf-8') as f:
        leitor = csv.reader(f, delimiter=";")
        cabecalho = next(leitor)  # pula o cabeçalho
        
        for linha in leitor:
            
            ecossistema, startup = linha
            json_model = monta_json(startup, ecossistema)
            req = requests.post(url, headers=headers, json=json_model)
            
            data = req.json()
            ds = data["results"][0]["result"]["data"]["dsr"]["DS"][0]
            vd = ds.get("ValueDicts", {})

            # como é sempre 1 registro, pega direto os valores
            cidade  = vd.get("D0", [""])[0] if vd.get("D0") else ""
            link    = vd.get("D1", [""])[0] if vd.get("D1") else ""
            estagio = vd.get("D2", [""])[0] if vd.get("D2") else ""
            modelo  = vd.get("D3", [""])[0] if vd.get("D3") else ""
            segm    = vd.get("D4", [""])[0] if vd.get("D4") else ""
            vert    = vd.get("D5", [""])[0] if vd.get("D5") else ""
            publico = vd.get("D6", [""])[0] if vd.get("D6") else ""
            start   = vd.get("D7", [""])[0] if vd.get("D7") else startup
            amb     = vd.get("D8", [""])[0] if vd.get("D8") else ""

            all_rows.append([
                ecossistema, cidade, link, estagio, modelo,
                segm, vert, publico, start, amb
            ])  
    
    return all_rows
    
startups = busca_startups()
with open("startups.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow([
            "Ecossistema",
            "Cidade",
            "Link",
            "Estágio de Maturidade",
            "Modelo de Negócio",
            "Segmento",
            "Vertical",
            "Público-alvo",
            "Startup",
            "Ambiente de Inovação"
        ])
        w.writerows(startups)

# with open("startups.csv","w",newline="",encoding="utf-8") as f:
#     w = csv.writer(f, delimiter=";")
#     w.writerow(["Ecossistema","Cidade","Link","Estágio de Maturidade","Modelo de Negócio",
#                 "Segmento","Vertical","Público-alvo","Startup","Ambiente de Inovação"])
            
            
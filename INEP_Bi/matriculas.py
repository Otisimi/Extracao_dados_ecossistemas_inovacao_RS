import requests
import json
import re
import os

url = "https://wabi-brazil-south-api.analysis.windows.net/public/reports/querydata?synchronous=true"

headers = {
    "ActivityId": "10050467-b51c-4be2-9a4e-96dc00cef203",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://app.powerbi.com",
    "Referer": "https://app.powerbi.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-PowerBI-ResourceKey": "0bb2cb50-9658-4f53-868e-203c3ba09b9b"
}

def get_matriculas(url, headers):
    matriculados= []
    with open("json_instituicoes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for instituicao in data:
            safe_name = instituicao.replace("'", "''")
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
                                    "Name": "c",
                                    "Entity": "DIM_CALENDARIO",
                                    "Type": 0
                                },
                                {
                                    "Name": "b1",
                                    "Entity": "BI_CURSO",
                                    "Type": 0
                                },
                                {
                                    "Name": "d",
                                    "Entity": "DIM_CATEGORIA",
                                    "Type": 0
                                },
                                {
                                    "Name": "d1",
                                    "Entity": "DIM_NOME_IES",
                                    "Type": 0
                                },
                                {
                                    "Name": "d11",
                                    "Entity": "DIM_CINE_BRASIL",
                                    "Type": 0
                                },
                                {
                                    "Name": "p",
                                    "Entity": "PARA_TODOS",
                                    "Type": 0
                                }
                                ],
                                "Select": [
                                {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "c"
                                        }
                                    },
                                    "Property": "Ano"
                                    },
                                    "Name": "Consulta1.Ano"
                                },
                                {
                                    "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                            "Source": "b1"
                                            }
                                        },
                                        "Property": "QT_INGRESSO_TOTAL"
                                        }
                                    },
                                    "Function": 0
                                    },
                                    "Name": "Sum(BI_CURSO.QT_INGRESSO_TOTAL)"
                                },
                                {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "d"
                                        }
                                    },
                                    "Property": "Categoria Administrativa"
                                    },
                                    "Name": "DIM_CATEGORIA.Categoria Administrativa",
                                    "NativeReferenceName": "Categoria"
                                },
                                {
                                    "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                            "Source": "b1"
                                            }
                                        },
                                        "Property": "QT_INGRESSO_TOTAL"
                                        }
                                    },
                                    "Function": 0
                                    },
                                    "Name": "Sum(BI_CURSO.QT_INGRESSO_TOTAL)1"
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
                                                "Source": "d1"
                                                }
                                            },
                                            "Property": "NO_IES"
                                            }
                                        }
                                        ],
                                        "Values": [
                                        [
                                            {
                                            "Literal": {
                                                "Value": f"'{safe_name}'"
                                            }
                                            }
                                        ]
                                        ]
                                    }
                                    }
                                },
                                {
                                    "Condition": {
                                    "Comparison": {
                                        "ComparisonKind": 2,
                                        "Left": {
                                        "Column": {
                                            "Expression": {
                                            "SourceRef": {
                                                "Source": "c"
                                            }
                                            },
                                            "Property": "Ano"
                                        }
                                        },
                                        "Right": {
                                        "Literal": {
                                            "Value": "2023D"
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
                                            "Expression": {
                                                "SourceRef": {
                                                "Source": "d11"
                                                }
                                            },
                                            "Property": "NO_CINE_AREA_GERAL"
                                            }
                                        }
                                        ],
                                        "Values": [
                                        [
                                            {
                                            "Literal": {
                                                "Value": "'Computação e TIC'"
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
                                            "Property": "Insumos 2 todos Campos"
                                            }
                                        }
                                        ],
                                        "Values": [
                                        [
                                            {
                                            "Literal": {
                                                "Value": "'''DIM_CATEGORIA''[Categoria Administrativa]'"
                                            }
                                            }
                                        ]
                                        ]
                                    }
                                    }
                                }
                                ]
                            },
                            "Binding": {
                                "Primary": {
                                "Groupings": [
                                    {
                                    "Projections": [0, 1, 3]
                                    }
                                ]
                                },
                                "Secondary": {
                                "Groupings": [
                                    {
                                    "Projections": [2],
                                    "SuppressedProjections": [1]
                                    }
                                ]
                                },
                                "DataReduction": {
                                "DataVolume": 4,
                                "Primary": {
                                    "Sample": {}
                                },
                                "Secondary": {
                                    "Top": {}
                                }
                                },
                                "Version": 1
                            }
                            }
                        }
                        ]
                    },
                    "QueryId": ""
                    }
                ],
                "cancelQueries": [],
                "modelId": 6380715
                }

            # Faz request e passa pra UTF-8
            req = requests.post(url, headers=headers, json=json_model)
            req.encoding = req.apparent_encoding
            req_json = req.json()

            rows = req_json["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
                    
            # Pega o ano e o nro de matriculados
            for r in rows:
                if "C" in r:
                    ano, qt_ingresso = r["C"]
                    matriculados.append({"Instiuição": instituicao, "Ano": ano, "QtIngresso": qt_ingresso})
                    
    return matriculados

matrics = get_matriculas(url, headers)
        
with open("json_matriculas.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(matrics, ensure_ascii=False, indent=2))
            
            
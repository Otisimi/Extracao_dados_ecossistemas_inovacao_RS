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
    "Região dos Vales"
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
                            {
                                "Name": "a",
                                "Entity": "Aceleradoras",
                                "Type": 0
                            }
                            ],
                            "Select": [
                            {
                                "Column": {
                                "Expression": {
                                    "SourceRef": {
                                    "Source": "a"
                                    }
                                },
                                "Property": "latitude"
                                },
                                "Name": "Aceleradoras.latitude",
                                "NativeReferenceName": "latitude"
                            },
                            {
                                "Column": {
                                "Expression": {
                                    "SourceRef": {
                                    "Source": "a"
                                    }
                                },
                                "Property": "longitude"
                                },
                                "Name": "Aceleradoras.longitude",
                                "NativeReferenceName": "longitude"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "sigla/nome fantasia"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.sigla/nome fantasia)",
                                "NativeReferenceName": "Sigla"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "nome completo"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.nome completo)",
                                "NativeReferenceName": "Nome completo"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "Área de atuação"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.Área de atuação)",
                                "NativeReferenceName": "Área de atuação"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "endereco"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.endereco)",
                                "NativeReferenceName": "Endereço"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "cep"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.cep)",
                                "NativeReferenceName": "CEP"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "municipio"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.municipio)",
                                "NativeReferenceName": "Município"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "ERIs"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.ERIs)",
                                "NativeReferenceName": "ERI"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "telefone"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.telefone)",
                                "NativeReferenceName": "Telefone"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "email"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.email)",
                                "NativeReferenceName": "E-mail"
                            },
                            {
                                "Aggregation": {
                                "Expression": {
                                    "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                        "Source": "a"
                                        }
                                    },
                                    "Property": "site"
                                    }
                                },
                                "Function": 3
                                },
                                "Name": "Min(Aceleradoras.site)",
                                "NativeReferenceName": "Site"
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
                                            "Source": "a"
                                            }
                                        },
                                        "Property": "ERIs"
                                        }
                                    }
                                    ],
                                    "Values": [
                                    [
                                        {
                                        "Literal": {
                                            "Value": f"'{eco}'"
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
                                "Projections": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                                }
                            ]
                            },
                            "SuppressedJoinPredicates": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                            "Version": 1,
                            "DataReduction": {
                            "DataVolume": 4,
                            "Primary": {
                                "OverlappingPointsSample": {
                                "X": {
                                    "Index": 1
                                },
                                "Y": {
                                    "Index": 0
                                }
                                }
                            }
                            }
                        }
                        }
                    }
                    ]
                },
                "QueryId": ""
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
            
            
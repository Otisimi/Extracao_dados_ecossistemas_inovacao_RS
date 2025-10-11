import requests
import json
import re
import os

url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "ActivityId": "04b65c5e-5d6b-4b4c-b458-15063b35ba09",
    "X-PowerBI-ResourceKey": "dabce6b5-0a57-4827-bfdf-39f731e5ee5d",
    "Origin": "https://app.powerbi.com",
    "Referer": "https://app.powerbi.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
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

def get_startup_by_eco(url, headers, ecossistemas):
    for eco in ecossistemas:
        json_model = {
            "version":"1.0.0",
            "queries":[
                {
                    "Query":{
                        "Commands":[
                        {
                            "SemanticQueryDataShapeCommand":{
                                "Query":{
                                    "Version":2,
                                    "From":[
                                    {
                                        "Name":"s",
                                        "Entity":"Startups",
                                        "Type":0
                                    }
                                    ],
                                    "Select":[
                                    {
                                        "Column":{
                                            "Expression":{
                                                "SourceRef":{
                                                "Source":"s"
                                                }
                                            },
                                            "Property":"Cidade"
                                        },
                                        "Name":"Startups (2).Cidade",
                                        "NativeReferenceName":"Cidade"
                                    },
                                    {
                                        "Column":{
                                            "Expression":{
                                                "SourceRef":{
                                                "Source":"s"
                                                }
                                            },
                                            "Property":"Link"
                                        },
                                        "Name":"Startups (2).Link",
                                        "NativeReferenceName":"Link"
                                    },
                                    {
                                        "Column":{
                                            "Expression":{
                                                "SourceRef":{
                                                "Source":"s"
                                                }
                                            },
                                            "Property":"Startup"
                                        },
                                        "Name":"Startups.Startup",
                                        "NativeReferenceName":"Startup"
                                    }
                                    ],
                                    "Where":[
                                    {
                                        "Condition":{
                                            "In":{
                                                "Expressions":[
                                                {
                                                    "Column":{
                                                        "Expression":{"SourceRef":{"Source":"s"}},
                                                        "Property":"Ecossistema Regional de Inovação"
                                                    }
                                                }
                                                ],
                                                "Values":[
                                                [
                                                    {"Literal":{"Value":f"'{eco}'"}}
                                                ]
                                                ]
                                            }
                                        }
                                    }
                                    ],
                                    "OrderBy":[
                                    {
                                        "Direction":1,
                                        "Expression":{
                                            "Column":{
                                                "Expression":{
                                                "SourceRef":{
                                                    "Source":"s"
                                                }
                                                },
                                                "Property":"Startup"
                                            }
                                        }
                                    }
                                    ]
                                },
                                "Binding":{
                                    "Primary":{
                                    "Groupings":[
                                        {
                                            "Projections":[
                                                0,
                                                1,
                                                2
                                            ],
                                            "Subtotal":1
                                        }
                                    ]
                                    },
                                    "DataReduction":{
                                    "DataVolume":3,
                                    "Primary":{
                                        "Window":{
                                            "Count":5000
                                        }
                                    }
                                    },
                                    "Version":1
                                }
                            }
                        }
                        ]
                    },
                    "QueryId":""
                }
            ],
            "cancelQueries":[
            ],
            "modelId":3574567
        }

        req = requests.post(url, headers=headers, json=json_model)
        req.encoding = req.apparent_encoding
        
        folder = "jsons_startups"
        os.makedirs(folder, exist_ok=True)
        
        file_name = eco.replace(" ", "_").replace("ã", "a").replace("ç", "c").replace("õ", "o").replace("ú", "u").replace("í", "i")
        
        complete_path = os.path.join(folder, file_name + ".json")
        
        with open(complete_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(req.json(), ensure_ascii=False, indent=2))

get_startup_by_eco(url, headers, ecossistemas)
            
            
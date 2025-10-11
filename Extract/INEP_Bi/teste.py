import json

# Load the JSON file
with open("json_instituicoes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Print each name in a new line
for name in data:
    print(name)
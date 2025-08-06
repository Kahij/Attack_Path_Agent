import json

def load_vulnerabilities(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)

    def load_topology(file_path: str):
        with open(file_path, 'r') as f:
            return json.load(f)

    def load_asset_criticality(file_path: str):
        with open(file_path, 'r') as f:
            return json.load(f)
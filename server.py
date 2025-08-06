from fastapi import FastAPI
from flask import Flask, jsonify
from src.utils.data_loader import load_vulnerabilities, load_topology, load_asset_criticality
from src.core.graph_builder import build_attack_graph
from src.core.path_finder import find_paths

#app = FastAPI()
app = Flask(__name__)

@app.get("/")
def root():
    return {"status": "Attack Path Agent is running"}

@app.route('/analyze', methods=['GET'])
def analyze():
    vulns = load_vulnerabilities('data/vulnerabilities.json')
    topology = load_topology('data/topology.json')
    assets = load_asset_criticality('data/assets.json')

    graph = build_attack_graph(vulns, topology, assets)
    entry_points = ["external_node"]  # example
    critical_assets = [a['id'] for a in assets if a['criticality'] >= 8]

    results = find_paths(graph, entry_points, critical_assets)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
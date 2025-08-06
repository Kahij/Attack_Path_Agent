import networkx as nx
from .risk_calculator import calculate_path_risk

def find_paths(graph, entry_points, critical_assets):
    results = []

    for entry in entry_points:
        for target in critical_assets:
            try:
                path = nx.shortest_path(graph, source=entry, target=target, weight='weight')
                risk = calculate_path_risk(graph, path)
                results.append({"path": path, "risk": risk})
            except nx.NetworkXNoPath:
                continue

    return sorted(results, key=lambda x: x['risk'], reverse=True)
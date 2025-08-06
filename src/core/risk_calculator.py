def calculate_path_risk(graph, path):
    total = 0
    for node in path:
        if graph.nodes[node].get("type") == "vulnerability":
            cvss = graph.nodes[node].get("cvss", 0)
            exploitability = graph.nodes[node].get("exploitability", 0)
            total += cvss * exploitability

    path_len = len(path)
    asset_node = path[-1]
    criticality = graph.nodes[asset_node].get("criticality", 1)

    risk = (total / path_len) * criticality
    return risk
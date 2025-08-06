import networkx as nx

def calculate_path_risk(G, path):
    total_score = 0
    for node in path:
        data = G.nodes[node]
        cvss = data.get("cvss", 0)
        exploitability = data.get("exploitability", 0.5)
        criticality = data.get("criticality", 1)
        total_score += cvss * exploitability * criticality

    # Normalize by path length
    return round(total_score / len(path), 2) if path else 0


def rank_attack_paths(G):
    ranked = []
    nodes = list(G.nodes)
    for src in nodes:
        for dst in nodes:
            if src != dst and nx.has_path(G, src, dst):
                path = nx.shortest_path(G, source=src, target=dst, weight='weight')
                score = calculate_path_risk(G, path)
                ranked.append({
                    "path": path,
                    "score": score
                })
    return sorted(ranked, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    from data_generator import generate_mock_vulnerabilities, build_attack_graph

    vulns = generate_mock_vulnerabilities(10)
    G = build_attack_graph(vulns)
    results = rank_attack_paths(G)
    for r in results[:5]:
        print(f"Path: {r['path']}, Score: {r['score']}")

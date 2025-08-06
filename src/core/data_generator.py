import random
import networkx as nx
import pandas as pd

# Simulate mock vulnerabilities
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]


def generate_mock_vulnerabilities(n=10):
    vulnerabilities = []
    for i in range(n):
        vuln = {
            "id": f"VULN{i+1}",
            "cvss": round(random.uniform(3.0, 10.0), 1),
            "exploitability": round(random.uniform(0.2, 1.0), 2),
            "risk": random.choice(RISK_LEVELS),
            "asset": f"Asset{random.randint(1, 5)}",
            "criticality": random.randint(1, 5)
        }
        vulnerabilities.append(vuln)
    return vulnerabilities


def build_attack_graph(vulnerabilities):
    G = nx.DiGraph()
    for v in vulnerabilities:
        G.add_node(v["id"], **v)

    for i in range(len(vulnerabilities) - 1):
        src = vulnerabilities[i]["id"]
        dst = vulnerabilities[i + 1]["id"]
        weight = 10 - vulnerabilities[i + 1]["cvss"]
        G.add_edge(src, dst, weight=round(weight, 2))

    return G


def export_graph_as_edge_list(G):
    edges = []
    for u, v, d in G.edges(data=True):
        edges.append({"source": u, "target": v, **d})
    return pd.DataFrame(edges)


if __name__ == "__main__":
    vulns = generate_mock_vulnerabilities(10)
    G = build_attack_graph(vulns)
    df_edges = export_graph_as_edge_list(G)
    print(df_edges.head())

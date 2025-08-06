import networkx as nx

def build_attack_graph(vulns, topology, assets):
    G = nx.DiGraph()

    for asset in assets:
        G.add_node(asset['id'], type='asset', criticality=asset['criticality'])

    for vuln in vulns:
        G.add_node(vuln['id'], type='vulnerability', cvss=vuln['cvss'],
                   exploitability=vuln['exploitability'], asset=vuln['asset'])

    for connection in topology:
        G.add_edge(connection['source'], connection['target'], type='network', weight=1.0)

    for vuln in vulns:
        G.add_edge(vuln['id'], vuln['asset'], type='exploit',
                   weight=1.0 - vuln['exploitability'])

    return G
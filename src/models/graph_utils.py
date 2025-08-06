import torch
from torch_geometric.data import Data
import networkx as nx
import numpy as np


FEATURE_KEYS = ["cvss", "exploitability", "criticality"]


def nx_to_pyg_data(G: nx.Graph, label_map=None):
    node_list = list(G.nodes)
    node_indices = {node: i for i, node in enumerate(node_list)}

    x = []
    for node in node_list:
        feats = [G.nodes[node].get(k, 0.0) for k in FEATURE_KEYS]
        x.append(feats)
    x = torch.tensor(x, dtype=torch.float)

    edge_index = []
    for src, dst in G.edges:
        edge_index.append([node_indices[src], node_indices[dst]])
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

    y = torch.zeros(len(node_list), dtype=torch.float)
    if label_map:
        for node, label in label_map.items():
            y[node_indices[node]] = label

    return Data(x=x, edge_index=edge_index, y=y, num_nodes=len(node_list))

import sys
import os 
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from gnn_model import AttackPathGNN
from graph_utils import nx_to_pyg_data
from core.data_generator import generate_mock_vulnerabilities, build_attack_graph


def create_labels(G):
    # Label: risk score as target (for regression)
    from core.rule_based_model import calculate_path_risk
    label_map = {}
    nodes = list(G.nodes)
    for node in nodes:
        path = [node]
        label_map[node] = calculate_path_risk(G, path)
    return label_map


def train():
    # Generate graph + labels
    vulns = generate_mock_vulnerabilities(20)
    G = build_attack_graph(vulns)
    label_map = create_labels(G)
    data = nx_to_pyg_data(G, label_map)

    model = AttackPathGNN(input_dim=data.num_features)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    model.train()
    for epoch in range(100):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index).squeeze()
        loss = F.mse_loss(out, data.y)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch:03d} | Loss: {loss:.4f}")

    print("\nSample predictions:")
    for i, pred in enumerate(out[:5]):
        print(f"Node {i}: Predicted Risk = {pred:.2f}, True = {data.y[i]:.2f}")


if __name__ == "__main__":
    train()

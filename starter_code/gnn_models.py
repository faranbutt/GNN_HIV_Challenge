#working/Molecular Graph/starter_code/gnn_models.py
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, GINConv, global_mean_pool, BatchNorm
class BaselineGCN(nn.Module):
    def __init__(self, in_feats=9, hidden=64):
        super().__init__()
        self.conv1 = GCNConv(in_feats, hidden)
        self.bn1 = BatchNorm(hidden)
        self.conv2 = GCNConv(hidden, hidden)
        self.bn2 = BatchNorm(hidden)
        self.fc = nn.Linear(hidden, 1)

    def forward(self, data):
        x, edge_index, batch = data.x.float(), data.edge_index, data.batch
        x = F.relu(self.bn1(self.conv1(x, edge_index)))
        x = F.relu(self.bn2(self.conv2(x, edge_index)))
        x = global_mean_pool(x, batch)
        return self.fc(x).squeeze(-1)

class GATGNN(nn.Module):
    def __init__(self, in_feats=9, hidden=32, heads=4):
        super().__init__()
        self.conv1 = GATConv(in_feats, hidden, heads=heads)
        self.conv2 = GATConv(hidden*heads, hidden, heads=1)
        self.fc = nn.Linear(hidden, 1)

    def forward(self, data):
        x, edge_index, batch = data.x.float(), data.edge_index, data.batch
        x = F.elu(self.conv1(x, edge_index))
        x = F.elu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        return self.fc(x).squeeze(-1)

class GINGNN(nn.Module):
    def __init__(self, in_feats=9, hidden=32):
        super().__init__()
        nn1 = nn.Sequential(nn.Linear(in_feats, hidden), nn.ReLU(), nn.Linear(hidden, hidden))
        self.conv1 = GINConv(nn1)
        nn2 = nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, hidden))
        self.conv2 = GINConv(nn2)
        self.fc = nn.Linear(hidden, 1)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        return self.fc(x).squeeze(-1)

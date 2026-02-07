# working/GNN-HIV-Challenge-2/starter_code/data_loader.py
import torch
import torch_geometric
from ogb.graphproppred import PygGraphPropPredDataset
from torch_geometric.loader import DataLoader

torch.serialization.add_safe_globals([
    torch_geometric.data.data.DataEdgeAttr, 
    torch_geometric.data.data.DataTensorAttr,
    torch_geometric.data.data.Data,
    torch_geometric.data.storage.GlobalStorage,
    torch_geometric.data.dataset.IndexType
])

def get_dataloaders(batch_size=32):
    dataset = PygGraphPropPredDataset(name='ogbg-molhiv', root='datasets/')
    split_idx = dataset.get_idx_split()

    train_loader = DataLoader(dataset[split_idx["train"]], batch_size=batch_size, shuffle=True)
    valid_loader = DataLoader(dataset[split_idx["valid"]], batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(dataset[split_idx["test"]], batch_size=batch_size, shuffle=False)
    
    return train_loader, valid_loader, test_loader
# working/GNN-HIV-Challenge-2/starter_code/train.py
import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from tqdm import tqdm
from ogb.graphproppred import Evaluator

from data_loader import get_dataloaders
from gnn_models import BaselineGCN, GATGNN, GINGNN

def train(model, device, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for step, batch in enumerate(tqdm(loader, desc="Iteration")):
        batch = batch.to(device)
        
        if batch.x.shape[0] == 1 or batch.batch[-1] == 0:
            pass 
        else:
            optimizer.zero_grad()
            pred = model(batch)
            y = batch.y.to(torch.float).view(pred.shape)
            
            is_labeled = y == y
            loss = criterion(pred[is_labeled], y[is_labeled])
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
    return total_loss / len(loader)

def evaluate(model, device, loader, evaluator):
    model.eval()
    y_true = []
    y_score = []

    with torch.no_grad():
        for step, batch in enumerate(loader):
            batch = batch.to(device)
            if batch.x.shape[0] == 1:
                pass
            else:
                pred = model(batch)
                y_true.append(batch.y.view(pred.shape).detach().cpu())
                y_score.append(pred.detach().cpu())

    y_true = torch.cat(y_true, dim=0).numpy()
    y_score = torch.cat(y_score, dim=0).numpy()
    
    input_dict = {
        "y_true": y_true.reshape(-1, 1), 
        "y_pred": y_score.reshape(-1, 1)
    }
    return evaluator.eval(input_dict)


def main():
    parser = argparse.ArgumentParser(description='GNN Training for OGB-HIV')
    parser.add_argument('--model', type=str, default='gcn', choices=['gcn', 'gat', 'gin'])
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--lr', type=float, default=0.001)
    parser.add_argument('--device', type=int, default=0)
    args = parser.parse_args()

    device = torch.device(f"cuda:{args.device}" if torch.cuda.is_available() else "cpu")
    train_loader, valid_loader, test_loader = get_dataloaders(args.batch_size)

    if args.model == 'gcn':
        model = BaselineGCN(in_feats=9, hidden=64).to(device)
    elif args.model == 'gat':
        model = GATGNN(in_feats=9, hidden=64).to(device)
    else:
        model = GINGNN(in_feats=9, hidden=64).to(device)

    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([20.0]).to(device))
    evaluator = Evaluator(name='ogbg-molhiv')

    best_valid_auc = 0
    os.makedirs('models', exist_ok=True)
    os.makedirs('submissions', exist_ok=True)

    print(f"Starting training for {args.epochs} epochs...")

    for epoch in range(1, args.epochs + 1):
        loss = train(model, device, train_loader, optimizer, criterion)
        
        train_perf = evaluate(model, device, train_loader, evaluator)
        valid_perf = evaluate(model, device, valid_loader, evaluator)
        
        print(f'Epoch: {epoch:02d}, Loss: {loss:.4f}, Train: {train_perf["rocauc"]:.4f}, Valid: {valid_perf["rocauc"]:.4f}')
        if valid_perf["rocauc"] > best_valid_auc:
            best_valid_auc = valid_perf["rocauc"]
            checkpoint_path = f'models/best_{args.model}_model.pth'
            torch.save(model.state_dict(), checkpoint_path)
            print(f"✨ New best model saved to {checkpoint_path}")

    print("\nTraining Finished. Generating test submission...")
    model.load_state_dict(torch.load(f'models/best_{args.model}_model.pth'))
    test_perf = evaluate(model, device, test_loader, evaluator)
    print(f"Final Test ROC-AUC: {test_perf['rocauc']:.4f}")

    model.eval()
    records = []
    with torch.no_grad():
        for batch in test_loader:
            batch = batch.to(device)
            probs = torch.sigmoid(model(batch))
            for p in probs.cpu().numpy():
                records.append(float(p))

    sub_df = pd.DataFrame({'probability': records})
    sub_df.index.name = 'graph_id'
    sub_df.to_csv(f'submissions/ogb_submission_{args.model}.csv')

if __name__ == "__main__":
    main()
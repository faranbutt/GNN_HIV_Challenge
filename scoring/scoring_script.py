# working/GNN-HIV-Challenge-2/scoring/scoring_script.py
import pandas as pd
from ogb.graphproppred import Evaluator
import argparse
import json

def score_submission(submission_file):
    # The truth labels are inside the downloaded OGB folder
    dataset = pd.read_csv('datasets/ogbg_molhiv/mapping/mol.csv.gz')
    # OGB provides a specific utility to get test labels
    from ogb.graphproppred import PygGraphPropPredDataset
    ds = PygGraphPropPredDataset(name='ogbg-molhiv', root='datasets/')
    split_idx = ds.get_idx_split()
    y_true = ds.get_idx_split()['test'] # This is simplified; better to use:
    y_true = ds.data.y[split_idx['test']]

    sub_df = pd.read_csv(submission_file)
    y_pred = torch.tensor(sub_df['probability'].values).reshape(-1, 1)

    evaluator = Evaluator(name='ogbg-molhiv')
    input_dict = {"y_true": y_true, "y_pred": y_pred}
    result = evaluator.eval(input_dict)
    
    return result['rocauc'], len(y_true)
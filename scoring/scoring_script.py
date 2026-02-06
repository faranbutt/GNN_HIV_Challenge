# scoring/scoring_script.py
import pandas as pd
import argparse
import json
import torch
import os
import sys

# Import OGB Evaluator
try:
    from ogb.graphproppred import Evaluator
except ImportError:
    print(json.dumps({"error": "OGB library not found. Install with pip install ogb"}))
    sys.exit(1)

def score_submission(submission_file, label_file='data/test_labels.csv'):
    # 1. Check if files exist
    if not os.path.exists(label_file):
        raise FileNotFoundError(f"Ground truth file not found at {label_file}")
    
    # 2. Load Ground Truth
    # Expects columns: graph_id, target
    true_df = pd.read_csv(label_file)
    y_true = torch.tensor(true_df['target'].values, dtype=torch.float32).view(-1, 1)

    # 3. Load Submission
    # Expects columns: graph_id, probability
    sub_df = pd.read_csv(submission_file)
    
    # Ensure sorting matches (optional but safer)
    # Merging on graph_id ensures we compare the correct predictions
    merged_df = pd.merge(true_df, sub_df, on='graph_id', suffixes=('_true', '_pred'))
    
    if len(merged_df) == 0:
        raise ValueError("No matching graph_ids found between submission and ground truth.")

    y_true_sorted = torch.tensor(merged_df['target'].values, dtype=torch.float32).view(-1, 1)
    y_pred_sorted = torch.tensor(merged_df['probability'].values, dtype=torch.float32).view(-1, 1)

    # 4. Calculate Score using OGB Evaluator
    evaluator = Evaluator(name='ogbg-molhiv')
    input_dict = {"y_true": y_true_sorted, "y_pred": y_pred_sorted}
    result = evaluator.eval(input_dict)
    
    return result['rocauc']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('submission_file', type=str, help='Path to submission CSV')
    parser.add_argument('--json', action='store_true', help='Output score as JSON')
    args = parser.parse_args()

    try:
        # Run scoring
        roc_auc = score_submission(args.submission_file)
        
        # Print output
        if args.json:
            print(json.dumps({"roc_auc": roc_auc}))
        else:
            print(f"ROC-AUC: {roc_auc:.4f}")
            
    except Exception as e:
        # Catch errors and print as JSON so the workflow can see them
        error_msg = str(e)
        if args.json:
            print(json.dumps({"error": error_msg, "roc_auc": 0.0}))
        else:
            print(f"Error: {error_msg}")
        sys.exit(1)
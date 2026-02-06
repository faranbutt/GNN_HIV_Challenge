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

# Updated Section in scoring_script.py
def score_submission(submission_file):
    label_path = 'datasets/ogbg_molhiv/raw/graph-label.csv.gz'
    test_idx_path = 'datasets/ogbg_molhiv/split/scaffold/test.csv.gz'
    
    # 1. Load ALL labels (41,127)
    all_labels = pd.read_csv(label_path, header=None)
    
    # 2. Load the Test Indices (tells us which rows are the test set)
    test_idx = pd.read_csv(test_idx_path, header=None).values.flatten()
    
    # 3. Extract only the 4,113 test labels
    y_true_values = all_labels.iloc[test_idx].values
    y_true = torch.tensor(y_true_values, dtype=torch.float32).view(-1, 1)

    # 4. Load the user's submission file (THIS WAS MISSING)
    sub_df = pd.read_csv(submission_file)
    
    # Extract probabilities
    if 'probability' in sub_df.columns:
        y_pred = torch.tensor(sub_df['probability'].values, dtype=torch.float32).view(-1, 1)
    else:
        # Fallback to the second column if header is missing/different
        y_pred = torch.tensor(sub_df.iloc[:, 1].values, dtype=torch.float32).view(-1, 1)

    # 5. Alignment Check
    if len(y_true) != len(y_pred):
        raise ValueError(f"Size mismatch: Labels has {len(y_true)} rows, but submission has {len(y_pred)} rows.")

    # 6. Calculate Score using OGB Evaluator
    evaluator = Evaluator(name='ogbg-molhiv')
    input_dict = {"y_true": y_true, "y_pred": y_pred}
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
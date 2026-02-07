# scoring/scoring_script.py
import pandas as pd
import argparse
import json
import torch
import os
import sys
from ogb.graphproppred import Evaluator

def score_submission(submission_file):
    label_path = 'datasets/ogbg_molhiv/raw/graph-label.csv.gz'
    test_idx_path = 'datasets/ogbg_molhiv/split/scaffold/test.csv.gz'

    if not os.path.exists(submission_file):
        raise FileNotFoundError(f"Submission file not found: {submission_file}")

    all_labels = pd.read_csv(label_path, header=None)
    test_idx = pd.read_csv(test_idx_path, header=None).values.flatten()

    y_true = torch.tensor(all_labels.iloc[test_idx].values, dtype=torch.float32).view(-1, 1)

    sub_df = pd.read_csv(submission_file)

    if 'probability' in sub_df.columns:
        y_pred = torch.tensor(sub_df['probability'].values, dtype=torch.float32).view(-1, 1)
    else:
        y_pred = torch.tensor(sub_df.iloc[:, -1].values, dtype=torch.float32).view(-1, 1)

    if len(y_true) != len(y_pred):
        raise ValueError(f"Size mismatch: labels={len(y_true)} vs preds={len(y_pred)}")

    evaluator = Evaluator(name='ogbg-molhiv')
    result = evaluator.eval({"y_true": y_true, "y_pred": y_pred})

    roc_auc = float(result["rocauc"])

    if roc_auc <= 0:
        raise ValueError("ROC-AUC computed as zero. Invalid submission.")

    return roc_auc

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("submission_file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        score = score_submission(args.submission_file)
        print(json.dumps({"roc_auc": score}) if args.json else f"ROC-AUC: {score:.4f}")
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

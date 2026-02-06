#working/GNN-HIV-Challenge-2/starter_code/baseline.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import os


BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
train_path = os.path.join(BASE_DIR, 'train.csv')
test_path = os.path.join(BASE_DIR, 'test.csv')
train = pd.read_csv(train_path)
X = train.drop('target', axis=1)
y = train['target']
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict_proba(X_val)[:,1]
score = roc_auc_score(y_val, y_pred)
print(f'Validation ROC-AUC Score: {score:.4f}')

test = pd.read_csv(test_path)
test_preds = clf.predict_proba(test)[:,1]
SUBMISSION_DIR = os.path.join(os.path.dirname(__file__), '..', 'submissions')
os.makedirs(SUBMISSION_DIR, exist_ok=True)

submission_path = os.path.join(SUBMISSION_DIR, 'sample_submission.csv')
pd.DataFrame({'graph_id': test['graph_id'], 'probability': test_preds}).to_csv(submission_path, index=False)
print(f'Sample submission saved to: {submission_path}')

# GNN HIV Challenge: Molecular Graph Classification for Drug Discovery

## 🎯 Challenge Overview
Welcome to the **GNN HIV Challenge**! This competition focuses on predicting the molecular properties of chemical compounds to identify potential inhibitors of HIV.

## 🏆 View Live Leaderboard

[Live Leaderboard here](https://faranbutt.github.io/GNN-HIV-Challenge-2/leaderboard.html)


## 🧪 Problem Description
The task is to classify **molecular graphs** to predict anti-HIV activity.

- **Input**: A molecular graph structure (atoms as nodes, bonds as edges) and atomic-level features  
- **Output**: A probability score indicating the likelihood that the molecule inhibits HIV replication  
- **Goal**: Develop Graph Neural Network models (GCN, GAT, GIN) that generalize to unseen molecular structures  

### Labels
- **0**: Non-Inhibitor (Inactive)  
- **1**: Inhibitor (Active)  

### 🤔 What’s Challenging?
- **Non-Euclidean Data**: Molecules are graph-structured data with varying sizes and complex topologies.  
- **Class Imbalance**: The dataset is imbalanced (~25% positive, ~75% negative), so ROC-AUC is preferred over accuracy.  
- **Feature Sparsity**: Models must learn meaningful molecular representations from limited atomic features.  
- **Generalization**: Models must capture biochemical patterns without overfitting.

### 📊 Dataset
The dataset consists of molecular graphs derived from chemical compound databases.

- **Total Graphs**: 5,000  
- **Training**: 4,000 graphs  
- **Test**: 1,000 graphs  
- **Features**: Node-level descriptors (atomic properties) and adjacency matrices (bonds)  
- **Format**: Separate files for metadata, graph structure, and node features  

### 📁 File Structure

#### 1. `data/train.csv` (Training Metadata)

| Column Name | Type | Description |
|------------|------|-------------|
| graph_id   | int  | Unique identifier for the molecular graph (0–3999) |
| target     | int  | Ground truth label (0 = Inactive, 1 = Active) |

#### 2. `data/test.csv` (Test Metadata)

| Column Name | Type | Description |
|------------|------|-------------|
| graph_id   | int  | Unique identifier for the molecular graph (4000–4999) |

#### 3. `data/node_features.pkl`
A dictionary mapping `graph_id` to a NumPy array of node features.

- **Shape**: `(num_nodes, num_node_features)`  
- **Content**: Atomic properties (e.g., atomic number, degree, hybridization)

#### 4. `data/graph_structures.pkl`
A dictionary mapping `graph_id` to adjacency information.

- **Key**: `edge_list` → List of tuples `[(node_u, node_v), ...]` representing bonds

## 🔄 Example Data Flow
To load a single training sample:

```python
import pandas as pd
import pickle

train_df = pd.read_csv('data/train.csv')
row = train_df.iloc[0]
gid = row['graph_id']

with open('data/node_features.pkl', 'rb') as f:
    feats = pickle.load(f)

with open('data/graph_structures.pkl', 'rb') as f:
    structs = pickle.load(f)

x = feats[gid]                   
edges = structs[gid]['edge_list'] 
y = row['target']            

```
# 🎯 Evaluation Metric

**Primary Metric**: ROC-AUC (Area Under the Receiver Operating Characteristic Curve)

- **Range**: 0.0 – 1.0  

### Interpretation
- **1.0**: Perfect classifier  
- **0.5**: Random guessing  
- **< 0.5**: Worse than random  

ROC-AUC is threshold-independent and robust to class imbalance, making it ideal for screening tasks.

---

# 🚀 Getting Started

## Installation
```bash
git clone https://github.com/faranbutt/GNN-HIV-Challenge-2.git
cd GNN-HIV-Challenge-2
pip install -r requirements.txt

```

# Running Baseline Models

Starter code is provided for the following architectures:

- **RFC** (RandomForest Classifier) 
- **GCN** (Graph Neural Network)
- **GIN** (Graph Isomorphism Network)
- **GAT** (Graph Attention Network)

## Train a Baseline GCN Model
```bash
#default model
python starter_code/train.py

#GCN
python starter_code/train.py --model gcn --epochs 15

#GAT
python starter_code/train.py --model gat --epochs 15

#GIN
python starter_code/train.py --model gin --epochs 15
```

## This Will Do

This process will:

- Train on `data/train.csv`  
- Generate predictions for `data/test.csv`  
- Save the submission file to `submissions/pyg_gcn.csv`  

---

# 🏆 How to Participate

- Fork this repository  
- Develop your model in a new branch or in your fork  
- Generate a CSV file `submissions/<your_username>.csv` with the following columns:
  - `graph_id`: Integer ID  
  - `probability`: Float prediction (0.0 to 1.0)  
- Commit the file to the `submissions/` folder  
- Open a Pull Request to the main branch  
- GitHub Actions will automatically evaluate your submission and comment on the PR with your score  

## 🏆 Leaderboard

<!-- LEADERBOARD-START -->

| Rank | User | Submission File | ROC-AUC | Date |
|------|------|----------------|---------|------|
| 1 | faranbutt | submissions/default.csv | 0.4747 | 2026-01-16 |

<!-- LEADERBOARD-END -->

## 📁 Repository Structure

```
├── .github
│   └── workflows
│       └── score_submission.yml
├── data
│   ├── graph_structures.pkl
│   ├── node_features.pkl
│   ├── test.csv
│   ├── test_labels.csv # (Non Accesable)
│   └── train.csv
├── scoring
│   ├── generate_html_leaderboard.py
│   ├── scoring_script.py
│   └── update_leaderboard.py
├── starter_code
│   ├── baseline.py
│   ├── data_loader.py
│   ├── gnn_models.py
│   └── train.py
├── submissions
│   └── submission_samples.csv
├── .gitignore
├── README.md
├── index.html
├── leaderboard.csv
├── leaderboard.html
├── leaderboard.md
├── pyproject.toml
└── requirements.txt
```

## Refrences
- [Basira Lab Deep Graph Learning Playlist](https://www.youtube.com/watch?v=gQRV_jUyaDw&list=PLug43ldmRSo14Y_vt7S6vanPGh-JpHR7T)
- [Basira Lab Deep Graph Learning Github](https://github.com/basiralab/DGL)

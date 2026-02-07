Bash
cat << 'EOF' > README.md
# 🧬 GNN HIV Challenge: The OGB Benchmark Edition

[![OGB-Dataset](https://img.shields.io/badge/Dataset-ogbg--molhiv-red)](https://ogb.stanford.edu/docs/graphprop/#ogbg-molhiv)
[![Metric-ROC--AUC](https://img.shields.io/badge/Metric-ROC--AUC-green)](#)
[![Leaderboard](https://img.shields.io/badge/Live-Leaderboard-blue)](https://faranbutt.github.io/GNN-HIV-Challenge-2/leaderboard.html)

## 🎯 Challenge Overview
This competition utilizes the **ogbg-molhiv** dataset from the Open Graph Benchmark (OGB). The task is to predict whether a molecular graph inhibits HIV virus replication. This is a **Graph Property Prediction** task using real-world biochemical data.

### 🔬 The Science
* **Input**: Molecular graphs where **Nodes** are atoms and **Edges** are chemical bonds.
* **Features**: 9-dimensional node features (atomic number, chirality, formal charge, etc.).
* **Split Type**: **Scaffold Splitting**. Molecules are separated based on structural frameworks rather than random assignment, making generalization significantly more difficult and realistic.
* **Goal**: Maximize the **ROC-AUC** score on the hidden test set.

---

## 📊 Dataset Statistics
| Property | Value |
| :--- | :--- |
| **Total Graphs** | 41,127 |
| **Avg. Nodes/Graph** | 25.5 |
| **Avg. Edges/Graph** | 27.5 |
| **Split Type** | Scaffold Split |
| **Task Type** | Binary Classification |
| **Primary Metric** | **ROC-AUC** |

---

## 🚀 Getting Started

### 1. Installation
Ensure you have the OGB library and PyTorch Geometric installed:
```bash
pip install ogb torch-geometric torch pandas numpy

```

### 2. Prepare the Data
The workflow will handle private data during scoring, but for local training, the dataset will download automatically via the starter code:

```bash
python scripts/download_private_data.py
```
### 3. Training the Baselines
We provide standardized starter code using the PygGraphPropPredDataset module.


### GCN (Graph Convolutional Network)
```python
python starter_code/train.py --model gcn --epochs 20
```
### GIN (Graph Isomorphism Network)
```python
python starter_code/train.py --model gin --epochs 20
```
### GAT (Graph Attention Network)
```python
python starter_code/train.py --model gat --epochs 20
```

## 📥 Submission Process (Human-vs-LLM Study)
To submit your results to the leaderboard:

1. **Generate Predictions**: Your training script will output a file in the `submissions/` folder (e.g., `ogb_submission_gin.csv`).
2. **Format**: The CSV must contain `graph_id` and `probability` columns.
3. **Organization**: Place your submission in `submissions/`.
4. **Metadata**: (Recommended) Include notes in your PR description stating if the model was created by a **Human**, **LLM-only**, or **Hybrid** approach.
5. **Pull Request**: Open a PR to the `main` branch. GitHub Actions will score your submission and update the leaderboard automatically.

## 🏆 Current Rankings
The **Interactive Leaderboard** tracks all submissions, allowing you to filter by model type and compare performance.

> [**Click here to view the Live Leaderboard**](https://faranbutt.github.io/GNN_HIV_Challenge/leaderboard.html)
EOF

## 📁 Repository Structure
```text
├── .github/workflows/    # Automated scoring & leaderboard CI
├── datasets/             # Local data storage (ignored by git)
├── scoring/              # Evaluation & HTML generation scripts
├── scripts/              # Data management scripts
├── starter_code/         # GNN models, data loaders, and training logic
├── submissions/          # User prediction files (.csv)
├── leaderboard.csv       # Authoritative score data
└── README.md             # Competition guide
```


## 📜 References

> [1] Wu, Z., et al. "MoleculeNet: A benchmark for molecular machine learning." *Chemical Science*, 2018.
>
> [2] Hu, W., et al. "Open Graph Benchmark: Datasets for Machine Learning on Graphs." *NeurIPS*, 2020.
EOF
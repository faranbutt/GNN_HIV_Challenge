#working/GNN-HIV-Challenge-2/scoring/update_leaderboard.py

import pandas as pd
import os
from datetime import datetime

def update_leaderboard():
    csv_path = 'leaderboard.csv'
    # Get values from environment (set by GitHub Action)
    user = os.getenv('PR_USER', 'Unknown')
    score = float(os.getenv('PR_SCORE', 0.0))
    sub_file = os.getenv('PR_SUBMISSION', 'Unknown')
    date_str = datetime.now().strftime('%Y-%m-%d')

    # 1. Update CSV
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=['Rank', 'User', 'Submission File', 'ROC-AUC', 'Date'])

    # Add new entry
    new_entry = pd.DataFrame([{
        'Rank': 0, 'User': user, 'Submission File': sub_file, 'ROC-AUC': score, 'Date': date_str
    }])
    df = pd.concat([df, new_entry], ignore_index=True)

    # Sort by score and re-rank
    df = df.sort_values(by='ROC-AUC', ascending=False).reset_index(drop=True)
    df['Rank'] = df.index + 1
    df.to_csv(csv_path, index=False)

    # 2. Update HTML (Simplified Generation)
    rows_html = ""
    for _, row in df.iterrows():
        rank_class = "top-1" if row['Rank'] == 1 else ""
        rows_html += f"""
        <tr class="{rank_class}">
            <td>{row['Rank']}</td>
            <td>{row['User']}</td>
            <td>{row['Submission File']}</td>
            <td>{row['ROC-AUC']:.4f}</td>
            <td>{row['Date']}</td>
        </tr>"""

    # ... (Wrap this in your HTML template from the earlier files and write to leaderboard.html)
    print(f"Leaderboard updated successfully for user {user}.")

if __name__ == "__main__":
    update_leaderboard()

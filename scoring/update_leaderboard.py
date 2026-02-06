#working/GNN-HIV-Challenge-2/scoring/update_leaderboard.py

import pandas as pd
import os
from datetime import datetime
import re
import sys

# File paths
leaderboard_csv = 'leaderboard.csv'
leaderboard_html = 'leaderboard.html'
readme_file = 'README.md'

def generate_html_content(df):
    """ Generates clean HTML for the leaderboard """
    rows_html = ""
    for _, row in df.iterrows():
        rank_class = "top-1" if int(row['Rank']) == 1 else ""
        rows_html += f"""
                <tr class="{rank_class}">
                    <td>{row['Rank']}</td>
                    <td>{row['User']}</td>
                    <td>{row['Submission File']}</td>
                    <td>{float(row['ROC-AUC']):.4f}</td>
                    <td>{row['Date']}</td>
                </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GNN HIV Challenge - Leaderboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f6f8fa; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ text-align: center; color: #333; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #2c3e50; color: white; }}
        tr:hover {{ background-color: #f1f1f1; }}
        .top-1 {{ background-color: #fff9c4; font-weight: bold; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 GNN HIV Challenge Leaderboard</h1>
        <p style="text-align: center; color: #666;">Metric: ROC-AUC (Higher is better)</p>
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>User</th>
                    <th>Submission File</th>
                    <th>ROC-AUC</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>{rows_html}
            </tbody>
        </table>
        <div class="footer">
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </div>
</body>
</html>"""
    return html_content

# 1. Load Data from Environment
user = os.getenv('PR_USER', 'Anonymous')
sub_file = os.getenv('PR_SUBMISSION', 'unknown.csv')
raw_score = os.getenv('PR_SCORE', '0').strip()

try:
    roc_auc = float(raw_score) if raw_score else 0.0
except ValueError:
    roc_auc = 0.0

# 2. Update Leaderboard CSV
try:
    leaderboard = pd.read_csv(leaderboard_csv)
except:
    leaderboard = pd.DataFrame(columns=['Rank', 'User', 'Submission File', 'ROC-AUC', 'Date'])

new_entry = pd.DataFrame([{
    'User': user, 
    'Submission File': sub_file, 
    'ROC-AUC': roc_auc, 
    'Date': datetime.now().strftime('%Y-%m-%d')
}])

leaderboard = pd.concat([leaderboard, new_entry], ignore_index=True)
leaderboard = leaderboard.sort_values(by='ROC-AUC', ascending=False).reset_index(drop=True)
leaderboard['Rank'] = leaderboard.index + 1
leaderboard.to_csv(leaderboard_csv, index=False)

# 3. Write HTML file
with open(leaderboard_html, 'w', encoding='utf-8') as f:
    f.write(generate_html_content(leaderboard))

# 4. Update README.md
table_md = "| Rank | User | Submission File | ROC-AUC | Date |\n|------|------|----------------|---------|------|\n"
for _, row in leaderboard.iterrows():
    table_md += f"| {row['Rank']} | {row['User']} | {row['Submission File']} | {float(row['ROC-AUC']):.4f} | {row['Date']} |\n"

if os.path.exists(readme_file):
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # FIX: Explicit markers used for matching
    pattern = r'.*?'
    replacement = f'\n\n{table_md}\n'
    
    if "" in content:
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("README updated successfully.")
    else:
        print("Markers not found in README!")

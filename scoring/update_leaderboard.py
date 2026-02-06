#working/GNN-HIV-Challenge-2/scoring/update_leaderboard.py

import pandas as pd
import os
from datetime import datetime
import re
leaderboard_csv = 'leaderboard.csv'
leaderboard_html = 'leaderboard.html'
readme_file = 'README.md'

def generate_html_content(df):
    """
    Generates HTML string for the leaderboards.
    """
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GNN HIV Challenge - Leaderboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f6f8fa; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #2c3e50; color: white; }
        tr:hover { background-color: #f1f1f1; }
        .top-1 { background-color: #fff9c4; font-weight: bold; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 0.9em; }
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
            <tbody>
"""

    for _, row in df.iterrows():
        rank_class = "top-1" if row['Rank'] == 1 else ""
        html_content += f"""
                <tr class="{rank_class}">
                    <td>{row['Rank']}</td>
                    <td>{row['User']}</td>
                    <td>{row['Submission File']}</td>
                    <td>{row['ROC-AUC']:.4f}</td>
                    <td>{row['Date']}</td>
                </tr>
"""

    html_content += f"""
            </tbody>
        </table>
        <div class="footer">
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </div>
</body>
</html>
"""
    return html_content

try:
    leaderboard = pd.read_csv(leaderboard_csv)
except FileNotFoundError:
    leaderboard = pd.DataFrame(columns=['Rank', 'User', 'Submission File', 'ROC-AUC', 'Date'])
user = os.getenv('PR_USER', 'Anonymous')
submission_file = os.getenv('PR_SUBMISSION', 'submission.csv')
roc_auc = float(os.getenv('PR_SCORE', 0))
new_entry = pd.DataFrame([{
    'Rank': len(leaderboard) + 1,
    'User': user,
    'Submission File': submission_file,
    'ROC-AUC': roc_auc,
    'Date': datetime.now().strftime('%Y-%m-%d')
}])

leaderboard = pd.concat([leaderboard, new_entry], ignore_index=True)
leaderboard = leaderboard.sort_values(by='ROC-AUC', ascending=False).reset_index(drop=True)
leaderboard['Rank'] = leaderboard.index + 1
leaderboard.to_csv(leaderboard_csv, index=False)
print(f"Updated {leaderboard_csv}")
html_content = generate_html_content(leaderboard)
with open(leaderboard_html, 'w') as f:
    f.write(html_content)
print(f"Generated {leaderboard_html}")
table_lines = [
    '| Rank | User | Submission File | ROC-AUC | Date |',
    '|------|------|----------------|---------|------|'
]
for _, row in leaderboard.iterrows():
    table_lines.append(
        f"| {row['Rank']} | {row['User']} | "
        f"{row['Submission File']} | "
        f"{row['ROC-AUC']:.4f} | {row['Date']} |"
    )

leaderboard_table = '\n'.join(table_lines)

with open(readme_file, 'r') as f:
    readme_content = f.read()

pattern = r'(<!-- LEADERBOARD-START -->).*?(<!-- LEADERBOARD-END -->)'
replacement = f'<!-- LEADERBOARD-START -->\n\n{leaderboard_table}\n\n<!-- LEADERBOARD-END -->'
updated_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

with open(readme_file, 'w') as f:
    f.write(updated_readme)
print(f"Updated {readme_file}")




# scoring/generate_html_leaderboard.py
import pandas as pd
from datetime import datetime

def generate_html(csv_file='leaderboard.csv', output_file='leaderboard.html'):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Rank', 'User', 'Submission File', 'ROC-AUC', 'Date'])

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

    html_content += """
            </tbody>
        </table>
        <div class="footer">
            <p>Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """</p>
        </div>
    </div>
</body>
</html>
"""

    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"Generated {output_file}")

if __name__ == "__main__":
    generate_html()
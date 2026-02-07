#working/GNN-HIV-Challenge-2/scoring/update_leaderboard.py

import pandas as pd
import os
from datetime import datetime
# Import the generator function from your other script
from generate_html_leaderboard import generate_html

def update_leaderboard():
    csv_path = 'leaderboard.csv'
    md_path = 'leaderboard.md'
    
    # Get values from environment (set by GitHub Action)
    user = os.getenv('PR_USER', 'Unknown')
    score_str = os.getenv('PR_SCORE', '0.0')
    
    # Safety check: if score is empty or invalid, treat as 0
    try:
        score = float(score_str)
    except ValueError:
        score = 0.0
        
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

    # Sort by score (descending) and re-rank
    df = df.sort_values(by='ROC-AUC', ascending=False).reset_index(drop=True)
    df['Rank'] = df.index + 1
    
    # Keep only the best score per user (Optional, common for Kaggle)
    # df = df.drop_duplicates(subset=['User'], keep='first')
    
    df.to_csv(csv_path, index=False)

    # 2. Update HTML (Calling your existing generator script)
    generate_html(csv_file=csv_path, output_file='leaderboard.html')

    # 3. Update Markdown (leaderboard.md)
    md_content = f"# 🏆 GNN HIV Challenge Leaderboard\n\n"
    md_content += f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
    md_content += df.to_markdown(index=False)
    
    with open(md_path, 'w') as f:
        f.write(md_content)

    print(f"Leaderboard updated successfully for user {user}. Score: {score}")

if __name__ == "__main__":
    update_leaderboard()
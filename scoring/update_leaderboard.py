#working/GNN-HIV-Challenge-2/scoring/update_leaderboard.py

# import pandas as pd
# import os
# from datetime import datetime
# from generate_html_leaderboard import generate_html

# def update_leaderboard():
#     csv_path = "leaderboard.csv"
#     md_path = "leaderboard.md"

#     user = os.getenv("PR_USER")
#     sub_file = os.getenv("PR_SUBMISSION")
#     score = float(os.getenv("PR_SCORE", "0"))

#     if score <= 0:
#         raise ValueError("Invalid score. Leaderboard update blocked.")

#     date_str = datetime.now().strftime("%Y-%m-%d")

#     if os.path.exists(csv_path):
#         df = pd.read_csv(csv_path)
#     else:
#         df = pd.DataFrame(columns=["Rank", "User", "Submission File", "ROC-AUC", "Date"])

#     df = pd.concat([df, pd.DataFrame([{
#         "Rank": 0,
#         "User": user,
#         "Submission File": sub_file,
#         "ROC-AUC": score,
#         "Date": date_str
#     }])], ignore_index=True)

#     df = df.sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)
#     df["Rank"] = df.index + 1

#     df.to_csv(csv_path, index=False)
#     generate_html(csv_file=csv_path, output_file="leaderboard.html")

#     with open(md_path, "w") as f:
#         f.write(f"# 🏆 Leaderboard\n\nLast updated: {datetime.utcnow()} UTC\n\n")
#         f.write(df.to_markdown(index=False))

# if __name__ == "__main__":
#     update_leaderboard()


import pandas as pd
import os
from datetime import datetime
from generate_html_leaderboard import generate_html

def update_leaderboard():
    csv_path = 'leaderboard.csv'
    md_path = 'leaderboard.md'
    
    # Get environment variables set by GitHub Actions
    user = os.getenv('PR_USER', 'Unknown')
    score_str = os.getenv('PR_SCORE', '0.0')
    
    try:
        score = float(score_str)
    except ValueError:
        score = 0.0
    
    sub_file = os.getenv('PR_SUBMISSION', 'Unknown')
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Load existing leaderboard
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=['Rank', 'User', 'Submission File', 'ROC-AUC', 'Date'])

    # Append new entry
    new_entry = pd.DataFrame([{
        'Rank': 0,
        'User': user,
        'Submission File': sub_file,
        'ROC-AUC': score,
        'Date': date_str
    }])
    df = pd.concat([df, new_entry], ignore_index=True)

    # Optional: Keep only the **best score per user**
    df = df.sort_values(by='ROC-AUC', ascending=False)
    df = df.drop_duplicates(subset=['User'], keep='first')  # keeps best score

    # Re-rank after sorting
    df['Rank'] = df.index + 1
    df = df.sort_values(by='Rank')  # just in case

    # Save CSV
    df.to_csv(csv_path, index=False)

    # Generate HTML leaderboard
    generate_html(csv_file=csv_path, output_file='leaderboard.html')

    # Generate Markdown leaderboard
    md_content = f"# 🏆 GNN HIV Challenge Leaderboard\n\n"
    md_content += f"Last Updated: {date_str}\n\n"
    md_content += df.to_markdown(index=False)
    with open(md_path, 'w') as f:
        f.write(md_content)

    print(f"✅ Leaderboard updated successfully for user {user}. Score: {score}")

if __name__ == "__main__":
    update_leaderboard()

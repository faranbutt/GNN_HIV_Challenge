#working/GNN-HIV-Challenge-2/scoring/update_leaderboard.py

import pandas as pd
import os
from datetime import datetime
from generate_html_leaderboard import generate_html

def update_leaderboard():
    csv_path = "leaderboard.csv"
    md_path = "leaderboard.md"

    user = os.getenv("PR_USER")
    sub_file = os.getenv("PR_SUBMISSION")
    score = float(os.getenv("PR_SCORE", "0"))

    if score <= 0:
        raise ValueError("Invalid score. Leaderboard update blocked.")

    date_str = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=["Rank", "User", "Submission File", "ROC-AUC", "Date"])

    df = pd.concat([df, pd.DataFrame([{
        "Rank": 0,
        "User": user,
        "Submission File": sub_file,
        "ROC-AUC": score,
        "Date": date_str
    }])], ignore_index=True)

    df = df.sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1

    df.to_csv(csv_path, index=False)
    generate_html(csv_file=csv_path, output_file="leaderboard.html")

    with open(md_path, "w") as f:
        f.write(f"# 🏆 Leaderboard\n\nLast updated: {datetime.utcnow()} UTC\n\n")
        f.write(df.to_markdown(index=False))

if __name__ == "__main__":
    update_leaderboard()

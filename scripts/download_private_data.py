# scripts/download_private_data.py
import os
import requests
import pandas as pd
import re

def convert_drive_link(url):
    """
    Converts a Google Drive 'view' link into a direct download link.
    """
    pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?export=download&id={file_id}'
    
    return url

def download_labels():
    output_path = 'data/test_labels.csv'
    os.makedirs('data', exist_ok=True)
    default_url = "https://example.com/dummy_data.csv" 
    url = os.getenv('PRIVATE_DATA_URL', default_url)
    
    download_url = convert_drive_link(url)
    
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        response = session.get(download_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("download successful.")
        return True
        
    except Exception as e:
        print(f"download failed: {e}")
        
        print("creating dummy labels for local testing.")
        try:
            test_df = pd.read_csv('data/test.csv')
            dummy_labels = pd.DataFrame({
                'graph_id': test_df['graph_id'],
                'target': [0] * len(test_df) 
            })
            dummy_labels.to_csv(output_path, index=False)
            print(f"created dummy labels at {output_path}")
            return True
        except FileNotFoundError:
            print("Error: 'data/test.csv' not found. Cannot create dummy labels.")
            return False

if __name__ == "__main__":
    download_labels()
import os
import requests
import re
import sys

def convert_drive_link(url):
    pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?export=download&id={file_id}'
    return url

def download_private_files():
    label_url = os.getenv("PRIVATE_LABEL_URL")
    test_url = os.getenv("PRIVATE_TEST_IDX_URL")

    if not label_url or not test_url:
        print("❌ Error: Private URLs not found in environment.")
        print("Participants: You cannot download the private test labels manually.")
        sys.exit(1)

    files_to_download = {
        "graph-label.csv.gz": {
            "url": label_url,
            "output_dir": "datasets/ogbg_molhiv/raw"
        },
        "test.csv.gz": {
            "url": test_url,
            "output_dir": "datasets/ogbg_molhiv/split/scaffold"
        }
    }

    session = requests.Session()
    for filename, info in files_to_download.items():
        output_path = os.path.join(info["output_dir"], filename)
        os.makedirs(info["output_dir"], exist_ok=True)
        
        download_url = convert_drive_link(info["url"])
        print(f"Downloading {filename}...")
        try:
            response = session.get(download_url, stream=True)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {filename}")

if __name__ == "__main__":
    download_private_files()
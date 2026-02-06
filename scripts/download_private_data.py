import os
import requests
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

def download_private_files():
    # Define the private files and their locations
    files_to_download = {
        "graph-label.csv.gz": {
            "url": "https://drive.google.com/file/d/11tHXyx0EJWhnUi6Z0SU4aScrcpUN0Bo7/view?usp=sharing",
            "output_dir": "datasets/ogbg_molhiv/raw"
        },
        "test.csv.gz": {
            "url": "https://drive.google.com/file/d/1ageBkaRCBxb5o2NM6lWSc05EiaOljPeG/view?usp=sharing",
            "output_dir": "datasets/ogbg_molhiv/split/scaffold"
        }
    }

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    for filename, info in files_to_download.items():
        output_path = os.path.join(info["output_dir"], filename)
        os.makedirs(info["output_dir"], exist_ok=True)
        
        # Check if environment variables exist, otherwise use the provided links
        # ENV keys: PRIVATE_LABEL_URL and PRIVATE_TEST_IDX_URL
        env_key = "PRIVATE_LABEL_URL" if "label" in filename else "PRIVATE_TEST_IDX_URL"
        url = os.getenv(env_key, info["url"])
        
        download_url = convert_drive_link(url)
        
        print(f"Downloading {filename}...")
        try:
            response = session.get(download_url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Successfully downloaded {filename} to {output_path}")
            
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    download_private_files()
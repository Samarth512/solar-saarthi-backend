import os
import requests
from pathlib import Path

def download_data_file():
    """
    Downloads the large h5 file if it doesn't exist locally.
    Replace the URL with your actual file hosting URL.
    """
    data_file = Path(__file__).parent / "india_spectral_tmy.h5"
    
    # Skip if file already exists
    if data_file.exists():
        return
        
    # Get the download URL from environment variable
    download_url = os.getenv("DATA_FILE_URL")
    if not download_url:
        raise ValueError("DATA_FILE_URL environment variable not set")
        
    print("Downloading data file...")
    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    
    # Save the file
    with open(data_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print("Data file downloaded successfully")

# --- REMOVE OR COMMENT OUT SCRIPT ENTRYPOINT ---
# if __name__ == "__main__":
#     download_data_file() 
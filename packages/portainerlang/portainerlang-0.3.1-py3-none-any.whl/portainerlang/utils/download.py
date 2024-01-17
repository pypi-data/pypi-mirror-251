import requests
import zipfile
import logging
import os
from tqdm import tqdm

logger = logging.getLogger('portainerlang.utils')

def download_and_extract(url, extract_to_path):
    """
    Downloads and extracts a zip file from the given URL to the specified directory.
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kilobyte
            zip_file_path = extract_to_path / 'temp_archive.zip'
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

            with open(zip_file_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                logger.error("something went wrong while downloading the file")

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_path)

            os.remove(zip_file_path)
        else:
            raise Exception(f"Failed to download the file: Status code {response.status_code}")
    except Exception as e:
        raise Exception(f"Error in download_and_extract: {e}")

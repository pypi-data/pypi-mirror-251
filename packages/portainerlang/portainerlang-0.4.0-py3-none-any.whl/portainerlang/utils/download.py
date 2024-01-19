import requests
import os
import zipfile
import logging
from rich.progress import Progress, SpinnerColumn
from urllib.parse import urlparse, unquote

logger = logging.getLogger('portainerlang.utils')

def download_and_extract(url, extract_to_path):
    """
    Downloads a zip file from the specified URL and extracts it to the given directory. This function handles the 
    download in chunks to manage memory efficiently and displays a progress bar to indicate download progress.

    The function first sends a GET request to the URL. If the response status code is 200 (OK), it proceeds with
    the download; otherwise, it raises an exception. The filename is extracted from the URL, and the content length 
    from the headers is used to track the download progress.

    The download process involves writing data in chunks of 1 Kilobyte to a file. During this process, the 
    function displays a progress bar using Rich's `Progress` class, which provides a visual indication of the 
    download progress on the CLI.

    After the download completes, the zip file is extracted to the target directory using the `zipfile` module. 
    The downloaded zip file is then deleted to clean up the directory.

    If any exception occurs during these processes, it is caught and re-raised with an appropriate error message 
    to facilitate debugging.

    :param url: A string representing the URL of the zip file to be downloaded.
    :param extract_to_path: A Path object representing the directory where the zip file should be extracted.
    :return: None. This function performs file I/O operations and does not return a value.
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = unquote(os.path.basename(parsed_url.path))

            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kilobyte
            zip_file_path = extract_to_path / filename

            with Progress(
                    SpinnerColumn(),
                    *Progress.get_default_columns(),
                ) as progress:
                    download_task = progress.add_task(f"[cyan]Downloading {filename}...", total=total_size_in_bytes)

                    with open(zip_file_path, 'wb') as file:
                        for data in response.iter_content(block_size):
                            file.write(data)
                            progress.update(download_task, advance=len(data))                

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_path)

            os.remove(zip_file_path)
        else:
            raise Exception(f"Failed to download the file: Status code {response.status_code}")
    except Exception as e:
        raise Exception(f"Error in download_and_extract: {e}")
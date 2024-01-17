import pathlib
import os
import logging
from .download import download_and_extract

logger = logging.getLogger('portainerlang.utils')

def create_app_directory():
    """
    Creates the application directory in the user's home folder.
    If it cannot create the directory for any reason, it raises an OSError.
    """
    app_dir = pathlib.Path.home() / '.portainerlang'
    
    try:
        if not app_dir.exists():
            app_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Failed to create directory {app_dir}: {e}") from e

def setup_assets(asset_url, asset_folder):
    """
    Sets up the assets for the application. Checks if assets exist in the asset_folder,
    and if not, downloads and extracts them from the asset_url. Raises an error if
    something goes wrong during the folder creation, download, or extraction process.
    """
    try:
        app_dir = pathlib.Path.home() / asset_folder
        app_dir.mkdir(parents=True, exist_ok=True)

        if not any(app_dir.iterdir()):
            logger.info("Assets directory is empty. Downloading assets.")
            download_and_extract(asset_url, app_dir)
        else:
            logger.debug("Assets already exist. Skipping setup.")
    except Exception as e:
        error_message = f"Failed to set up assets in {asset_folder}: {e}"
        logger.error(error_message)
        raise RuntimeError(error_message) from e
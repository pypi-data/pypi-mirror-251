import os
from .query.query import process_query
from .logging.logging import setup_debug_logger, setup_package_logger
from .utils.env import initialize_environment, MissingEnvironmentVariablesError
from .utils.assets import create_app_directory, setup_assets

def main():
    """
    Main function that sets up the application environment,
    downloads necessary assets, and processes CLI queries.
    """

    # Check for a debug flag/environment variable
    debug_mode = os.getenv('DEBUG', False)

    if debug_mode:
        setup_debug_logger()
        logger = logging.getLogger()
        logger.debug("Running in debug mode")
    else:
        logger = setup_package_logger('portainerlang')

    try:
        create_app_directory()
    except OSError as e:
        logger.error(f"An error occurred while creating the application directory: {e}")
        exit(1)

    try:
        asset_url = "https://anthony.portainer.io/portainerlang-faiss.zip"
        asset_folder = ".portainerlang/assets"
        setup_assets(asset_url, asset_folder)
    except Exception as e:
        logger.error(f"An error occurred during assets setup: {e}")
        exit(1)

    try:
        required_vars = ['OPENAI_API_KEY']
        initialize_environment(required_vars)
    except MissingEnvironmentVariablesError as e:
        logger.error(e)
        exit(1)

    process_query()

if __name__ == '__main__':
    main()

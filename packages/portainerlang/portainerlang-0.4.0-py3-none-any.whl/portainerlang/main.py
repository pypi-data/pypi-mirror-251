import os

from .logging.logging import setup_debug_logger, setup_package_logger
from .utils.env import initialize_environment, MissingEnvironmentVariablesError
from .utils.assets import create_app_directory, setup_assets
from .cli.commands import entrypoint

def main():
    """
    Main entry point for the application. This function is responsible for setting up the application environment,
    including logging, downloading necessary assets, and initializing environment variables. It also calls the
    `entrypoint` function to start processing CLI queries.

    The function first checks for a debug mode flag through an environment variable. If debug mode is enabled,
    it sets up a debug logger; otherwise, it sets up a standard package logger. 

    It then attempts to create the application directory. If this process fails due to an OSError, an error is
    logged, and the application exits with an error code.

    The function also handles the download and setup of necessary assets from a specified URL. If this setup
    fails due to a RuntimeError, an error is logged, and the application exits with an error code.

    Additionally, the function checks for required environment variables and initializes them. If any required
    variables are missing, it raises a MissingEnvironmentVariablesError, logs the error, and exits with an
    error code.

    Finally, the function calls `entrypoint` to start processing CLI queries.

    :return: None. This function is designed to initialize the application and does not return a value.
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
        asset_folder = ".portainerlang/faiss"
        setup_assets(asset_url, asset_folder)
    except RuntimeError as e:
        logger.error(f"An error occurred during setup: {e}")
        exit(1)

    try:
        required_vars = ['OPENAI_API_KEY']
        initialize_environment(required_vars)
    except MissingEnvironmentVariablesError as e:
        logger.error(e)
        exit(1)

    entrypoint()

if __name__ == '__main__':
    main()

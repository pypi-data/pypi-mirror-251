import logging

def setup_debug_logger(log_level=logging.DEBUG):
    """
    Sets up the root logger for debugging purposes.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=log_level, format=log_format, datefmt=date_format)


def setup_package_logger(name, log_level=logging.INFO):
    """
    Sets up a logger for the specific package.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger

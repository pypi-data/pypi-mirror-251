import logging
import os


def get_logger(
    logger_name: str, logger_level: str = "INFO", logger_file_level: str = "DEBUG"
) -> logging.Logger:
    """
    This function creates and returns a custom logger.
    By default, it prints infos, warning and errors in the console and saves also the debugs in the .log file

    Args:
        logger_name (string): The name of the Logger
        logger_level (string): The level of logs you want to see in the terminal
        logger_file_level (string): The level of logs you want to have in the .log file

    Returns:
        type: Logger

    Raises:
        AssertionError: If the levels of 'logger_level' and 'logger_file_level' are not
        one of the standard logging levels (NOTSET | INFO | DEBUG | WARNING | ERROR | CRITICAL)

    Example:
        >>> my_logger = get_logpunk("my_module")
        >>> my_logger
        <Logger my_module (DEBUG)>
    """

    # Initialize map
    level_map = {
        "NOTSET": logging.NOTSET,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    # Test input parameters
    assert (
        logger_level in level_map.keys()
    ), "[LOG ERROR] 'logger_level' should be: NOTSET | INFO | DEBUG | WARNING | ERROR | CRITICAL"
    assert (
        logger_file_level in level_map.keys()
    ), "[LOG ERROR] 'logger_file_level' should be:  NOTSET | INFO | DEBUG | WARNING | ERROR | CRITICAL"

    # Initialize logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # log_format = "| %(asctime)s | %(levelname)s | source: %(name)s |--> %(message)s"
    # log_format = "| {asctime} | {levelname} | source: {name} |--> {message}"
    log_format = "|{:^13}|{:^17}|{:^17}|--> {}".format(
        "%(asctime)s", "%(levelname)s", "%(name)s", "%(message)s"
    )

    # Create a console handler and set the level to 'logger_level'
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level_map[logger_level])
    console_handler.setFormatter(logging.Formatter(log_format))

    # Define the name and the path of the .log file
    directory = "./.logs"
    if not os.path.exists(directory):
        os.mkdir(directory)
    filename = logger_name.strip().lower().replace(" ", "_") + ".log"
    filepath = os.path.join(directory, filename)

    # Create a file handler and set the level to 'logger_file_level'
    file_handler = logging.FileHandler(filepath)
    file_handler.setLevel(level_map[logger_file_level])
    file_handler.setFormatter(logging.Formatter(log_format))

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

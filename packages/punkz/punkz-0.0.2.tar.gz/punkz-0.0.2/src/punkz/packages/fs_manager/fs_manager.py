import os
from logging import Logger
from typing import Any, Callable, Iterator


class FileSystemManager:
    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger

    def create_file(self, file_name: str, content: str) -> None:
        """
        Creates a new file with the given file name and content.

        Args:
            file_name (str): The name of the file to create.
            content (str): The content to write to the file.

        Raises:
            OSError: If an error occurs while creating the file.

        Returns:
            None
        """
        try:
            with open(file_name, "w", encoding="utf-8") as new_file:
                new_file.write(content)
            message = f"File created: {file_name}"
            self.logger.debug(message) if self.logger else print(message)
        except OSError as error:
            message = f"An OSError occurred while creating the file {file_name}"
            self.logger.error(message) if self.logger else print(message)
            self.logger.error(error) if self.logger else print(error)

    def get_filepath_from_directory(self, folder_name: str) -> Iterator[str]:
        """
        Given a folder name, returns an iterator of file paths in that folder.

        Args:
        - folder_name (str): the name of the folder to scan for files

        Returns:
        - Iterator[str]: an iterator of file paths in the folder
        """
        for file in self.scan_directory_for_files(folder_name):
            yield os.path.join(folder_name, file)

    def scan_directory_for_files(self, folder_name: str) -> Iterator[str]:
        """
        Scans the specified directory for files and yields their names.

        Args:
            folder_name (str): The name of the directory to scan.

        Yields:
            str: The name of a file in the directory.
        """
        message = f"Scanning directory {folder_name}"
        self.logger.debug(message) if self.logger else None
        with os.scandir(folder_name) as it:
            for entry in it:
                if entry.is_file():
                    yield entry.name

    def create_directory(self, directory: str) -> None:
        """
        Create a directory if it doesn't exist.

        Args:
            directory (str): The directory to create.

        Returns:
            None
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            message = f"Folder created: {directory}"
            self.logger.debug(message) if self.logger else None
            return None
        message = f"Folder already exists: {directory}"
        self.logger.debug(message) if self.logger else None

    def get_filepath(self, filepath: str, func: Callable, *args: Any) -> str:
        """
        Given a filepath, checks if the file exists.
        If it does, returns the filepath, otherwise
        returns the result of the function.

        Args:
            filepath (str): The filepath to check.
            func (Callable): The function to call if the file does not exist.

        Returns:
            str: The filepath or the result of the function.
        """
        if os.path.exists(filepath):
            return filepath
        else:
            return func(*args)

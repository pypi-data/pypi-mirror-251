from datetime import datetime
import json
from logging import Logger
import os
from typing import Any
from punkz.core.cache.providers import BaseCacheProvider
from punkz.packages.fs_manager import FileSystemManager


class LocalCacheProvider(BaseCacheProvider):
    def __init__(self, base_directory: str, logger: Logger | None = None) -> None:
        super().__init__()
        self.logger = logger
        self.base_directory = base_directory
        self.fs_manager = FileSystemManager(self.logger)

    def read(
        self, file_name: str, func_name: str, cache_instance_id: str
    ) -> Any | None:
        cache_dir = self._get_cache(cache_instance_id, func_name, self.base_directory)
        file_path = os.path.join(os.getcwd(), cache_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                cached_result = self._parse_types(json.loads(f.read()))
            if cached_result and self._is_cached_result_valid(
                cached_result["metadata"]["expiration"]
            ):
                return cached_result["cached_data"]
            else:
                self.logger.debug("This is expired") if self.logger else None
        return None

    def write(
        self,
        file_name: str,
        func_name: str,
        content: str,
        expiration_date: str,
        cache_instance_id: str,
    ) -> None:
        cache_result = {
            "cached_data": str(content),
            "metadata": {
                "timestamp": str(
                    datetime.now().strftime(self._default_datetime_str_format)
                ),
                "expiration": expiration_date,
            },
        }
        cache_dir = self._get_cache(cache_instance_id, func_name, self.base_directory)
        file_path = os.path.join(os.getcwd(), cache_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(cache_result))

    def _get_cache(
        self, cache_instance_id: str, func_name: str, base_dir: str = None
    ) -> str:
        """
        Get cache directory for a function call.
        Parameters:
            func_name (str): name of the function.
        Returns:
            cache_dir (str): cache directory for the function call.
        """
        cache_dir = self._get_cache_dir_name(cache_instance_id, func_name, base_dir)
        self.fs_manager.create_directory(cache_dir)
        return cache_dir

    def _get_cache_dir_name(
        self, cache_instance_id: str, func_name: str, base_dir: str
    ) -> str:
        """
        Create cache directory path for a function call.
        Parameters:
            func_name (str): name of the function.
        Returns:
            cache_dir (str): cache directory for the function call.
        """
        cache_name = func_name + "_cache"
        return os.path.join(self.base_directory, cache_instance_id, cache_name)

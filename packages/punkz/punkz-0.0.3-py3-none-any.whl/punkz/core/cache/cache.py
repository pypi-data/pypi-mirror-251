from ast import literal_eval
from datetime import datetime
import hashlib
from logging import Logger
import os
from typing import Any, Callable
import json
from datetime import datetime, timedelta
from punkz.core.cache import LocalCacheProvider
from punkz.core.cache import AWSS3CacheProvider


class Cache:
    def __init__(
        self,
        provider: LocalCacheProvider | AWSS3CacheProvider,
        cache_instance_id: str,
        expiration: str | None = None,
        logger: Logger | None = None,
    ) -> None:
        self.logger = logger
        self._default_datetime_str_format = "%d-%m-%Y %H:%M:%S"
        self._deltatime_unit_mapping = {
            "d": "days",
            "h": "hours",
            "m": "minutes",
            "s": "seconds",
        }
        self.provider = provider
        self.expiration_date = self._compute_expiration_date(expiration)
        self.cache_instance_id = cache_instance_id

    def _compute_expiration_date(self, delta_str: str | None) -> str:
        """
        Compute the expiration date based on the given delta string.

        Args:
            delta_str (str | None): The delta string representing the time duration.

        Returns:
            str: The expiration date in the format specified by self._default_datetime_str_format.

        Raises:
            ValueError: If the time unit is invalid.

        """
        if delta_str:
            # Parse the input string to extract the value and unit
            value, unit = int(delta_str[:-1]), delta_str[-1]
            # Validate the unit and calculate the timedelta
            if unit in self._deltatime_unit_mapping:
                delta = timedelta(**{self._deltatime_unit_mapping[unit]: value})
                future_date = datetime.now() + delta
                return future_date.strftime(self._default_datetime_str_format)
            else:
                raise ValueError(
                    'Invalid time unit. Use "d" for days, "h" for hours. E.g. "45d" or "2h"'
                )
        return "never"

    def _sha256_hash(self, string: str) -> str:
        """
        Get sha256 hash of a string.
        Parameters:
            string (str): string to be hashed.
        Returns:
            hash (str): sha256 hash of the string.
        """
        hash = hashlib.sha256()
        hash.update(string.encode("utf-8"))
        return hash.hexdigest()

    def _normalize_text(self, text: str) -> str:
        """
        Normalize the given text by converting it to lowercase, removing leading and trailing whitespaces,
        and replacing multiple whitespaces with a single space.

        Args:
            text (str): The text to be normalized.

        Returns:
            str: The normalized text.
        """
        normalized_text = text.lower()

        # Remove leading and trailing whitespaces
        normalized_text = normalized_text.strip()

        # Replace multiple whitespaces with a single space
        normalized_text = " ".join(normalized_text.split())

        return normalized_text

    def _build_filename_from_params(self, *args, **kwargs) -> str:
        """
        Get hash key for a function call.
        Parameters:
            *args (list): list of arguments.
            **kwargs (dict): dictionary of keyword arguments.
        Returns:
            hash_key (str): hash key for the function call.
        """
        name: str = ""
        for arg in args:
            name += f"_{str(arg)}"
        for key, value in kwargs.items():
            name += f"_{str(key)}" + f"_{str(value)}"
        name = self._normalize_text(name).replace(" ", "_")
        return name

    def cache(self, func) -> Callable:
        """
        Decorator to cache the results of a function call.
        Parameters:
            func (function): function to be cached.
            base_dir (str): directory to store the cached results.
            use_sha256 (bool): whether to use sha256 hash for the cached file name.
        Returns:
        """
        self.logger.debug(f"Cache decorator called for function {func.__name__}")
        def wrapper(*args, **kwargs):
            hash_key = (
                func.__name__
                + "_"
                + self._sha256_hash(self._build_filename_from_params(*args, **kwargs))
            )
            file_name = hash_key + ".json"
            self.logger.debug(f"Cache file name: {file_name}")
            result = self.provider.read(
                file_name, func.__name__, self.cache_instance_id
            )
            self.logger.debug(f"Cache result: {result}")
            if not result:
                self.logger.debug("Cache miss")
                result = func(*args, **kwargs)
                self.provider.write(
                    file_name,
                    func.__name__,
                    result,
                    self.expiration_date,
                    self.cache_instance_id,
                )

            return result

        return wrapper

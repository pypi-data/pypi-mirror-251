from abc import ABC, abstractmethod
from ast import literal_eval
from datetime import datetime
from typing import Any


class BaseCacheProvider(ABC):
    def __init__(self) -> None:
        self._default_datetime_str_format = "%d-%m-%Y %H:%M:%S"

    @abstractmethod
    def read(self, file_name: str, func_name: str) -> Any:
        pass

    @abstractmethod
    def write(self, file_name: str, func_name: str, content: str) -> None:
        pass

    def _is_cached_result_valid(self, expiration_date: str) -> bool:
        """
        Check if the cached result is valid.
        Parameters:
            expiration_date (str): expiration date of the cached result.
        Returns:
            True if the cached result is valid, False otherwise.
        """
        if expiration_date == "never":
            return True
        else:
            return datetime.now() < datetime.strptime(
                expiration_date, self._default_datetime_str_format
            )

    def _has_expiration_changed(
        self, expiration_date: str, cached_expiration_date
    ) -> bool:
        """
        Check if the expiration date has changed.
        Parameters:
            expiration_date (str): expiration date of the cached result.
        Returns:
            True if the expiration date has changed, False otherwise.
        """
        return cached_expiration_date != expiration_date

    @staticmethod
    def _parse_types(res: str) -> Any:
        """
        Parse the type of the result.
        Parameters:
            res (str): result of the function call.
        Returns:
            The parsed result.
        """
        try:
            parsed_res = literal_eval(res)
        except:
            parsed_res = res

        return parsed_res

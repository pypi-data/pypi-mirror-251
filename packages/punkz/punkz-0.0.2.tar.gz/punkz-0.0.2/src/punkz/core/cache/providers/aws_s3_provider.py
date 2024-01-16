from datetime import datetime
from io import BytesIO
import json
from logging import Logger
import os
from typing import Any
from punkz.core.cache.providers import BaseCacheProvider
from punkz.packages.aws import AWS


class AWSS3CacheProvider(BaseCacheProvider):
    def __init__(
        self,
        bucket_name: str,
        access_key_id: str,
        secret_access_key: str,
        logger: Logger | None = None,
    ) -> None:
        super().__init__()
        self.logger = logger
        self.bucket_name = bucket_name
        self.aws = AWS(self.logger, access_key_id, secret_access_key)

    def read(
        self, file_name: str, func_name: str, cache_instance_id: str
    ) -> Any | None:
        cache_subfolder_name = func_name + "_cache"
        object_key = os.path.join(cache_instance_id, cache_subfolder_name, file_name)
        s3_object_metadata = self.aws.S3.get_object_metadata(
            self.bucket_name, object_key
        )
        if s3_object_metadata and self._is_cached_result_valid(
            s3_object_metadata["expiration"]
        ):
            bytes_content = self.aws.S3.download_bytes(
                self.bucket_name,
                object_key,
            )
            content_as_bytes = bytes_content.read()
            content = self._parse_types(content_as_bytes.decode("utf-8"))
            if content:
                return content["cached_data"]
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
        metadata = {
            "expiration": expiration_date,
        }
        json_cache_result = json.dumps(cache_result)
        in_memory_file = BytesIO(json_cache_result.encode("utf-8"))
        cache_subfolder_name = func_name + "_cache"
        object_key = os.path.join(cache_instance_id, cache_subfolder_name, file_name)
        self.aws.S3.upload_bytes(in_memory_file, self.bucket_name, object_key, metadata)


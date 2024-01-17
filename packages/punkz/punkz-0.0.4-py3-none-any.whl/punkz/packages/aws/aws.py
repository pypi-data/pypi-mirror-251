from logging import Logger
from typing import Any
from punkz.packages.aws.s3 import S3
from punkz.packages.log import get_logger
import boto3


class AWS:
    def __init__(
        self, logger: Logger | None, access_key_id: str, secret_access_key: str
    ) -> None:
        self.logger = logger

        self.aws_access_key_id = access_key_id
        self.aws_secret_access_key = secret_access_key
        boto3.setup_default_session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        self.S3 = S3(self.aws_access_key_id, self.aws_secret_access_key, logger)

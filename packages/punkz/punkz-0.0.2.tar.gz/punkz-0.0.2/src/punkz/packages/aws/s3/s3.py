from io import BytesIO
from logging import Logger
from typing import Any
import boto3
import botocore.exceptions
from punkz.packages.aws.progress import ProgressPercentage
import os


class S3:
    def __init__(
        self, aws_access_key_id: str, aws_secret_access_key: str, logger: Logger | None
    ) -> None:
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.logger = logger
        self.s3 = boto3.resource("s3")

    def get_file_list_from_s3(self, bucket_name: str) -> Any:
        """Get a list of files from an S3 bucket
        Args:
            bucket_name: Bucket to list files from
        Returns:
            List of files in the bucket
        """
        bucket = self.s3.Bucket(bucket_name)
        list_of_files = []
        for my_bucket_object in bucket.objects.all():
            list_of_files.append(my_bucket_object.key)
        message = f"List of files correctly retrieved from {bucket_name}"
        self.logger.debug(message) if self.logger else None
        return list_of_files

    def download_file(
        self,
        bucket_name: str,
        object_key: str,
        local_file_path: str,
        verbose: bool = False,
    ) -> Any:
        """Download a file to an S3 bucket
        Args:
            bucket_name: Bucket to download from
            object_key: S3 object key
            local_file_path: Path to the file you want to save (e.g. my_data/my_file.txt)
        Returns:
            The file from AWS S3
        """

        try:
            callback = (
                None
                if not verbose
                else ProgressPercentage(
                    filename=local_file_path,
                    filesize=self.s3.meta.client.head_object(
                        Bucket=bucket_name, Key=object_key
                    )["ContentLength"],
                    operation_type="Downloading",
                ),
            )

            self.s3.meta.client.download_file(
                bucket_name,
                object_key,
                local_file_path,
                Callback=callback,
            )

            message = f"File downloaded successfully: {local_file_path}"
            self.logger.debug(message) if self.logger else None
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                message = f"The object '{object_key}' does not exist in the bucket '{bucket_name}'."
                self.logger.error(message) if self.logger else print(message)
            else:
                message = f"Error downloading file: {e}"
                self.logger.error(message) if self.logger else print(message)

    def download_bytes(
        self, bucket_name: str, object_key: str, verbose: bool = False
    ) -> BytesIO:
        """Download a file to an S3 bucket as bytes
        Args:
            bucket_name: Bucket to download from
            object_key: S3 object key
            local_file_path: Path to the file you want to save (e.g. my_data/my_file.txt)
        Returns:
            The file from AWS S3
        """
        try:
            callback = (
                None
                if not verbose
                else ProgressPercentage(
                    filename=object_key,
                    filesize=self.s3.meta.client.head_object(
                        Bucket=bucket_name, Key=object_key
                    )["ContentLength"],
                    operation_type="Downloading",
                )
            )

            bytes_file = BytesIO()
            self.s3.meta.client.download_fileobj(
                bucket_name,
                object_key,
                bytes_file,
                Callback=callback,
            )
            message = f"File downloaded successfully: {object_key}"
            self.logger.debug(message) if self.logger else None
            bytes_file.seek(0)
            return bytes_file
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                message = f"The object '{object_key}' does not exist in the bucket '{bucket_name}'."
                self.logger.error(message) if self.logger else print(message)
            else:
                message = f"Error downloading file: {e}"
                self.logger.error(message) if self.logger else print(message)

    def upload_file(
        self,
        file_name: str,
        bucket_name: str,
        object_name: str = None,
        metadata: dict = None,
        verbose: bool = False,
    ) -> bool:
        """Upload a file to an S3 bucket
        Args:
            file_name: File to upload
            bucket: Bucket to upload to
            object_name: S3 object name. If not specified, file_name is used
            metadata: Metadata to associate with the uploaded object
        Returns:
            True if the file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            extra_args = {}
            if metadata:
                extra_args["Metadata"] = metadata

            file_size = float(os.path.getsize(file_name))
            callback = (
                None
                if not verbose
                else ProgressPercentage(
                    filename=file_name,
                    filesize=file_size,
                    operation_type="Uploading",
                )
            )

            response = self.s3.meta.client.upload_file(
                file_name,
                bucket_name,
                object_name,
                Callback=callback,
                ExtraArgs=extra_args,
            )
            message = f"File uploaded successfully: {file_name}"
            self.logger.debug(message) if self.logger else None
        except botocore.exceptions.ClientError as e:
            message = f"Error uploading file: {e}"
            self.logger.error(message) if self.logger else print(message)
            return False
        return True

    def upload_bytes(
        self,
        file: BytesIO,
        bucket_name: str,
        object_name: str,
        metadata: dict = None,
        verbose: bool = False,
    ) -> bool:
        """Upload a stream of bytes to an S3 bucket
        Args:
            file: File to upload in BytesIO format
            bucket: Bucket to upload to
            object_name: S3 object name
            metadata: Metadata to associate with the uploaded object
        Returns:
            True if the file was uploaded, else False
        """
        try:
            extra_args = {}
            if metadata:
                extra_args["Metadata"] = metadata

            file_size = float(len(file.getbuffer()))

            callback = (
                None
                if not verbose
                else ProgressPercentage(
                    filename=object_name,
                    filesize=file_size,
                    operation_type="Uploading",
                )
            )

            response = self.s3.meta.client.upload_fileobj(
                file,
                bucket_name,
                object_name,
                Callback=callback,
                ExtraArgs=extra_args,
            )
            message = f"Object uploaded successfully: {object_name}"
            self.logger.debug(message) if self.logger else None
        except botocore.exceptions.ClientError as e:
            message = f"Error uploading object: {e}"
            self.logger.error(message) if self.logger else print(message)
            return False
        return True

    def get_object_metadata(self, bucket_name: str, object_key: str) -> dict | None:
        """Get metadata of an object from an S3 bucket
        Args:
            bucket_name: Bucket containing the object
            object_key: S3 object key
        Returns:
            Metadata of the S3 object as a dictionary
        """
        try:
            response = self.s3.meta.client.head_object(
                Bucket=bucket_name, Key=object_key
            )
            message = f"Metadata of object '{object_key}' retrieved successfully."
            self.logger.debug(message) if self.logger else None
            return response.get("Metadata", {})
        except botocore.exceptions.ClientError as e:
            message = f"Error getting object metadata: {e}"
            self.logger.debug(message) if self.logger else None
            return None

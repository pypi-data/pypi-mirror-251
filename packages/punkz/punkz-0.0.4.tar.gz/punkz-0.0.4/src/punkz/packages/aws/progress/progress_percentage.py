import os
import sys
import threading


class ProgressPercentage(object):
    def __init__(self, filename: str, filesize: float, operation_type: str) -> None:
        self.operation_type = operation_type
        self._filename = filename
        self._size = filesize
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount: int) -> None:
        """
        Update the progress bar with the number of bytes received.

        Args:
            bytes_amount: The number of bytes received.
        """
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s %s  %s / %s  (%.2f%%)"
                % (
                    self.operation_type,
                    self._filename,
                    self._seen_so_far,
                    self._size,
                    percentage,
                )
            )
            sys.stdout.flush()

"""
This module provides a utility class, S3Downloader, for downloading files from Amazon S3 (Simple Storage Service) buckets. It utilizes the boto3 and s3transfer libraries to handle the connection and file transfer from S3 to the local filesystem efficiently and securely.

The S3Downloader class offers a convenient and straightforward static method for downloading files, abstracting the underlying boto3 session and transfer manager setup. This approach is useful in applications that require direct interaction with S3 for file downloads, such as data synchronization tasks, backup scripts, or data processing workflows.

Usage Example:
    # Specify the S3 bucket details and local file path
    bucket_name = 'my-bucket'  # Replace with your S3 bucket name
    s3_object_key = 'path/to/s3/object'  # Replace with the path to your S3 object
    local_file_path = 'path/to/local/file'  # Replace with the desired local path for the downloaded file

    # Call the static method to download the file
    S3Downloader.download_file_from_s3(bucket_name, s3_object_key, local_file_path)

Note:
    The module requires the installation of boto3 and s3transfer packages.
    Ensure that AWS credentials are configured properly for boto3 to access the specified S3 bucket.
"""

import os
import sys
import boto3
from s3transfer import TransferManager

OS_NAME = os.name
sys.path.append("../..")

if OS_NAME.lower() == "nt":
    print("environment_logging: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

from cdh_dav_python.cdc_admin_service.environment_logging import LoggerSingleton


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class S3Downloader:
    """
    This module provides a class for downloading files from an S3 bucket.

    Usage:
        bucket_name = 'my-bucket'  # Replace with your S3 bucket name
        s3_object_key = 'path/to/s3/object'  # Replace with the path to your S3 object
        local_file_path = 'path/to/local/file'  # Replace with the desired local path for the downloaded file

        S3Downloader.download_file_from_s3(bucket_name, s3_object_key, local_file_path)
    """

    @staticmethod
    def download_file_from_s3(
        bucket_name: str,
        s3_object_key: str,
        local_file_path: str,
        data_product_id: str,
        environment: str,
    ):
        """
        Downloads a file from an S3 bucket to a local file path.

        Args:
            bucket_name (str): The name of the S3 bucket.
            s3_object_key (str): The key of the S3 object.
            local_file_path (str): The local file path where the file will be downloaded.
            data_proudct_id (str): The ID of the data product.
            environment (str): The environment where the S3 bucket is located.

        Returns:
            None
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("fetch_and_save_pipeline"):
            try:
                # Create a boto3 session
                session = boto3.Session()

                # Create an S3 client
                s3 = session.client("s3")

                # Create a transfer manager
                transfer_manager = TransferManager(s3)

                # Download the file
                transfer_manager.download_file(
                    bucket=bucket_name, key=s3_object_key, fileobj=local_file_path
                )

                # Wait for the download to finish (optional, only if you need to block until download completes)
                transfer_manager.shutdown(wait=True)

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

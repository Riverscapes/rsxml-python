""" Verify Etags

This is just a little helper script to upload files to S3 using both single part
and multipart uploads, and then fetch the Etag from S3 to verify that our etag
calculation matches what S3 produces.

These values go into the test_etags.py unit tests to verify correctness of our etag calculations.

There is no reason to run this script other than to regenerate those values if the etag calculation
algorithm changes.

"""
import os

import boto3
import questionary
from botocore.exceptions import NoCredentialsError


def upload_file(file_path: str, bucket_name: str, object_name=None, force_multipart=False):
    """Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :param force_multipart: If True, forces multipart upload even for small files
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Upload the file
    s3_client = boto3.client('s3')

    try:
        print(f"Uploading {file_path} to {bucket_name}/{object_name}...")

        if force_multipart:
            # Force multipart upload configuration
            # Set threshold to 0 to force multipart for any file size
            config = boto3.s3.transfer.TransferConfig(
                multipart_threshold=1,
                multipart_chunksize=50 * 1024 * 1024  # 50MB chunks to match rsxml defaults
            )
            s3_client.upload_file(file_path, bucket_name, object_name, Config=config)
        else:
            # Standard upload (let boto3 decide, or force single part by setting high threshold)
            # To ensure single part for testing, we set a very high threshold
            config = boto3.s3.transfer.TransferConfig(
                multipart_threshold=10 * 1024 * 1024 * 1024  # 10GB threshold
            )
            s3_client.upload_file(file_path, bucket_name, object_name, Config=config)

        # Fetch the object to get the ETag
        response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
        remote_etag = response['ETag']
        print(f"Upload Successful. Remote ETag: {remote_etag}")
        return remote_etag

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"Upload failed: {e}")
        return None


def main():

    bucket_name = questionary.text("S3 Bucket name:").ask()
    s3_prefix = questionary.text("S3 Prefix (optional):", default="matt/s3etagtest").ask()
    if not bucket_name:
        return

    dir_path = questionary.path("Directory containing files to upload:").ask()
    if not dir_path:
        return

    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} does not exist.")
        return

    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and not f.startswith('.')]

    print(f"Found {len(files)} files in {dir_path}")

    for filename in files:
        file_path = os.path.join(dir_path, filename)

        print(f"\n--- Processing {filename} ---")

        # 1. Upload as Single Part (Standard MD5)
        print("1. Uploading as Single Part...")
        etag_single = upload_file(file_path, bucket_name, s3_prefix + f"/single_part/{filename}", force_multipart=False)

        # 2. Upload as Multipart
        print("2. Uploading as Multipart...")
        etag_multipart = upload_file(file_path, bucket_name, s3_prefix + f"/multipart/{filename}", force_multipart=True)
        print(f"Summary for {filename}:")
        print(f"  Single Part ETag: {etag_single}")
        print(f"  Multipart ETag:   {etag_multipart}")


if __name__ == "__main__":
    main()

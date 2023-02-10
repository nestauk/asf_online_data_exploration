"""
Utility functions for data collection.
"""

import json
import io
import boto3
import os
from asf_online_data_exploration import PROJECT_DIR


def dictionary_to_s3(data_dict: dict, s3_bucket: str, s3_folder: str, file_name: str):
    """
    Transforms a dictionary into a json and uploads to S3.
    Args:
        data_dict: dictionary with the data
        s3_bucket: S3 bucket name where to upload the file
        s3_folder: folder where to store the file within the S3 bucket
        file_name: name of the file
    """
    s3_client = boto3.client("s3")
    obj = io.BytesIO(json.dumps(data_dict).encode("utf-8"))
    s3_client.upload_fileobj(obj, s3_bucket, os.path.join(s3_folder, file_name))


def save_json_to_local_inputs_folder(data_dict: dict, folder: str, file_name: str):
    """
    Saves json file to local inputs folder.

    Args:
        data_dict: dictionary with the data
        folder: path to local folder, within the inputs/ folder, where to store data
        file_name: name of the file
    """

    path_local_inputs = os.path.join(PROJECT_DIR, "inputs/")
    full_path = os.path.join(path_local_inputs, folder)

    # Creates local folder path if it does not exist
    os.makedirs(full_path, exist_ok=True)

    obj = json.dumps(data_dict)
    # Writing to sample.json
    with open(os.path.join(full_path, file_name), "w") as outfile:
        outfile.write(obj)


def read_json_from_s3(bucket: str, file_path: str) -> dict:
    """
    Reads a json file from S3 without downloading it.

    Args:
        bucket: S3 bucket name
        file_path: file path (including file name)
    Returns:
        dictionary with json file data
    """
    s3_resource = boto3.resource("s3")
    json_file = s3_resource.Object(bucket, file_path)
    json_file = json_file.get()["Body"].read().decode("utf-8")
    return json.loads(json_file)


def read_json_from_local_path(file_path: str) -> dict:
    """
    Reads a json file from a local folder.

    Args:
        file_path: file path (including file name)
    Returns:
        dictionary with json file data
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    return data

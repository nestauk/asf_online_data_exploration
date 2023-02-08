"""
Script to test the data collection pipeline for The Guardian's Open Platform content endpoint.
"""

from asf_online_data_exploration.pipeline.data_collection.the_guardian import (
    collect_and_process_guardian_data,
)
from asf_online_data_exploration.config.data_collection_parameters import (
    query_parameters_guardian,
)
from asf_online_data_exploration.utils.data_collection_utils import read_json_from_s3
import os
import boto3
import pandas as pd
import time

S3_BUCKET = "asf-online-data-exploration"
DATA_COLLECTION_FOLDER = "inputs/data_collection/the_guardian/test/"

if __name__ == "__main__":
    print("Collecting The Guardian data...")

    test_ruleset_guardian = [
        {"value": '"heat pumps" AND cost', "tag": "testing_api"},
    ]

    query_parameters_guardian["from-date"] = "2022-01-01"
    query_parameters_guardian["to-date"] = "2022-06-01"

    collect_and_process_guardian_data(
        api_key="test",
        rules=test_ruleset_guardian,
        query_params=query_parameters_guardian,
        s3_bucket=S3_BUCKET,
        s3_folder=DATA_COLLECTION_FOLDER,
    )

    print("Finished data collection. Let's perform some tests.")

    query_tag = test_ruleset_guardian[0]["tag"]
    from_date = query_parameters_guardian["from-date"]
    to_date = query_parameters_guardian["to-date"]

    filename = f"guardian_{query_tag}_S{from_date}F{to_date}.json"
    data = read_json_from_s3(S3_BUCKET, file_path=f"{DATA_COLLECTION_FOLDER}{filename}")

    no_problem = True

    if len(data) != 51:
        print("Problem! Wrong number of results.")
        no_problem = False

    keys_intersection = set(data[0].keys()).intersection(
        [
            "id",
            "type",
            "sectionId",
            "sectionName",
            "webPublicationDate",
            "webTitle",
            "webUrl",
            "apiUrl",
            "isHosted",
            "pillarId",
            "pillarName",
        ]
    )
    if len(keys_intersection) != 11:
        print("Problem! Not all variables are being collected.")
        no_problem = False

    if no_problem:
        print("All tests passed!")

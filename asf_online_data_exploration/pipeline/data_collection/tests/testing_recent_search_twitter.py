"""
Script to test the data collection pipeline for Twitter's recent search endpoint.

Data is collected from the API twice (program sleeps for 3 minutes in between) for two different rules.
Then the following checks are performed:
- if no repeated tweets are collected (for the same tag, at different times).

Not being checked and why:
- Not checking if all expected variables are present, as these might not be present if all values are missing
(e.g. one might want to collect geolocation parameters, but geolocation is always missing, the 'geo' field won't be retrieved)
"""

import pytest
from asf_online_data_exploration.pipeline.data_collection.recent_search_twitter import (
    collect_and_process_twitter_data,
)
from asf_online_data_exploration.config.data_collection_parameters import (
    query_parameters_twitter,
)
from asf_online_data_exploration.utils.data_collection_utils import read_json_from_s3
import os
import boto3
import pandas as pd
import time

S3_BUCKET = "asf-online-data-exploration"
DATA_COLLECTION_FOLDER = "inputs/data_collection/recent_search_twitter/test/"


def test_data_collected_from_api():
    """
    Tests data collected from Twitter's API v2:
    - if no repeated tweets are collected (for the same tag, at different times)
    """

    test_ruleset_twitter = [
        {
            "value": '"my cute dog" OR "my cute cat" -is:retweet',
            "tag": "testing_api_t1",
        },
        {
            "value": '"heat pump" (noise OR noisy OR installation) -is:retweet',
            "tag": "testing_api_t2",
        },
    ]

    # Collecting data twice to check if the since_id is working
    collect_and_process_twitter_data(
        bearer_token=os.environ.get("BEARER_TOKEN"),
        rules=test_ruleset_twitter,
        query_params=query_parameters_twitter,
        s3_bucket=S3_BUCKET,
        s3_folder=DATA_COLLECTION_FOLDER,
    )

    time.sleep(60 * 3)  # Sleeping 3 min between data collections

    collect_and_process_twitter_data(
        bearer_token=os.environ.get("BEARER_TOKEN"),
        rules=test_ruleset_twitter,
        query_params=query_parameters_twitter,
        s3_bucket=S3_BUCKET,
        s3_folder=DATA_COLLECTION_FOLDER,
    )

    # Let's check if IDs are unique
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(S3_BUCKET)

    # all data collection files stored in S3
    files = [
        objects.key for objects in bucket.objects.filter(Prefix=DATA_COLLECTION_FOLDER)
    ]

    for i in range(len(test_ruleset_twitter)):
        tag = test_ruleset_twitter[i]["tag"]
        files_tag = [f for f in files if tag in f]
        files_tag.sort(reverse=True)
        # only checks latest files, if this script is run more than once
        files_tag = files_tag[:2]

        file_1 = read_json_from_s3(S3_BUCKET, files_tag[0])
        file_1 = pd.DataFrame(file_1["data"])
        file_2 = read_json_from_s3(S3_BUCKET, files_tag[1])
        file_2 = pd.DataFrame(file_2["data"])

        # check if there are IDs in common in the two data collection instances
        if (len(file_1) != 0) and (len(file_2) != 0):
            ids_intersection = set(file_1["id"]).intersection(file_2["id"])
            assert len(ids_intersection) == 0

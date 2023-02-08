"""
Script to test the data collection pipeline for Twitter's recent search endpoint.

We collect data from the API twice (program sleeps for 3 minutes in between) for two different rules
to check if the there are any common tweet IDs in the files for the same rule (there shouldn't be).
"""

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

if __name__ == "__main__":
    print("Collecting Twitter data...")

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
    print("Sleeping 3 min between data collections.")
    time.sleep(60 * 3)
    collect_and_process_twitter_data(
        bearer_token=os.environ.get("BEARER_TOKEN"),
        rules=test_ruleset_twitter,
        query_params=query_parameters_twitter,
        s3_bucket=S3_BUCKET,
        s3_folder=DATA_COLLECTION_FOLDER,
    )

    print(
        f"Twitter data collected. You can find the files on S3 -> bucket: {S3_BUCKET}, folder: {DATA_COLLECTION_FOLDER}"
    )

    print("Let's check if IDs are unique...")

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

        no_problem = True
        # check if there are IDs in common in the two data collection instances
        if (len(file_1) != 0) and (len(file_2) != 0):
            ids_intersection = set(file_1["id"]).intersection(file_2["id"])
            if len(ids_intersection) > 0:
                print(
                    f"Problem! Files with data collected for tag {tag} have IDs in common."
                )
                no_problem = False
        if no_problem:
            print("All tests passed!")

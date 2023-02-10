"""
Script to test the data collection pipeline for The Guardian's Open Platform content endpoint.

Checks performed:
- all expected variables are present;
- expected number of results.
"""

import pytest
import os
from asf_online_data_exploration.pipeline.data_collection.the_guardian import (
    collect_and_process_guardian_data,
)
from asf_online_data_exploration.config.data_collection_parameters import (
    query_parameters_guardian,
)
from asf_online_data_exploration.utils.data_collection_utils import read_json_from_s3
from asf_online_data_exploration import base_config, PROJECT_DIR

S3_BUCKET = base_config["S3_BUCKET"]
S3_DATA_COLLECTION_FOLDER = base_config["THE_GUARDIAN_S3_TEST_DATA_COLLECTION_FOLDER"]
LOCAL_DATA_COLLECTION_FOLDER = base_config[
    "THE_GUARDIAN_LOCAL_TEST_DATA_COLLECTION_FOLDER"
]


def test_data_collected_from_api():
    """
    Tests data collected from The Guardian Open Platform:
    - if all expected variables are present;
    - if the expected number of results was collected.
    """

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
        folder=S3_DATA_COLLECTION_FOLDER,
    )

    query_tag = test_ruleset_guardian[0]["tag"]
    from_date = query_parameters_guardian["from-date"]
    to_date = query_parameters_guardian["to-date"]

    filename = f"guardian_{query_tag}_S{from_date}F{to_date}.json"
    data = read_json_from_s3(
        S3_BUCKET, file_path=os.path.join(S3_DATA_COLLECTION_FOLDER, filename)
    )

    assert (
        len(data) == 60
    )  # we know this value from this explorer: https://open-platform.theguardian.com/explore/

    for key in [
        "id",
        "type",
        "sectionId",
        "sectionName",
        "webPublicationDate",
        "webTitle",
        "webUrl",
        "apiUrl",
        "fields",
        "isHosted",
        "pillarId",
        "pillarName",
    ]:
        assert key in data[0].keys()

    for key in [
        "headline",
        "standfirst",
        "trailText",
        "byline",
        "main",
        "body",
        "newspaperPageNumber",
        "wordcount",
        "firstPublicationDate",
        "isInappropriateForSponsorship",
        "isPremoderated",
        "lastModified",
        "newspaperEditionDate",
        "productionOffice",
        "publication",
        "shortUrl",
        "shouldHideAdverts",
        "showInRelatedContent",
        "thumbnail",
        "legallySensitive",
        "lang",
        "isLive",
        "bodyText",
        "charCount",
        "shouldHideReaderRevenue",
        "showAffiliateLinks",
        "bylineHtml",
    ]:
        assert key in data[0]["fields"].keys()


def test_saving_locally():
    """
    Testing the option of saving data to local folder.
    """

    test_ruleset_guardian = [
        {"value": '"heat pumps" AND cost', "tag": "testing_api"},
    ]

    query_parameters_guardian["from-date"] = "2022-01-01"
    query_parameters_guardian["to-date"] = "2022-06-01"

    collect_and_process_guardian_data(
        api_key="test",
        rules=test_ruleset_guardian,
        query_params=query_parameters_guardian,
        folder=LOCAL_DATA_COLLECTION_FOLDER,
    )

    query_tag = test_ruleset_guardian[0]["tag"]
    from_date = query_parameters_guardian["from-date"]
    to_date = query_parameters_guardian["to-date"]

    path_to_folder = os.path.join(PROJECT_DIR / "inputs/", LOCAL_DATA_COLLECTION_FOLDER)
    filename = f"guardian_{query_tag}_S{from_date}F{to_date}.json"
    path_to_file = os.path.join(path_to_folder, filename)
    assert os.path.exists(path_to_file)

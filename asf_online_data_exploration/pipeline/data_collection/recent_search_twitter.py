"""
Script to collect Twitter data from the past 7 days using the recent search endpoint, given a set of rules and query parameters.
If data on a specific ruleset has been collected sometime in the past 7 days, only new data gets collected.
"""

import requests
import json
import time
import random
import boto3
import json
from datetime import datetime, timedelta
import pandas as pd
import os
from asf_online_data_exploration.config.data_collection_parameters import (
    heating_technologies_ruleset_twitter,
    query_parameters_twitter,
)
from asf_online_data_exploration.utils.data_collection_utils import (
    dictionary_to_s3,
    read_json_from_s3,
)

ENDPOINT_URL = "https://api.twitter.com/2/tweets/search/recent"
S3_BUCKET = "asf-online-data-exploration"
DATA_COLLECTION_FOLDER = "inputs/data_collection/recent_search_twitter/"


def request_headers(bearer_token: str) -> dict:
    """
    Set up the request headers.
    Returns a dictionary summarising the bearer token authentication details.

    Args:
        bearer_token: bearer token credentials
    """
    return {"Authorization": "Bearer {}".format(bearer_token)}


def connect_to_endpoint(headers: dict, parameters: dict) -> json:
    """
    Connects to the endpoint and requests data.
    Returns a json with Twitter data if a 200 status code is yielded.
    Programme stops if there is a problem with the request and sleeps
    if there is a temporary problem accessing the endpoint.

    Args:
        headers: request headers
        parameters: query parameters
    """

    response = requests.request(
        "GET", url=ENDPOINT_URL, headers=headers, params=parameters
    )
    response_status_code = response.status_code
    if response_status_code != 200:
        if response_status_code >= 400 and response_status_code < 500:
            raise Exception(
                "Cannot get data, the program will stop!\nHTTP {}: {}".format(
                    response_status_code, response.text
                )
            )

        sleep_seconds = random.randint(5, 60)
        print(
            "Cannot get data, your program will sleep for {} seconds...\nHTTP {}: {}".format(
                sleep_seconds, response_status_code, response.text
            )
        )
        time.sleep(sleep_seconds)
        return connect_to_endpoint(headers, parameters)
    # sleeping 5 seconds not to surpass rate limit
    time.sleep(5)
    return response.json()


def process_twitter_data(json_response: json, data: list) -> list:
    """
    Processes new Twitter data.

    Args:
        json_response: new data collected from the endpoint
        data: all data

    Returns:
        Returns updated data.
    """
    if "data" in json_response.keys():
        data["data"] = data["data"] + json_response["data"]

        if "users" in json_response["includes"].keys():
            data["includes"]["users"] = (
                data["includes"]["users"] + json_response["includes"]["users"]
            )

        if "places" in json_response["includes"].keys():
            data["includes"]["places"] = (
                data["includes"]["places"] + json_response["includes"]["places"]
            )

        if "media" in json_response["includes"].keys():
            data["includes"]["media"] = (
                data["includes"]["media"] + json_response["includes"]["media"]
            )

    return data


def empty_data_dict() -> dict:
    """
    Creates and returns an empty Twitter style endpoint dictionary output.
    """
    data = dict()
    data["data"] = []
    data["includes"] = dict()
    data["includes"]["users"] = []
    data["includes"]["places"] = []
    data["includes"]["media"] = []

    return data


def get_max_ids_json(s3_bucket, s3_folder) -> dict:
    """
    Gets max_tweet_id.json file from S3 if it exists. Otherwise, it creates one.
    This file contains information about the latest tweet ID collected for a specific
    rule.
    Arg:
        s3_bucket: name of S3 bucket where file is stored
        s3_folder: folder where file is stored within the S3 bucket
    Returns:
        Dictionary with latest tweet IDs collected so far.
    """
    # Connecting to s3
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(s3_bucket)

    # Check if we already have a json with information about previous data collections
    data_collection_json = [
        objects.key for objects in bucket.objects.filter(Prefix=s3_folder)
    ]
    if f"{s3_folder}max_tweet_id.json" in data_collection_json:
        max_ids_json = read_json_from_s3(
            s3_bucket, file_path=f"{s3_folder}max_tweet_id.json"
        )
    else:  # if not, we create one
        max_ids_json = dict()

    return max_ids_json


def update_max_ids_json(
    json_response, max_ids_json, query_tag, date_time_collection_start
):
    """
    Updates dictionary with latest tweet IDs collected so far for a specific query tag:
    - newest_id is extracted from the json response metadata
    - info about when the latest ID was posted
    - collection datetime

    Args:
        json_response: json response from API call (contains data collected)
        max_ids_json: dictionary with latest tweet IDs collected
        query_tag: tag for query we are collecting data on
        date_time_collection_start: date time we started data collection
    """
    # newest id info
    newest_id = json_response["meta"]["newest_id"]
    max_ids_json[query_tag]["newest_id"] = newest_id
    data_df = pd.DataFrame(json_response["data"])

    # newest id datetime created
    max_id_datetime = data_df[data_df["id"] == newest_id]["created_at"].iloc[0]
    max_ids_json[query_tag]["created_at"] = max_id_datetime

    # data collection date time
    max_ids_json[query_tag]["collection_datetime"] = date_time_collection_start


def collect_and_process_twitter_data(
    bearer_token: str, rules: list, query_params: dict, s3_bucket: str, s3_folder: str
):
    """
    Collects, processes and saves twitter data following a set of rules and query parameters.

    If "max_tweet_id.json" exists on S3, it collects data since the last ID collected in a
    previous instance. Otherwise, it collects data from the past 7 days.

    Args:
        bearer_token: Twitter bearer token credentials
        rules: rules for collecting Twitter data. Each rules should contain "value" and "tag" keys
        query_paramers: parameters for data collection
    """

    # Authentication with bearer token
    headers = request_headers(bearer_token)

    # Date time when collection is starting
    date_time_collection_start = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # Getting info about latest collected tweets
    max_ids_json = get_max_ids_json(s3_bucket, s3_folder)

    # data collection for every possible rule
    for i in range(len(rules)):
        # starting with an empty dictionary to store all data
        data = empty_data_dict()

        # Altering query parameters to account for each rule
        query_params["query"] = rules[i]["value"]
        query_tag = rules[i]["tag"]

        # Checking if we have info about the latest tweet ID collected for the query_tag
        if (query_tag in max_ids_json.keys()) and (
            "newest_id" in max_ids_json[query_tag].keys()
        ):
            # We only use the since_id param if that latest tweet ID collected was posted in the past 7 days
            created_at = datetime.strptime(
                max_ids_json[query_tag]["created_at"], "%Y-%m-%dT%H:%M:%S.000Z"
            )
            if created_at + timedelta(7) > datetime.now():
                query_params["since_id"] = max_ids_json[query_tag]["newest_id"]
        else:
            max_ids_json[query_tag] = dict()

        # Collecting and processing data
        json_response = connect_to_endpoint(headers, query_params)
        data = process_twitter_data(json_response, data)

        # Define a filename and uploading data to s3
        filename = f"recent_search_{query_tag}_{date_time_collection_start}.json"
        dictionary_to_s3(data, s3_bucket, s3_folder, filename)

        # updating json with info about max tweet id collected, to be used next time we collect data
        # note that first page of tweets contains the newest possible tweets
        if "newest_id" in json_response["meta"].keys():
            # Updating json with max tweet id collected
            update_max_ids_json(
                json_response, max_ids_json, query_tag, date_time_collection_start
            )

        # collect tweets from next pages
        while "next_token" in json_response["meta"]:
            query_params["next_token"] = json_response["meta"]["next_token"]

            json_response = connect_to_endpoint(headers, query_params)
            data = process_twitter_data(json_response, data)

            # Uploading to S3
            dictionary_to_s3(data, s3_bucket, s3_folder, filename)

        # Saving max_tweet_id.json to s3 after finishing data collection for the current rule
        dictionary_to_s3(max_ids_json, s3_bucket, s3_folder, "max_tweet_id.json")

        # Removing these from query parameters before collecting data for next rule
        for key in ["query", "since_id"]:
            query_params.pop(key, None)


if __name__ == "__main__":
    bearer_token = os.environ.get("BEARER_TOKEN")

    collect_and_process_twitter_data(
        bearer_token=bearer_token,
        rules=heating_technologies_ruleset_twitter,
        query_params=query_parameters_twitter,
        s3_bucket=S3_BUCKET,
        s3_folder=DATA_COLLECTION_FOLDER,
    )

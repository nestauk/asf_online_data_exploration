"""
Script to collect data from The Guardian Open Platform on a topic of choice using the content endpoint.

A developer is allowed to make up to 500 calls per day and 1 call per second.
"""

import requests
import json
import time
import random
import json
import os
from datetime import datetime
from asf_online_data_exploration.config.data_collection_parameters import (
    heating_technologies_ruleset_guardian,
    query_parameters_guardian,
    dates_for_guardian_collection,
)
from asf_online_data_exploration.utils.data_collection_utils import dictionary_to_s3

ENDPOINT_URL = "https://content.guardianapis.com/search?"
S3_BUCKET = "asf-online-data-exploration"
DATA_COLLECTION_FOLDER = "inputs/data_collection/the_guardian/"


def define_endpoint_url(api_key, query_params):
    """
    Defines endpoint url starting from the base content endpoint URL and
    using the api_key and query parameters.
    Args:
        api_key: API key credentials
        query_params: query parameters
    Returns:
        Endpoint URL ready for API call
    """
    url = f"{ENDPOINT_URL}&api-key={api_key}"
    for key in query_params.keys():
        url = url + f"&{key}={query_params[key]}"
    return url


def connect_to_endpoint(endpoint_url: str) -> json:
    """
    Connects to the endpoint and requests data.
    Returns a json with The Guardian data if a 200 status code is yielded.
    Programme stops if there is a problem with the request and sleeps
    if there is a temporary problem accessing the endpoint.

    Args:
        endpoint_url: url to endpoint
    """
    response = requests.request("GET", url=endpoint_url)
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
        return connect_to_endpoint(endpoint_url)
    # sleep 1 second not to surpass rate limit
    time.sleep(1)
    return response.json()["response"]


def collect_and_process_guardian_data(
    api_key, rules, query_params, s3_bucket: str, s3_folder: str
):
    """
    Collects, processes and saves The Guardian data following a set of rules and query parameters.

    Args:
        api_key: API key credentials
        rules: rules for collecting Twitter data. Each rules should contain "value" and "tag" keys
        query_paramers: parameters for data collection
    """
    from_date = query_params.get("from-date", "").replace("/", "_") 
    to_date = query_params.get("to-date", "").replace("/", "_") 
    specified_time_frame_flag = "from-date" in query_params

    # data collection for every possible rule
    for rule in rules:
        query_params["q"] = rule["value"]
        query_tag = rule["tag"]

        endpoint_url = define_endpoint_url(api_key, query_params)

        # Collecting and processing data
        json_response = connect_to_endpoint(endpoint_url)
        data = json_response["results"]

        # Extracting parameters from json response
        total_pages = json_response["pages"]
        current_page = json_response["currentPage"]  # this should be 1

        # Define a filename and uploading data to s3
        if specified_time_frame_flag:
            filename = f"guardian_{query_tag}_S{from_date}F{to_date}.json"
        else:
            filename = f"guardian_{query_tag}_{datetime.now()}.json"
        dictionary_to_s3(data, s3_bucket, s3_folder, filename)

        current_page += 1
        while current_page <= total_pages:
            # Adding the current page to the query parameters
            query_params["page"] = current_page
            endpoint_url = define_endpoint_url(api_key, query_params)

            # Collecting and processing data
            json_response = connect_to_endpoint(endpoint_url)
            data = data + json_response["results"]

            # Uploading to S3
            dictionary_to_s3(data, s3_bucket, s3_folder, filename)

            current_page += 1

        # Removing page from query_params for next rule's collection to start at page 1
        query_params.pop("page", None)


if __name__ == "__main__":
    guardian_api_key = os.environ.get("GUARDIAN_API_KEY")

    for date in dates_for_guardian_collection:
        query_parameters_guardian["from-date"] = date[
            "from-date"
        ]
        query_parameters_guardian["to-date"] = date[
            "to-date"
        ]

        collect_and_process_guardian_data(
            guardian_api_key,
            heating_technologies_ruleset_guardian,
            query_parameters_guardian,
            S3_BUCKET,
            DATA_COLLECTION_FOLDER,
        )

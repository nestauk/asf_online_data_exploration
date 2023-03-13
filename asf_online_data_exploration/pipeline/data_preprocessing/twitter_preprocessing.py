import pandas as pd
import os
import boto3
from nesta_ds_utils.loading_saving.S3 import (
    get_bucket_filenames_s3,
    download_obj,
    upload_obj,
)
from asf_online_data_exploration import base_config
from asf_online_data_exploration.config import data_collection_parameters

S3_BUCKET = base_config["S3_BUCKET"]
TWITTER_CONCATENATED_FILES_PATH = base_config["TWITTER_CONCATENATED_FILES_PATH"]
tags = [
    rule["tag"]
    for rule in data_collection_parameters.heating_technologies_ruleset_twitter
]


def append_new_data(
    data_table: pd.DataFrame, new_data: dict, tag: str, collection_datetime: str
) -> pd.DataFrame:
    """
    Transforms new data from dictionary to dataframe, adds the data collection tag
    and collection datetime as variables and then appends new data to the dataframe with all data.
    Args:
        data_table: data table with all data appended so far.
        new_data: new data to be added to data_table
        tag: data collection tag (e.g. "ashp" stading for Air Source Heat Pumps)
        collection_datetime: data collection datetime
    Returns:
        Updated data_table with new data.
    """
    new_data = pd.DataFrame(new_data)

    if len(new_data) > 0:  # some files have no data
        new_data["tag"] = tag
        new_data["collection_date_time"] = collection_datetime

        data_table = pd.concat([data_table, new_data])
    return data_table


def identify_tag(file_name: str) -> str:
    """
    Identifies which tag is in file name.
    """
    for tag in tags:
        if tag in file_name:
            return tag


def extract_prefix_from_file_name(file_name: str) -> str:
    """
    Extracts file prefix from file name (one or more tokens separated by an underscore).
    Args:
        file_name: file name following the structure: "file_name_prefix_specific_tag_YYYY_MM_DD"
        where "specific_tag" is a tag in tags.
    Returns:
        The file name prefix (if applied to the example above, would return "file_name_prefix")
    """
    tag = identify_tag(file_name)
    file_prefix = file_name.split(tag)[0]
    file_prefix = file_prefix[:-1]  # removing "_"
    return file_prefix


def download_concatenated_data(file_prefix: str) -> tuple:
    """
    Downloads the tweets, users, places and media concatenated tables from S3 to memory.

    Args:
        file_prefix: file prefix to look for.
    Returns:
        tweets table, users_tale, places_table, media_table
    """
    tweets_table = download_obj(
        bucket_name=S3_BUCKET,
        path_from=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_tweets.csv"
        ),
        download_as="dataframe",
    )
    users_table = download_obj(
        bucket_name=S3_BUCKET,
        path_from=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_users.csv"
        ),
        download_as="dataframe",
    )
    places_table = download_obj(
        bucket_name=S3_BUCKET,
        path_from=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_places.csv"
        ),
        download_as="dataframe",
    )
    media_table = download_obj(
        bucket_name=S3_BUCKET,
        path_from=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_media.csv"
        ),
        download_as="dataframe",
    )

    return tweets_table, users_table, places_table, media_table


def update_tables_with_new_data(
    new_data: dict,
    tweets_table: pd.DataFrame,
    users_table: pd.DataFrame,
    places_table: pd.DataFrame,
    media_table: pd.DataFrame,
    tag: str,
    collection_datetime: str,
) -> tuple:
    """
    Updates the data tables (tweets_table, users_table, places_table and media_table) with new data.
    Args:
        new_data: new data
        tweets_table: table with tweets information
        users_table: table with users infomration
        places_table: table with places information
        media_table: table with mediainformation
        tag: data collection tag
        collection_datetime: data collection datetime
    Returns:
        Updated tweets_table, users_table, places_table and media_table
    """
    tweets_table = append_new_data(
        tweets_table, new_data["data"], tag=tag, collection_datetime=collection_datetime
    )
    users_table = append_new_data(
        users_table,
        new_data["includes"]["users"],
        tag=tag,
        collection_datetime=collection_datetime,
    )
    places_table = append_new_data(
        places_table,
        new_data["includes"]["places"],
        tag=tag,
        collection_datetime=collection_datetime,
    )
    media_table = append_new_data(
        media_table,
        new_data["includes"]["media"],
        tag=tag,
        collection_datetime=collection_datetime,
    )

    return tweets_table, users_table, places_table, media_table


def upload_all_tables(
    tweets_table, users_table, places_table, media_table, file_prefix
):
    """
    Uploads the data tables (tweets_table, users_table, places_table and media_table) to S3.
    Args:
        tweets_table: table with tweets information
        users_table: table with users infomration
        places_table: table with places information
        media_table: table with media information
        file_prefix: file name prefix
    """
    upload_obj(
        obj=tweets_table,
        bucket=S3_BUCKET,
        path_to=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_tweets.csv"
        ),
    )
    upload_obj(
        obj=users_table,
        bucket=S3_BUCKET,
        path_to=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_users.csv"
        ),
    )
    upload_obj(
        obj=places_table,
        bucket=S3_BUCKET,
        path_to=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_places.csv"
        ),
    )
    upload_obj(
        obj=media_table,
        bucket=S3_BUCKET,
        path_to=os.path.join(
            TWITTER_CONCATENATED_FILES_PATH, f"/{file_prefix}_media.csv"
        ),
    )


def map_file_names_to_last_modified(bucket_name, path_to_files):
    """ """
    session = boto3.session.Session()
    s3_resource = session.resource("s3")
    list_contents_in_path = s3_resource.meta.client.list_objects(
        Bucket=bucket_name, Prefix=path_to_files
    )["Contents"]

    return {file["Key"]: file["LastModified"] for file in list_contents_in_path}


def get_everything_after_tag(file_name):
    tag = identify_tag(file_name)
    return file_name.split(tag)[1]


def concatenate_and_upload_data(raw_data_path):
    """
    Concatenates files found under a specific directory on an S3 bucket
    that have one of the data collection tags that haven't been concatenated
    (this is checked using the metadata.json file). The concatenated file is
    uploaded to S3.

    Args:
        raw_data_path: path to S3 bucket directory.
    """

    raw_data_dir_name = raw_data_path.split("/")[-2]  # dir name only

    # check if there are concatenated outputs already on S3
    files_in_concatenated_path = get_bucket_filenames_s3(
        bucket_name=S3_BUCKET, dir_name=TWITTER_CONCATENATED_FILES_PATH
    )
    metadata_file_path = os.path.join(TWITTER_CONCATENATED_FILES_PATH, "metadata.json")

    # if there are concatenated outputs already on S3, last_file_name_concatenated is last file_name already concatenated
    last_file_name_concatenated = ""
    if metadata_file_path in files_in_concatenated_path:
        metadata = download_obj(
            bucket_name=S3_BUCKET, path_from=metadata_file_path, download_as="dict"
        )
        if raw_data_dir_name in metadata.keys():
            last_file_name_concatenated = metadata[raw_data_dir_name]
    else:  # no metadata file in concatenated outputs, so nothing has been concatenated yet
        metadata = dict()

    # file_names will have sorted file names to concatenate
    file_names = get_bucket_filenames_s3(bucket_name=S3_BUCKET, dir_name=raw_data_path)
    file_names = [f for f in file_names if f.endswith(".json")]
    file_names = [f for f in file_names if "test/" not in f]
    file_names.remove(
        os.path.join(raw_data_path, "max_tweet_id.json")
    )  # removing the data collection metadata file
    file_names.sort(key=get_everything_after_tag)

    file_prefix = extract_prefix_from_file_name(file_names[0])
    print("file_prefix")
    print(file_prefix)

    # if some files have already been concatenated we assess where to start and download concatenated data so far
    if last_file_name_concatenated != "":
        index_start = file_names.index(last_file_name_concatenated) + 1
        file_names = file_names[index_start:]
        (
            tweets_table,
            users_table,
            places_table,
            media_table,
        ) = download_concatenated_data(file_prefix)
    else:  # no files have been concatenated yet
        tweets_table, users_table, places_table, media_table = (
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
        )

    print("last_file_name_concatenated")
    print(last_file_name_concatenated)

    mapping_filename_lastmodified = map_file_names_to_last_modified(
        S3_BUCKET, raw_data_path
    )
    # if there's at least one new file to concatenate
    if len(file_names) != 0:
        for file in file_names:
            print("file: " + file)
            input_json = download_obj(
                bucket=S3_BUCKET, path_from=file, download_as="dict"
            )
            tag = identify_tag(file)
            collection_datetime = mapping_filename_lastmodified[file]
            (
                tweets_table,
                users_table,
                places_table,
                media_table,
            ) = update_tables_with_new_data(
                input_json,
                tweets_table,
                users_table,
                places_table,
                media_table,
                tag,
                collection_datetime,
            )

        upload_all_tables(
            tweets_table, users_table, places_table, media_table, file_prefix
        )
        metadata[raw_data_dir_name] = file
        print("metadata")
        print(metadata)
        upload_obj(
            obj=metadata,
            bucket=S3_BUCKET,
            path_to=os.path.join(TWITTER_CONCATENATED_FILES_PATH, "metadata.json"),
        )
    else:
        raise IOError("No new files to concatenate!")


def preprocess_data(concatenated_data_dir):
    """
    Preprocesses Twitter data and saves resulting tables to S3.
    """


if __name__ == "__main__":
    raw_data_path = "inputs/data_collection/recent_search_twitter/"
    concatenate_and_upload_data(raw_data_path)

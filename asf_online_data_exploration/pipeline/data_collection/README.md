# Data collection pipeline

This directory contains scripts for collecting data from **Twitter API v2 recent endpoint** and from **The Guardian Open Platform content endpoint**.

## Twitter API v2 recent search

The `recent_search_twitter.py` script contains the pipeline for collecting Twitter data from the past 7 days on set of parameters using the recent search endpoint.

Running `asf_online_data_exploration/pipeline/data_collection/recent_search_twitter.py` will collect data from the past 7 days on a set of parameters that can be found under `asf_online_data_exploration/config/data_collection_parameters.py`. Data is stored to the `asf-online-data-exploration` S3 bucket.

Alternatively, to perform your own data collection create a script with the following code

```
from asf_online_data_exploration.pipeline.data_collection.the_guardian import (
    collect_and_process_twitter_data,
)

ruleset = [{"value": ..., "tag": ...}]
query_parameters_twitter = [...]
S3_BUCKET = ...
DATA_COLLECTION_FOLDER = ...

collect_and_process_twitter_data(
        bearer_token=os.environ.get("BEARER_TOKEN"),
        rules=ruleset,
        query_params=query_parameters_twitter,
        s3_bucket=S3_BUCKET,
        s3_folder=DATA_COLLECTION_FOLDER,
    )
```

## The Guardian Open platform

The `the_guardian.py` script contains the pipeline for collecting news articles from The Guardian Open Platform on a set of parameters.

Running `asf_online_data_exploration/pipeline/data_collection/the_guardian.py` will collect news articles on a set of parameters that can be found under `asf_online_data_exploration/config/data_collection_parameters.py`. Data is stored to the `asf-online-data-exploration` S3 bucket.

Alternatively, to perform your own data collection create a script with the following code

```
from asf_online_data_exploration.pipeline.data_collection.the_guardian import (
    collect_and_process_guardian_data,
)

api_key = ...
ruleset = [{"value": ..., "tag": ...}]
query_parameters_guardian = []
S3_BUCKET = ...
DATA_COLLECTION_FOLDER = ...

collect_and_process_guardian_data(
        api_key=api_key,
        rules=ruleset,
        query_params=query_parameters_guardian,
        s3_bucket=S3_BUCKET,
        s3_folder=DATA_COLLECTION_FOLDER,
    )
```

## Resources

[to be improved...]

### Twitter API v2

In order to collect data from Twitter, you need to have a [developer account](https://developer.twitter.com/en/portal/petition/essential/basic-info).

- [How to build queries or the recent search endpoint](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)
- [Data dictionaries](https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet)

### The Guardian Open Platform

- [Create an account and request API key](https://open-platform.theguardian.com/access/)
- [The Guardian Open Platform Explorer](https://open-platform.theguardian.com/explore/)
- [The Guardian Open Platform API documentation](https://open-platform.theguardian.com/documentation/)

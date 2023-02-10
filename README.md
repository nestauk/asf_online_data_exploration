# asf_online_data_exploration

## Summary

This repo contains scripts for exploring **online data** from sources such as Twitter, online news outlets or online forums, with the main aim of generating ideas for ASF projects involving opinions/thoughts shared by different types of users online.

## Data Collection

Our [data collection pipeline](https://github.com/nestauk/asf_online_data_exploration/tree/dev/asf_online_data_exploration/pipeline/data_collection) contains functions to collect data from Twitter's API v2 recent search endpoint and from The Guardian Open Platform content endpoint.

Both require access to developer credentials:

- [Apply for Twitter Developer credentials](https://developer.twitter.com/en/portal/petition/essential/basic-info);
- [Apply for The Guardian Open Platform credentials](<(https://open-platform.theguardian.com/access/)>).

## Processing

Coming soon...

## Prototype

Coming soon...

## Setup

- Meet the data science cookiecutter [requirements](http://nestauk.github.io/ds-cookiecutter/quickstart), in brief:
  - Install: `direnv` and `conda`
- Run `make install` to configure the development environment:
  - Setup the conda environment
  - Configure `pre-commit`
- Run `direnv allow`;
- Activate conda enviroment
  - `conda activate asf_online_data_exploration`
- Set your credentials as enviroment variables
  - `export BEARER_TOKEN="ADD_YOUR_BEARER_TOKEN_HERE"` and replace `ADD_YOUR_BEARER_TOKEN_HERE` with your bearer token credentials.
  - `export GUARDIAN_API_KEY="ADD_YOUR_API_KEY_HERE"` and replace `ADD_YOUR_API_KEY_HERE` with your API key credentials. Alternatively, set `export GUARDIAN_API_KEY="test"`

## Folder structure

```
asf_online_data_exploration/
├─ analysis/
├─ config/
│  ├─ base.yaml - file paths info
│  ├─ data_collection_parameters.py - parameters for data collection
├─ getters/
├─ notebooks/
├─ pipeline/
│  ├─ data_collection/
│  │  ├─ recent_search_twitter.py - functions to collect data from Twitter's recent search endpoint
│  │  ├─ the_guardian.py - functions to collect data from The Guardian Open Platform content endpoint
│  │  ├─ tests/
│  │  | ├─ testing_recent_search_twitter.py - functions to test data collection pipeline for Twitter's recent search endpoint
│  │  | ├─ testing_the_guardian.py - functions to test data collection pipeline for The Guardian Open Platform content endpoint
├─ utils/
│  ├─ data_collection_utils.py - utility functions for retrieving and uploading data
inputs/
outputs/
```

## Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>

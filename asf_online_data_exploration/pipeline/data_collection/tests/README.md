# Tests

Tests to assess if the **data collection pipeline** is collecting data from Twitter, The Guardian Open Platform and Media Cloud as expected.

Run the following on your command line to run the tests:

- `pytest asf_online_data_exploration/pipeline/data_collection/tests/testing_the_guardian.py` (should take around 4 seconds to run)
- `pytest asf_online_data_exploration/pipeline/data_collection/tests/testing_recent_search_twitter.py` (should take around 4 minutes to run)

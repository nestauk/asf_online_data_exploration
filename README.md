# asf_online_data_exploration

## Setup

- Meet the data science cookiecutter [requirements](http://nestauk.github.io/ds-cookiecutter/quickstart), in brief:
  - Install: `direnv` and `conda`
- Run `make install` to configure the development environment:
  - Setup the conda environment
  - Configure `pre-commit`
- Activate conda enviroment
  - c`onda activate asf_online_data_exploration`
- Set your credentials as enviroment variables
  - `export BEARER_TOKEN="ADD_YOUR_BEARER_TOKEN_HERE"` and replace `ADD_YOUR_BEARER_TOKEN_HERE` with your bearer token credentials.
  - `export GUARDIAN_API_KEY="ADD_YOUR_API_KEY_HERE"` and replace `ADD_YOUR_API_KEY_HERE` with your API key credentials. Alternatively, set `export GUARDIAN_API_KEY="test"`

## Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>

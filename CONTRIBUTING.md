# Contributing

## Setup

To contribute to the project and start making changes to the library, you need to install poetry:

```bash
# In your virtual environment
pip install poetry
```

Then you need to install all dependencies + the necessary development dependencies:

```bash
poetry install --all-extras
```

After that, you need to install the `pre-commit` hooks:

```bash
pre-commit install
```

And you are good to go.

### Docs

To install dependencies for docs, you need to run:

```bash
pip install -r ./docs/requirements.txt
```

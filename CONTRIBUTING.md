# Contributing

## Setup

To contribute to the project and start making changes to the library, install dependencies with uv:

```bash
uv sync --all-extras --group dev --group tests
```

After that, install the `pre-commit` hooks:

```bash
uv run pre-commit install
```

And you are good to go.

### Docs

To install dependencies for docs, you need to run:

```bash
uv pip install -r ./docs/requirements.txt
```

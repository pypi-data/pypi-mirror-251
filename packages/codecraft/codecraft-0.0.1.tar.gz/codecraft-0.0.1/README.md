# CodeCraft

AI code assistant to help you write code faster, cover it with tests and more

## Getting started

```shell
cd path/to/your/project
pip install codecraft
export OPENAI_API_KEY=your-key-goes-here
```

## Usage

Once installed, codecraft can be run through its command-line interface.

### Command-line Interface

Run a codecraft session using the following command:

```python
codecraft
```

Optional Arguments:
- -q or --query: Run with a specific query.
- -c or --coverage: Run with coverage analysis.

```shell
codecraft --query "Your query here"
codecraft --coverage
```

## Requirements

 - python: 3.10+

## First run

On the first run `codecraft` create folder `.codecraft/prompts` with main prompts so you can tune prompts for your project

Also `codecraft` will add `.codecraft` to `.gitignore` file - not to use prompts in GIT

## Envs

### CODECRAFT_MODEL_NAME

Model name in OpenAI API to use

### OPENAI_API_KEY

API key for OpenAI API

### CODECRAFT_COV_FOLDER

Folder to use in coverage report (default: `.`)

## Contributing

Contributions to `codecraft` are welcome! Please read our contributing guidelines for details on how to submit pull requests

### Clone repository

```shell
git clone ...
```

### Install dependencies

```shell
poetry install
```

### Use with your project

```shell
cd path/to/your/project
pip install -e path/to/cloned/codecraft
codecraft
```

## License

`codecraft` is licensed under MIT License

## Contact

For any queries or suggestions, feel free to contact us at [hello@welltory.com]
# GPSlibrary

GPSlibrary is a Python package for plotting and analyzing GPS and other data. This package also includes comprehensive documentation for users and developers.

## Table of Contents

- [Installation](#installation)
- [Local Development](#local-development)
- [Running the Documentation Locally](#running-the-documentation-locally)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install GPSlibrary from the Vedur GitLab package registry, run:
```bash
pip install gpslibrary --index-url https://git.vedur.is/api/v4/projects/448/packages/pypi/simple
```

## Local Development

To set up a local development environment for GPSlibrary:

1. Clone the repository from Vedur GitLab:

```bash
git clone https://git.vedur.is/aut/gpslibrary.git
```

2. Navigate to the project directory:

```bash
cd gpslibrary
```

3. Create and activate a virtual environment:

```bash
python -m venv env source env/bin/activate
```

4. Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

5. Install the package in editable mode:

```bash
pip install -e .
```


## Running the Documentation Locally

To build and serve the GPSlibrary documentation locally:

1. Install MkDocs and required plugins:

```bash
pip install mkdocs mkdocs-material mkdocstrings-python
```


2. Serve the documentation on a local server:

```bash
mkdocs serve
```

3. Open a browser to `http://127.0.0.1:8000` to view the documentation.


## Contributing

We welcome contributions to the GPSlibrary project! Please refer to the authors for guidelines on how to make contributions.

## License

GPSlibrary is released under the [MIT License](LICENSE). See the LICENSE file for more details.


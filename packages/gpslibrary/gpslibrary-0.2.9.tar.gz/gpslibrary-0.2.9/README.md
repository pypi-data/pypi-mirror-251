# Package containing libraries to handle ploting and analysing GPS and other data plus its documentation

This repository contains the package and the documentation for the GPSlibrary Python package.

## Table of Contents

- [Package Installation](#installationpackage)
- [Documentation Installation](#installation)
- [Running the Documentation Locally](#running-the-documentation-locally)


# Installing the GPSlibrary package for local development
First, clone the repository to your machine:
```
git clone --branch dev_support --single-branch git@git.vedur.is:aut/ut-dev/gpslibrary.git
```
Set your mount path to an environmental variable $MOUNT_PATH by adding it to your .bashrc or .bashrcprofile file:
```
EXPORT $MOUNT_PATH=/path/to/mount
source ~/.bashrc
```
Create and activate a virtual environment:
```bash
python3 venv env

source env/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Install the gpslibrary from the repo or pip. If from repo:

```bash
pip install .
```
Alternative is to install from the package registry (Gitlab):
```bash
pip install gpslibrary --index-url https://git.vedur.is/api/v4/projects/448/packages/pypi/simple
```

# Running the GPSlibrary Documentation

## Installation

Build the documentation into static HTML files that can be served in any web server:
```bash
mkdocs build
```

Run the mkdocs server in the 8080 port:
```bash
mkdocs serve --dev-addr=127.0.0.1:8080
```

Open Browser in http://127.0.0.1:8080


# mets-retriever

## About

CLI tool for bulk downloading [Archivematica][am] METS files.

Unlike Gloria the flat-coated retriever mix, `mets-retriever` is all about fetching.

![Gloria, the flat-coated retriever mix](media/gloria.jpg)

## Usage

After installing with pip (see below), use the `retrieve-mets` command.

`retrieve-mets` has two subcommands, `fetch-all` and `fetch-one`. Both
subcommands have common arguments:

* METS files are fetched to a directory specified with the `--output-dir`
argument. If one is not provided, a `mets_files` directory will be created
in the current directory and METS files will be written there.
* Storage Service credentials must be included using the `--ss-url` and
`--ss-api-key` arguments for both commands. By default these default to values
from the Archivematica Docker development environment.

```
Usage: retrieve-mets [OPTIONS] COMMAND [ARGS]...

  METS Retriever CLI tool

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  fetch-all  Fetch all METS files not already retrieved.
  fetch-one  Fetch single METS file, even if it's already been retrieved.
```

### `fetch-all`

To fetch all AIP METS files that have not already been retreived, use the
`fetch-all` subcommand. E.g.:

```bash
retrieve-mets fetch-all
```

Once a METS file is fetched, its UUID is stored in a local SQLite database so
that it will not be fetched again on subsequent runs.

This command accepts several optional arguments:

```
Usage: retrieve-mets fetch-all [OPTIONS]

  Fetch all METS files not already retrieved.

Options:
  --ss-url TEXT      Storage Service host URL  [default:
                     http://127.0.0.1:62081; required]
  --ss-api-key TEXT  Storage Service API key  [default: test; required]
  --output-dir TEXT  Path to output directory  [default: mets_files; required]
  --help             Show this message and exit.

```

### `fetch-one`

To fetch (or re-fetch) a single AIP METS file, use the `fetch-one` subcommand.
E.g.:

```bash
retrieve-mets fetch-one 68ee3c66-d90a-4b9a-a33c-2e4e6d339ff7
```

This command accepts several optional arguments:

```
Usage: retrieve-mets fetch-one [OPTIONS] AIP_UUID

  Fetch single METS file, even if it's already been retrieved.

Options:
  --ss-url TEXT      Storage Service host URL  [default:
                     http://127.0.0.1:62081; required]
  --ss-api-key TEXT  Storage Service API key  [default: test; required]
  --output-dir TEXT  Path to output directory  [default: mets_files; required]
  --help             Show this message and exit.

```

## Install

### Install mets-retriever package

`mets-retriever` requires Python 3.6+.

#### Via PyPI

```bash
pip install mets-retriever
```

#### Manually

Download this repo:

```bash
git clone https://github.com/artefactual-labs/mets-retriever.git
```

Change into the cloned directory and install:

```bash
cd mets-retriever/
pip install .
```

## Development

### Installation

For development, it may be useful to install `mets-retriever` with
`pip install -e .`, which will apply changes made to the source code
immediately.

### Testing

To run all tests with tox: `tox`

Or run tests directly with pytest:
```bash
pip install -r requirements/test.txt
pytest
```

### Publishing to PyPI

This repository contains a [Makefile](Makefile) with commands to aid in
building packages and publishing to [PyPI][pypi].

To check that the package is valid:
```bash
make package-check
```

To upload the package to PyPI (this requires PyPI credentials and being
listed as a collaborator on the `auditmatica` project):
```bash
make package-upload
```

To clean up package distribution files:
```bash
make clean
```

[am]: https://archivematica.org
[pypi]: https://pypi.org/

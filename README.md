<!--
SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# markdown-gettext

A command line program to do i18n and l10n for individual Markdown files.

CommonMark compliant. All core Markdown elements are supported, as well as
YAML front matter, table, and definition list.

## Install

```bash
pip install markdown-gettext
```

## Usage

You can use either `md-gettext` or `markdown-gettext` command

#### Extraction
```
md-gettext extract [-p PACKAGE] [-r REPORT_ADDR] [-t TEAM_ADDR] md pot

positional arguments:
  md                    path of the Markdown file to extract messages from
  pot                   path of the POT file to create

optional arguments:
  -p PACKAGE, --package PACKAGE
                        the package name in POT metadata
  -r REPORT_ADDR, --report-addr REPORT_ADDR
                        the report address in POT metadata
  -t TEAM_ADDR, --team-addr TEAM_ADDR
                        the team address in POT metadata
```

#### Generation
```
md-gettext generate [-l LANG] in-md po out-md

positional arguments:
  in-md                 path of the source Markdown file
  po                    path of the PO file containing translations
  out-md                path of the Markdown file to create

optional arguments:
  -l LANG, --lang LANG  language of translations
```

## Notes

Some notes about how different elements are handled:
- Inlines: newlines and consecutive spaces are not kept;
- Content of each HTML block isn't parsed into finer tokens but processed
as a whole;
- Fenced code blocks: only `//` single comments are processed;

## Development environment

- With Conda

```bash
conda env create -f environment.yml
conda activate mg
poetry install
```

# adela &mdash; Adjektiivietsin ja -laskija

Adela is a program for investigating strings of adjectives inside Finnish-language texts. It uses the [trankit](https://github.com/nlp-uoregon/trankit) (Nguyen, Minh Van and Lai, Viet Dac and Veyseh, Amir Pouran Ben and Nguyen, Thien Huu) toolkit for ingest.

## Dependencies

- Python 3.10.11
- pip 23.0.1
- NVIDIA CUDA Toolkit 12.4

## Installation

The installation process is a bit fragile but should be future-proof because it specifies exact versions for all its parts. Make sure your system fulfills the [dependencies](#dependencies)!

Follow the below steps to install adela:

1. ``python3.10 -m venv .venv``
2. ``source .venv/bin/activate``
3. ``pip install -r requirements.txt``
4. ``pip install numpy --pre torch --force-reinstall --index-url https://download.pytorch.org/whl/nightly/cu124``
5. Install trankit

Install trankit like this:

````bash
git submodule init
git submodule update
cd trankit
pip install .
````

## Usage

``python script.py input [output]``

The script reads a UTF-8 formatted plain text file as input, and writes results in CoNLL-U format to ``output`` and CSV format to ``{input%.txt}.csv``. If ``output`` is not provided, results are saved to ``{input%.txt}.conllu``. If given input is a directory, ``output`` is ignored and every ``.txt`` file in the directory is attempted to parse and results are saved inside the directory per-file as ``{input%.txt}.conllu`` and ``{input%.txt}.csv``.

## Copyright

```
Copyright © 2026 Adela Noponen & Emma Koskinen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

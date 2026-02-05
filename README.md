# Trankit runner

This took a lot of effort to get working.

## Dependencies

- Python 3.10.11
- CUDA Toolkit 12.4

## Installation

1. ``python3.10 -m venv .venv``
2. ``source .venv/bin/activate``
3. ``pip install -r requirements.txt``
4. ``pip3 install numpy --pre torch --force-reinstall --index-url https://download.pytorch.org/whl/nightly/cu124``
5. Install trankit

Install trankit like this:

````bash
git submodule init
git submodule update
cd trankit
pip install .
````
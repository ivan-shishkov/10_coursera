# Coursera Dump

This script allows to get info about educational courses (title, language, start date, number of weeks, average rating, URL) from [Coursera.org](https://www.coursera.org/) and save it to the XLSX file.

# Quickstart

For script launch need to install Python 3.5 and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

Usage:

```bash

$ python3 coursera.py -h
usage: coursera.py [-h] [--count COUNT] output

positional arguments:
  output         a xlsx file to save info about Coursera courses

optional arguments:
  -h, --help     show this help message and exit
  --count COUNT  a count of randomly selected Coursera courses (default: 20)

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

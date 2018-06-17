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
usage: coursera.py [-h] [--output OUTPUT] [--count COUNT]

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  a xlsx file to save info about Coursera courses
  --count COUNT    a count of randomly selected Coursera courses (default: 20)

```

Example of script launch on Linux:

```bash

$ python3 coursera.py --count 100 --output coursera_courses_100.xlsx
Getting info about Coursera courses...
Info about Coursera courses successfully saved to coursera_courses_100.xlsx

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

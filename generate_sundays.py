#!/usr/local/bin/python
#
# This script generates a csv file containing all the Sundays from now until
# UNTIL_YEAR appending the arguments as extra columns
#

import csv
import datetime
import json
import os
import re
import sys


def lookup_req(param):
    try:
        return os.environ[param]
    except KeyError:
        raise EnvironmentError(f"Missing required {param} variable!")


DATETIME_FORMAT = "%A %d %B %Y"  # Format: 'Sunday 16 May 2021'
UNTIL_YEAR = 2024
EXTRA_COLUMNS = sys.argv[1:]
OUTPUT_FILE = 'zakgeld.csv'

try:
    LOG_LEVEL = os.environ['LOG_LEVEL']
except KeyError:
    LOG_LEVEL = 'INFO'

try:
    from_year = os.environ['FROM_YEAR']
    from_date = datetime.date(year=int(from_year), month=1, day=1)
except KeyError:
    from_date = datetime.date.today()

def logger(level, msg):
    log_levels = {
        'ERROR': 0,
        'WARNING': 1,
        'INFO': 2,
        'DEBUG': 3
    }
    if log_levels[LOG_LEVEL] >= log_levels[level]:
        print(f"[{level}] {msg}")


def validate_datetime(string, dt_format):
    try:
        datetime.datetime.strptime(string, dt_format)
        return string
    except ValueError:
        raise ValidationException(f"Invalid datetime: {string} does not match format: {dt_format}")


def main():
    until_year = UNTIL_YEAR


    d_delta = datetime.date(year=until_year, month=1, day=1) - from_date

    output_list = []
    for i in range(d_delta.days):
        incr = from_date + datetime.timedelta(days=i)
        if incr.weekday() == 6:
            output_list.append(incr.strftime(DATETIME_FORMAT))

    logger("INFO", f"Output file: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, mode='w') as target_file:
        writer = csv.writer(target_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        ALL_COLUMNS = ['Date']
        if EXTRA_COLUMNS:
            ALL_COLUMNS = ['Date'] + EXTRA_COLUMNS
        writer.writerow(ALL_COLUMNS)

        logger("INFO", f"Columns: {ALL_COLUMNS}")

        for date in output_list:
            writer.writerow([date])


if __name__ == "__main__":
    main()

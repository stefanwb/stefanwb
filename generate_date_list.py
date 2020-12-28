#!/usr/local/bin/python

import datetime
import json
import os
import re


def lookup_req(param):
    try:
        return os.environ[param]
    except KeyError:
        raise EnvironmentError(f"Missing required {param} variable!")


FILE_DATETIME_FORMAT = '%Y%m%d%H%M%S%f'  # Format: '20190901120012345'

try:
    LOG_LEVEL = os.environ['LOG_LEVEL']
except KeyError:
    LOG_LEVEL = 'INFO'


def logger(level, src_key, msg):
    log_levels = {
        'ERROR': 0,
        'WARNING': 1,
        'INFO': 2,
        'DEBUG': 3
    }
    if log_levels[LOG_LEVEL] >= log_levels[level]:
        print(f"[{level}] [{src_key}] {msg}")


def validate_datetime(string, dt_format):
    try:
        datetime.datetime.strptime(string, dt_format)
        return string
    except ValueError:
        raise ValidationException(f"Invalid datetime: {string} does not match format: {dt_format}")


def main():
    until_year = 2021

    d_delta = datetime.date(year=until_year, month=1, day=1) - datetime.date.today()

    output_list = []
    for i in range(d_delta.days):
        incr = datetime.date.today() + datetime.timedelta(days=i)
        if incr.weekday() == 6:
            output_list.append(incr.strftime("%A %d %B %Y"))

    import csv

    with open('zakgeld.csv', mode='w') as zakgeld_file:
        writer = csv.writer(zakgeld_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Date', 'Alexa'])
        for date in output_list:
            writer.writerow([date])


if __name__ == "__main__":
    main()

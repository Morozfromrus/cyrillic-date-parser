# -*- coding: utf-8 -*-

import re
from datetime import datetime


def str_repr(content, idate):
    mreprs = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4,
              'мая': 5, 'май': 5, 'июн': 6, 'июл': 7,
              'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11,
              'дек': 12}

    pattern = (r'(?:{month_regexp}' +
               ')|(?:{month_regexp}'.join([mrpr for mrpr in mreprs.keys()]) +
               ')').format(month_regexp=r'\d{1,2}\W*')
    matches = re.findall(pattern, content)

    for match in matches:
        pattern = r'\d{4}'  # year
        year_matches = re.findall(pattern, content)
        try:
            year = int(year_matches.pop())
        except IndexError:
            year = idate.year

        pattern = ('(?:' + ')|(?:'.join([mrpr for mrpr in mreprs.keys()]) + ')')
        month_matches = re.findall(pattern, match)
        try:
            month_sym = month_matches.pop()
            month = mreprs[month_sym]
        except IndexError:
            month = idate.month

        pattern = r'\d{1,2}'
        day_matches = re.findall(pattern, match)
        try:
            day = int(day_matches.pop())
        except IndexError:
            day = idate.day

        try:
            idate = datetime(day=day, month=month, year=year, hour=idate.hour, minute=idate.minute, second=idate.second)
        except ValueError as err:
            err.message = err.message + '. Debug data: day={day}, month={month}, hour={hour}, minute={minute}, second={second}, content={content}'.format(day=day, month=month, hour=idate.hour, minute=idate.minute, second=idate.second, content=content)
            raise
        break

    return (content, idate)

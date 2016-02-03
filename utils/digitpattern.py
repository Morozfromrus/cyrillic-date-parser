import re
from datetime import datetime


def digit_pattern(content, idate):
    patterns = ['(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})',
                '(?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2})',
                '(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2})']

    for pattern in patterns:
        try:
            date = re.search(pattern, content).groupdict()
        except AttributeError:
            continue

        if len(date['year']) == 2:
            date['year'] = '20{year}'.format(year=date['year'])

        date = {
            'day': int(date['day']),
            'month': int(date['month']),
            'year': int(date['year']),
            'hour': idate.hour,
            'minute': idate.minute,
            'second': idate.second
        }
        idate = datetime(**date)
        break

    return content, idate

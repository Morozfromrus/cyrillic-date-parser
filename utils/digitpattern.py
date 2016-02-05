import re
from datetime import datetime


def digit_pattern(content, idate):
    patterns = ['(?P<year>\d{4})\-(?P<month>\d{1,2})\-(?P<day>\d{1,2})t(?P<hour>\d{2})\:(?P<minute>\d{2})\:(?P<second>\d{2})',
                '(?P<year>\d{4})\-(?P<month>\d{1,2})\-(?P<day>\d{1,2})\s(?P<hour>\d{2})\:(?P<minute>\d{2})',
                '(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})\s(?P<hour>\d{2})\:(?P<minute>\d{2})',
                '(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})',
                '(?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2})',
                '(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2})',
                '(?P<hour>\d{2})\:(?P<minute>\d{2})\:(?P<second>\d{2})',
                '(?P<hour>\d{2})\:(?P<minute>\d{2})']

    for pattern in patterns:
        try:
            date = re.search(pattern, content).groupdict()
        except AttributeError:
            continue

        date = {
            'day': date.get('day', idate.day),
            'month': date.get('month', idate.month),
            'year': date.get('year', idate.year),
            'hour': date.get('hour', 0),
            'minute': date.get('minute', 0),
            'second': date.get('second', 0)
        }

        for rn, rv in date.iteritems():
            date[rn] = int(rv)

        if date.get('year') < 100:
            date['year'] += 2000

        idate = datetime(**date)
        content = re.sub(pattern, '', content)
        break

    return content, idate

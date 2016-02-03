import re
from datetime import datetime


def digit_pattern(content, idate):
        pattern = r'\d{1,2}.\d{1,2}.\d{2,4}'
        matches = re.findall(pattern, content)

        for match in matches:
            pattern = r'\d{1,4}'
            lmatches = re.findall(pattern, match)

            year = lmatches[2]

            if len(year) == 2:
                year = '20{year}'.format(year=year)
            year = int(year)

            date = {
                'day': int(lmatches[0]),
                'month': int(lmatches[1]),
                'year': year
            }

        if matches:
            idate = datetime(**date)

        return content, idate

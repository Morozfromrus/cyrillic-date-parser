import re
from datetime import datetime


def digit_pattern(content, idate):
        pattern = r'\d{1,2}.\d{1,2}.\d{4}'
        matches = re.findall(pattern, content)

        for match in matches:
            pattern = r'\d{1,4}'
            lmatches = re.findall(pattern, match)
            date = {
                'day': int(lmatches[0]),
                'month': int(lmatches[1]),
                'year': int(lmatches[2])
            }

        if matches:
            idate = datetime(**date)

        return content, idate

# -*- coding: utf-8 -*-

import re
from datetime import datetime

def rel_repr(content, idate):
    days_inc = 0
    rel_list = {
        'позавчера': -2,
        'вчера': -1,
        'сегодня': 0,
        'завтра': +1,
        'послезавтра': +2
    }
    pattern = '(' + '|'.join(rel_list.keys()) + ')'
    rel_matches = re.findall(pattern, content)

    for rel_item in rel_matches:
        if rel_item in rel_list:
            content = content.replace(rel_item, '')
            days_inc = rel_list[rel_item]
            break

    idate = datetime(day=idate.day + days_inc,
                     month=idate.month,
                     year=idate.year,
                     hour=idate.hour,
                     minute=idate.minute,
                     second=idate.second)

    return (content, idate)

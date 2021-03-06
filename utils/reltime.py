# -*- coding: utf-8 -*-

import re
import operator
from dateutil.relativedelta import relativedelta
from datetime import datetime


def rel_time(content, idate):
    date = idate
    pattern = r'(\d{1,2}\W?ч|\d{1,2}\W?ч|в\W?\d{1,2}:\d{1,2}|в\W?\d{1,2}:\d{1,2}|\d{1,2}\W?ми|\d{1,2}\W?\d{1,2}\W?м|в\W?\d{1,2}|\d{1,2}:\d{1,2})'
    pattern = r'(?:\s|^)(дней|лет|нед|год|мес|день|дня|час|мин|сек|\d{1,2}\W?м|\d{1,2}\W?ч)(?:\s|$)'
    descr = re.findall(pattern, content)

    flag_after = 'через' in content
    flag_before = 'назад' in content

    if flag_after:
        oper = operator.add
    elif flag_before:
        oper = operator.sub
    else:
        def oper(date, tdelta):  # TODO optimize it!
            result = datetime(
                year=tdelta.years if tdelta.years else date.year,
                month=tdelta.months if tdelta.months else date.month,
                day=tdelta.days if tdelta.days else date.day,
                hour=tdelta.hours if tdelta.hours else date.hour,
                minute=tdelta.minutes if tdelta.minutes else date.minute,
                second=tdelta.seconds if tdelta.seconds else date.second
            )
            return result

    try:
        years_val_in_content = int(re.findall(r'(\d+)\s?г', content).pop())
        if len(str(years_val_in_content)) == 2:
            years_val_in_content = int('20{year}'.format(year=years_val_in_content))
        date = oper(date, relativedelta(years=years_val_in_content))
    except IndexError:
        if len(descr) > 0 and 'год' in descr[0]:
            date = oper(date, relativedelta(years=1))

    try:
        weeks_val_in_content = int(re.findall(r'(\d+)\s?нед', content).pop())
        date = oper(date, relativedelta(days=weeks_val_in_content*7))
    except IndexError:
        if len(descr) > 0 and 'нед' in descr[0]:
            date = oper(date, relativedelta(days=7))

    try:
        days_val_in_content = int(re.findall(r'(\d+)\s?дн', content).pop())
        date = oper(date, relativedelta(days=days_val_in_content))
    except IndexError:
        if descr and 'день' in descr[0]:
            date = oper(date, relativedelta(days=1))

    try:
        hour_val_in_content = int(re.findall(r'(\d+)\s*ч', content).pop())
        date = oper(date, relativedelta(hours=hour_val_in_content))
    except IndexError:
        if descr and descr[0] == 'час':
            date = oper(date, relativedelta(hours=1))

    try:
        minutes_val_in_content = int(re.findall(r'(\d+)\s*м', content).pop())
        if 'мес' not in content:
            date = oper(date, relativedelta(minutes=minutes_val_in_content))
    except IndexError:
        if descr and descr[0] == 'мин':
            date = oper(date, relativedelta(minutes=1))
        else:
            if 'hour_val_in_content' in locals() \
               and not flag_after \
               and not flag_before:
                date = datetime(year=date.year,
                                month=date.month,
                                day=date.day,
                                hour=date.hour,
                                minute=0,
                                second=0)

    try:
        seconds_val_in_content = int(re.findall(r'(\d+)\s*с', content).pop())
        date = oper(date, relativedelta(seconds=seconds_val_in_content))
    except IndexError:
        if descr and descr[0] == 'сек':
            date = oper(date, relativedelta(seconds=1))
        else:
            if ('hour_val_in_content' in locals() or \
               'minutes_val_in_content' in locals()) \
               and not flag_after \
               and not flag_before:
                date = datetime(year=date.year,
                                month=date.month,
                                day=date.day,
                                hour=date.hour,
                                minute=date.minute,
                                second=0)

    return (content, date)

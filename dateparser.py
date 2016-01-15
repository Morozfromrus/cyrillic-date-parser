# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

class DateParser(object):
    @staticmethod
    def replace_digit_reprs(content):
        content = content.lower()

        dreprs = {
            'ноль': 0,
            'один': 1,
            'два': 2,
            'три': 3,
            'четыре': 4,
            'пять': 5,
            'шесть': 6,
            'семь': 7,
            'восемь': 8,
            'девять': 9,
            'десять': 10,
            'одиннадцать': 11,
            'двенадцать': 12,
            'тринадцать': 13,
            'четырнадцать': 14,
            'пятнадцать': 15,
            'шестнадцать': 16,
            'семнадцать': 17,
            'восемнадцать': 18,
            'девятнадцать': 19,
            'двадцать': 20
        }

        for dr, di in dreprs.iteritems():
            content = content.replace(dr, str(di))

        return content

    @staticmethod
    def get_date_by_digit_pattern(content):
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
        return datetime(**date)

    @staticmethod
    def get_date_by_string_repr(content):
        result = {
            'day': 1,
            'month': 1,
            'year': datetime.now().year
        }

        mreprs = {
            'янв': 1,
            'фев': 2,
            'мар': 3,
            'апр': 4,
            'мая': 5,
            'май': 5,
            'июн': 6,
            'июл': 7,
            'авг': 8,
            'сен': 9,
            'окт': 10,
            'ноя': 11,
            'дек': 12
        }

        pattern = ('(?:{month_regexp}' + ')|(?:{month_regexp}'.join([mrpr for mrpr in mreprs.keys()]) + ')').format(month_regexp='\d{1,2}\W*')
        matches = re.findall(pattern, content)

        for match in matches:
            pattern = r'\d{4}'  # year
            year_matches = re.findall(pattern, content)
            try:
                year = int(year_matches.pop())
            except IndexError:
                year = datetime.now().year

            pattern = ('(?:' + ')|(?:'.join([mrpr for mrpr in mreprs.keys()]) + ')')
            month_matches = re.findall(pattern, match)
            try:
                month_sym = month_matches.pop()
                month = mreprs[month_sym]
            except IndexError:
                month = datetime.now().month

            pattern = r'\d{1,2}'
            day_matches = re.findall(pattern, match)
            try:
                day = int(day_matches.pop())
            except IndexError:
                day = datetime.now().day

            return datetime(day=day, month=month, year=year)

    @staticmethod
    def get_day_by_rel_repr(content):
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
                days_inc = rel_list[rel_item]
                break
        return days_inc + datetime.now().day

    @staticmethod
    def get_time_by_digit_pattern(content):
        date = datetime.now()

        pattern = r'(\d{1,2}\W?ч|\d{1,2}\W?ч|в\W?\d{1,2}:\d{1,2}|в\W?\d{1,2}:\d{1,2}|\d{1,2}\W?ми|\d{1,2}\W?\d{1,2}\W?м|в\W?\d{1,2}|\d{1,2}:\d{1,2})'
        joined_results = ' '.join(re.findall(pattern, content))
        digits = re.findall(r'\d{1,2}', joined_results)
        pattern = r'(дней|лет|нед|год|мес|день|дня|час|мин|\d{1,2}\W?м|\d{1,2}\W?ч)'
        descr = re.findall(pattern, content)

        if ('через' in content) and len(descr) > 0:
            try:
                hour_val_in_content = int(re.findall(r'(\d{1,2})\W?ч', content).pop())
                date += timedelta(hours=hour_val_in_content)
            except IndexError:
                if (descr[0] == 'час'):
                    date += timedelta(hours=1)

            if descr[0] == 'мин' or re.match(r'\d{1,2}\W?м', descr[0]) and 'мес' not in content:
                if len(digits) > 0:
                    date += timedelta(minutes=int(digits[0]))

        return date

if __name__ == '__main__':
    dp = DateParser()
    test_cases = {
        'replace_digit_reprs': {
            'один два три четыре пять': u'1 2 3 4 5',
        },
        'get_date_by_digit_pattern': {
            '12.06.1975': datetime(day=12, month=6, year=1975),
            '01.01.2015': datetime(day=1, month=1, year=2015)
        },
        'get_date_by_string_repr': {
            '1 января': datetime(day=1, month=1, year=datetime.now().year),
            '28 февраля': datetime(day=28, month=2, year=datetime.now().year),
            '28 февраля 2015 года': datetime(day=28, month=2, year=2015),
        },
        'get_day_by_rel_repr': {
            'позавчера': datetime.now().day-2,
            'вчера': datetime.now().day-1,
            'сегодня': datetime.now().day,
            'завтра': datetime.now().day+1,
            'послезавтра': datetime.now().day+2
        },
        'get_time_by_digit_pattern': {
            'через 2 часа': (datetime.now() + timedelta(hours=1.9), datetime.now() + timedelta(hours=2.1)),
            'через 5 минут': (datetime.now() + timedelta(minutes=4), datetime.now() + timedelta(minutes=6)),
            'через час': (datetime.now() + timedelta(hours=0.9), datetime.now() + timedelta(hours=1.1)),
            'через час и одну минуту': (datetime.now() + timedelta(hours=1), datetime.now() + timedelta(hours=1.1)),
            'через час и 5 минут': (datetime.now() + timedelta(hours=1), datetime.now() + timedelta(hours=1.1)),
            # 'через 2 ч 50 мин': (datetime.now() + timedelta(hours=2, minutes=49), datetime.now() + timedelta(hours=2, minutes=51)),
            # 'через 2 часа 30 минут': (datetime.now() + timedelta(hours=2.4), datetime.now() + timedelta(hours=2.6)),
            # '12 часов': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=12),
            # '1ч': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=1),
            # 'в 15:17': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=15, minute=17),
            # 'в19:26': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=19, minute=26),
            # '2часа 53 минуты': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=2, minute=53),
            # '5 часов 20минут': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=5, minute=20),
            # '19 30минут': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=19, minute=30),
            # 'в 17': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=17),
            # 'в11': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=11),
            # '14:10': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=14, minute=10),
            # 'в 10 часов 50 минут': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=10, minute=50),
        }
    }

    for method, cases in test_cases.iteritems():
        method_to_call = getattr(DateParser, method)
        for initial, expected in cases.iteritems():
            try:
                method_result = method_to_call(initial)
                if isinstance(expected, tuple):
                    assert method_result >= expected[0] and method_result <= expected[1]
                else:
                    assert method_result == expected
            except AssertionError:
                print('*'*10)
                print('Test failed for {method} called "{initial}"'.format(method=method, initial=initial))
                print('%s != %s' % (method_result, expected))
    print('I tested everything')

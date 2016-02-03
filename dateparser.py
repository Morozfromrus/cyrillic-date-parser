# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
from copy import copy

from utils.replacedigitreprs import replace_digit_reprs
from utils.digitpattern import digit_pattern
from utils.strepr import str_repr
from utils.relrepr import rel_repr
from utils.reltime import rel_time


class DateParser(object):
    @classmethod
    def parse(cls, content, pattern=None):
        try:
            result = cls.__main_parse_logic__(content, pattern)
        except Exception, exc:
            print u'Error catched:'
            print u'Content = {content}'.format(content=content)
            print u'Pattern = {pattern}'.format(pattern=pattern)
            print u'Message = {msg}'.format(msg=exc.message)
            raise
        return result

    @staticmethod
    def __main_parse_logic__(content, pattern=None):
        content = content.lower()
        content = content.encode('utf-8', 'ignore')
        print '-'*100
        print content
        idate = datetime.now()  # initial date

        def custom_pattern(pattern):
            def def_pattern(content, idate):
                groups = re.match(pattern, content).groupdict()
                idate = datetime(year=int(groups.get('year', idate.year)),
                                 month=int(groups.get('month', idate.month)),
                                 day=int(groups.get('day', idate.day)),
                                 hour=int(groups.get('hour', idate.hour)),
                                 minute=int(groups.get('minute', idate.minute)),
                                 second=int(groups.get('second', idate.second)))
                return content, idate
            return def_pattern

        registered_patterns = [replace_digit_reprs,
                               custom_pattern(pattern),
                               digit_pattern,
                               str_repr,
                               rel_repr,
                               rel_time]
        ov = (copy(content), copy(idate))
        for rp in registered_patterns:
            content, idate = rp(content, idate)
            if rp.__name__ == 'def_pattern' and pattern:
                break
            if ov[0] != content or ov[1] != idate:
                ov = (copy(content), copy(idate))
                print rp.__name__
                print 'was: {content}, {date}'.format(content=ov[0], date=ov[1])
                print 'then: {content}, {date}'.format(content=content, date=idate)

        return '%04d-%02d-%02dT%02d:%02d:%02d' % (idate.year,
                                                  idate.month,
                                                  idate.day,
                                                  idate.hour,
                                                  idate.minute,
                                                  idate.second)

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
            'через 2  часа': (datetime.now() + timedelta(hours=1.9), datetime.now() + timedelta(hours=2.1)),
            'через 5 минут': (datetime.now() + timedelta(minutes=4), datetime.now() + timedelta(minutes=6)),
            'через 5     минут': (datetime.now() + timedelta(minutes=4), datetime.now() + timedelta(minutes=6)),
            'через час': (datetime.now() + timedelta(hours=0.9), datetime.now() + timedelta(hours=1.1)),
            'через час и одну минуту': (datetime.now() + timedelta(hours=1), datetime.now() + timedelta(hours=1.1)),
            'через час и 5 минут': (datetime.now() + timedelta(hours=1), datetime.now() + timedelta(hours=1.1)),
            'через 2 ч': (datetime.now() + timedelta(hours=1.9), datetime.now() + timedelta(hours=2.1)),
            'через 2 ч 50 мин': (datetime.now() + timedelta(hours=2, minutes=49), datetime.now() + timedelta(hours=2, minutes=51)),
            'через 2 часа 30 минут': (datetime.now() + timedelta(hours=2.4), datetime.now() + timedelta(hours=2.6)),
            'через 1 день': (datetime.now() + timedelta(days=0.9), datetime.now() + timedelta(days=1.1)),
            'через 4 дня': (datetime.now() + timedelta(days=3.9), datetime.now() + timedelta(days=4.1)),
            'через 5 дней': (datetime.now() + timedelta(days=4.9), datetime.now() + timedelta(days=5.1)),
            'через 3 недели': (datetime.now() + timedelta(weeks=2.9), datetime.now() + timedelta(weeks=3.1)),
            'через неделю': (datetime.now() + timedelta(weeks=0.9), datetime.now() + timedelta(weeks=1.1)),
            '2 ч назад': (datetime.now() - timedelta(hours=2.1), datetime.now() - timedelta(hours=1.9)),
            '2 ч 50 мин назад': (datetime.now() - timedelta(hours=2, minutes=51), datetime.now() - timedelta(hours=2, minutes=49)),
            '2 часа 30 минут назад': (datetime.now() - timedelta(hours=2, minutes=31), datetime.now() - timedelta(hours=2, minutes=29)),
            '1 день назад': (datetime.now() - timedelta(days=1.1), datetime.now() - timedelta(days=0.9)),
            '4 дня назад': (datetime.now() - timedelta(days=4.1), datetime.now() - timedelta(days=3.9)),
            '5 дней назад': (datetime.now() - timedelta(days=5.1), datetime.now() - timedelta(days=4.9)),
            '3 недели назад': (datetime.now() - timedelta(weeks=3.1), datetime.now() - timedelta(weeks=2.9)),
            '12 часов': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=12),
            '1ч': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=1),
            'в 15:17': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=15, minute=17),
            'в19:26': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=19, minute=26),
            '2часа 53 минуты': (datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=2, minute=52),
                                 datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=2, minute=54)),
            '5 часов 20минут': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=5, minute=20),
            '14:10': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=14, minute=10),
            'в 10 часов 50 минут': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=10, minute=50),
            'через 2 года': (datetime.now() + relativedelta(years=2) - relativedelta(hours=1),
                             datetime.now() + relativedelta(years=2) + relativedelta(hours=1)),
            '2 года назад': (datetime.now() - relativedelta(years=2, hours=1),
                             datetime.now() - relativedelta(years=2) + relativedelta(hours=1)),
            # 'через 2 месяца': (datetime.now() + timedelta(months=1.9), datetime.now() + timedelta(months=2.1)),
            # 'через 5 лет': (datetime.now() + timedelta(years=4.9), datetime.now() + timedelta(years=5.1)),
            # '2 месяца назад': (datetime.now() - timedelta(months=2.1), datetime.now() - timedelta(months=1.9)),
            # '5 лет назад': (datetime.now() - timedelta(years=5.1), datetime.now() - timedelta(years=4.9)),
            # 'в 17': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=17),
            # 'в11': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=11),
        },
        # 'get_time_by_weekday': {
        #     'понедельник',
        #     'вторник',
        #     'среда',
        #     'четверг',
        #     'пятница',
        #     'суббота',
        #     'воскресенье'
        # }
    }

    only_test_cases = dict()
    for method, cases in test_cases.iteritems():
        for initial, expected in cases.iteritems():
            if re.match(r'^\!.*', initial):
                try:
                    only_test_cases[method][initial[1:]] = expected
                except KeyError:
                    only_test_cases[method] = dict()
                    only_test_cases[method][initial[1:]] = expected

    if only_test_cases:
        test_cases = only_test_cases

    tcnt, tsuc, terr = 0, 0, 0

    for method, cases in test_cases.iteritems():
        method_to_call = getattr(DateParser, method)
        for initial, expected in cases.iteritems():
            try:
                method_result = method_to_call(initial)
                tcnt += 1

                if isinstance(expected, tuple):
                    assert method_result >= expected[0] and method_result <= expected[1]
                else:
                    assert method_result == expected

                tsuc += 1
            except AssertionError:
                terr += 1
                print('Test failed for {method} called "{initial}"'.format(method=method, initial=initial))
                print('%s != %s' % (method_result, expected))
                print('_'*3)

    print('{tcnt} tests done, {tsuc} succeeded, {terr} failed'.format(
        tcnt = tcnt,
        tsuc = tsuc,
        terr = terr
    ))

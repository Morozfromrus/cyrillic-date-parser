# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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
            print 'Error catched:'
            if content:
                print 'Content = {content}'.format(content=content.encode('utf-8', 'ignore'))
            if pattern:
                print 'Pattern = {pattern}'.format(pattern=pattern.encode('utf-8', 'ignore'))
            print 'Message = {msg}'.format(msg=exc.message)
            raise
        return result

    @staticmethod
    def __main_parse_logic__(content, pattern=None):
        try:
            content = content.lower()
        except AttributeError:
            raise Exception('Content is None, string expected')

        content = content.encode('utf-8', 'ignore')
        idate = datetime(year=datetime.now().year,
                         month=datetime.now().month,
                         day=datetime.now().day,
                         hour=datetime.now().hour,
                         minute=datetime.now().minute,
                         second=datetime.now().second)  # initial date

        def custom_pattern(pattern):
            if pattern:
                def def_pattern(content, idate):
                    try:
                        groups = re.search(pattern, content).groupdict()
                    except AttributeError:
                        return content, idate

                    mreprs = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4,
                              'мая': 5, 'май': 5, 'июн': 6, 'июл': 7,
                              'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11,
                              'дек': 12}

                    for mkey, mval in mreprs.iteritems():
                        if mkey in groups.get('month'):
                            groups['month'] = mval
                            break

                    idate = datetime(year=int(groups.get('year', idate.year)),
                                     month=int(groups.get('month', idate.month)),
                                     day=int(groups.get('day', idate.day)),
                                     hour=int(groups.get('hour', idate.hour)),
                                     minute=int(groups.get('minute', idate.minute)),
                                     second=int(groups.get('second', idate.second)))
                    return content, idate
                return def_pattern
            else:
                def null_pattern(content, idate):
                    return content, idate
                return null_pattern

        registered_patterns = [replace_digit_reprs,
                               custom_pattern(pattern),
                               digit_pattern,
                               str_repr,
                               rel_repr,
                               rel_time]

        for rp in registered_patterns:
            ov = (copy(content), copy(idate))
            try:
                content, idate = rp(content, idate)
            except:
                print ''
                print 'Method: {method}'.format(method=rp.__name__)
                print 'Content: {content}'.format(content=content)
                print 'Date: {date}'.format(date=idate)
                print ''
                raise

            if rp.__name__ == 'def_pattern' and pattern:
                break
            if ov[0] != content or ov[1] != idate:
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
        # u'12.06.1975': datetime(day=12, month=6, year=1975),
        # u'01.01.2015': datetime(day=1, month=1, year=2015),
        # u'1 января': datetime(day=1, month=1, year=datetime.now().year),
        # u'28 февраля': datetime(day=28, month=2, year=datetime.now().year),
        u'28 февраля 2015 года': (datetime(day=28, month=2, year=2015), datetime(day=1, month=3, year=2015)),
        # u'позавчера': (datetime.now() - relativedelta(hours=48), datetime.now() - relativedelta(hours=49)),
        # u'вчера': (datetime.now() - timedelta(hours=23), datetime.now() - timedelta(hours=25)),
        # u'сегодня': (datetime.now() - timedelta(hours=1), datetime.now() + timedelta(hours=1)),
        # u'завтра': (datetime.now() + timedelta(hours=23), datetime.now() + timedelta(hours=25)),
        # u'послезавтра': datetime.now().day+2,
        u'через 2 часа': (datetime.now() + timedelta(hours=1.9), datetime.now() + timedelta(hours=2.1)),
        u'через 2  часа': (datetime.now() + timedelta(hours=1.9), datetime.now() + timedelta(hours=2.1)),
        u'через 5 минут': (datetime.now() + timedelta(minutes=4), datetime.now() + timedelta(minutes=6)),
        u'через 5     минут': (datetime.now() + timedelta(minutes=4), datetime.now() + timedelta(minutes=6)),
        u'через час': (datetime.now() + timedelta(hours=0.9), datetime.now() + timedelta(hours=1.1)),
        # u'через час и одну минуту': (datetime.now() + timedelta(hours=1), datetime.now() + timedelta(hours=1.1)),
        u'через час и 5 минут': (datetime.now() + timedelta(hours=1), datetime.now() + timedelta(hours=1.1)),
        u'через 2 ч': (datetime.now() + timedelta(hours=1.9), datetime.now() + timedelta(hours=2.1)),
        u'через 2 ч 50 мин': (datetime.now() + timedelta(hours=2, minutes=49), datetime.now() + timedelta(hours=2, minutes=51)),
        u'через 2 часа 30 минут': (datetime.now() + timedelta(hours=2.4), datetime.now() + timedelta(hours=2.6)),
        u'через 1 день': (datetime.now() + timedelta(days=0.9), datetime.now() + timedelta(days=1.1)),
        u'через 4 дня': (datetime.now() + timedelta(days=3.9), datetime.now() + timedelta(days=4.1)),
        u'через 5 дней': (datetime.now() + timedelta(days=4.9), datetime.now() + timedelta(days=5.1)),
        u'через 3 недели': (datetime.now() + timedelta(weeks=2.9), datetime.now() + timedelta(weeks=3.1)),
        # u'через неделю': (datetime.now() + timedelta(weeks=0.9), datetime.now() + timedelta(weeks=1.1)),
        u'2 ч назад': (datetime.now() - timedelta(hours=2.1), datetime.now() - timedelta(hours=1.9)),
        u'2 ч 50 мин назад': (datetime.now() - timedelta(hours=2, minutes=51), datetime.now() - timedelta(hours=2, minutes=49)),
        u'2 часа 30 минут назад': (datetime.now() - timedelta(hours=2, minutes=31), datetime.now() - timedelta(hours=2, minutes=29)),
        u'1 день назад': (datetime.now() - timedelta(days=1.1), datetime.now() - timedelta(days=0.9)),
        u'4 дня назад': (datetime.now() - timedelta(days=4.1), datetime.now() - timedelta(days=3.9)),
        u'5 дней назад': (datetime.now() - timedelta(days=5.1), datetime.now() - timedelta(days=4.9)),
        u'3 недели назад': (datetime.now() - timedelta(weeks=3.1), datetime.now() - timedelta(weeks=2.9)),
        u'12 часов': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=12),
        u'1ч': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=1),
        u'в 15:17': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=15, minute=17),
        u'в19:26': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=19, minute=26),
        u'2часа 53 минуты': (datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=2, minute=52),
                             datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=2, minute=54)),
        u'5 часов 20минут': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=5, minute=20),
        u'14:10': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=14, minute=10),
        u'в 10 часов 50 минут': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=10, minute=50),
        u'через 2 года': (datetime.now() + relativedelta(years=2) - relativedelta(hours=1),
                          datetime.now() + relativedelta(years=2) + relativedelta(hours=1)),
        u'2 года назад': (datetime.now() - relativedelta(years=2, hours=1),
                          datetime.now() - relativedelta(years=2) + relativedelta(hours=1)),
        u'11:47 ДНК естественные и точные науки физика химия': datetime(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, hour=11, minute=47),
    }

    only_test_cases = dict()
    for initial, expected in test_cases.iteritems():
        if re.match(r'^\!.*', initial):
            try:
                only_test_cases[initial[1:]] = expected
            except KeyError:
                only_test_cases = dict()
                only_test_cases[initial[1:]] = expected

    if only_test_cases:
        test_cases = only_test_cases

    tcnt, tsuc, terr = 0, 0, 0

    method_to_call = DateParser.parse
    for initial, expected in test_cases.iteritems():
        try:
            method_result = method_to_call(initial)
            method_result = datetime.strptime(method_result, '%Y-%m-%dT%H:%M:%S')

            tcnt += 1

            if isinstance(expected, tuple):
                assert method_result >= expected[0] and method_result <= expected[1]
            else:
                assert method_result == expected

            tsuc += 1
        except AssertionError:
            terr += 1
            print(u'')
            print(u'*'*3)
            print(u'Test "{initial}" failed'.format(initial=initial))
            print(u'%s != %s' % (method_result, expected))
            print(u'*'*3)
            print(u'')

    print('{tcnt} tests done, {tsuc} succeeded, {terr} failed'.format(
        tcnt = tcnt,
        tsuc = tsuc,
        terr = terr
    ))

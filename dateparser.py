# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from copy import copy
from testcases import testcases
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

    only_test_cases = dict()
    for initial, expected in testcases.iteritems():
        if re.match(r'^\!.*', initial):
            try:
                only_test_cases[initial[1:]] = expected
            except KeyError:
                only_test_cases = dict()
                only_test_cases[initial[1:]] = expected

    if only_test_cases:
        testcases = only_test_cases

    tcnt, tsuc, terr = 0, 0, 0

    method_to_call = DateParser.parse
    for initial, expected in testcases.iteritems():
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

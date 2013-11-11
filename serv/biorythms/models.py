# -*- coding: utf-8 -*-
from django.db import models
from math import sin, pi
from dateutil.rrule import rrule, DAILY
import collections

PEAK_VALUE = 90
DAY_TYPE_PEAK = 'peak'
DAY_TYPE_GREAT_CRITICAL = 'great_critical_day'
DAY_TYPE_CRITICAL = 'critical_day'

PHYSICAL_PERIOD = 23
EMOTIONAL_PERIOD = 28
BRAIN_PERIOD = 33

def bio(time_diff, period):
    return sin(2 * pi * time_diff / period) * 100

def day_bio(time_diff):
    return {
        PHYSICAL_PERIOD: bio(time_diff, PHYSICAL_PERIOD),
        EMOTIONAL_PERIOD: bio(time_diff, EMOTIONAL_PERIOD),
        BRAIN_PERIOD: bio(time_diff, BRAIN_PERIOD),
    }


def is_great_critical(critical):
    return (
        len(critical) == 3
        and not reduce(
            lambda res, x: res+(x['type']!='+'), critical, 0
        )
    )

def get_critical_preiods(day, time_diff):
    critical = []
    for period in (EMOTIONAL_PERIOD, PHYSICAL_PERIOD, BRAIN_PERIOD):
        if int(bio(time_diff, period) * bio(time_diff+1, period)) < 0 \
            or int(bio(time_diff, period)) == 0:
            critical.append({
                'period':period,
                # + график возрастает
                # - график убывает
                'type': '+' if int(bio(time_diff+1, period))>0 else '-'
            })

    day_type = (
        DAY_TYPE_GREAT_CRITICAL
        if is_great_critical(critical)
        else DAY_TYPE_CRITICAL
    )
    return {day_type: critical} if critical else {}

def get_peak_preiods(day, time_diff):
    critical = []
    for period in (EMOTIONAL_PERIOD, PHYSICAL_PERIOD, BRAIN_PERIOD):
        if abs(int(bio(time_diff, period))) >= PEAK_VALUE:
            critical.append({
                'period': period,
                'type': '+' if int(bio(time_diff, period))>0 else '-'
            })
    return {DAY_TYPE_PEAK: critical} if critical else {}


def git_important_days(birthday_dt, begin_date, end_date):
    '''
    высчитывает особые дни в период begin_date по end_date
    '''
    days = {}
    for day in rrule(DAILY, dtstart=begin_date, until=end_date):
        time_diff = (day.date() - birthday_dt).days

        critical = get_critical_preiods(day, time_diff)
        peak = get_peak_preiods(day, time_diff)
        if (peak or critical) and not days.get(day):
            days[day.date()] = {
                'biorythms': day_bio(time_diff),
                'day': day.date()
            }
        if peak:
            days[day.date()].update(peak)
        if critical:
            days[day.date()].update(critical)
    return collections.OrderedDict(sorted(days.items()))


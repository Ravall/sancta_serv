# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import Http404
from serv import utils
import json
from numerology.models import BirthdayForm
from datetime import datetime, timedelta, date
from calendar import monthrange, month_name
from math import sin, pi
from django.core.urlresolvers import reverse
import collections
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY
from pytils import dt as pytils_dt


PHYSICAL_PERIOD = 23
EMOTIONAL_PERIOD = 28
BRAIN_PERIOD = 33

def index(request):
    if request.method == 'POST':
        birthday_form = BirthdayForm(request.POST)
        if birthday_form.is_valid():
            birthday = datetime.strptime(
                birthday_form.cleaned_data['date'], '%d.%m.%Y'
            ).strftime('%Y-%m-%d')
            return redirect('bio_birthday', birthday=birthday)
    else:
        birthday_form = BirthdayForm()

    return render_to_response(
        'biorythms/index.html',
        {
            'form': birthday_form,
        },
        context_instance=RequestContext(request)
    )


def bio(time_diff, period):
    return sin(2 * pi * time_diff / period) * 100


def git_important_days(birthday_dt, begin_date, end_date):
    '''
    высчитывает особые дни в период begin_date по end_date
    '''
    def get_critical_preiods(day, birthday_dt):
        critical = []
        for period in (EMOTIONAL_PERIOD, PHYSICAL_PERIOD, BRAIN_PERIOD):
            time_diff = (day - birthday_dt).days
            if int(bio(time_diff, period) * bio(time_diff+1, period)) < 0 \
                or int(bio(time_diff, period)) == 0:
                critical.append({
                    'period':period,
                    # + график возрастает
                    # - график убывает
                    'type': '+' if int(bio(time_diff+1, period))>0 else '-'
                })

        return critical
    days = {}
    for day in rrule(DAILY, dtstart=begin_date, until=end_date):

        critical = get_critical_preiods(day, birthday_dt)
        if critical:
            if not days.get(day):
                days[day.date()] = {}
            days[day.date()].update({
                'is_critical': True,
                'critical_perods': critical,
            })

            if len(critical) == 3 \
            and not reduce(lambda res, x: res+(x['type']!='+'), critical, 0):
                days[day.date()].update({
                'is_critical': False,
                'is_great_critical_day': True,
                'critical_perods': critical,
            })


    return collections.OrderedDict(sorted(days.items()))




def biorythm(request, birthday, month, year):
    try:
        birthday_dt = datetime.strptime(birthday, '%Y-%m-%d')
    except ValueError:
        raise Http404()



    months = [
        'январь', 'февраль', 'март',
        'апрель', 'май', 'июнь',
        'июль', 'август', 'сентябрь',
        'октябрь', 'ноябрь', 'декабрь'
    ]

    today = date.today()

    ch_month = today.month if month is None else int(month)
    ch_year = today.year if year is None else int(year)
    cur_date = date(ch_year, ch_month, 1)

    begin_date = cur_date - timedelta(days=2)
    end_date = date(
        ch_year, ch_month, monthrange(ch_year, ch_month)[1]
    ) + timedelta(days=2)

    begin_days = (begin_date - birthday_dt.date()).days


    data = [
        {
            'day': (
                birthday_dt+timedelta(days=t)
            ).strftime('%Y-%m-%d'),
            'fiz': int(bio(t, 23)),
            'emo': int(bio(t, 28)),
            'smart': int(bio(t, 33)),
        }
        for t in xrange(
            (begin_date - birthday_dt.date()).days,
            (end_date - birthday_dt.date()).days
        )
    ]

    def get_link(month_diff):
        prev_date = date(ch_year, ch_month, 1) + relativedelta(months=month_diff)
        if today.year != prev_date.year:
            args = (birthday, ('%02d' %  prev_date.month), prev_date.year)
        elif prev_date.month != today.month:
            args = (birthday, '%02d' % prev_date.month)
        else:
            args = (birthday,)
        return reverse('bio_birthday', args=args)

    return render_to_response(
        'biorythms/biorythm.html',
        {
            'birthday': birthday_dt.strftime('%d.%m.%Y'),
            'data': json.dumps(data),
            'today': (
                str(today) if ch_month == today.month and ch_year == today.year
                else None
            ),
            'current_date': cur_date,
            'year': ch_year if ch_year != today.year else None,
            'link_pref':get_link(-1),
            'link_next':get_link(1),
            'critical_days': git_important_days(
                birthday_dt, begin_date, end_date
            ),
            'consts': {
                'PHYSICAL_PERIOD': PHYSICAL_PERIOD,
                'EMOTIONAL_PERIOD': EMOTIONAL_PERIOD,
                'BRAIN_PERIOD': BRAIN_PERIOD
            }
        },
        context_instance=RequestContext(request)
    )

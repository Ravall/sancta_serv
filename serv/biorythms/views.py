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
from dateutil.relativedelta import relativedelta


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


def biorythm(request, birthday, month, year):
    try:
        birthday_dt = datetime.strptime(birthday, '%Y-%m-%d')
    except ValueError:
        raise Http404()

    def bio(time_diff, period):
        return sin(2 * pi * time_diff / period) * 100

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

    def get_critical_days():
        def is_critical_day(i, period):
            return ((begin_days + i) * 2 / float(period)) % 1 == 0
        days = {}
        for i in xrange(34):
            for period in (23, 28, 33):
                if is_critical_day(i, period):
                    t = (begin_days + i)
                    day = (birthday_dt+timedelta(days=t)).strftime('%Y-%m-%d')
                    if not days.get(day):
                        days[day] = []
                    days[day] += (period,)
        return days

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
            'today': (str(today) if ch_month == today.month and ch_year == today.year else None),
            'month_name': months[cur_date.month-1],
            'year': ch_year if ch_year != today.year else None,
            'link_pref':get_link(-1),
            'link_next':get_link(1),
            'critical_days': get_critical_days()
        },
        context_instance=RequestContext(request)
    )

# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import Http404
from serv import utils
import json
from numerology.models import BirthdayForm
from datetime import datetime, timedelta, date

from django.core.urlresolvers import reverse

from dateutil.relativedelta import relativedelta

from pytils import dt as pytils_dt
from support.models import sancta_date
from biorythms.models import (
    bio, git_important_days, day_bio,
    PHYSICAL_PERIOD, EMOTIONAL_PERIOD, BRAIN_PERIOD
)

def index(request):

    content = utils.api_request(
        'sancta/article/{0}.json'.format('biorythms_about')
    )
    content = json.loads(content)

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
            'url': 'bio_home',
            'form': birthday_form,
            'content': content
        },
        context_instance=RequestContext(request)
    )



def biorythm(request, birthday, cur_date=None):
    today = date.today()
    try:
        #распарсим дату дня рождния
        birthday_dt = datetime.strptime(birthday, '%Y-%m-%d').date()
        if cur_date:
            # если день на который нужно расчитать установлен,
            # то распарсим его
            cur_date = datetime.strptime(cur_date, '%Y-%m-%d').date()
        else:
            # если день на который нужно расчитать не установлен
            # то будем считать на сегодня
            cur_date = today
    except ValueError:
        raise Http404()
    begin_date, end_date = sancta_date.month_range(cur_date)
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
            (begin_date - birthday_dt).days,
            (end_date - birthday_dt).days
        )
    ]

    critical_days = git_important_days(birthday_dt, begin_date, end_date)

    try:
        curday_info = critical_days[cur_date]
    except:
        curday_info = {
            'biorythms': day_bio(
                (cur_date - birthday_dt).days
            )
        }

    return render_to_response(
        'biorythms/biorythm.html',
        {
            'birthday': birthday_dt,
            'today_date': cur_date,
            'today_info': curday_info,
            'data': json.dumps(data),
            'critical_days': critical_days,
            'real_today':today,
            'url': 'bio_home',
        },
        context_instance=RequestContext(request)
    )

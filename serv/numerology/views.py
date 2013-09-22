# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import BirthdayForm, get_birthday_num
from django.shortcuts import redirect
from django.http import Http404
from serv import utils
import json

def index(request):
    content = utils.api_request(
        'sancta/article/{0}.json'.format('chislo_rozhdeniya_raschet')
    )
    content = json.loads(content)

    if request.method == 'POST':
        birthday_form = BirthdayForm(request.POST)
        if birthday_form.is_valid():
            result = get_birthday_num(birthday_form.cleaned_data['date'])
            return redirect('num_birthday', digit=result)
    else:
        birthday_form = BirthdayForm()

    return render_to_response(
        'numerology/index.html',
        {
            'url': 'num_home',
            'form': birthday_form,
            'article': content
        },
        context_instance=RequestContext(request)
    )


def digit_birhday(request, digit):
    digit = int(digit)
    if not( (digit > 0 and digit < 10) or digit in (11, 22) ):
        raise Http404
    content = utils.api_request(
        'sancta/article/chislo_rozhdeniya_{0}.json'.format(digit)
    )
    content = json.loads(content)
    return render_to_response(
        'numerology/num.html',
        {
            'url': 'num_home',
            'num': digit,
            'article': content
        },
        context_instance=RequestContext(request)
    )

def all(request):
    return render_to_response(
        'numerology/all.html',
        {
            'url': 'all_nums'
        },
        context_instance=RequestContext(request)
    )

# -*- coding: utf-8 -*-

from django import template
from biorythms.models import (
    PHYSICAL_PERIOD, EMOTIONAL_PERIOD, BRAIN_PERIOD,
    DAY_TYPE_PEAK, DAY_TYPE_GREAT_CRITICAL, DAY_TYPE_CRITICAL
)
register = template.Library()  #: Django template tag/filter registrator

@register.filter
def critical_type_info(info):
    type_info = ''
    if DAY_TYPE_CRITICAL in info.keys():
        if len(info[DAY_TYPE_CRITICAL]) == 2:
            type_info = 'Двойной критический день:'
        elif len(info[DAY_TYPE_CRITICAL]) == 3:
            type_info = 'Тройной критический день:'
        else:
            type_info = 'Критический день:'
    elif DAY_TYPE_GREAT_CRITICAL in info.keys():
        type_info = 'Великий критический день'
    return type_info


@register.filter
def period_info(info):
    day_info = ''
    if DAY_TYPE_PEAK in info.keys():
        for peaks in info[DAY_TYPE_PEAK]:
            day_info +='<p>Высокие показатели ' if peaks['type'] == '+' else '<p>Низкие показатели'


            if peaks['period'] == PHYSICAL_PERIOD:
                day_info += ' физического'
            elif peaks['period'] == EMOTIONAL_PERIOD:
                day_info += ' эмоционального'
            elif peaks['period'] == BRAIN_PERIOD:
                day_info += ' умственного'
            day_info += ' биоритма</p>'

    if DAY_TYPE_CRITICAL in info.keys():
        for indx, period in enumerate(info[DAY_TYPE_CRITICAL]):
            if indx == 0:
                day_info += '<p>Переключение фазы'
            elif indx+1 == len(info[DAY_TYPE_CRITICAL]):
                day_info += ' и '
            else:
                day_info += ', '

            if period['period'] == PHYSICAL_PERIOD:
                day_info += ' физического'
            elif period['period'] == EMOTIONAL_PERIOD:
                day_info += ' эмоционального'
            elif period['period'] == BRAIN_PERIOD:
                day_info += ' умственного'

            if indx+1 == len(info[DAY_TYPE_CRITICAL]):
                day_info += ' биоритма</p>'
    return day_info


@register.filter
def biorithm(today_info, period):
    bio_int = int(round(today_info['biorythms'][period]))
    hint = ''
    if bio_int > 90:
        hint = '(<span class="attention">пиковый высокий</span>)'
    elif bio_int < -90:
        hint = '(<span class="attention">пиковый низкий</span>)'
    return '{0} {1}'.format(bio_int, hint)



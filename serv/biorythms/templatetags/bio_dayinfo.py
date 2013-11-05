# -*- coding: utf-8 -*-

from django import template
from biorythms.views import PHYSICAL_PERIOD, EMOTIONAL_PERIOD, BRAIN_PERIOD
register = template.Library()  #: Django template tag/filter registrator

@register.filter
def critical_type_info(info):
    if info['is_critical']:
        if len(info['critical_perods']) == 2:
            type_info = 'Двойной критический день'
        elif len(info['critical_perods']) == 3:
            type_info = 'Тройной критический день'
        else:
            type_info = 'Критический день'
    elif info['is_great_critical_day']:
        type_info = 'Великий критический день'
    return type_info


@register.filter
def period_info(info):
    if not info['is_critical']:
        return
    for indx, period in enumerate(info['critical_perods']):
        if indx == 0:
            day_info = 'Переключение фазы'
        elif indx+1 == len(info['critical_perods']):
            day_info += ' и '
        else:
            day_info += ', '

        if period['period'] == PHYSICAL_PERIOD:
            day_info += ' физического'
        elif period['period'] == EMOTIONAL_PERIOD:
            day_info += ' эмоционального'
        elif period['period'] == BRAIN_PERIOD:
            day_info += ' умственного'

        if indx+1 == len(info['critical_perods']):
            day_info += ' биоритма'
    return day_info


@register.filter
def biorithm(today_info, period):
    print today_info['biorythms']
    bio_int = int(round(today_info['biorythms'][period]))
    hint = ''
    if bio_int > 90:
        hint = '(<span class="bio_very_hight">пиковый высокий</span>)'
    elif bio_int > 70:
        hint = '(<span class="bio_hight">высокий</span>)'
    elif bio_int < -70:
        hint = '(<span class="bio_low">низкий</span>)'
    elif bio_int < -90:
        hint = '(<span class="bio_very_low">пиковый низкий</span>)'
    elif bio_int == 0:
        hint = '(<span class="bio_critical">критический</span>)'
    return '{0} {1}'.format(bio_int, hint)



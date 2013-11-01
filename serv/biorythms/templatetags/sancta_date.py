# -*- coding: utf-8 -*-

from pytils import dt
from django import template


register = template.Library()  #: Django template tag/filter registrator


def sancta_ru_strftime_inflected(date, format="%d.%m.%Y"):
    '''
    выводит в именительном падеже дату
    '''
    return dt.ru_strftime(format, date)


register.filter('sancta_ru_strftime_inflected', sancta_ru_strftime_inflected)
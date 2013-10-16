# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
import time


def validator_date(value):
    try:
        time.strptime(value, '%d.%m.%Y')
    except ValueError:
        raise ValidationError('некорректная дата')


class BirthdayForm(forms.Form):
    date = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'введите дату рождения'}
        ),
        validators=[validator_date],
        error_messages = {
            'required': "введите дату. Пример: 03.11.1983",
        }
    )


def get_birthday_num(data):
    def num(data):
        while True:
            data = reduce(lambda res, x: res+int(x), list(str(data)), 0)
            if data < 10 or data in (11, 22):
                break
        return data
    return num(''.join(data.split('.')))



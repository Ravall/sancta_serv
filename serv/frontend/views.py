# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse


def index(request):
    return HttpResponsePermanentRedirect(reverse('num_home'))

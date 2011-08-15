#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    index.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from django.contrib import auth
#from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import openchain.config
from openchain.modules import auth_support

def main(request):
    auth_this = auth_support.auth_user(request)
    data = {
        'username': auth.get_user(request),
        'req_url': '/',
        'auth': auth_this,
        'content': 'home.html',
        'Title': openchain.config.Title,
    }

    return render_to_response('index.html', data)


# vi: ts=4

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    login.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-26
# Description:
# TODO:

from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from modules import support

def main(request):
    if request.method == 'POST':
        auth.logout(request)

    data = support.default_answer_data(request)

    if request.method == 'POST':
        if data['auth']:
            try:
                url = request.POST['next']
            except:
                url = '/'
            return redirect(url)

    try:
        data['next'] = request.GET['next']
    except:
        data['next'] = '/'

    return render_to_response('auth.html', data)

# vi: ts=4

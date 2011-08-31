#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Login page"""

from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from modules import support

def main(request):
    """return login page"""

    if request.method == 'POST':
        auth.logout(request)

    data = support.default_answer_data(request)

    if request.method == 'POST':
        if data['auth']:
            try:
                url = request.POST['next']
            except KeyError:
                url = '/'

            return redirect(url)

    try:
        data['next'] = request.GET['next']
    except KeyError:
        data['next'] = '/'

    return render_to_response('auth.html', data)

# vi: ts=4

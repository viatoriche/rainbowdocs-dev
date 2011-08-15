#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    alldocs.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import openchain.config
from openchain.modules import auth_support
from openchain.modules import database

def main(request):
    auth_this = auth_support.auth_user(request)
    if not auth_this: raise Http404

    data = {
        'docs': database.get_doc().all()
    }

    return render_to_response('alldocs.html', data)

# vi: ts=4

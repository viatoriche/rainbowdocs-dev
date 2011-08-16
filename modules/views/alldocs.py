#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    alldocs.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from django.http import Http404
from django.shortcuts import render_to_response
from openchain.modules import auth_support
from openchain.modules.database import Data

def main(request):
    auth_this = auth_support.auth_user(request)
    if not auth_this: raise Http404

    data = Data()

    r_data = {
        'docs': data.doc.all()
    }

    return render_to_response('alldocs.html', r_data)

# vi: ts=4

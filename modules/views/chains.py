#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    chains.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-19
# Description:
# TODO:

from django.http import Http404
from django.shortcuts import render_to_response
from openchain.modules import auth_support
from openchain.modules.database import Data

def addcheck(request, id_main = 0, id_slave = 0):
    auth_this = auth_support.auth_user(request)
    if not auth_this: raise Http404

    if id_main == 0 or id_slave == 0: raise Http404

    db = Data()

    data = {
        'check': db.check_add_chain(id_main, id_slave)
    }

    return render_to_response('chains/addcheck.html', data)

# vi: ts=4

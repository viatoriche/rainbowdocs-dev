#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    support.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-19
# Description:
# TODO:

from django.contrib import auth
from django.shortcuts import redirect
import config
from modules import auth_support
from modules.database import Data

def default_answer_data(request):
    db = Data()
    auth_this = auth_support.auth_user(request)
    return {
        'username': auth.get_user(request),
        'auth': auth_this,
        'req_url': request.path,
        'Title': config.Title,
        'Need': len(db.get_all_need_slave())
        }

def auth_error():
    return redirect('/')

# vi: ts=4

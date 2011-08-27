#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    support.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-19
# Description:
# TODO:

from django.shortcuts import redirect
import config
from modules import auth_support
from modules.database import DataBase as Data
from django.template import RequestContext

def default_answer_data(request):
    db = Data()
    auth_this = auth_support.auth_user(request)

    if auth_this:
        need = len(db.get_all_need_slave(request.user))
    else:
        need = 0

    return RequestContext(request, {
        'auth': auth_this,
        'req_url': request.path,
        'Title': config.Title,
        'Need': need,
        })

def auth_error():
    return redirect('/login/')

def perm_error():
    return redirect('/documents/perm_error/')

def check_doc_perm(request, doc, write = False):
    db = Data()

    user = request.user

    if user.is_superuser: return True

    if db.check_user_perm(doc = doc, user = user, write = write):
        return True

    groups = request.user.groups
    for group in groups.all():
        if db.check_group_perm(doc = doc, group = group, write = write):
            return True

    return False

# vi: ts=4

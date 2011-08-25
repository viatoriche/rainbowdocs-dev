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
from modules.database import Data

def default_answer_data(request):
    db = Data()
    auth_this = auth_support.auth_user(request)
    try:
        username = request.user.get_full_name()
    except:
        username = request.user.username
    if username == '':
        username = request.user.username

    perm = check_permission(request)
    return {
        'username': username,
        'auth': auth_this,
        'req_url': request.path,
        'Title': config.Title,
        'Need': len(db.get_all_need_slave()),
        'perm': perm
        }

def auth_error():
    return redirect('/')

def check_permission(request):
    user = request.user
    if user.is_superuser:
        return {'group': 'root', 'read': True, 'write': True, 'delete': True}
    else:
        dbgroups = user.groups.all()
        groups = []
        for dbgroup in dbgroups:
            groups.append(dbgroup.name)

        group = ', '.join(groups)

        return {'group': group, 'read': False, 'write': False, 'delete': False}

# vi: ts=4

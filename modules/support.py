#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Support functions"""

from django.shortcuts import redirect
import config
from modules import auth_support
from modules.database import DataBase
from django.template import RequestContext

def default_answer_data(request):
    """Generate default data for views"""

    databse = DataBase()
    auth_this = auth_support.auth_user(request)

    if auth_this:
        need = len(databse.get_all_need_slave(request.user))
    else:
        need = 0

    return RequestContext(request, {
        'auth': auth_this,
        'req_url': request.path,
        'Title': config.Title,
        'Need': need,
        })

def auth_error():
    """redirect to login page"""
    return redirect('/login/')

def perm_error():
    """redirect to perms error page"""
    return redirect('/documents/perm_error/')

def check_doc_perm(request, doc, write = False):
    """Return True, if ok perms for doc"""

    database = DataBase()

    user = request.user

    # True if superuser
    if user.is_superuser:
        return True

    # True if user ok
    if database.check_user_perm(doc = doc, user = user, write = write):
        return True

    # Else check groups perms, and true if ok
    groups = request.user.groups
    for group in groups.all():
        if database.check_group_perm(doc = doc, group = group, write = write):
            return True

    # Else - False
    return False

# vi: ts=4

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    auth.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:
from django.contrib import auth

def auth_user(request):
    try:
        request.POST['logout']
        logout = True
    except:
        logout = False

    if logout:
        auth.logout(request)
        return False

    if request.user.is_authenticated():
        return True

    try:
        login = request.POST['login']
        passwd = request.POST['pass']
    except:
        return False

    user = auth.authenticate(username=login, password=passwd)
    if user is not None and user.is_active:
        # Pass OK, User active
        auth.login(request, user)
        return True
    else:
        return False

# vi: ts=4

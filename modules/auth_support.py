#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15

"""Auth Support Module"""

from django.contrib import auth

def auth_user(request):
    """Function auth_user - get request and authorize user (if in POST
    login and password)
    Response: True if authorized, False - not authorized

    """

    if request.method == 'POST':
        try:
            # Test POST logout
            request.POST['logout']
            # Test OK -- logout
            auth.logout(request)
            return False
        except KeyError:
            pass

    if request.user.is_authenticated():
        return True

    if request.method == 'POST':
        try:
            login = request.POST['login']
            passwd = request.POST['pass']
        except KeyError:
            return False

        user = auth.authenticate(username=login, password=passwd)
        if user is not None and user.is_active:
            # Pass OK, User active
            auth.login(request, user)
            return True
        else:
            return False

# vi: ts=4

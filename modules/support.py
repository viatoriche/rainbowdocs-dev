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
import openchain.config

def default_answer_data(request, auth_this):
    return {
        'username': auth.get_user(request),
        'auth': auth_this,
        'req_url': request.path,
        'Title': openchain.config.Title,
        }

# vi: ts=4

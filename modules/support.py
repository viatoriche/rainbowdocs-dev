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
from openchain.modules import auth_support
from openchain.modules.database import Data

def default_answer_data(request):
    db = Data()
    return {
        'username': auth.get_user(request),
        'auth': auth_support.auth_user(request),
        'req_url': request.path,
        'Title': openchain.config.Title,
        'Need': len(db.get_all_need_slave())
        }

# vi: ts=4

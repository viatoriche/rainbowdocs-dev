#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    support.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-26
# Description:
# TODO:

from django.shortcuts import render_to_response, redirect
from modules import support

def main(request):
    data = support.default_answer_data(request)

    data['content'] = 'support.html'

    return render_to_response('index.html', data)

# vi: ts=4

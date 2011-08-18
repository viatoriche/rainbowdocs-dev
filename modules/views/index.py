#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    index.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from django.shortcuts import render_to_response
from openchain.modules import support

def main(request):
    data = support.default_answer_data(request)
    data['content'] = 'home.html'

    return render_to_response('index.html', data)


# vi: ts=4

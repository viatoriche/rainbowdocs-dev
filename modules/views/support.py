#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Support Page"""

from django.shortcuts import render_to_response
from modules import support

def main(request):
    """Return support page"""
    data = support.default_answer_data(request)

    data['content'] = 'support.html'

    return render_to_response('index.html', data)

# vi: ts=4

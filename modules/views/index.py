#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Index - main page"""

from django.shortcuts import render_to_response
from modules import support

def main(request):
    """Return main home page"""

    data = support.default_answer_data(request)
    data['content'] = 'home.html'

    return render_to_response('index.html', data)


# vi: ts=4

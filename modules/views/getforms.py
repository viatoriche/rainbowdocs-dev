#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    getforms.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-18
# Description:
# TODO:

from django.http import Http404
from django.shortcuts import render_to_response
from openchain.modules import parse_docs, support
from openchain.modules.database import Data
from openchain import settings

def main(request):
    data = support.default_answer_data(request)
    if not data['auth']: raise Http404

    db = Data()

    p = parse_docs.Parser(settings.PRINT_FORMS_DIR)
    scanned = []
    for pf in p.scan():
        scanned.append(pf)
        path_pf = pf[0]
        title_pf = pf[1]
        id_doc = db.add_doc(path_pf, title_pf)
        for tag in pf[2]:
            tag_name = tag[0]
            tag_desc = tag[1]
            id_tag = db.add_tag(tag_name, tag_desc)
            db.add_link(id_doc, id_tag)

    data['scanned'] = scanned
    data['content'] = 'getforms.html'

    return render_to_response('index.html', data)

# vi: ts=4

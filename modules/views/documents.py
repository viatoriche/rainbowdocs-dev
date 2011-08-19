#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    documents.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-19
# Description:
# TODO:

from django.http import Http404
from django.shortcuts import render_to_response
from openchain.modules import support, auth_support, parse_docs
from openchain.modules.database import Data
from openchain import settings

def parse(request):
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
    data['content'] = 'documents/parse.html'

    return render_to_response('index.html', data)

def all(request):
    auth_this = auth_support.auth_user(request)
    if not auth_this: raise Http404

    db = Data()

    data = {
        'docs': db.doc.all()
    }

    return render_to_response('documents/all.html', data)

def new(request, id_doc = 0, id_num = 0):
    if id_doc == 0: raise Http404
    data = support.default_answer_data(request)
    if not data['auth']: raise Http404

    db = Data()
    if not db.check_doc(id_doc): raise Http404

    if request.method == 'POST':
        try:
            num = db.add_number(id_num)
            for tag in request.POST:
                db.add_data(number = num, id_doc = id_doc, id_tag = tag, tag_value = request.POST[tag])

            all_data = db.data.filter(number = num)
            data['Title_Doc'] = db.doc.get(id = id_doc).title
            showthis = []
            for d in all_data:
                showthis.append('{0}: {1}'.format(db.tag.get(id = d.id_tag).description, d.tag_value))
            data['showthis'] = showthis
            data['content'] = 'documents/show.html'

            return render_to_response('index.html', data)
        except:
            raise Http404

    try:
        doc = db.doc.get(id = id_doc)
        data['Title_Doc'] = doc.title
        cur_tags = db.link.filter(id_doc = id_doc)
        tags = []
        for tag in cur_tags:
            tags.append(
                           (
                               tag.id_tag, # 0
                               db.tag.get(id = tag.id_tag).description # 1
                           )
                       )

        data['tags'] = tags
        data['content'] = 'documents/new.html'

        return render_to_response('index.html', data)
    except:
        raise Http404

# vi: ts=4

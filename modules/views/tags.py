#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    tags.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-22
# Description:
# TODO:

from django.shortcuts import render_to_response
from modules import support
from modules.database import Data

def show(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if request.method == 'POST':
        try:
            id_tag = request.POST['id_tag']
            db.del_tag(id_tag)
        except:
            pass

    all_tags = db.tag.all()

    out = []

    for tag in all_tags:
        numbers = db.numbers_from_tag(tag.id)
        out.append( (tag.id, tag.name, tag.description, numbers) )

    data['out'] = out
    data['content'] = 'tags/show.html'

    return render_to_response('index.html', data)


def links(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if request.method == 'POST':
        try:
            id_link = request.POST['id_link']
            db.del_link(id_link)
        except:
            pass

    all_docs = db.doc.all()

    out = []

    for doc in all_docs:
        lns = []
        doc_links = db.link.filter(id_doc = doc.id)
        for link in doc_links:
            tag = db.tag.get(id = link.id_tag)
            lns.append( (link.id, tag.name, tag.description) )

        out.append( (doc.title, lns) )

    data['out'] = out
    data['content'] = 'tags/links.html'

    return render_to_response('index.html', data)
# vi: ts=4

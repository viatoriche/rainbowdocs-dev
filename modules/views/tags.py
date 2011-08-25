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
        if request.POST['do'] == 'delete':
            id_tag = request.POST['id_tag']
            db.del_tag(id_tag)
        if request.POST['do'] == 'add':
            name = request.POST['name']
            desc = request.POST['description']
            db.add_tag(name, desc)

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
        if request.POST['do'] == 'delete':
            id_link = request.POST['id_link']
            db.del_link(id_link)
        elif request.POST['do'] == 'add':
            id_doc = request.POST['id_doc']
            id_tag = request.POST['id_tag']
            db.add_link(id_doc, id_tag)

    all_docs = db.doc.all()
    all_tags = db.tag.all()

    out = []

    for doc in all_docs:
        lns = []
        doc_links = db.link.filter(id_doc = doc.id)
        use_tags = []
        free_tags = []
        for link in doc_links:
            tag = db.tag.get(id = link.id_tag)
            use_tags.append(tag)
            lns.append( (link.id, tag.name, tag.description) )

        for tag in all_tags:
            if tag not in use_tags:
                free_tags.append(tag)

        out.append( (doc.title, lns, free_tags, doc.id) )

    data['out'] = out
    data['content'] = 'tags/links.html'

    return render_to_response('index.html', data)
# vi: ts=4

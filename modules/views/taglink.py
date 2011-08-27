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
from modules.database import DataBase as Data
from django.contrib.auth.decorators import permission_required

@permission_required('main.can_view_tag', login_url='/login/')
def show(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if request.method == 'POST':
        if request.POST['do'] == 'delete':
            id_tag = request.POST['id_tag']
            if request.user.has_perm('main.delete_tag'):
                db.del_tag(db.tag.get(id = id_tag))
        if request.POST['do'] == 'add':
            name = request.POST['name']
            desc = request.POST['description']
            if request.user.has_perm('main.add_tag'):
                db.add_tag(name, desc)

    all_tags = db.tag.all()

    out = []

    for tag in all_tags:
        numbers = db.numbers_from_tag(tag)
        out.append( {'tag': tag, 'numbers': numbers} )

    data['out'] = out
    data['content'] = 'tags/show.html'

    return render_to_response('index.html', data)

@permission_required('main.can_view_link', login_url='/login/')
@permission_required('main.can_view_tag', login_url='/login/')
@permission_required('main.can_view_doc', login_url='/login/')
def links(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if request.method == 'POST':
        if request.POST['do'] == 'delete':
            id_link = request.POST['id_link']
            if request.user.has_perm('main.delete_link'):
                db.del_link_id(id_link)
        elif request.POST['do'] == 'add':
            id_doc = request.POST['id_doc']
            id_tag = request.POST['id_tag']
            if request.user.has_perm('main.add_link'):
                db.add_link(db.doc.get(id = id_doc), 
                        db.tag.get(id = id_tag))

    all_docs = db.doc.all()
    all_tags = db.tag.all()

    out = []

    for doc in all_docs:
        lns = []
        doc_links = db.link.filter(doc = doc)
        use_tags = []
        free_tags = []
        for link in doc_links:
            tag = link.tag
            use_tags.append(tag)
            lns.append(link)

        for tag in all_tags:
            if tag not in use_tags:
                free_tags.append(tag)

        out.append( {'doc': doc, 'links': lns, 'free_tags': free_tags} )

    data['out'] = out
    data['content'] = 'tags/links.html'

    return render_to_response('index.html', data)
# vi: ts=4

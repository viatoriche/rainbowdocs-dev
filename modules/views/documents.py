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
from django.shortcuts import render_to_response, redirect
from modules import support, auth_support, parse_docs
from modules.database import Data
import settings

def odt(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    if num == '0': raise Http404

    db = Data()
    p = parse_docs.Parser(settings.PRINT_FORMS_DIR)

    static_dir = u'{0}/forms/'.format(settings.STATICFILES_DIRS[0])
    static_url = settings.STATIC_URL
    destfile = u'{0}.odt'.format(num)

    id_doc = db.id_doc_from_number(num)
    sourcefile = db.doc.get(id = id_doc).print_form

    doc_num = db.number.get(id = num)
    date = str(doc_num.date_change)
    if doc_num.held_status:
        date_held = str(doc_num.date_held)
    else:
        date_held = ''

    tags = {}
    doc_data = db.data.filter(number = num)
    for dt in doc_data:
        tags[u'{0}'.format(db.tag.get(id = dt.id_tag).name)] = dt.tag_value

    if p.create_form(sourcefile, 
                    u'{0}{1}'.format(static_dir, destfile), 
                    num,
                    date, date_held,
                    tags):
        return redirect(u'{0}forms/{1}'.format(static_url, destfile))
    else:
        raise Http404

def parse(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    p = parse_docs.Parser(settings.PRINT_FORMS_DIR)
    scanned = []
    for pf in p.scan():
        path_pf = pf[0]
        title_pf = pf[1]
        main_pf = pf[3]
        id_doc = db.add_doc(path_pf, title_pf, main_pf)
        doc_alltags = db.link.filter(id_doc = id_doc)
        new_tags = pf[2]
        tags = []
        test_tags = []
        for tag in new_tags:
            tag_name = tag[0]
            test_tags.append(tag_name)
            tag_desc = tag[1]
            try:
                id_tag = db.tag.get(name = tag_name).id
                db.link.get(id_doc = id_doc, id_tag = id_tag)
            except:
                tags.append(tag)
            id_tag = db.add_tag(tag_name, tag_desc)
            db.add_link(id_doc, id_tag)
        delete_tags = []
        for tag in doc_alltags:
            t = db.tag.get(id = tag.id_tag)
            name = t.name
            desc = t.description
            if name not in test_tags:
                delete_tags.append( (name, desc) )

        scanned.append( (path_pf, title_pf, tags, main_pf, delete_tags) )

    data['scanned'] = scanned
    data['content'] = 'documents/parse.html'

    return render_to_response('index.html', data)

def all(request):
    auth_this = auth_support.auth_user(request)
    if not auth_this: return support.auth_error()

    db = Data()

    data = {
        'docs': db.doc.all()
    }

    return render_to_response('documents/all.html', data)

def held(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    if num == '0': raise Http404

    db = Data()
    db.change_number(num, True)

    return redirect('/documents/show/')

def edit(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()
    if num == '0': return redirect('/documents/edit/')

    db = Data()

    if request.method == 'POST':
        if request.POST['do'] == 'change':
            for tag in request.POST:
                db.change_data(number = num, id_tag = tag, tag_value = request.POST[tag])

            return redirect('/documents/show/{0}/'.format(num))
        if request.POST['do'] == 'add_tag':
            if db.add_data(number = num, 
                           id_tag = request.POST['id_tag'], 
                           tag_value = request.POST['tag_value'])[0]:
                db.change_number(number = num)

    all_data = db.data.filter(number = num)
    all_db_tags = db.tag.all()
    id_doc = db.number.get(id = num).id_doc
    doc = db.doc.get(id = id_doc)

    data['Title_Doc'] = doc.title
    data['template'] = doc.print_form
    data['Number'] = num
    num_db = db.number.get(id = num)
    data['Date'] = num_db.date_change
    data['held_status'] = num_db.held_status
    if data['held_status']:
        data['date_held'] = num_db.date_held
    showthis = []
    test_tags = []
    for d in all_data:
        showthis.append((d.id_tag, db.tag.get(id = d.id_tag).description, d.tag_value))
        test_tags.append(d.id_tag)

    all_tags = []
    for tag in all_db_tags:
        if tag.id not in test_tags:
            all_tags.append(tag)

    data['all_tags'] = all_tags
    data['showthis'] = showthis

    data['content'] = 'documents/edit.html'

    return render_to_response('index.html', data)

def show(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()
    db = Data()

    if num == '0':
        if request.method == 'POST':
            number = request.POST['number']
            if request.POST['do'] == 'Show':
                return redirect('/documents/show/{0}/'.format(number))
            elif request.POST['do'] == 'Edit':
                return redirect('/documents/edit/{0}/'.format(number))
            elif request.POST['do'] == 'Held':
                return redirect('/documents/held/{0}/'.format(number))
            elif request.POST['do'] == 'ODT':
                return redirect('/documents/odt/{0}/'.format(number))


        nums = db.number.all()
        out = []
        for n in nums:
            # 0 - number, 1 - title, 2 - date_change, 3 - held, 4 - dateheld
            out.append((n.id, 
                        db.doc.get(id = db.id_doc_from_number(n.id)).title, 
                        n.date_change,
                        n.held_status,
                        n.date_held))
        data['out'] = out
        data['content'] = 'documents/numbers.html'

        return render_to_response('index.html', data)

    if request.method == 'POST':
        if request.POST['do'] == 'del_tag':
            id_tag = request.POST['id_tag']
            db.del_tag_from_datadoc(num, id_tag)
        elif request.POST['do'] == 'del_number':
            if db.del_number(num):
                return redirect('/documents/show/')

    all_data = db.data.filter(number = num)
    id_doc = db.id_doc_from_number(num)
    doc = db.doc.get(id = id_doc)

    data['Title_Doc'] = doc.title
    data['template'] = doc.print_form
    data['Number'] = num
    data['Date'] = db.number.get(id = num).date_change
    data['held_status'] = db.number.get(id = num).held_status
    data['Date_Held'] = db.number.get(id = num).date_held
    showthis = []
    for d in all_data:
        showthis.append( (db.tag.get(id = d.id_tag).description, 
                          d.tag_value,
                          d.id_tag) 
                       )
    data['showthis'] = showthis
    data['content'] = 'documents/show.html'

    return render_to_response('index.html', data)

def new(request, id_doc = '0', id_num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if id_doc == '0':
        if request.method == 'POST':
            id_doc = request.POST['id_doc']
            num = '0'
            if db.doc.get(id = id_doc).main:
                return redirect('/documents/new/{0}/{1}/'.format(id_doc, num))
            else:
                raise Http404

        docs = db.doc.filter(main = True)

        data['content'] = 'documents/choose.html'
        data['docs'] = docs
        return render_to_response('index.html', data)

    if not db.check_doc(id_doc): raise Http404

    if request.method == 'POST':
        if id_num == '0':
            if db.doc.get(id = id_doc).main:
                num = db.add_number(id_doc, id_user = request.user.id)
                for tag in request.POST:
                    db.add_data(number = num, 
                                id_tag = tag, 
                                tag_value = request.POST[tag])

                return redirect('/documents/show/{0}/'.format(num))
            else:
                raise Http404
        else:
            id_main_doc = db.id_doc_from_number(id_num)
            if id_main_doc == 0: raise Http404

            slaves = db.get_slave_docs(id_main_doc, id_num)
            if id_doc in slaves:
                num = db.add_number(id_doc = id_doc, id_user = request.user.id, main_number = id_num)
                for tag in request.POST:
                    db.add_data(number = num, id_tag = tag, tag_value = request.POST[tag])

                return redirect('/documents/show/{0}/'.format(num))
            else:
                raise Http404


    doc = db.doc.get(id = id_doc)
    data['Title_Doc'] = doc.title
    cur_links = db.link.filter(id_doc = id_doc)
    tags = []
    for link in cur_links:
        if id_num != '0':
            try:
                value = db.data.get(number = id_num, id_tag = link.id_tag).tag_value
            except:
                value = ''

            tags.append({'id': link.id_tag, 
                         'desc': db.tag.get(id = link.id_tag).description, 
                         'value': value})
        else:
            tags.append({'id': link.id_tag, 'desc': db.tag.get(id = link.id_tag).description, 'value': ''})

    data['tags'] = tags
    data['content'] = 'documents/new.html'

    return render_to_response('index.html', data)

# vi: ts=4

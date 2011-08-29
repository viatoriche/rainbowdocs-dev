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
from modules.database import DataBase as Data
import settings
from django.contrib.auth.decorators import permission_required

def perm_error(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    data['content'] = 'documents/perm_error.html'

    return render_to_response('index.html', data)

@permission_required('main.can_view_number', login_url='/login/')
def odf(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    if num == '0': raise Http404

    db = Data()
    p = parse_docs.Parser(settings.PRINT_FORMS_DIR)

    static_dir = u'{0}/forms/'.format(settings.STATICFILES_DIRS[0])
    static_url = settings.STATIC_URL

    doc_num = db.number.get(id = num)
    doc = doc_num.doc

    #destfile = '{1} - {0}'.format(str(doc.print_form), num)
    destfile = str(num) + ' - ' + doc.print_form

    if not support.check_doc_perm(request, doc):
        return support.perm_error()

    sourcefile = doc.print_form

    date = str(doc_num.date_change)
    if doc_num.held_status:
        date_held = str(doc_num.date_held)
    else:
        date_held = ''

    tags = {}
    doc_data = db.data.filter(number = doc_num)
    for dt in doc_data:
        tags[u'{0}'.format(dt.tag.name)] = dt.tag_value

    author = doc_num.user.get_full_name()
    if author == '':
        author = doc_num.user.username

    if p.create_form(sourcefile, 
                    u'{0}{1}'.format(static_dir, destfile), 
                    num,
                    date, date_held,
                    tags, author):
        return redirect(u'{0}forms/{1}'.format(static_url, destfile))
    else:
        raise Http404

@permission_required('main.add_doc', login_url='/login/')
@permission_required('main.add_tag', login_url='/login/')
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
        doc = db.add_doc(path_pf, title_pf, main_pf)
        doc_links = db.link.filter(doc = doc)
        new_tags = pf[2]
        tags = []
        test_tags = []
        for tag in new_tags:
            tag_name = tag[0]
            test_tags.append(tag_name)
            tag_desc = tag[1]
            try:
                dbtag = db.tag.get(name = tag_name)
                db.link.get(doc = doc, tag = dbtag)
            except:
                tags.append(tag)
            db_tag = db.add_tag(tag_name, tag_desc)
            db.add_link(doc, db_tag)
        delete_tags = []
        for link in doc_links:
            t = link.tag
            name = t.name
            desc = t.description
            if name not in test_tags:
                delete_tags.append( (name, desc) )

        scanned.append( (path_pf, title_pf, tags, main_pf, delete_tags) )

    data['scanned'] = scanned
    data['content'] = 'documents/parse.html'

    return render_to_response('index.html', data)

@permission_required('main.can_view_doc', login_url='/login/')
def all(request):
    auth_this = auth_support.auth_user(request)
    if not auth_this: return support.auth_error()

    db = Data()

    data = {
        'docs': db.doc.all()
    }

    return render_to_response('documents/all.html', data)

@permission_required('main.change_number', login_url='/login/')
def held(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    if num == '0': raise Http404

    db = Data()

    number = db.number.get(id = num)

    if not support.check_doc_perm(request, number.doc, True):
        return support.perm_error()

    db.change_number(number, True)

    return redirect('/documents/show/')

@permission_required('main.can_view_number', login_url='/login/')
def edit(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()
    if num == '0': return redirect('/documents/edit/')

    db = Data()

    num = db.number.get(id = num)

    if not support.check_doc_perm(request, num.doc, True):
        return support.perm_error()

    if request.method == 'POST':
        if request.POST['do'] == 'change':
            for tag in request.POST:
                if tag == 'do': continue
                if request.user.has_perm('main.change_data'):
                    db.change_data(number = num, 
                               tag = db.tag.get(id = tag), 
                               tag_value = request.POST[tag])

            return redirect('/documents/show/{0}/'.format(num.id))

        if request.POST['do'] == 'add_tag':
            if request.user.has_perm('main.add_data') and request.user.has_perm('main.change_number'):
                if db.add_data(number = num, 
                           tag = db.tag.get(id = request.POST['id_tag']), 
                           tag_value = request.POST['tag_value']):
                    db.change_number(number = num)

    all_data = db.data.filter(number = num)
    all_db_tags = db.tag.all()
    doc = num.doc

    data['Title_Doc'] = doc.title
    data['template'] = doc.print_form
    data['Number'] = num.id
    data['Date'] = num.date_change
    data['Author'] = '{0} [{1}]'.format(num.user.username, num.user.get_full_name())
    data['held_status'] = num.held_status
    if data['held_status']:
        data['date_held'] = num.date_held
    showthis = []
    test_tags = []
    for d in all_data:
        showthis.append(d)
        test_tags.append(d.tag)

    all_tags = []
    for tag in all_db_tags:
        if tag not in test_tags:
            all_tags.append(tag)

    data['all_tags'] = all_tags
    data['showthis'] = showthis

    data['content'] = 'documents/edit.html'

    return render_to_response('index.html', data)

@permission_required('main.can_view_number', login_url='/login/')
def show(request, num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()
    db = Data()

    if num == '0':
        if request.method == 'POST':
            number = request.POST['number']
            num = db.number.get(id = number)

            if not support.check_doc_perm(request, num.doc):
                return support.perm_error()

            if request.POST['do'] == 'Show':
                return redirect('/documents/show/{0}/'.format(number))
            elif request.POST['do'] == 'Edit':
                if not support.check_doc_perm(request, num.doc, True):
                    return support.perm_error()

                return redirect('/documents/edit/{0}/'.format(number))
            elif request.POST['do'] == 'Held':
                if not support.check_doc_perm(request, num.doc, True):
                    return support.perm_error()

                return redirect('/documents/held/{0}/'.format(number))
            elif request.POST['do'] == 'ODF':
                return redirect('/documents/odf/{0}/'.format(number))

        nums = db.number.all()
        data['numbers'] = nums
        data['content'] = 'documents/numbers.html'

        return render_to_response('index.html', data)

    num = db.number.get(id = num)
    if not support.check_doc_perm(request, num.doc):
        return support.perm_error()

    if request.method == 'POST':
        if request.POST['do'] == 'del_tag':
            if not support.check_doc_perm(request, num.doc, True):
                return support.perm_error()

            id_tag = request.POST['id_tag']
            if request.user.has_perm('main.delete_data') and request.user.has_perm('main.change_number'):
                db.del_tag_from_datadoc(num, db.tag.get(id = id_tag))
        elif request.POST['do'] == 'del_number':
            if request.user.has_perm('main.delete_number'):
                if not support.check_doc_perm(request, num.doc, True):
                    return support.perm_error()

                if db.del_number(num):
                    return redirect('/documents/show/')


    all_data = db.data.filter(number = num)
    doc = num.doc

    data['Title_Doc'] = doc.title
    data['template'] = doc.print_form
    data['Number'] = num.id
    data['Date'] = num.date_change
    data['Author'] = '{0} [{1}]'.format(num.user.username, num.user.get_full_name())
    data['held_status'] = num.held_status
    data['Date_Held'] = num.date_held

    data['showthis'] = all_data
    data['content'] = 'documents/show.html'

    return render_to_response('index.html', data)

@permission_required('main.add_number', login_url='/login/')
@permission_required('main.add_data', login_url='/login/')
def new(request, id_doc = '0', id_num = '0'):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if id_doc == '0':
        if request.method == 'POST':
            id_doc = request.POST['id_doc']

            if not support.check_doc_perm(request, db.doc.get(id = id_doc), True):
                return support.perm_error()

            num = '0'
            if db.doc.get(id = id_doc).main:
                return redirect('/documents/new/{0}/{1}/'.format(id_doc, num))
            else:
                raise Http404

        docs = db.doc.filter(main = True)

        docs = db.perm_doc_filter(request.user, docs, True)

        data['content'] = 'documents/choose.html'
        data['docs'] = docs
        return render_to_response('index.html', data)

    if not db.check_doc_id(id_doc): raise Http404

    doc = db.doc.get(id = id_doc)
    if not support.check_doc_perm(request, doc, True):
        return support.perm_error()

    if request.method == 'POST':
        if id_num == '0':
            if doc.main:
                num = db.add_number(doc, user = request.user)
                for tag in request.POST:
                    db.add_data(number = num,
                                tag = db.tag.get(id = tag),
                                tag_value = request.POST[tag])

                return redirect('/documents/show/{0}/'.format(num.id))
            else:
                raise Http404
        else:
            main_num = db.number.get(id = id_num)

            slaves = db.get_slave_docs(main_num)
            if doc in slaves:
                num = db.add_number(doc = doc, user = request.user, main_number = main_num)
                for tag in request.POST:
                    db.add_data(number = num, tag = db.tag.get(id = tag), tag_value = request.POST[tag])

                return redirect('/documents/show/{0}/'.format(num.id))
            else:
                raise Http404


    data['Title_Doc'] = doc.title
    cur_links = db.link.filter(doc = doc)
    tags = []
    for link in cur_links:
        if id_num != '0':
            num = db.number.get(id = id_num)
            try:
                value = db.data.get(number = num, tag = link.tag).tag_value
            except:
                value = ''

            tags.append({'id': link.tag.id, 
                         'desc': link.tag.description, 
                         'value': value})
        else:
            tags.append({'id': link.tag.id, 'desc': link.tag.description, 'value': ''})

    data['tags'] = tags
    data['content'] = 'documents/new.html'

    return render_to_response('index.html', data)

# vi: ts=4

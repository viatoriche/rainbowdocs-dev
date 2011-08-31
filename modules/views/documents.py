#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Module documents"""


from django.http import Http404
from django.shortcuts import render_to_response, redirect
from modules import support, auth_support, parse_docs
from modules.database import DataBase
import settings
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist

def perm_error(request):
    """Default return if error"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    data['content'] = 'documents/perm_error.html'

    return render_to_response('index.html', data)

@permission_required('main.can_view_number', login_url='/login/')
def odf(request, num = '0'):
    """Create and view ODF document"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    if num == '0':
        raise Http404

    database = DataBase()
    parser = parse_docs.Parser(settings.PRINT_FORMS_DIR)

    static_dir = u'{0}/forms/'.format(settings.STATICFILES_DIRS[0])
    static_url = settings.STATIC_URL

    doc_num = database.number.get(id = num)
    doc = doc_num.doc

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
    doc_data = database.data.filter(number = doc_num)
    for datadoc in doc_data:
        tags[u'{0}'.format(datadoc.tag.name)] = datadoc.tag_value

    author = doc_num.user.get_full_name()
    if author == '':
        author = doc_num.user.username

    if parser.create_form(
            sourcefile,
            doc.type_odf,
            int(doc.ods_list),
            u'{0}{1}'.format(static_dir, destfile),
            num,
            date,
            date_held,
            tags,
            author):
        return redirect(u'{0}forms/{1}'.format(static_url, destfile))
    else:
        raise Http404

@permission_required('main.add_doc', login_url='/login/')
@permission_required('main.add_tag', login_url='/login/')
def parse(request):
    """Parse all printforms and add new docs"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    database = DataBase()

    parser = parse_docs.Parser(settings.PRINT_FORMS_DIR)
    scanned = []
    for path_pf, title_pf, new_tags, main_pf, type_odf, odf_list in parser.scan():
        doc = database.add_doc(path_pf, title_pf, type_odf, odf_list, main_pf)
        doc_links = database.link.filter(doc = doc)
        tags = []
        test_tags = []
        for tag_name, tag_desc in new_tags:
            test_tags.append(tag_name)
            try:
                tag = database.tag.get(name = tag_name)
                database.link.get(doc = doc, tag = tag)
            except ObjectDoesNotExist:
                tags.append( (tag_name, tag_desc) )
            database_tag = database.add_tag(tag_name, tag_desc)
            database.add_link(doc, database_tag)
        delete_tags = []
        for link in doc_links:
            tag = link.tag
            name = tag.name
            desc = tag.description
            if name not in test_tags:
                delete_tags.append( (name, desc) )

        scanned.append( (path_pf, title_pf, tags, main_pf, delete_tags) )

    data['scanned'] = scanned
    data['content'] = 'documents/parse.html'

    return render_to_response('index.html', data)

@permission_required('main.can_view_doc', login_url='/login/')
def all(request):
    """Return all docs"""

    auth_this = auth_support.auth_user(request)
    if not auth_this:
        return support.auth_error()

    database = DataBase()

    data = {
        'docs': database.doc.all()
    }

    return render_to_response('documents/all.html', data)

@permission_required('main.change_number', login_url='/login/')
def held(request, num = '0'):
    """Change held_status of nunmber"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    if num == '0':
        raise Http404

    database = DataBase()

    number = database.number.get(id = num)

    if not support.check_doc_perm(request, number.doc, True):
        return support.perm_error()

    database.change_number(number, True)

    return redirect('/documents/show/')

@permission_required('main.can_view_number', login_url='/login/')
def edit(request, num = '0'):
    """Edit data of number-document"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()
    if num == '0':
        return redirect('/documents/edit/')

    database = DataBase()

    num = database.number.get(id = num)

    if not support.check_doc_perm(request, num.doc, True):
        return support.perm_error()

    if request.method == 'POST':
        if request.POST['do'] == 'change':
            for tag in request.POST:
                if tag == 'do':
                    continue

                if request.user.has_perm('main.change_data'):
                    database.change_data(number = num, 
                                         tag = database.tag.get(id = tag), 
                                         tag_value = request.POST[tag])

            return redirect('/documents/show/{0}/'.format(num.id))

        if request.POST['do'] == 'add_tag':
            if request.user.has_perm(
                    'main.add_data') and request.user.has_perm(
                    'main.change_number'):
                if database.add_data(
                       number = num,
                       tag = database.tag.get(id = request.POST['id_tag']),
                       tag_value = request.POST['tag_value']):
                    database.change_number(number = num)

    all_data = database.data.filter(number = num)
    all_database_tags = database.tag.all()
    doc = num.doc

    data['Title_Doc'] = doc.title
    data['template'] = doc.print_form
    data['Number'] = num.id
    data['Date'] = num.date_change
    data['Author'] = '{0} [{1}]'.format(num.user.username,
                                        num.user.get_full_name())
    data['held_status'] = num.held_status
    if data['held_status']:
        data['date_held'] = num.date_held
    showthis = []
    test_tags = []
    for d in all_data:
        showthis.append(d)
        test_tags.append(d.tag)

    all_tags = []
    for tag in all_database_tags:
        if tag not in test_tags:
            all_tags.append(tag)

    data['all_tags'] = all_tags
    data['showthis'] = showthis

    data['content'] = 'documents/edit.html'

    return render_to_response('index.html', data)

@permission_required('main.can_view_number', login_url='/login/')
def show(request, num = '0'):
    """Show data of number"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()
    database = DataBase()

    if num == '0':
        if request.method == 'POST':
            number = request.POST['number']
            num = database.number.get(id = number)

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

        nums = database.number.all()
        data['numbers'] = nums
        data['content'] = 'documents/numbers.html'

        return render_to_response('index.html', data)

    num = database.number.get(id = num)
    if not support.check_doc_perm(request, num.doc):
        return support.perm_error()

    if request.method == 'POST':
        if request.POST['do'] == 'del_tag':
            if not support.check_doc_perm(request, num.doc, True):
                return support.perm_error()

            id_tag = request.POST['id_tag']
            if request.user.has_perm(
                'main.delete_data') and request.user.has_perm(
                'main.change_number'):
                database.del_tag_from_datadoc(num,
                                              database.tag.get(id = id_tag))

        elif request.POST['do'] == 'del_number':
            if request.user.has_perm('main.delete_number'):
                if not support.check_doc_perm(request, num.doc, True):
                    return support.perm_error()

                if database.del_number(num):
                    return redirect('/documents/show/')


    all_data = database.data.filter(number = num)
    doc = num.doc

    data['Title_Doc'] = doc.title
    data['template'] = doc.print_form
    data['Number'] = num.id
    data['Date'] = num.date_change
    data['Author'] = '{0} [{1}]'.format(num.user.username,
                                        num.user.get_full_name())
    data['held_status'] = num.held_status
    data['Date_Held'] = num.date_held

    data['showthis'] = all_data
    data['content'] = 'documents/show.html'

    return render_to_response('index.html', data)

@permission_required('main.add_number', login_url='/login/')
@permission_required('main.add_data', login_url='/login/')
def new(request, id_doc = '0', id_num = '0'):
    """Create new document"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    database = DataBase()

    if id_doc == '0':
        if request.method == 'POST':
            id_doc = request.POST['id_doc']

            if not support.check_doc_perm(
                    request, 
                    database.doc.get(id = id_doc), 
                    True):
                return support.perm_error()

            num = '0'
            if database.doc.get(id = id_doc).main:
                return redirect('/documents/new/{0}/{1}/'.format(id_doc, num))
            else:
                raise Http404

        docs = database.doc.filter(main = True)

        docs = database.perm_doc_filter(request.user, docs, True)

        data['content'] = 'documents/choose.html'
        data['docs'] = docs
        return render_to_response('index.html', data)

    if not database.check_doc_id(id_doc):
        raise Http404

    doc = database.doc.get(id = id_doc)
    if not support.check_doc_perm(request, doc, True):
        return support.perm_error()

    if request.method == 'POST':
        if id_num == '0':
            if doc.main:
                num = database.add_number(doc, user = request.user)
                for tag in request.POST:
                    database.add_data(number = num,
                                      tag = database.tag.get(id = tag),
                                      tag_value = request.POST[tag])

                return redirect('/documents/show/{0}/'.format(num.id))
            else:
                raise Http404
        else:
            main_num = database.number.get(id = id_num)

            slaves = database.get_slave_docs(main_num)
            if doc in slaves:
                num = database.add_number(doc = doc,
                                          user = request.user,
                                          main_number = main_num)
                for tag in request.POST:
                    database.add_data(number = num, 
                                      tag = database.tag.get(id = tag),
                                      tag_value = request.POST[tag])

                return redirect('/documents/show/{0}/'.format(num.id))
            else:
                raise Http404


    data['Title_Doc'] = doc.title
    cur_links = database.link.filter(doc = doc)
    tags = []
    for link in cur_links:
        if id_num != '0':
            num = database.number.get(id = id_num)
            try:
                value = database.data.get(number = num,
                                          tag = link.tag).tag_value
            except ObjectDoesNotExist:
                value = ''

            tags.append({'id': link.tag.id, 
                         'desc': link.tag.description, 
                         'value': value})
        else:
            tags.append({'id': link.tag.id, 
                         'desc': link.tag.description, 'value': ''})

    data['tags'] = tags
    data['content'] = 'documents/new.html'

    return render_to_response('index.html', data)

# vi: ts=4

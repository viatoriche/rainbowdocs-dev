#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)

"""Module for manipulate chains"""

from django.http import Http404
from django.shortcuts import render_to_response, redirect
from modules import auth_support, support
from modules.database import DataBase
from django.contrib.auth.decorators import permission_required


@permission_required('main.can_view_chain', login_url='/login/')
@permission_required('main.can_view_doc', login_url='/login/')
def add(request):
    """Add/Delete Chain"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    database = DataBase()

    if request.method == 'POST': # chains: 1-1 1-2 3-2 4-5
        doit = ''
        try:
            request.POST['save']
            doit = 'save'
        except KeyError:
            doit = ''

        if doit == '':
            try:
                request.POST['delete']
                doit = 'delete'
            except KeyError:
                return redirect('/chains/add/')

        if doit == 'save':
            try:
                chains = request.POST['chains']
            except KeyError:
                return redirect('/chains/add/')

            s_chains = chains.split(' ')
            for s_chain in s_chains:
                try:
                    id_main, id_slave = s_chain.split('-')[0:2]
                    if request.user.has_perm('main.add_chain'):
                        database.add_chain(database.doc.get(id = id_main),
                                           database.doc.get(id = id_slave))
                except ValueError:
                    pass

        if doit == 'delete':
            try:
                chain_id = request.POST['chain_id']
            except KeyError:
                return redirect('/chains/add/')

            if request.user.has_perm('main.delete_chain'):
                database.chain.get(id = chain_id).delete()

        return redirect('/chains/add/')
    else:
        data['docs'] = database.doc.all()
        data['chains'] = database.chain.all()
        data['content'] = 'chains/add.html'
        return render_to_response('index.html', data)


@permission_required('main.can_view_number', login_url='/login/')
def need(request):
    """Need documents for create"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    database = DataBase()

    docs = database.get_all_need_slave(request.user)

    data['content'] = 'chains/need.html'
    data['need_docs'] = docs

    return render_to_response('index.html', data)

@permission_required('main.can_view_chain', login_url='/login/')
def addcheck(request, id_main = 0, id_slave = 0):
    """Test to add chains

    Response: True - ok, False - not ok
    """

    auth_this = auth_support.auth_user(request)
    if not auth_this:
        return support.auth_error()

    if id_main == 0 or id_slave == 0:
        raise Http404

    database = DataBase()

    data = {
        'check': database.check_add_chain(id_main, id_slave)
    }

    return render_to_response('chains/addcheck.html', data)

# vi: ts=4

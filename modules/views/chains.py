#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    chains.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-19
# Description:
# TODO:

from django.http import Http404
from django.shortcuts import render_to_response, redirect
from modules import auth_support, support
from modules.database import DataBase
from django.contrib.auth.decorators import permission_required

@permission_required('main.can_view_chain', login_url='/login/')
@permission_required('main.can_view_doc', login_url='/login/')
def add(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = DataBase()

    if request.method == 'POST': # chains: 1-1 1-2 3-2 4-5
        try:
            chains = request.POST['chains']
        except:
            return redirect('/chains/add/')
        s_chains = chains.split(' ')
        for s_chain in s_chains:
            try:
                id_main = s_chain.split('-')[0]
                id_slave = s_chain.split('-')[1]
                if request.user.has_perm('main.add_chain'):
                    db.add_chain(db.doc.get(id = id_main), db.doc.get(id = id_slave))
            except:
                pass

        return redirect('/chains/add/')
    else:
        data['docs'] = db.doc.all()
        data['chains'] = db.chain.all()
        data['content'] = 'chains/add.html'
        return render_to_response('index.html', data)


@permission_required('main.can_view_number', login_url='/login/')
def need(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = DataBase()

    docs = db.get_all_need_slave(request.user)

    data['content'] = 'chains/need.html'
    data['need_docs'] = docs

    return render_to_response('index.html', data)

@permission_required('main.can_view_chain', login_url='/login/')
def addcheck(request, id_main = 0, id_slave = 0):
    auth_this = auth_support.auth_user(request)
    if not auth_this: return support.auth_error()

    if id_main == 0 or id_slave == 0: raise Http404

    db = DataBase()

    data = {
        'check': db.check_add_chain(id_main, id_slave)
    }

    return render_to_response('chains/addcheck.html', data)

# vi: ts=4

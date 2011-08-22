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
from modules.database import Data

def add(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

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
                db.add_chain(id_main, id_slave)
            except:
                pass

        return redirect('/chains/add/')
    else:
        data['docs'] = db.doc.all()
        data['chains'] = db.chain.all()
        data['content'] = 'chains/add.html'
        return render_to_response('index.html', data)


def need(request):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    data['content'] = 'chains/need.html'
    data['need_docs'] = db.get_all_need_slave()

    return render_to_response('index.html', data)


def addcheck(request, id_main = 0, id_slave = 0):
    auth_this = auth_support.auth_user(request)
    if not auth_this: return support.auth_error()

    if id_main == 0 or id_slave == 0: raise Http404

    db = Data()

    data = {
        'check': db.check_add_chain(id_main, id_slave)
    }

    return render_to_response('chains/addcheck.html', data)

# vi: ts=4

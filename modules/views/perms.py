#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.shortcuts import render_to_response , redirect
from modules import support
from modules.database import DataBase as Data

def user(request, doit = '', permid = ''):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if request.method == 'POST':
        if request.POST['do'] == 'add':
            try:
                if request.POST['write'] == u'enable': write = True
            except:
                write = False

            if request.user.has_perm('main.add_user_perms'):
                for doc_id in request.POST.getlist('doc_id'):
                    db.add_user_perm(doc = db.doc.get(id = doc_id),
                                   user = db.user.get(id = request.POST['user_id']),
                                   write = write)
            return redirect('/perms/user/')

    if doit == 'delete':
        if request.user.has_perm('main.delete_user_perms'):
            db.user_perms.get(id = permid).delete()
            return redirect('/perms/user/')

    if doit == 'toggle':
        if request.user.has_perm('main.change_user_perms'):
            up = db.user_perms.get(id = permid)
            up.write = not up.write
            up.save()
            return redirect('/perms/user/')

    users = db.user.all()
    docs = db.doc.all()
    perms = db.user_perms.all()

    data['type'] = 'user'
    data['users'] = users
    data['docs'] = docs
    data['allperms'] = perms

    data['content'] = 'perms/user.html'

    return render_to_response('index.html', data)

def group(request, doit = '', permid = ''):
    data = support.default_answer_data(request)
    if not data['auth']: return support.auth_error()

    db = Data()

    if request.method == 'POST':
        if request.POST['do'] == 'add':
            try:
                if request.POST['write'] == u'enable': write = True
            except:
                write = False

            if request.user.has_perm('main.add_group_perms'):
                for doc_id in request.POST.getlist('doc_id'):
                    db.add_group_perm(doc = db.doc.get(id = doc_id),
                                   group = db.group.get(id = request.POST['group_id']),
                                   write = write)

            return redirect('/perms/group/')

    if doit == 'delete':
        if request.user.has_perm('main.delete_group_perms'):
            db.group_perms.get(id = permid).delete()
            return redirect('/perms/group/')

    if doit == 'toggle':
        if request.user.has_perm('main.change_group_perms'):
            gp = db.group_perms.get(id = permid)
            gp.write = not gp.write
            gp.save()
            return redirect('/perms/group/')

    groups = db.group.all()
    docs = db.doc.all()
    perms = db.group_perms.all()

    data['type'] = 'group'
    data['groups'] = groups
    data['docs'] = docs
    data['allperms'] = perms

    data['content'] = 'perms/group.html'

    return render_to_response('index.html', data)


# vi: ts=4 sw=4

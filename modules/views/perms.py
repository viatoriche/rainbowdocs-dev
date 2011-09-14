#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""Permission view-module"""

from django.shortcuts import render_to_response , redirect
from modules import support
from modules.database import DataBase

def user(request, doit = '', permid = ''):
    """Return user permissions"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    database = DataBase()

    if request.method == 'POST':
        if request.POST['do'] == 'add':
            try:
                if request.POST['write'] == u'enable':
                    write = True
            except KeyError:
                write = False

            if request.user.has_perm('main.add_user_perms'):
                for doc_id in request.POST.getlist('doc_id'):
                    database.add_user_perm(doc = database.doc.get(id = doc_id),
                                           user = database.user.get(
                                               id = request.POST['user_id']),
                                           write = write)
            return redirect('/perms/user/')

    if doit == 'delete':
        if request.user.has_perm('main.delete_user_perms'):
            database.user_perms.get(id = permid).delete()
            return redirect('/perms/user/')

    if doit == 'toggle':
        if request.user.has_perm('main.change_user_perms'):
            user_perms = database.user_perms.get(id = permid)
            user_perms.write = not user_perms.write
            user_perms.save()
            return redirect('/perms/user/')

    users = database.user.all()
    docs = database.doc.all()
    perms = database.user_perms.all()

    data['type'] = 'user'
    data['users'] = users
    data['docs'] = docs
    data['allperms'] = perms

    data['content'] = 'perms/user.html'

    return render_to_response('index.html', data)

def group(request, doit = '', permid = ''):
    """Return group permissions"""

    data = support.default_answer_data(request)
    if not data['auth']:
        return support.auth_error()

    database = DataBase()

    if request.method == 'POST':
        if request.POST['do'] == 'add':
            try:
                if request.POST['write'] == u'enable':
                    write = True
            except KeyError:
                write = False

            if request.user.has_perm('main.add_group_perms'):
                for doc_id in request.POST.getlist('doc_id'):
                    database.add_group_perm(doc = database.doc.get(
                                                id = doc_id),
                                            group = database.group.get(
                                                id = request.POST['group_id']),
                                            write = write)

            return redirect('/perms/group/')

    if doit == 'delete':
        if request.user.has_perm('main.delete_group_perms'):
            database.group_perms.get(id = permid).delete()
            return redirect('/perms/group/')

    if doit == 'toggle':
        if request.user.has_perm('main.change_group_perms'):
            group_perms = database.group_perms.get(id = permid)
            group_perms.write = not group_perms.write
            group_perms.save()
            return redirect('/perms/group/')

    groups = database.group.all()
    docs = database.doc.all()
    perms = database.group_perms.all()

    data['type'] = 'group'
    data['groups'] = groups
    data['docs'] = docs
    data['allperms'] = perms

    data['content'] = 'perms/group.html'

    return render_to_response('index.html', data)


# vi: ts=4 sw=4

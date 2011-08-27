#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    database.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

import datetime

from main.models import Doc, Tag, Data, Link, Chain, Number, User_perms, Group_perms
from django.contrib.auth.models import User, Group

class DataBase():
    def __init__(self):
        self.chain = Chain.objects
        self.doc = Doc.objects
        self.link = Link.objects
        self.tag = Tag.objects
        self.data = Data.objects
        self.number = Number.objects
        self.user_perms = User_perms.objects
        self.group_perms = Group_perms.objects
        self.user = User.objects
        self.group = Group.objects

    def check_user_perm(self, user, doc, write = False):
        try:
            p = self.user_perms.get(doc = doc, user = user)
            if not write:
                return True
            else:
                return p.write and write
        except:
            return False

    def check_group_perm(self, group, doc, write = False):
        try:
            p = self.group_perms.get(doc = doc, group = group)
            if not write:
                return True
            else:
                return p.write and write
        except:
            return False

    def add_user_perm(self, user, doc, write = False):
        try:
            p = self.user_perms.get(doc = doc, user = user)
            p.write = write
            p.save()
        except:
            self.user_perms.create(doc = doc, user = user, write = write)

    def add_group_perm(self, group, doc, write = False):
        try:
            p = self.group_perms.get(group = group, doc = doc)
            p.write = write
            p.save
        except:
            self.group_perms.create(doc = doc, group = group, write = write)

    def perm_doc_filter(self, user, input_docs, write = False):
        if user.is_superuser:
            return input_docs

        docs = []
        if write:
            user_perms = self.user_perms.filter(user = user, write = write)
        else:
            user_perms = self.user_perms.filter(user = user)


        for user_perm in user_perms:
            if user_perm.doc not in docs and user_perm.doc in input_docs:
                docs.append(user_perm.doc)

        groups = user.groups
        for group in groups.all():

            if write:
                group_perms = self.group_perms.filter(group = group, write = write)
            else:
                group_perms = self.group_perms.filter(group = group)

            for group_perm in group_perms:
                if group_perm.doc not in docs and group_perm.doc in input_docs:
                    docs.append(group_perm.doc)

        return docs

    # Add Doc
    def add_doc(self, print_form, title, main = False):
        doc = None
        try:
            doc = self.doc.get(print_form = print_form)
            doc.title = title
            doc.main = main
            doc.save()
        except:
            doc = self.doc.create(print_form = print_form, title = title, main = main)

        return doc

    def check_doc_id(self, id):
        try:
            self.doc.get(id = id)
            return True
        except:
            return False

    # Doc_tag add
    def add_tag(self, name, description):
        if name == '': return None
        if description == '': description = name
        try:
            tag = self.tag.get(name = name)
            tag.description = description
            tag.save()
        except:
            tag = self.tag.create(name = name, description = description)

        return tag

    # Doc_link add
    def add_link(self, doc, tag):
        try:
            link = self.link.get(doc = doc, tag = tag)
        except:
            link = self.link.create(doc = doc, tag = tag)
        return link

    def del_link_id(self, id_link):
        try:
            self.link.get(id = id_link).delete()
        except:
            pass


    def del_tag(self, tag):
        numbers = self.numbers_from_tag(tag)
        if len(numbers) > 0: return False
        try:
            self.link.filter(tag = tag).delete()
            tag.delete()
            return True
        except:
            return False

    # Chain add
    def add_chain(self, main_doc, slave_doc):
        try:
            chain = self.chain.get(main_doc = main_doc, slave_doc = slave_doc)
        except:
            chain = self.chain.create(main_doc = main_doc, slave_doc = slave_doc)
        return chain

    # Chain check add
    def check_add_chain(self, id_main_doc, id_slave_doc):
        try:
            main_doc = self.doc.get(id = id_main_doc)
            slave_doc = self.doc.get(id = id_slave_doc)
        except:
            return False
        try:
            self.chain.get(main_doc = main_doc, slave_doc = slave_doc)
            return False
        except:
            return True

    # Doc_number add
    def add_number(self, doc, user, main_number = None):
        if main_number == None:
            return self.number.create(
                                  doc = doc,
                                  user = user,
                                  held_status = False,
                                 )
        else:
            return self.number.create(
                                  doc = doc,
                                  user = user,
                                  held_status = False,
                                  main_number = main_number
                                 )


    def change_number(self, number, held_status = False):
        try:
            if number.held_status == True:
                return False
            if held_status:
                number.date_held = datetime.datetime.now()
            number.held_status = held_status
            number.save()
            return True
        except:
            return False

    def del_number(self, number):
        try:
            if number.held_status == True:
                return False
            self.data.filter(number = number).delete()
            number.delete()
            return True
        except:
            return False

    # Doc_data add
    def add_data(self, number, tag, tag_value):
        try:
            self.data.get(number = number, tag = tag)
            return False
        except:
            self.data.create(number = number, 
                                    tag = tag, tag_value = tag_value)
            return True

    def del_tag_from_datadoc(self, number, tag):
        try:
            if self.change_number(number = number):
                self.data.get(number = number, tag = tag).delete()
                return True
            else:
                return False
        except:
            return False


    # Doc_data add
    def change_data(self, number, tag, tag_value):
        try:
            if self.change_number(number = number):
                data = self.data.get(number = number, tag = tag)
                data.tag_value = tag_value
                data.save()
                return data
            else:
                return None
        except:
            return None

    def numbers_from_doc(self, doc):
        return self.number.filter(doc = doc)

    def get_slave_docs(self, main_number):

        docs_chain = self.chain.filter(main_doc = main_number.doc)
        slave_docs = []
        for doc_chain in docs_chain:
            slave_docs.append(doc_chain.slave_doc)

        # Created docs
        created_slave_numbers = self.number.filter(main_number = main_number)
        created_slave_doc = []
        for created_slave_number in created_slave_numbers:
            try:
                created_slave_doc.append(created_slave_number.doc)
            except:
                pass

        out = []
        for slave_doc in slave_docs:
            if slave_doc not in created_slave_doc:
                out.append(slave_doc)

        return out

    def get_all_need_slave(self, user):
        held_numbers = self.number.filter(held_status = True)
        out = []
        for held_number in held_numbers:
            slave_docs = self.get_slave_docs(held_number)
            slave_docs = self.perm_doc_filter(user, slave_docs, True)

            for slave_doc in slave_docs:
                out.append( (slave_doc, held_number) )

        return out

    def numbers_from_tag(self, tag):
        docs = self.data.filter(tag = tag)
        out = []
        for doc in docs:
            if doc.number not in out:
                out.append(doc.number)
        return out

# vi: ts=4

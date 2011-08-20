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

from main.models import Doc, Doc_tag, Doc_data, Doc_link, Chain, Doc_number

class Data():
    def __init__(self):
        self.chain = Chain.objects
        self.doc = Doc.objects
        self.link = Doc_link.objects
        self.tag = Doc_tag.objects
        self.data = Doc_data.objects
        self.number = Doc_number.objects

    # Add Doc
    def add_doc(self, print_form, title, main = False):
        try:
            doc = self.doc.get(print_form = print_form)
            doc.title = title
            doc.main = main
            doc.save()
        except:
            self.doc.create(print_form = print_form, title = title, main = main)
        return self.doc.get(print_form = print_form).id

    def check_doc(self, id):
        try:
            self.doc.get(id = id)
            return True
        except:
            return False

    # Doc_tag add
    def add_tag(self, name, description):
        try:
            tag = self.tag.get(name = name)
            tag.description = description
            tag.save()
        except:
            self.tag.create(name = name, description = description)
        return self.tag.get(name = name).id

    # Doc_link add
    def add_link(self, id_doc, id_tag):
        try:
            self.link.get(id_doc = id_doc, id_tag = id_tag)
        except:
            if self.check_doc(id_doc):
                self.link.create(id_doc = id_doc, id_tag = id_tag)
            else:
                return -1
        return self.link.get(id_doc = id_doc, id_tag = id_tag).id

    # Chain add
    def add_chain(self, id_main_doc, id_slave_doc):
        try:
            self.chain.get(id_main_doc = id_main_doc, id_slave_doc = id_slave_doc)
        except:
            if self.check_doc(id = id_main_doc) == True and self.check_doc(id = id_slave_doc) == True:
                self.chain.create(id_main_doc = id_main_doc, id_slave_doc = id_slave_doc)
            else:
                return -1
        return self.chain.get(id_main_doc = id_main_doc, id_slave_doc = id_slave_doc).id

    # Chain check add
    def check_add_chain(self, id_main_doc, id_slave_doc):
        if self.check_doc(id = id_main_doc) == True and self.check_doc(id = id_slave_doc) == True:
            try:
                self.chain.get(id_main_doc = id_main_doc, id_slave_doc = id_slave_doc)
                return False
            except:
                return True
        else:
            return False

    # Doc_number add
    def add_number(self, main_number = 0):
        return self.number.create(held_status = False, 
                                  date_create = datetime.datetime.now(),
                                  date_change = datetime.datetime.now(),
                                  main_number = main_number).id

    def change_number(self, number, held_status = False):
        try:
            n = self.number.get(id = number)
            if n.held_status == True:
                return (False, n.id)
            if not held_status: n.date_change = datetime.datetime.now()
            else: n.date_held = datetime.datetime.now()
            n.held_status = held_status
            n.save()
            return (True, n.id)
        except:
            return (False, 0)

    # Doc_data add
    def add_data(self, number, id_doc, id_tag, tag_value):
        try:
            id = self.data.get(number = number, id_doc = id_doc, 
                                 id_tag = id_tag, tag_value = tag_value).id
            return (False, id)
        except:
            try:
                self.number.get(id = number)
                self.link.get(id_doc = id_doc, id_tag = id_tag)
                id = self.data.create(number = number, id_doc = id_doc, 
                                        id_tag = id_tag, tag_value = tag_value).id
                return (True, id)
            except:
                return (False, 0)

    # Doc_data add
    def change_data(self, number, id_tag, tag_value):
        try:
            if self.change_number(number = number)[0]:
                data = self.data.get(number = number, id_tag = id_tag)
                data.tag_value = tag_value
                data.save()
                return (True, data.id)
            else:
                return (False, data.id)
        except:
            return (False, 0)

    def id_doc_from_number(self, number):
        doc_data = self.data.filter(number = number)
        try:
            return doc_data[0].id_doc
        except:
            return 0


    def get_slave_docs(self, id_main_doc, main_number):

        slave_docs = self.chain.filter(id_main_doc = id_main_doc)

        # Created docs
        created_slave_numbers = self.number.filter(main_number = main_number)
        created_slave_doc = []
        for created_slave_number in created_slave_numbers:
            created_slave_doc.append(self.data.filter(number = created_slave_number.id)[0].id_doc)

        out = []
        for slave_doc in slave_docs:
            id_slave_doc = slave_doc.id_slave_doc
            if id_slave_doc not in created_slave_doc:
                out.append(u'{0}'.format(id_slave_doc))

        return out

    def get_all_need_slave(self):
        held_numbers = self.number.filter(held_status = True)
        need_docs = []
        for held_number in held_numbers:
            id_doc = self.id_doc_from_number(held_number.id)
            if id_doc == 0: continue
            slave_docs = self.get_slave_docs(id_doc, held_number.id)
            for id_slave_doc in slave_docs:
                need_docs.append((
                        id_slave_doc, 
                        held_number.id, 
                        self.doc.get(id = id_doc).title, 
                        self.doc.get(id = id_slave_doc).title))

        return need_docs


# vi: ts=4

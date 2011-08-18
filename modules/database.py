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

from openchain.main.models import Doc, Doc_tag, Doc_data, Doc_link, Chain, Doc_number

class Data():
    def __init__(self):
        self.chain = Chain.objects
        self.doc = Doc.objects
        self.link = Doc_link.objects
        self.tag = Doc_tag.objects
        self.data = Doc_data.objects
        self.number = Doc_number.objects

    def add_doc(self, print_form, title):
        try:
            doc = self.doc.get(print_form = print_form)
            doc.title = title
            doc.save()
        except:
            self.doc.create(print_form = print_form, title = title)
        return self.doc.get(print_form = print_form).id

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
            self.link.create(id_doc = id_doc, id_tag = id_tag)
        return self.link.get(id_doc = id_doc, id_tag = id_tag).id

    # Chain add
    def add_chain(self, id_main_doc, id_slave_doc):
        try:
            self.chain.get(id_main_doc = id_main_doc, id_slave_doc = id_slave_doc)
        except:
            self.chain.create(id_main_doc = id_main_doc, id_slave_doc = id_slave_doc)
        return self.chain.get(id_main_doc = id_main_doc, id_slave_doc = id_slave_doc).id

    # Doc_number add
    def add_number(self, main_number = 0):
        return self.number.create(held_status = False, 
                                  date_create = datetime.datetime.now(), 
                                  date_change = datetime.datetime.now(),
                                  main_number = main_number).id

    # Doc_data add
    def add_data(self, number, id_doc, id_tag, tag_value):
        try:
            self.data.get(number = number, id_doc = id_doc, 
                                 id_tag = id_tag, tag_value = tag_value)
            return False
        except:
            try:
                self.number.get(id = number)
                self.link.get(id_doc = id_doc, id_tag = id_tag)
                self.data.create(number = number, id_doc = id_doc, 
                                        id_tag = id_tag, tag_value = tag_value)
                return True
            except:
                return False



# vi: ts=4

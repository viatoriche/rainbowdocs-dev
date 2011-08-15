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

### ADD DATA → ----------------------------------------------------- ← ADD DATA

# Doc add
def add_doc(print_form_value, title_value):
    try:
        Doc.objects.get(print_form = print_form_value)
    except:
        Doc.objects.create(print_form = print_form_value, title = title_value)
    return Doc.objects.get(print_form = print_form_value).id

# Doc_tag add
def add_tag(tag_name, tag_desc):
    try:
        attr = Doc_tag.objects.get(name = tag_name)
        attr.description = tag_desc
    except:
        Doc_tag.objects.create(name = tag_name, description = tag_desc)
    return Doc_tag.objects.get(name = tag_name).id

# Doc_link add
def add_link(id_doc_value, id_tag_value):
    try:
        Doc_link.objects.get(id_doc = id_doc_value, id_tag = id_tag_value)
    except:
        Doc_link.objects.create(id_doc = id_doc_value, id_tag = id_tag_value)
    return Doc_link.objects.get(id_doc = id_doc_value, id_tag = id_tag_value).id

# Chain add
def add_chain(id_main_doc_value, id_slave_doc_value):
    try:
        Chain.objects.get(id_main_doc = id_main_doc_value, id_slave_doc = id_slave_doc_value)
    except:
        Chain.objects.create(id_main_doc = id_main_doc_value, id_slave_doc = id_slave_doc_value)
    return Chain.objects.get(id_main_doc = id_main_doc_value, id_slave_doc = id_slave_doc_value).id

# Doc_number add
def add_doc_number(main_number_value = 0):
    return Doc_number.objects.create(held_status = False, 
                              date_create = datetime.datetime.now(), 
                              date_change = datetime.datetime.now(),
                              main_number = main_number_value).id

def add_doc_data(number_value, id_doc_value, id_tag_value, tag_data):
    try:
        Doc_data.objects.get(number = number_value, id_doc = id_doc_value, id_tag = id_tag_value, tag_value = tag_data)
        return False
    except:
        try:
            Doc_number.objects.get(id = number_value)
            Doc_link.objects.get(id_doc = id_doc_value, id_tag = id_tag_value)
            Doc_data.objects.create(number = number_value, id_doc = id_doc_value, id_tag = id_tag_value, tag_value = tag_data)
            return True
        except:
            return False

### ADD DATA ←

### CHANGE DATA → ------------------------------ ← CHANGE DATA

### CHANGE DATA ←

### GET OBJECTS → --------------------------------- ← GET OBJECTS

def get_chain():
    return Chain.objects

def get_doc():
    return Doc.objects

def get_link():
    return Doc_link.objects

def get_tag():
    return Doc_tag.objects

def get_data():
    return Doc_data.objects

def get_number():
    return Doc_number.objects

### GET OBJECTS ←
# vi: ts=4

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Database Module, all functions for database"""

import datetime

from main.models import Doc, Tag, Data, Link, Chain, Number
from main.models import User_perms, Group_perms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

class DataBase:
    """Class: DataBase

    chain - Chain
    doc - Doc
    link - Link
    tag - Tag
    data - Data
    number - Number
    user_perms - User_perms
    group_perms - Group_perms
    user - User
    group - Group
    """

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

    # Tested
    def check_user_perm(self, user, doc, write = False):
        """Return True, if user valide for doc
        write - perm for write
        """

        try:
            perm = self.user_perms.get(doc = doc, user = user)
            if not write:
                return True
            else:
                return perm.write and write
        except ObjectDoesNotExist:
            return False

    # Tested
    def check_group_perm(self, group, doc, write = False):
        """Return True, if group valide for doc
        write - perm for write
        """

        try:
            perm = self.group_perms.get(doc = doc, group = group)
            if not write:
                return True
            else:
                return perm.write and write
        except ObjectDoesNotExist:
            return False

    # Tested
    def add_user_perm(self, user, doc, write = False):
        """Add perms for user, write - perm for write"""

        try:
            perm = self.user_perms.get(doc = doc, user = user)
            perm.write = write
            perm.save()
        except ObjectDoesNotExist:
            self.user_perms.create(doc = doc, user = user, write = write)

    # Tested
    def add_group_perm(self, group, doc, write = False):
        """Add perms for group, write - perm for write"""

        try:
            perm = self.group_perms.get(group = group, doc = doc)
            perm.write = write
            perm.save()
        except ObjectDoesNotExist:
            self.group_perms.create(doc = doc, group = group, write = write)

    # Tested
    def perm_doc_filter(self, user, input_docs, write = False):
        """Return all docs, which valide for user (and his groups)
        from input_docs, write - write only
        """

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
                group_perms = self.group_perms.filter(group = group,
                                                      write = True)
            else:
                group_perms = self.group_perms.filter(group = group)

            for group_perm in group_perms:
                if group_perm.doc not in docs and group_perm.doc in input_docs:
                    docs.append(group_perm.doc)

        return docs

    # Tested
    def add_doc(self, print_form, title, main = False):
        """Add Doc method, return doc"""

        try:
            # Change
            doc = self.doc.get(print_form = print_form)
            doc.title = title
            doc.main = main
            doc.save()
        except ObjectDoesNotExist:
            # Add new
            doc = self.doc.create(print_form = print_form,
                                  title = title, 
                                  main = main)

        return doc

    # Tested
    def check_doc_id(self, id_doc):
        """return True, if doc with id - getted"""

        try:
            self.doc.get(id = id_doc)
            return True
        except ObjectDoesNotExist:
            return False

    # Tested
    def add_tag(self, name, description):
        """Add tag into database, return tag"""

        if name == '':
            return None

        if description == '':
            description = name

        try:
            # Change
            tag = self.tag.get(name = name)
            tag.description = description
            tag.save()
        except ObjectDoesNotExist:
            # Add
            tag = self.tag.create(name = name, description = description)

        return tag

    # Tested
    def add_link(self, doc, tag):
        """Add link, return link"""

        try:
            # Change
            link = self.link.get(doc = doc, tag = tag)
        except ObjectDoesNotExist:
            # Add
            link = self.link.create(doc = doc, tag = tag)
        return link

    # Tested
    def del_link_id(self, id_link):
        """Del link by id"""

        try:
            self.link.get(id = id_link).delete()
        except ObjectDoesNotExist:
            pass

    # Tested
    def del_tag(self, tag):
        """Del tag, and del links with tag, Return True if ok"""

        numbers = self.numbers_from_tag(tag)
        if len(numbers) > 0:
            return False

        try:
            # Delete links and tag
            self.link.filter(tag = tag).delete()
            tag.delete()
            return True
        except ObjectDoesNotExist:
            return False

    # Tested
    def add_chain(self, main_doc, slave_doc):
        """Add chain, return chain"""

        try:
            # Get chain
            chain = self.chain.get(main_doc = main_doc,
                                   slave_doc = slave_doc)
        except ObjectDoesNotExist:
            # else create new chain
            chain = self.chain.create(main_doc = main_doc,
                                      slave_doc = slave_doc)
        return chain

    # Tested
    def check_add_chain(self, id_main_doc, id_slave_doc):
        """Check for can add chain, Return True - can add"""

        # Check docs
        try:
            main_doc = self.doc.get(id = id_main_doc)
            slave_doc = self.doc.get(id = id_slave_doc)
        except ObjectDoesNotExist:
            return False

        try:
            # Get, if ok - cannot add
            self.chain.get(main_doc = main_doc, slave_doc = slave_doc)
            return False
        except ObjectDoesNotExist:
            return True

    # Tested
    def add_number(self, doc, user, main_number = None):
        """Add number for doc, and main datas, return number"""

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


    # Tested
    def change_number(self, number, held_status = False):
        """Change number, True if ok"""

        try:
            # Cannot change, if helded
            if number.held_status == True:
                return False

            # If change held status - change datetime
            if held_status:
                number.date_held = datetime.datetime.now()

            number.held_status = held_status
            number.save()
            return True
        except ValueError:
            return False

    # Tested
    def del_number(self, number):
        """Del number"""

        try:
            # Cannot del helded number
            if number.held_status == True:
                return False

            # Del all data for number
            self.data.filter(number = number).delete()
            number.delete()
            return True
        except ValueError:
            return False

    # Tested
    def add_data(self, number, tag, tag_value):
        """Add data for number, return True if ok"""

        try:
            # Can add only new data
            self.data.get(number = number, tag = tag)
            return False
        except ObjectDoesNotExist:
            # Create
            self.data.create(number = number,
                             tag = tag,
                             tag_value = tag_value)
            return True

    # Tested
    def del_tag_from_datadoc(self, number, tag):
        """Del one tag, from data of number, return True if ok"""

        try:
            # Test and change number (for date - change)
            if self.change_number(number = number):
                # if can change - delete
                self.data.get(number = number, tag = tag).delete()
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    # Tested
    def change_data(self, number, tag, tag_value):
        """Change data of number, return data of None"""

        try:
            # Test and change number (for date - change)
            if self.change_number(number = number):
                # if can change - change
                data = self.data.get(number = number, tag = tag)
                data.tag_value = tag_value
                data.save()
                return data
            else:
                return None
        except ObjectDoesNotExist:
            return None

    # Tested
    def numbers_from_doc(self, doc):
        """Get all number type of doc"""
        return self.number.filter(doc = doc)

    # Tested
    def get_slave_docs(self, main_number):
        """Get all slave docs, for create"""

        # Get all docs from chains, where main_doc - type doc of main_number
        docs_chain = self.chain.filter(main_doc = main_number.doc)
        slave_docs = []
        for doc_chain in docs_chain:
            slave_docs.append(doc_chain.slave_doc)

        # Get all created docs from created slave numbers
        created_slave_numbers = self.number.filter(main_number = main_number)
        created_slave_docs = []
        for created_slave_number in created_slave_numbers:
            created_slave_docs.append(created_slave_number.doc)

        out = []
        for slave_doc in slave_docs:
            # If not create, then append
            if slave_doc not in created_slave_docs:
                out.append(slave_doc)

        return out

    # Tested
    def get_all_need_slave(self, user):
        """Get all slave docs and main_number, for create, by user"""

        # If doc are helded
        held_numbers = self.number.filter(held_status = True)
        out = []
        for held_number in held_numbers:
            slave_docs = self.get_slave_docs(held_number)
            # filter by user, and only writeable
            slave_docs = self.perm_doc_filter(user, slave_docs, True)

            for slave_doc in slave_docs:
                out.append( (slave_doc, held_number) )

        return out

    # Tested
    def numbers_from_tag(self, tag):
        """get all numbers, where this tag"""

        docs = self.data.filter(tag = tag)
        out = []
        for doc in docs:
            if doc.number not in out:
                out.append(doc.number)
        return out

# vi: ts=4

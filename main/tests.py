#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    test.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from django.test import TestCase
from django.test.client import Client
from django.contrib import auth
from modules import parse_docs
from modules import database

class WebTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        auth.models.User.objects.create_user('test', 'test@test.ru', 'nya')

    def testBasic(self):
        response = self.client.post('', {'login': 'test', 'pass': 'nya'})
        login = self.client.login(username='test', password='nya')
        self.assertEqual(login, True)
        self.assertContains(response, 'logout')

        database.add_doc('jopa0.odt', 'JOPA0')
        database.add_doc('jopa1.odt', 'JOPA1')
        database.add_doc('jopa2.odt', 'JOPA2')

        response = self.client.get('/alldocs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="1">JOPA0</div>')
        self.assertContains(response, '<div id="2">JOPA1</div>')
        self.assertContains(response, '<div id="3">JOPA2</div>')

        # logout
        response = self.client.post('', {'logout': 'logout'} )
        self.assertContains(response, 'Auth')

        response = self.client.get('/alldocs/')
        self.assertEqual(response.status_code, 404)

class ParseDocTest(TestCase):
    def testParse_database(self):
        p = parse_docs.Parser()
        for i in p.scan():
            pass

        id_doc = database.add_doc('jopa.odt', 'JOPA1')
        id_doc = database.add_doc('jopa.odt', 'JOPA')
        self.assertEqual(id_doc, 1)

        id_doc2 = database.add_doc('jopa2.odt', 'JOPA2')
        self.assertEqual(id_doc2, 2)

        id_doc3 = database.add_doc('jopa3.odt', 'JOPA3')
        self.assertEqual(id_doc3, 3)

        id_tag = database.add_tag('FIO', 'Name and Surname')
        id_tag = database.add_tag('FIO', 'Name and Surname')
        self.assertEqual(id_tag, 1)

        id_tag2 = database.add_tag('date', u'Date')
        self.assertEqual(id_tag2, 2)

        id_link = database.add_link(1, 1)
        id_link = database.add_link(1, 1)
        self.assertEqual(id_link, 1)

        id_link2 = database.add_link(1, 2)
        id_link3 = database.add_link(2, 2)

        self.assertEqual((id_link2, id_link3), (2, 3))

        id_chain = database.add_chain(1, 2)
        id_chain = database.add_chain(1, 2)
        self.assertEqual(id_chain, 1)

        id_chain2 = database.add_chain(3, 1)
        self.assertEqual(id_chain2, 2)

        id_num = database.add_doc_number()
        self.assertEqual(id_num, 1)

        id_num = database.add_doc_number(1)
        self.assertEqual(id_num, 2)

        res_add = database.add_doc_data(1, 1, 1, 'gggg')
        self.assertEqual(res_add, True)

        res_add = database.add_doc_data(3, 1, 1, 'gggg')
        self.assertEqual(res_add, False)

        res_add = database.add_doc_data(2, 3, 1, 'gggg')
        self.assertEqual(res_add, False)

        self.assertEqual(database.get_doc().all()[0].title, 'JOPA1')

# vi: ts=4

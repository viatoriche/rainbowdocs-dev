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
from modules.database import Data
from openchain import settings


class WebTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        auth.models.User.objects.create_user('test', 'test@test.ru', 'nya')

    def testBasic(self):
        data = Data()
        response = self.client.post('', {'login': 'test', 'pass': 'nya'})
        login = self.client.login(username='test', password='nya')
        self.assertEqual(login, True)
        self.assertContains(response, 'logout')

        data.add_doc('jopa0.odt', 'JOPA0')
        data.add_doc('jopa1.odt', 'JOPA1')
        data.add_doc('jopa2.odt', 'JOPA2')

        response = self.client.get('/alldocs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="1">JOPA0</div>')
        self.assertContains(response, '<div id="2">JOPA1</div>')
        self.assertContains(response, '<div id="3">JOPA2</div>')

        response = self.client.get('/getforms/')
        self.assertEqual(response.status_code, 200)
        print response.content

        # logout
        response = self.client.post('', {'logout': 'logout'} )
        self.assertContains(response, 'Auth')

        response = self.client.get('/alldocs/')
        self.assertEqual(response.status_code, 404)

class ParseDocTest(TestCase):
    def testParse_database(self):
        data = Data()
        p = parse_docs.Parser(settings.PRINT_FORMS_DIR)
        print 'All print forms:'
        scanned = p.scan()
        for pf in scanned:
            path_pf = pf[0]
            title_pf = pf[1]
            print u'Path: {0} / Title: {1}\nTags:'.format(path_pf, title_pf)
            for tag in pf[2]:
                tag_name = tag[0]
                tag_desc = tag[1]
                print u'Name: {0} / Description: {1}'.format(tag_name, tag_desc)

        id_doc = data.add_doc('jopa.odt', 'JOPA1')
        id_doc = data.add_doc('jopa.odt', 'JOPA')
        self.assertEqual(id_doc, 1)

        id_doc2 = data.add_doc('jopa2.odt', 'JOPA2')
        self.assertEqual(id_doc2, 2)

        id_doc3 = data.add_doc('jopa3.odt', 'JOPA3')
        self.assertEqual(id_doc3, 3)

        id_tag = data.add_tag('FIO', 'Name and Surname')
        id_tag = data.add_tag('FIO', 'Name and Surname 2')
        self.assertEqual(id_tag, 1)
        self.assertEqual(data.tag.get(id=1).description, 'Name and Surname 2')

        id_tag2 = data.add_tag('date', u'Date')
        self.assertEqual(id_tag2, 2)

        id_link = data.add_link(1, 1)
        id_link = data.add_link(1, 1)
        self.assertEqual(id_link, 1)

        id_link2 = data.add_link(1, 2)
        id_link3 = data.add_link(2, 2)

        self.assertEqual((id_link2, id_link3), (2, 3))

        id_chain = data.add_chain(1, 2)
        id_chain = data.add_chain(1, 2)
        self.assertEqual(id_chain, 1)

        id_chain2 = data.add_chain(3, 1)
        self.assertEqual(id_chain2, 2)

        id_num = data.add_number()
        self.assertEqual(id_num, 1)

        id_num = data.add_number(1)
        self.assertEqual(id_num, 2)

        res_add = data.add_data(1, 1, 1, 'gggg')
        self.assertEqual(res_add, True)

        res_add = data.add_data(3, 1, 1, 'gggg')
        self.assertEqual(res_add, False)

        res_add = data.add_data(2, 3, 1, 'gggg')
        self.assertEqual(res_add, False)

        self.assertEqual(data.doc.all()[0].title, 'JOPA1')

# vi: ts=4

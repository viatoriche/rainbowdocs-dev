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
from modules.database import DataBase


class WebTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        auth.models.User.objects.create_user('test', 'test@test.ru', 'nya')

    def testBasic(self):
        db = DataBase()
        response = self.client.post('', {'login': 'test', 'pass': 'nya'})
        login = self.client.login(username='test', password='nya')
        self.assertEqual(login, True)
        self.assertContains(response, 'logout')

        doc1 = db.add_doc('jopa0.odt', 'JOPA0', True)
        doc2 = db.add_doc('jopa1.odt', 'JOPA1', True)
        doc3 = db.add_doc('jopa2.odt', 'JOPA2', False)

        response = self.client.get('/documents/all/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="1">JOPA0</div>')
        self.assertContains(response, '<div id="2">JOPA1</div>')
        self.assertContains(response, '<div id="3">JOPA2</div>')

        response = self.client.get('/documents/parse/')
        self.assertEqual(response.status_code, 200)
        #print response.content

        response = self.client.get('/chains/addcheck/1/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'True')

        db.add_chain(doc1, doc1)
        db.add_chain(doc1, doc2)

        response = self.client.get('/chains/addcheck/1/1/')
        self.assertContains(response, 'False')

        response = self.client.get('/chains/addcheck/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/chains/addcheck/1/')
        self.assertEqual(response.status_code, 404)

        t1 = db.add_tag('tag1', 'tag1')
        t2 = db.add_tag('tag2', 'tag2')
        t3 = db.add_tag('tag3', 'tag3')

        db.add_link(doc1, t3)
        db.add_link(doc1, t2)
        db.add_link(doc1, t1)

        response = self.client.get('/documents/new/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="1">JOPA0</option>')

        response = self.client.post('/documents/new/', {'id_doc': '1'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/new/1/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'tag3')
        self.assertContains(response, 'tag2')
        self.assertContains(response, 'tag1')

        response = self.client.post('/documents/new/1/', {t1.id: 'nya1', t2.id: 'nya2', t3.id: 'nya3'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, 'nya1')
        self.assertContains(response, 'nya2')
        self.assertContains(response, 'nya3')

        response = self.client.get('/documents/edit/1/')
        self.assertContains(response, '<input type="submit" value="Change">')

        response = self.client.post('/documents/edit/1/', {'do': 'change', t1.id: 'nya1_e', t2.id: 'nya2_e', t3.id: 'nya3_e'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, 'nya1_e')
        self.assertContains(response, 'nya2_e')
        self.assertContains(response, 'nya3_e')

        response = self.client.get('/documents/held/1/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, '<b>Helded:')

        response = self.client.get('/chains/need/')
        self.assertContains(response, '<a href="/documents/new/1/1/">JOPA0 → JOPA0</a><br>')
        self.assertContains(response, '<a href="/documents/new/2/1/">JOPA0 → JOPA1</a><br>')

        response = self.client.get('/chains/add/')
        self.assertContains(response, '<input type="text" name="chains" value="1-1 1-2 ">')

        response = self.client.post('/chains/add/', {'chains': '2-1'})
        response = self.client.get('/chains/add/')
        self.assertContains(response, '<input type="text" name="chains" value="1-1 1-2 2-1 ">')

        # logout
        response = self.client.post('', {'logout': 'logout'} )
        self.assertContains(response, 'Auth')

        response = self.client.get('/documents/all/')
        self.assertEqual(response.status_code, 302)

class DBTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.user = auth.models.User.objects.create_user('test', 'test@test.ru', 'nya')

    def testBasic(self):
        db = DataBase()

        doc1 = db.add_doc('jopa.odt', 'JOPA1', True)
        doc1 = db.add_doc('jopa.odt', 'JOPA', True)
        self.assertEqual(doc1.id, 1)
        self.assertEqual(doc1.title, 'JOPA')

        doc2 = db.add_doc('jopa2.odt', 'JOPA2', False)
        self.assertEqual(doc2.id, 2)

        doc3 = db.add_doc('jopa3.odt', 'JOPA3', False)
        self.assertEqual(doc3.id, 3)

        tag1 = db.add_tag('FIO', 'Name and Surname')
        tag1 = db.add_tag('FIO', 'Name and Surname 2')
        self.assertEqual(tag1.id, 1)
        self.assertEqual(tag1.description, 'Name and Surname 2')

        tag2 = db.add_tag('date', u'Date')
        self.assertEqual(tag2.id, 2)

        link1 = db.add_link(doc1, tag1)
        link1 = db.add_link(doc1, tag1)
        self.assertEqual(link1.id, 1)

        link2 = db.add_link(doc1, tag2)
        link3 = db.add_link(doc2, tag2)

        self.assertEqual((link2.id, link3.id), (2, 3))

        chain1 = db.add_chain(doc1, doc2)
        self.assertEqual(chain1.id, 1)
        chain1 = db.add_chain(doc1, doc2)
        self.assertEqual(chain1.id, 1)

        chain2 = db.add_chain(doc3, doc1)
        self.assertEqual(chain2.id, 2)

        num1 = db.add_number(doc1, self.user)
        self.assertEqual(num1.id, 1)

        num2 = db.add_number(doc1, self.user, num1)
        self.assertEqual(num2.id, 2)

        data1 = db.add_data(num1, tag1, 'gggg')
        self.assertEqual(data1, True)

        data2 = db.add_data(num1, tag1, 'hhhh')
        self.assertEqual(data2, False)

        data2 = db.add_data(num2, tag1, 'hhhh')
        self.assertEqual(data2, True)

        data1 = db.change_data(num1, tag1, 'lololo')
        self.assertEqual(data1.tag_value, 'lololo')

        r = db.change_number(num1, False)
        self.assertEqual(r, True)

        r = db.change_number(num1, True)
        self.assertEqual(r, True)

        docs = db.get_slave_docs(num1)
        self.assertEqual(docs[0].id, 2)

        slaves = db.get_all_need_slave()
        self.assertEqual(slaves[0][0].id, 2)

        numbers = db.numbers_from_doc(doc1)
        self.assertEqual((numbers[0].id, numbers[1].id), (1, 2))


# vi: ts=4
